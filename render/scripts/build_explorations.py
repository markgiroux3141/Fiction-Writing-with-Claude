#!/usr/bin/env python3
r"""Compile plate-exploration working documents into one reading PDF.

These are not manuscript text — they are riffs, rendered moments, doctrine
arguments and notes — so they do not go through build.sh's edition pipeline.
This produces a plain reading copy: a contents page, one section per source
file starting on its own page, and a divider for each photograph.

    python render/scripts/build_explorations.py                 # default set
    python render/scripts/build_explorations.py --plate the-stooping-one
    python render/scripts/build_explorations.py a.md b.md -o out.pdf

Note on the first run: MiKTeX builds its file-name database and font cache
on first use, during which xelatex can sit for minutes looking hung. It is
not. Let it finish; later runs take about a second. xelatex is invoked with
stdin closed and -interaction=nonstopmode so a genuine error stops rather
than waiting at a prompt that nothing can answer.

The generated header is deliberately package-light — kernel commands plus
fancyhdr — but that is portability, not necessity: sectsty, etoolbox and
titling are all installed here.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPLORATIONS = ROOT / "bible" / "plate-explorations"
FONTS = ROOT / "render" / "fonts"
OUT = ROOT / "render" / "out"

# The default set: the two plates currently under exploration, in the order
# they were written, which is the order they are meant to be read in.
DEFAULT = [
    "the-scratched-face.md",
    "the-scratched-face-prose-01.md",
    "the-scratched-face-prose-01-r2.md",
    "the-stooping-one-prose-01.md",
    "the-stooping-one-prose-02.md",
]

HEADER = r"""
\usepackage{fancyhdr}

% Working documents, not a manuscript: no section numbers.
\setcounter{secnumdepth}{-2}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.2pt}
\fancyhead[L]{\footnotesize\scshape\nouppercase{\leftmark}}
\fancyhead[R]{\footnotesize\thepage}
\fancypagestyle{plain}{%
  \fancyhf{}\renewcommand{\headrulewidth}{0pt}\fancyfoot[C]{\footnotesize\thepage}}

\makeatletter
% Each source file opens a \section, so give every one its own page.
\renewcommand\section{\clearpage\@startsection{section}{1}{\z@}%
  {-3.5ex \@plus -1ex \@minus -.2ex}{2.3ex \@plus .2ex}%
  {\normalfont\LARGE\scshape\raggedright}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
  {-3.25ex \@plus -1ex \@minus -.2ex}{1.4ex \@plus .2ex}%
  {\normalfont\large\itshape\raggedright}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
  {-3.25ex \@plus -1ex \@minus -.2ex}{1.2ex \@plus .2ex}%
  {\normalfont\normalsize\scshape\raggedright}}

% Off-page rules and premises are set as block quotes throughout these
% files. Set them apart so they do not read as body prose.
\renewenvironment{quote}
  {\list{}{\rightmargin\leftmargin}\item\relax\itshape\small}
  {\endlist}

\newcommand{\platepart}[1]{%
  \clearpage
  \thispagestyle{empty}%
  \addcontentsline{toc}{part}{#1}%
  \vspace*{\fill}%
  {\centering\Huge\scshape #1\par}%
  \vspace*{\fill}%
  \clearpage}
\makeatother

% No page number on the title page.
\makeatletter
\let\@oldmaketitle\maketitle
\renewcommand{\maketitle}{\@oldmaketitle\thispagestyle{empty}}
\makeatother

\setlength{\emergencystretch}{3em}
\raggedbottom
"""


def plate_of(name):
    """Group files by photograph: the slug before -prose/-beats/etc."""
    stem = Path(name).stem
    return re.split(r"-(?:prose|beats|skeleton|variants|story-shapes|shape)\b",
                    stem)[0]


def titlecase(slug):
    small = {"the", "of", "a", "an", "and", "in", "at", "on"}
    words = slug.split("-")
    return " ".join(w.capitalize() if i == 0 or w not in small else w
                    for i, w in enumerate(words))


def combine(paths, dest):
    """Concatenate sources, lifting each file's H1 up to be its section head."""
    chunks, current = [], None
    for p in paths:
        raw = p.read_text(encoding="utf-8").strip()
        first, rest = raw.split("\n", 1)
        title = re.sub(r"^#\s*", "", first).replace("*", "").strip()

        plate = plate_of(p.name)
        if plate != current:
            chunks.append(r"\platepart{%s}" % titlecase(plate))
            current = plate

        chunks.append("# %s\n" % title)
        chunks.append(r"\markboth{%s}{}" % title)
        chunks.append("*Source:* `%s`\n" % p.name)
        chunks.append(rest.strip())

    dest.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="markdown sources (default: the current two plates)")
    ap.add_argument("--plate", help="only files whose name starts with this slug")
    ap.add_argument("-o", "--output", default=str(OUT / "plate-explorations.pdf"))
    args = ap.parse_args()

    if args.files:
        paths = [Path(f) for f in args.files]
    elif args.plate:
        paths = sorted(EXPLORATIONS.glob(args.plate + "*.md"))
    else:
        paths = [EXPLORATIONS / f for f in DEFAULT]

    missing = [p for p in paths if not p.is_file()]
    if missing:
        sys.exit("missing: " + ", ".join(str(m) for m in missing))
    if not paths:
        sys.exit("no source files matched")

    out_pdf = Path(args.output).resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "header.tex").write_text(HEADER, encoding="utf-8")
        combine(paths, td / "combined.md")

        fontopts = (
            "Path=%s/,UprightFont=LibreCaslonText.ttf,"
            "ItalicFont=LibreCaslonText-Italic.ttf,"
            "BoldFont=OldStandard-Bold.ttf,"
            "BoldItalicFont=LibreCaslonText-Italic.ttf" % FONTS.as_posix()
        )
        cmd = [
            "pandoc", "combined.md", "-o", "doc.tex", "--standalone",
            "--from=markdown+pipe_tables+smart",
            "--toc", "--toc-depth=2",
            "--include-in-header=header.tex",
            "-V", "documentclass=article", "-V", "papersize=a4",
            "-V", "geometry:margin=2.6cm,top=2.4cm,bottom=2.6cm",
            "-V", "fontsize=11pt", "-V", "linestretch=1.15",
            "-V", "mainfont=Libre Caslon Text",
            "-V", "mainfontoptions=" + fontopts,
            "-V", "colorlinks=true", "-V", "linkcolor=black",
            "-V", "urlcolor=black", "-V", "toccolor=black",
            "-V", "title=Plate Explorations",
            # Escaped: a bare & is an alignment character in LaTeX.
            "-V", "subtitle=" + r" \& ".join(
                dict.fromkeys(titlecase(plate_of(p.name)) for p in paths)
            ) + " — reading copy",
        ]
        r = subprocess.run(cmd, cwd=td, capture_output=True, text=True)
        if r.returncode:
            sys.exit("pandoc failed:\n" + r.stderr)

        # Two passes so the table of contents resolves. stdin is closed so a
        # LaTeX error stops rather than sitting at an interactive prompt.
        for i in (1, 2):
            r = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "doc.tex"],
                cwd=td, capture_output=True, text=True, stdin=subprocess.DEVNULL)

        log = (td / "doc.log").read_text(encoding="utf-8", errors="replace")
        if not (td / "doc.pdf").is_file():
            errs = [l for l in log.splitlines() if l.startswith("! ")]
            sys.exit("xelatex produced no PDF:\n" + "\n".join(errs[:20]))

        shutil.copy(td / "doc.pdf", out_pdf)

        pages = re.search(r"Output written on doc\.pdf \((\d+) pages", log)
        bad = len(re.findall(r"^! ", log, re.M))
        glyphs = len(re.findall(r"Missing character", log))

    print("%s  (%s pages, %d sources)" %
          (out_pdf, pages.group(1) if pages else "?", len(paths)))
    if bad or glyphs:
        print("  warnings: %d latex errors, %d missing glyphs" % (bad, glyphs))


if __name__ == "__main__":
    main()

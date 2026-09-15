# -*- coding: utf-8 -*-
"""LaTeX conversion for the anthology."""
import re

SPECIALS = {
    '\\': r'\textbackslash{}',
    '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
    '{': r'\{', '}': r'\}',
    '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
}

FOOTREF = re.compile(r'\{\*\d+\}|\[\d{1,3}\]|(?<=[a-z.,;!?"”])\[[A-Z]\]')


def _curl(t):
    """ASCII quotes -> typographic. Text that already uses curly quotes passes through."""
    out, open_d = [], True
    for i, ch in enumerate(t):
        if ch == '"':
            out.append('“' if open_d else '”')
            open_d = not open_d
        elif ch == "'":
            prev = t[i - 1] if i else ' '
            nxt = t[i + 1] if i + 1 < len(t) else ' '
            if prev.isalnum():
                out.append('’')
            elif nxt.isalnum():
                out.append('‘')
            else:
                out.append('’')
        else:
            out.append(ch)
    return ''.join(out)


def latex(t):
    t = t.replace('​', '').replace('﻿', '').replace('­', '')
    t = FOOTREF.sub('', t)
    t = _curl(t)
    # protect _italics_ before escaping
    t = re.sub(r'_([^_]{1,400}?)_', '\x01\\1\x02', t)
    t = ''.join(SPECIALS.get(c, c) for c in t)
    t = t.replace('\x01', r'\emph{').replace('\x02', '}')
    t = re.sub(r'(?<!-)--(?!-)', '—', t)        # ASCII em dash
    t = re.sub(r'\s*—\s*', '—', t)          # set em dashes tight
    t = t.replace('...', r'\dots{}').replace('…', r'\dots{}')
    t = re.sub(r'  +', ' ', t)
    return t.strip()


PREAMBLE = r"""\documentclass[10pt,twoside,openany]{book}
\usepackage{fontspec}
\usepackage[papersize={6in,9in},inner=0.80in,outer=0.62in,
            top=0.72in,bottom=0.80in,headsep=13pt,footskip=26pt]{geometry}
\usepackage{microtype}
\usepackage{fancyhdr}
\usepackage[hidelinks,bookmarksopen=false,bookmarksnumbered=false,
            pdftitle={Sixty-Two Ghost Stories},
            pdfauthor={Various},
            pdfsubject={An anthology drawn from the Standing Water reference library}]{hyperref}

\defaultfontfeatures{Path=FONTPATH/,Ligatures=TeX}
\setmainfont{LibreCaslonText.ttf}[
  ItalicFont=LibreCaslonText-Italic.ttf,
  ItalicFeatures={RawFeature={-liga;-hlig;-dlig;-clig}},
  BoldFont=LibreCaslonText.ttf, BoldFeatures={FakeBold=1.6},
  BoldItalicFont=LibreCaslonText-Italic.ttf,
  BoldItalicFeatures={FakeBold=1.6,RawFeature={-liga;-hlig;-dlig;-clig}},
  Scale=0.98]
\newfontfamily\headfont{OldStandard-Regular.ttf}[
  ItalicFont=OldStandard-Italic.ttf, BoldFont=OldStandard-Bold.ttf]

\linespread{1.13}
\frenchspacing
\setlength{\parindent}{1.1em}
\setlength{\emergencystretch}{2em}
\widowpenalty=10000 \clubpenalty=10000
\raggedbottom
\setcounter{tocdepth}{0}
\setcounter{secnumdepth}{-1}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyhead[LE]{\headfont\scriptsize\MakeUppercase{\leftmark}}
\fancyhead[RO]{\headfont\scriptsize\MakeUppercase{\rightmark}}
\fancyfoot[C]{\headfont\small\thepage}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\headfont\small\thepage}%
  \renewcommand{\headrulewidth}{0pt}}

% ---- one story ----------------------------------------------------------
\newcommand{\story}[3]{%
  \clearpage
  \thispagestyle{plain}%
  \phantomsection
  \addcontentsline{toc}{chapter}{\texorpdfstring{%
     #1\,\textperiodcentered\,\textit{#2}}{#1 - #2}}%
  \markboth{#2}{#1}%
  \vspace*{10mm}%
  {\centering
   \rule{0.30\textwidth}{0.4pt}\par\vspace{7mm}
   {\headfont\LARGE #1\par}\vspace{5mm}
   {\headfont\itshape\large #2\par}\vspace{1.5mm}
   {\headfont\footnotesize #3\par}\vspace{6mm}
   \rule{0.30\textwidth}{0.4pt}\par}
  \vspace{9mm}%
  \par\noindent\ignorespaces}

\newcommand{\sect}[1]{\par\vspace{5.5mm}{\centering\headfont\normalsize #1\par}%
  \vspace{3.5mm}\par\noindent\ignorespaces}
\newcommand{\scenebreak}{\par\vspace{3.5mm}{\centering\rule{0.10\textwidth}{0.4pt}\par}%
  \vspace{3.5mm}\par\noindent\ignorespaces}

\begin{document}
\frontmatter
\thispagestyle{empty}
\vspace*{40mm}
{\centering
 {\headfont\Huge Sixty-Two\\[3mm] Ghost Stories\par}
 \vspace{12mm}
 \rule{0.42\textwidth}{0.4pt}\par
 \vspace{12mm}
 {\headfont\large\itshape The best of the reference library\par}
 \vspace{3mm}
 {\headfont\large 1824\,--\,1936\par}
 \vspace{55mm}
 {\headfont\footnotesize Selected and set from \texttt{reference/texts}\par}
 {\headfont\footnotesize for \textit{Standing Water}\par}
\par}

\clearpage
\thispagestyle{empty}
\vspace*{12mm}
{\centering{\headfont\large A note on this volume\par}\vspace{8mm}}
\small
NOTEBODY
\normalsize

\clearpage
\pagestyle{fancy}
\renewcommand{\contentsname}{\headfont\normalsize\hfill Contents\hfill}
\markboth{Contents}{Contents}
\tableofcontents

\mainmatter
BODY
\end{document}
"""

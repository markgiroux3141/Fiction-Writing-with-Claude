#!/usr/bin/env python
"""Compile story drafts into the body TeX of the Standing Water edition.

    python scripts/build_tex.py <story.md> [<story.md> ...] > out/body.tex

A story is one Markdown file with YAML front matter. Everything the printed
page needs comes from the front matter (`title`) and from the prose; nothing
editorial is injected here, because this book has no editorial apparatus — it
is a trade collection of 1898, not a critical edition.

Handled:
  ---            front matter, and (in the body) a scene break
  # Title        the story title, if the front matter has none
  <!-- ... -->   dropped, so working notes never reach the page
  *italic*       italic
  **bold**       letterspaced caps (the text face has no true small caps)
  paragraphs     everything else

Plate placement comes from plates.json, keyed by story slug:

    { "01-the-game": { "file": "plate-01.jpg", "numeral": "I",
                       "caption": "...", "where": "before" } }
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]      # render/
REPO = ROOT.parent

# --------------------------------------------------------------- front matter


def split_front_matter(text):
    """Return (meta dict, body). Only the scalars this build reads are
    parsed — a real YAML parse is not worth a dependency for two keys, and
    the drafts use block scalars that would need one."""
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw = text[3:end]
            body = text[end + 4:]
            for line in raw.splitlines():
                m = re.match(r"^([a-z_]+):\s*(.*)$", line)
                if m and m.group(2) and not m.group(2).startswith(">"):
                    # YAML ends a scalar at an unquoted " #", and the drafts
                    # annotate their front matter freely — the title reached
                    # the printed page as "The Long Way Round   # chosen by
                    # Mark, 2026-09-10" until this was stripped.
                    val = re.split(r"\s+#", m.group(2))[0]
                    meta[m.group(1)] = val.strip().strip('"')
    return meta, body


# ---------------------------------------------------------------- escaping

TEX_ESCAPE = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def esc(s):
    return "".join(TEX_ESCAPE.get(c, c) for c in s)


# ------------------------------------------------------------------- quotes
# The drafts are written with straight quotes and the book must print curly
# ones, so the conversion happens here and not in the drafts.
#
# It is NOT optional and it cannot be left to the font. The faces are loaded
# with `Ligatures = TeX`, which switches on XeTeX's tex-text mapping, and that
# mapping rewrites a lone `"` as U+201D — a CLOSING quote. Every quotation in
# the first printed facsimile therefore opened with a closing mark. It is not
# an old-typography convention and no period book does it; it is what TeX does
# to a straight quote when you have not told it which way the mark faces.
#
# A quote OPENS when what precedes it is nothing, space, an opening bracket or
# a dash, AND what follows it is not space. The second condition is what gets
# interrupted dialogue right: in `"I never—"` the last mark follows a dash but
# ends the line, so it closes.
_DQ_OPEN = re.compile(r'(?:(?<=^)|(?<=[\s(\[{–—]))"(?=[^\s])')

# Single quotes are apostrophes in this book — possessives, contractions, and
# elisions like 'em and '98 that a word-initial rule would turn the wrong way.
# So everything becomes U+2019 except the one unambiguous case: a single quote
# against the inside of a double quote, which is speech reported inside speech.
_SQ_OPEN = re.compile(r'(?<=[“(])\'')


def quotes(s):
    s = _DQ_OPEN.sub("“", s).replace('"', "”")
    return _SQ_OPEN.sub("‘", s).replace("'", "’")


def inline(s):
    """Markdown inline → TeX. Escaping runs first, so the markers have to be
    found afterwards; they survive escaping untouched."""
    s = quotes(esc(s))
    s = re.sub(r"\*\*(.+?)\*\*", r"\\caps{\1}", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\\emph{\1}", s)
    # An em dash typed as three hyphens or as the character both want the
    # character; TeX ligatures would otherwise eat a spaced hyphen pair.
    s = s.replace("---", "\u2014").replace("--", "\u2013")
    return s


# ------------------------------------------------------------------- body

def clean(body):
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return body


def blocks(body):
    """Yield ('break', None) or ('para', text)."""
    for chunk in re.split(r"\n\s*\n", body):
        chunk = chunk.strip()
        if not chunk:
            continue
        if re.fullmatch(r"(-{3,}|\*{3,}|#{1,6}\s*)", chunk):
            yield ("break", None)
            continue
        # A numbered movement heading — "## 1", "## IV." — is a scene break,
        # not a heading. The movements are the writer's own divisions and a
        # book of this period marks them with a rule and never with a number.
        # Without this the headings fell through to the title case below and
        # were dropped in silence, running five movements together as one
        # unbroken run of prose. An h1 is still the title.
        if re.fullmatch(r"#{2,6}\s*[0-9IVXLC]+\.?", chunk):
            yield ("break", None)
            continue
        if chunk.startswith("#"):
            continue                      # the title; taken from front matter
        yield ("para", " ".join(l.strip() for l in chunk.splitlines()))


def opening(text):
    r"""The first paragraph of a story in a book of this period opens with a
    two-line drop capital and runs its first few words on in caps. Returns
    the \lettrine call."""
    # Turn the quotes before splitting, not after. Each piece below goes
    # through inline() separately, and a mark decided from its neighbours
    # cannot be decided once it is alone in a fragment: an opening quote cut
    # off from the word it introduces came out as a closing one. quotes() is
    # idempotent, so the later inline() calls leave the turned marks alone.
    text = quotes(text)
    m = re.match(r"^(\W*)(\w)(\S*)\s+(.*)$", text, flags=re.S)
    if not m:
        return inline(text)
    pre, initial, rest_of_word, remainder = m.groups()
    # Carry three or four words into the run-in, stopping at a comma so the
    # caps never run past a clause.
    words, carried = remainder.split(), []
    for w in words[:4]:
        carried.append(w)
        if w.endswith((",", ";", ".")):
            break
    tail = " ".join(words[len(carried):])
    runin = " ".join(carried)
    # Whatever stood before the initial — an opening quote, if the scene
    # begins on dialogue. It was captured and then dropped, so a scene opening
    # on speech lost its quote mark and nothing said so. It is set ahead of the
    # drop capital here, which loses nothing; hanging it in the margin instead
    # is the finer setting and is Mark's to call.
    return (f"{inline(pre)}\\lettrine{{{esc(initial)}}}{{{inline(rest_of_word)} "
            f"\\caps{{{inline(runin)}}}}} {inline(tail)}")


def story_slug(path):
    """The plates.json key for a story. Front matter `slug:` wins: the
    manuscript filename follows the title, which can differ from the folder
    ("The Long Way Round" is promoted out of stories/03-ti-jean/), and a
    plate keyed to the folder would then go unfound."""
    meta, _ = split_front_matter(path.read_text(encoding="utf-8"))
    if meta.get("slug"):
        return meta["slug"]
    return path.parent.name if path.name.startswith("draft") else path.stem


def check_quotes(path, text):
    """Warn on a paragraph whose quotes do not pair off. The conversion above
    decides each mark from its neighbours and so cannot tell a typo from a
    convention; an odd count is where it would have guessed. Stderr only —
    the body goes to stdout and a warning must not land in the TeX.

    A continued speech legitimately opens a paragraph without closing it, so
    if the book ever does that, this will say so and can be relaxed then."""
    n = text.count('"')
    if n % 2:
        print(f"   quote warning: {path.name}: {n} quote marks in "
              f"«{text[:60]}…»", file=sys.stderr)


def render_story(path, plate=None):
    meta, body = split_front_matter(path.read_text(encoding="utf-8"))
    title = meta.get("title")
    if not title:
        m = re.search(r"^#\s+(.+)$", body, flags=re.M)
        title = m.group(1).strip() if m else path.stem
    out = []
    if plate and plate.get("where", "before") == "before":
        out.append(plate_tex(plate))
    out.append(f"\\storyhead{{{inline(title)}}}")
    first = True
    for kind, text in blocks(clean(body)):
        if kind == "break":
            # A break arriving before any prose is the movement heading that
            # opens the story, and a rule under the story head would set a
            # division above the first word of the division.
            if not any(b.startswith("\\lettrine") or b.startswith("\\noindent")
                       for b in out):
                continue
            out.append("\\scenebreak")
            first = True                  # a new scene, not a new story
            continue
        check_quotes(path, text)
        if first:
            out.append(opening(text) if not out[-1:] == ["\\scenebreak"]
                       else f"\\noindent {inline(text)}")
            first = False
        else:
            out.append(inline(text))
        out.append("")
    if plate and plate.get("where") == "after":
        out.append(plate_tex(plate))
    out.append("\\storyend")
    return "\n".join(out)


def plate_tex(p):
    # A full-bleed plate is the leaf itself. It carries no numeral and no
    # caption, because there is no margin left to set one in.
    if p.get("full_bleed"):
        return f"\\platefull{{{p['file']}}}"
    return (f"\\plate{{{p['file']}}}{{{p.get('numeral', '')}}}"
            f"{{{inline(p.get('caption', ''))}}}")


def main():
    # The body is emitted on stdout and redirected into out/body.tex by
    # build.sh. On Windows, Python encodes stdout in the console codepage,
    # which is cp1252 here — so every em dash was written as the single byte
    # 0x97. XeLaTeX reads UTF-8, where 0x97 is not a valid start byte, and it
    # neither errors nor stops: the dashes simply came out as garbage glyphs
    # mid-sentence. The file has to be declared UTF-8 explicitly.
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")

    args = [Path(a) for a in sys.argv[1:]]
    if not args:
        sys.exit("usage: build_tex.py <story.md> ...")
    plates_file = ROOT / "plates.json"
    plates = json.loads(plates_file.read_text()) if plates_file.exists() else {}

    pieces = []
    for p in args:
        slug = story_slug(p)
        plate = plates.get(slug)
        pieces.append(render_story(p, plate))
        print(f"   {slug}"
              f"{'' if plate else '   (no plate in plates.json)'}",
              file=sys.stderr)
    print("\n\n".join(pieces))


if __name__ == "__main__":
    main()

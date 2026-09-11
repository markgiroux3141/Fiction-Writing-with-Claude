#!/usr/bin/env python
r"""Choose which file of each story the book is built from, and say why.

    python scripts/sources.py            # one path per line, on stdout
    python scripts/sources.py --explain  # the reasoning, on stderr

Each story can exist twice: as `manuscript/<slug>.md`, promoted, and as
`stories/<slug>/draft-NN.md`, in progress. The rule is **the newest file
wins**, and the build always names the one it picked.

A promoted file is matched to its story folder by the `slug:` in its front
matter, not by its filename. The manuscript copy is named for the title, and
a title chosen after the folder was made ("The Long Way Round" in
`stories/03-ti-jean/`) leaves the two names disagreeing — matching on the
filename then found no promoted copy for the folder AND no folder for the
promoted copy, and printed the story twice, once from each.

The rule used to be "manuscript wins if it exists at all", which is the
obvious reading of a promoted-work directory and is wrong in exactly one
common case: a story is promoted, revising continues, and every build after
that quietly sets the promoted copy. That happened here — a manuscript holding
draft 01 shadowed drafts 02 and 03 for a day, with the build reporting success
and the right number of units each time. Nothing about the output said which
text it was.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def draft_number(p):
    m = re.search(r"draft-(\d+)", p.name)
    return int(m.group(1)) if m else -1


def slug_of(path):
    """The story folder a file belongs to. Front matter `slug:` wins, because
    the manuscript filename follows the title and the folder does not."""
    head = path.read_text(encoding="utf-8", errors="replace")[:4000]
    m = re.search(r"^slug:\s*([^\s#]+)", head, flags=re.M)
    return m.group(1).strip().strip('"') if m else path.stem


def promoted_by_slug():
    """{slug: manuscript path} for everything in manuscript/."""
    return {slug_of(p): p for p in sorted((REPO / "manuscript").glob("*.md"))}


def choose():
    """Return [(path, note)] in reading order."""
    out = []
    seen = set()
    promoted_all = promoted_by_slug()

    for d in sorted((REPO / "stories").glob("*/")):
        slug = d.name
        if slug.startswith("_"):
            continue
        drafts = sorted(d.glob("draft-*.md"), key=draft_number)
        latest = drafts[-1] if drafts else None
        promoted = promoted_all.get(slug)

        if latest and promoted:
            if latest.stat().st_mtime > promoted.stat().st_mtime:
                out.append((latest, f"{latest.name} (newer than the manuscript "
                                    f"copy, which is behind)"))
            else:
                out.append((promoted, f"manuscript/{promoted.name} (promoted; "
                                      f"{latest.name} is older)"))
        elif latest:
            out.append((latest, latest.name))
        elif promoted:
            out.append((promoted, f"manuscript/{promoted.name}"))
        if latest or promoted:
            seen.add(slug)

    # A promoted story whose draft directory has gone away still belongs in
    # the book.
    for slug, p in sorted(promoted_all.items()):
        if slug not in seen:
            out.append((p, f"manuscript/{p.name} (no draft directory)"))

    return out


def main():
    # Windows Python ends a printed line with CRLF, and bash's mapfile keeps
    # the CR — so every path came back with a trailing carriage return and
    # every open() failed with "Invalid argument". Paths crossing into a
    # shell array have to be LF-terminated.
    sys.stdout.reconfigure(newline="\n")

    chosen = choose()
    for path, note in chosen:
        print(f"   {path.parent.name}/  <-  {note}", file=sys.stderr)
        if "--explain" not in sys.argv:
            print(path.as_posix())
    if not chosen:
        print("   no story sources found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
r"""Select the body face.

    python scripts/set_face.py caslon      # writes tex/face.tex
    python scripts/set_face.py --list

The face files live in tex/faces/. Each sets the main font and, if the face
has real small capitals, points \caps at them instead of the synthesised
version in the preamble.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACES = ROOT / "tex" / "faces"


def main():
    names = sorted(p.stem for p in FACES.glob("*.tex"))
    if len(sys.argv) < 2 or sys.argv[1] in ("--list", "-l"):
        print("faces: " + ", ".join(names))
        cur = ROOT / "tex" / "face.tex"
        print("current: " + (cur.read_text(encoding="utf-8").splitlines()[0][2:].strip()
                             if cur.exists() else "(default: oldstandard)"))
        return 0
    want = sys.argv[1]
    src = FACES / f"{want}.tex"
    if not src.exists():
        sys.exit(f"no such face: {want}\nfaces: {', '.join(names)}")
    shutil.copyfile(src, ROOT / "tex" / "face.tex")
    print(f"   face -> {want}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

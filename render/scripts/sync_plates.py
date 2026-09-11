#!/usr/bin/env python
"""Turn the chosen photographs into the plates the book prints.

The originals live outside the repo, under generator filenames carrying
spaces and commas, which graphicx handles badly. plates.json names the source
for each story slug; this resolves it, crops the physical plate edge away,
runs it through a period reproduction process (scripts/plate_process.py), and
writes JPEG into plates/ under a clean name.

    python scripts/sync_plates.py

The cropping is the point and is not a convenience. What comes out of the
image generator is a photograph OF A PLATE — hand-cut edges, pour ridges,
bare corners. No 19th-century process could print any of that: the negative
is masked to a rectangle before it ever reaches the press. Passing the
artifact through whole is a museum-scan aesthetic that belongs to our century
and not to the book's.

What this does NOT do is age the photograph. The image is already an aged
object, and render/scripts/age.py deliberately leaves plate leaves alone for
the same reason.
"""
import json
import sys
from pathlib import Path

from PIL import Image

import plate_process

ROOT = Path(__file__).resolve().parents[1]
PLATES = ROOT / "plates"
# 0.92 x 4.0in of live measure at 400 dpi is ~1470px; 1800 leaves headroom for
# a larger trim without going back to the 2500px originals on every build.
LONG_EDGE = 1800
# Live width of a plate on the page, which fixes the resolution a screen
# ruling has to be computed against.
PLATE_INCHES = 4.2
# Trim aspect (height / width): 5.5 x 8.25 in. A full-bleed plate is cropped
# to this, never stretched to it.
PAGE_ASPECT = 8.25 / 5.5


def main():
    spec = json.loads((ROOT / "plates.json").read_text(encoding="utf-8"))
    root = Path(spec.get("_photos_root", ""))
    PLATES.mkdir(exist_ok=True)

    ok = missing = 0
    for key, p in spec.items():
        # Underscore keys are settings unless they carry a src; _cover and
        # _frontispiece are real images that simply have no story slug.
        if not isinstance(p, dict) or "src" not in p:
            continue
        # A src with a slash in it is relative to the repo, which is how a
        # photograph that already lives inside the project gets referenced
        # without moving it. Everything else sits under _photos_root.
        src = (ROOT.parent / p["src"]) if "/" in p["src"] else (root / p["src"])
        dst = PLATES / p["file"]
        if not src.exists():
            print(f"   WARN  {key}: no such photograph — {p['src']}")
            missing += 1
            continue
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            print(f"   {p['file']}  (current)")
            ok += 1
            continue
        img = Image.open(src).convert("RGB")
        name = p.get("process", "photogravure")
        if name != "as_is":
            crop = p.get("crop")
            img = plate_process.trim_plate_edge(
                img, crop=tuple(crop) if crop else None,
                inset=p.get("inset", 0.04))
        # Resize before the process runs, not after: the aquatint grain, the
        # screen ruling and the plate mark are all measured in output pixels,
        # so processing at the source size and shrinking afterwards would
        # scale the process itself along with the picture.
        img.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)
        kw = dict(p.get("process_args", {}))
        if name == "as_is":
            kw.setdefault("aspect", PAGE_ASPECT)
            kw.setdefault("inset", p.get("inset", 0.015))
        if name == "halftone":
            # The screen ruling is a fact about the page, so the resolution
            # the plate is reproduced at has to be handed to it.
            kw.setdefault("ppi", img.size[0] / PLATE_INCHES)
            kw.setdefault("margin", 0.085)
        img = plate_process.PROCESSES[name](img, **kw)
        img.save(dst, "JPEG", quality=94, optimize=True)
        print(f"   {p['file']}  <-  {p['src']}"
              f"  {img.size[0]}x{img.size[1]}  {name}")
        ok += 1

    print(f"   {ok} plate(s) synced, {missing} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

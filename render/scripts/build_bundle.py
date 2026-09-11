#!/usr/bin/env python
"""Turn a PDF into a book bundle the reader can open.

    python scripts/build_bundle.py out/standing-water-facsimile.pdf ../flip/books \
        --id standing-water --title "Standing Water" \
        --subtitle "Of Roots, Reflections, and the Faces Beneath" \
        --boards ../"cover art"/cover.png

A bundle is a directory and nothing more:

    <books>/<id>/book.json
    <books>/<id>/pages/0001.jpg ...

`book.json` is the whole contract between a book and the app. Any PDF can be
turned into one; nothing in the format knows about this project's pipeline,
which is the point — the app reads bundles, not facsimiles, so a book from
somewhere else is a first-class book.

The PDF is rasterized to screen resolution on the way in, deliberately. The
facsimile is a 200 dpi print raster and a tablet leaf is about 700 px wide, so
shipping the PDF and decoding it on the device would cost three times the bytes
and a PDF engine's memory to show the same picture.

`id` is the bundle's identity and must be stable across rebuilds: bookmarks and
last-read position hang off it, and changing it silently orphans a reader's
place in the book.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

SCHEMA = 1
DEFAULT_WIDTH = 1100     # px per leaf — ~1.5x on a 1408px-wide tablet spread


def make_back_board(cover, size):
    """A plausible back board, derived from the front one.

    The cover is the front board: ornate blind-stamped border, gilt title, and
    the mounted print set into it. The back board of a book like this is the
    same cloth with the same border and nothing inside it.

    So it is built by keeping the front board's own border and emptying the
    panel it frames — the title and the print are replaced with flat board of
    the cloth's own colour, carrying a generated weave.

    The first version instead filled the panel with the front board's own
    high-frequency detail, on the theory that a high-pass keeps texture. A
    high-pass keeps EDGES, and the strongest edges in that panel are the
    lettering and the print's border, so the back board came out with a
    legible mirror-image "Standing Water" embossed across it. Bookcloth at
    this scale is a fine weave, and a weave is cheaper to generate than to
    rescue.
    """
    w, h = size
    src = (Image.open(cover).convert("RGB")
           .transpose(Image.FLIP_LEFT_RIGHT)
           .resize((w, h), Image.LANCZOS))
    a = np.asarray(src, dtype=np.float32)

    mx = int(round(w * 0.085))
    my = int(round(h * 0.058))
    panel = a[my:h - my, mx:w - mx]
    ph, pw, _ = panel.shape

    # Cloth colour: the dark end of the board, not the mean — the mean is
    # dragged light by the print and the gilt, which are the two things this
    # is removing.
    flat_all = a.reshape(-1, 3)
    lum = flat_all.mean(axis=1)
    cloth = flat_all[lum <= np.percentile(lum, 45)].mean(axis=0)

    rng = np.random.default_rng(11)
    n = rng.normal(0.0, 5.0, (ph, pw)).astype(np.float32)
    n = np.asarray(
        Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8), "L")
        .filter(ImageFilter.GaussianBlur(0.5)), dtype=np.float32) - 128.0
    yy = np.arange(ph, dtype=np.float32)[:, None]
    xx = np.arange(pw, dtype=np.float32)[None, :]
    weave = (np.sin(yy * 1.9) + np.sin(xx * 1.9)) * 1.6
    flat = cloth[None, None, :] + (n + weave)[:, :, None]

    # A back board is not blank: it carries the same blind-stamped double rule
    # the front does, pressed into the cloth — a dark trough with a light
    # ridge beside it, never a printed rule. Without it the panel reads as a
    # black rectangle rather than as board.
    def blind_rule(inset):
        i = int(round(min(pw, ph) * inset))
        t = max(1, int(round(min(pw, ph) * 0.006)))
        for y0, y1, x0, x1 in ((i, i + t, i, pw - i), (ph - i - t, ph - i, i, pw - i),
                               (i, ph - i, i, i + t), (i, ph - i, pw - i - t, pw - i)):
            flat[y0:y1, x0:x1] *= 0.72
            flat[max(0, y0 - t):y0, max(0, x0 - t):x1] *= 1.18
    blind_rule(0.035)
    blind_rule(0.075)

    # Feather generously: a narrow feather leaves a visible rectangular seam
    # where the flat panel meets the real board.
    f = max(2, int(round(min(pw, ph) * 0.07)))
    mask = np.ones((ph, pw), dtype=np.float32)
    ramp = np.linspace(0, 1, f, dtype=np.float32)
    mask[:f, :] *= ramp[:, None]
    mask[-f:, :] *= ramp[::-1, None]
    mask[:, :f] *= ramp[None, :]
    mask[:, -f:] *= ramp[None, ::-1]
    a[my:h - my, mx:w - mx] = panel * (1 - mask[:, :, None]) + flat * mask[:, :, None]

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ey = np.minimum(yy, h - 1 - yy) / (h * 0.5)
    ex = np.minimum(xx, w - 1 - xx) / (w * 0.5)
    vign = np.clip(np.minimum(ey, ex) * 3.0, 0, 1) ** 0.6
    a *= (0.74 + 0.26 * vign)[:, :, None]

    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def native_dpi(pdf, width):
    """The dpi that renders this PDF at `width` pixels, with no resampling.

    The first version hardcoded 150 dpi and then resized the result up to
    `width`. On a 5.5-inch page that is 825 px being stretched to 1100 — so
    every page in every bundle was a third larger than the detail it carried,
    and the pages were SOFTER and BIGGER than rendering at the right dpi:
    upscaling injects interpolation noise, which JPEG then spends bytes
    encoding. Deriving the dpi from the trim removes both problems at once.
    """
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    inches = None
    for line in out.stdout.splitlines():
        if line.lower().startswith("page size:"):
            try:
                inches = float(line.split(":", 1)[1].strip().split()[0]) / 72.0
            except (ValueError, IndexError):
                pass
            break
    if not inches:
        return 150          # pdfinfo unavailable; the old behaviour
    return max(1, int(round(width / inches)))


def rasterize(pdf, pages_dir, width, dpi=None):
    if dpi is None:
        dpi = native_dpi(pdf, width)
        print(f"   rasterizing at {dpi} dpi for {width}px (no resampling)")
    for old in pages_dir.glob("*.jpg"):
        old.unlink()
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-jpeg", "-r", str(dpi), str(pdf),
                        str(Path(tmp) / "pg")], check=True)
        raw = sorted(Path(tmp).glob("pg*.jpg"))
        if not raw:
            sys.exit("pdftoppm produced no pages")
        size = None
        for i, p in enumerate(raw, start=1):
            img = Image.open(p).convert("RGB")
            img = img.resize((width, round(img.height * width / img.width)),
                             Image.LANCZOS)
            size = img.size
            img.save(pages_dir / f"{i:04d}.jpg", "JPEG", quality=82,
                     optimize=True)
    return len(raw), size


def write_index(books_dir):
    """Regenerate books/index.js from every bundle present.

    A .js file assigning a global rather than JSON, and with every manifest
    INLINED, because fetch() of a local file is blocked under file:// — and
    the same flip/ directory has to keep working when opened by double-
    clicking it on Windows. One generated file means the shelf needs no
    network and no fetch to list what is bundled.
    """
    books = []
    for man in sorted(books_dir.glob("*/book.json")):
        m = json.loads(man.read_text(encoding="utf-8"))
        m["base"] = f"books/{man.parent.name}"
        books.append(m)
    payload = json.dumps(books, indent=2)
    (books_dir / "index.js").write_text(
        "// Generated by render/scripts/build_bundle.py — do not edit.\n"
        f"window.BUNDLED_BOOKS = {payload};\n", encoding="utf-8")
    (books_dir / "index.json").write_text(payload + "\n", encoding="utf-8")
    return [b["id"] for b in books]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("books_dir")
    ap.add_argument("--id", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default=None)
    ap.add_argument("--author", default=None)
    ap.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    ap.add_argument("--dpi", type=int, default=None,
                    help="rasterization dpi; derived from --width and the "
                         "page size when omitted, which is what you want")
    ap.add_argument("--single", action="store_true",
                    help="one leaf at a time rather than a two-page spread")
    ap.add_argument("--boards", default=None, metavar="COVER_PNG",
                    help="front board image; a back board is derived from it "
                         "and appended, and the front is assumed to be page 1 "
                         "of the PDF already")
    ap.add_argument("--index-only", action="store_true",
                    help="just regenerate books/index.js")
    args = ap.parse_args()

    books_dir = Path(args.books_dir)
    books_dir.mkdir(parents=True, exist_ok=True)

    if args.index_only:
        print("   index:", ", ".join(write_index(books_dir)) or "(empty)")
        return

    dest = books_dir / args.id
    pages_dir = dest / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    count, size = rasterize(Path(args.pdf), pages_dir, args.width, args.dpi)
    print(f"   {count} page(s) at {size[0]}x{size[1]}")

    names = [f"pages/{i:04d}.jpg" for i in range(1, count + 1)]

    if args.boards:
        cover = Path(args.boards)
        if not cover.exists():
            sys.exit(f"no cover at {cover}")
        # Only the BACK board is added. The front board is page one of the
        # PDF, so prepending it again would show the cover twice.
        make_back_board(cover, size).save(pages_dir / "back-board.jpg", "JPEG",
                                          quality=88, optimize=True)
        # The leaves between the two boards have to pair up: the reader shows
        # the first and last alone, as a closed book does, so an odd number in
        # between leaves one spread unmatched and every spread after it off by
        # one. The book's own last leaf is blank, so duplicating it as the
        # pastedown inside the back board is both the fix and what is there.
        if (len(names) + 1) % 2:
            shutil.copyfile(pages_dir / Path(names[-1]).name,
                            pages_dir / "back-pastedown.jpg")
            names.append("pages/back-pastedown.jpg")
            print("   + back pastedown, to keep the spreads paired")
        names.append("pages/back-board.jpg")
        print("   + back board (the front is page one of the PDF)")

    manifest = {
        "schema": SCHEMA,
        "id": args.id,
        "title": args.title,
        "subtitle": args.subtitle,
        "author": args.author,
        "build": time.strftime("%Y%m%d-%H%M%S"),
        "pageWidth": size[0],
        "pageHeight": size[1],
        "spread": not args.single,
        "showCover": True,
        "cover": names[0],
        "count": len(names),
        "pages": names,
    }
    (dest / "book.json").write_text(json.dumps(manifest, indent=2),
                                    encoding="utf-8")
    print(f"   -> {dest / 'book.json'} ({len(names)} leaves)")
    print("   index:", ", ".join(write_index(books_dir)))


if __name__ == "__main__":
    main()

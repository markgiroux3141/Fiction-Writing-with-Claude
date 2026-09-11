#!/usr/bin/env python
"""Turn a built PDF into the page images the flipbook reads.

    python scripts/build_flip.py out/standing-water-facsimile.pdf ../flip

Writes <dest>/pages/p-0001.jpg .. and <dest>/pages.json. The viewer is static
HTML and reads nothing else, so the whole flip/ directory can be served from
anywhere or opened over a local file server.

The facsimile is already a raster at 200 dpi; this downsamples to a screen
resolution, because a flipbook that loads 90 MB of print-resolution JPEG to
show two pages at a time is a flipbook nobody waits for.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

WIDTH = 1100          # px per leaf — enough for a 2x display at ~550 CSS px


def make_back_board(cover, size):
    """A plausible back board, derived from the front one.

    The cover is the front board: ornate blind-stamped border, gilt title, and
    the mounted print set into it. The back board of a book like this is the
    same cloth with the same border and nothing inside it.

    So it is built by keeping the front board's own border and emptying the
    panel it frames — the title and the print are replaced with flat board of
    the cloth's own colour, carrying the cloth's own grain lifted off the
    original by a high-pass. The whole thing is mirrored, because a back board
    has its spine edge on the other side.

    The first version instead sampled a patch of margin and mirror-tiled it.
    The patch had a slice of the ornate border in it, so the result was
    vertical stripes: wallpaper, not bookcloth.
    """
    w, h = size
    src = (Image.open(cover).convert("RGB")
           .transpose(Image.FLIP_LEFT_RIGHT)
           .resize((w, h), Image.LANCZOS))
    a = np.asarray(src, dtype=np.float32)

    # The panel inside the border. Equal absolute margins on all four sides.
    mx = int(round(w * 0.085))
    my = int(round(h * 0.058))
    panel = a[my:h - my, mx:w - mx]
    ph, pw, _ = panel.shape

    # Cloth colour: the dark end of the board, not the mean — the mean is
    # dragged light by the print and the gilt, which are the two things this
    # is removing.
    dark = a.reshape(-1, 3)
    lum = dark.mean(axis=1)
    cloth = dark[lum <= np.percentile(lum, 45)].mean(axis=0)

    # Cloth grain, generated rather than lifted. Taking the panel's own high
    # frequencies looked like the cheaper trick and was: a high-pass keeps
    # EDGES, and the strongest edges in that panel are the title and the
    # border of the mounted print, so the back board came out with a legible
    # mirror-image "Standing Water" embossed across it. Bookcloth at this
    # scale is a fine weave, and a weave is cheaper to make than to rescue.
    rng = np.random.default_rng(11)
    n = rng.normal(0.0, 5.0, (ph, pw)).astype(np.float32)
    n = np.asarray(
        Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8), "L")
        .filter(ImageFilter.GaussianBlur(0.5)), dtype=np.float32) - 128.0
    yy = np.arange(ph, dtype=np.float32)[:, None]
    xx = np.arange(pw, dtype=np.float32)[None, :]
    weave = (np.sin(yy * 1.9) + np.sin(xx * 1.9)) * 1.6
    grain = (n + weave)[:, :, None]

    flat = cloth[None, None, :] + grain

    # A back board is not blank: it carries the same blind-stamped double rule
    # the front does, pressed into the cloth. It is an emboss, so each line is
    # a dark trough with a light ridge beside it, never a printed rule — and
    # without it the panel reads as a black rectangle rather than as board.
    def blind_rule(inset):
        i = int(round(min(pw, ph) * inset))
        t = max(1, int(round(min(pw, ph) * 0.006)))
        for y0, y1, x0, x1 in ((i, i + t, i, pw - i), (ph - i - t, ph - i, i, pw - i),
                               (i, ph - i, i, i + t), (i, ph - i, pw - i - t, pw - i)):
            flat[y0:y1, x0:x1] *= 0.72
            flat[max(0, y0 - t):y0, max(0, x0 - t):x1] *= 1.18
    blind_rule(0.035)
    blind_rule(0.075)

    # Feather the fill into the border. Generously: a narrow feather leaves a
    # visible rectangular seam where the flat panel meets the real board.
    f = max(2, int(round(min(pw, ph) * 0.07)))
    mask = np.ones((ph, pw), dtype=np.float32)
    ramp = np.linspace(0, 1, f, dtype=np.float32)
    mask[:f, :] *= ramp[:, None]
    mask[-f:, :] *= ramp[::-1, None]
    mask[:, :f] *= ramp[None, :]
    mask[:, -f:] *= ramp[None, ::-1]
    a[my:h - my, mx:w - mx] = panel * (1 - mask[:, :, None]) + flat * mask[:, :, None]

    # Handled boards go dark at the edges and corners.
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ey = np.minimum(yy, h - 1 - yy) / (h * 0.5)
    ex = np.minimum(xx, w - 1 - xx) / (w * 0.5)
    vign = np.clip(np.minimum(ey, ex) * 3.0, 0, 1) ** 0.6
    a *= (0.74 + 0.26 * vign)[:, :, None]

    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: build_flip.py <pdf> <dest-dir>")
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    pages_dir = dest / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for old in pages_dir.glob("p-*.jpg"):
        old.unlink()

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-jpeg", "-r", "150", str(src),
                        str(Path(tmp) / "pg")], check=True)
        raw = sorted(Path(tmp).glob("pg*.jpg"))
        if not raw:
            sys.exit("pdftoppm produced no pages")
        size = None
        for i, p in enumerate(raw, start=1):
            img = Image.open(p).convert("RGB")
            h = round(img.height * WIDTH / img.width)
            img = img.resize((WIDTH, h), Image.LANCZOS)
            size = img.size
            img.save(pages_dir / f"p-{i:04d}.jpg", "JPEG",
                     quality=82, optimize=True)
        print(f"   {len(raw)} page(s) at {size[0]}x{size[1]}")

    # --- the boards --------------------------------------------------------
    # The text block is the aged PDF; the covers are not paper and are not
    # aged, so they are added here rather than being bound into the facsimile.
    names = [f"pages/p-{i:04d}.jpg" for i in range(1, len(raw) + 1)]
    cover = Path(__file__).resolve().parents[2] / "cover art" / "cover.png"
    if cover.exists():
        # Only the BACK board is added here. The front board is page one of
        # the PDF, so prepending it again would show the cover twice.
        back = make_back_board(cover, size)
        back.save(pages_dir / "cover-back.jpg", "JPEG", quality=88,
                  optimize=True)
        # The leaves between the two boards have to pair up. page-flip shows
        # the first and last leaves alone, as a closed book does, so an odd
        # number in between leaves one spread unmatched and every spread after
        # it off by one. The book's own last leaf is blank, so duplicating it
        # as the pastedown inside the back board is both the fix and what is
        # actually there.
        if (len(names) + 1) % 2:
            shutil.copyfile(pages_dir / Path(names[-1]).name,
                            pages_dir / "pastedown-back.jpg")
            names = names + ["pages/pastedown-back.jpg"]
            print("   + back pastedown, to keep the spreads paired")
        names = names + ["pages/cover-back.jpg"]
        print("   + back board (the front is page one of the PDF)")
    else:
        print(f"   WARN  no cover at {cover}")

    manifest = {
        "title": "Standing Water",
        "count": len(names),
        "width": size[0],
        "height": size[1],
        "pages": names,
    }
    (dest / "pages.json").write_text(json.dumps(manifest, indent=2),
                                     encoding="utf-8")
    # Also as a script that assigns a global. fetch() of a local JSON file is
    # blocked by CORS under file://, so a manifest loaded with <script src>
    # is what lets index.html be opened by double-clicking it.
    (dest / "pages.js").write_text(
        "window.BOOK = " + json.dumps(manifest, indent=2) + ";\n",
        encoding="utf-8")
    print(f"   -> {dest / 'pages.js'}")


if __name__ == "__main__":
    main()

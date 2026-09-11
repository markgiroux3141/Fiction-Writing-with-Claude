#!/usr/bin/env python
"""Age a clean PDF into a facsimile of a handled, printed book.

    python age.py clean.pdf aged.pdf [--dpi 300] [--pages 1-12]

The clean build stays clean: everything here is a post-process, so the
typography is never compromised to serve the texture.

Per page, in order:
  1. render at DPI via pdftoppm (poppler — no Ghostscript needed)
  2. lift the ink as a mask and vary its density with low-frequency noise,
     so some letters print heavy and some starve, as on a hand-fed press
     (--fade sets how deep the starving goes; the default halves it)
  3. spread the ink slightly (the bite of type into damp paper)
  4. multiply the ink over a freshly generated sheet of book paper
  5. bleed a faint mirror of the previous page's ink through the sheet
  6. drift the page: sub-degree rotation, sub-percent scale, a few px of slip
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import img2pdf
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import paper  # noqa: E402
import paper_scan  # noqa: E402


def rasterize(pdf, dpi, workdir, first=None, last=None):
    """Colour raster. The text pages are greyscale anyway; the plates are
    photographs and must keep their colour, which is also how they are
    detected below."""
    stem = str(Path(workdir) / "pg")
    cmd = ["pdftoppm", "-png", "-r", str(dpi)]
    if first:
        cmd += ["-f", str(first)]
    if last:
        cmd += ["-l", str(last)]
    cmd += [str(pdf), stem]
    subprocess.run(cmd, check=True)
    return sorted(Path(workdir).glob("pg*.png"))


def ink_mask(page_img):
    """0..1 coverage. The clean render is black on white, so invert."""
    a = np.asarray(page_img.convert("L"), dtype=np.float32) / 255.0
    return 1.0 - a


def is_plate(png, thresh=0.15):
    """True if the page carries a photograph.

    The Necronomicon pipeline this came from tested saturation, because every
    plate in that book was a warm sepia and every text page was neutral. Here
    the plates are wet-plate collodion and several of them — the sheet on the
    staircase, most obviously — are all but neutral grey, so the saturation
    test passed them through the ageing pass as if they were type.

    Continuous tone is the reliable signal instead. A text page is white with
    a few per cent of near-black ink and a thin antialiased fringe; almost
    nothing sits in the middle. A photograph fills half the leaf with midtones.
    """
    a = np.asarray(Image.open(png).convert("L"), dtype=np.float32) / 255.0
    mid = float(((a > 0.12) & (a < 0.88)).mean())
    return mid > thresh


def age_plate_page(png, seed, **_):
    """A plate leaf passes through untouched.

    Every plate in this book is a full-bleed photograph of a leaf that is
    already an aged object — a print on its own mount, with its own paper, its
    own tone and its own damage. There is nothing left for the ageing pass to
    add, and everything it might add is a second copy of something the
    photograph already has.

    An earlier version multiplied the book's paper over the plate page so that
    the mount would match the text block. That was right while the plate was a
    small image centred on a leaf of the book's own paper. Once the photograph
    became the whole leaf it was simply a second sheet of paper laid over the
    first, and it showed: the plate came out visibly darker and browner than
    the photograph it was made from.
    """
    return Image.open(png).convert("RGB")


# How much of the press's under-inking to keep. The uneven-inking field and
# the roller band together take the faintest type down to 0.56 of full
# density, and at that depth a few passages on every page are genuinely hard
# to read — a facsimile is meant to look handled, not to cost the reader the
# sentence. 0.5 halves the starvation, so the faintest type prints at about
# 0.78 and the pattern of variation is unchanged, only shallower. Heavy
# passages are not touched: the field runs above full density as well, and
# nothing above 1.0 is rescaled, so no page comes out darker than before.
FADE = 0.5


def age_page(png, seed, prev_ink=None, gutter="left", age=1.0,
             sheets=(), leaf=0, verso=False, fade=FADE):
    src = Image.open(png)
    w, h = src.size
    shape = (h, w)
    rng = np.random.default_rng(seed)

    ink = ink_mask(src)

    # --- uneven inking across the forme -----------------------------------
    density = 0.62 + 0.72 * paper.fbm(shape, np.random.default_rng(seed + 11),
                                      octaves=4, cells=3)
    # a press is inked in bands as the roller travels
    band = 0.90 + 0.10 * np.sin(np.linspace(0, np.pi * rng.uniform(1.5, 3.0), h))[:, None]
    # fbm is normalised to 0..1 on every page, so this field spans exactly
    # 0.62..1.34 each time and the band takes another tenth off in places:
    # the floor is a fact about the page, not an occasional accident. Pull
    # only the starved side back toward full density.
    starve = density * band
    starve = np.where(starve < 1.0, 1.0 - (1.0 - starve) * fade, starve)
    ink = np.clip(ink * starve, 0, 1)

    # --- bite: type presses out into damp paper ---------------------------
    spread = np.asarray(
        Image.fromarray((ink * 255).astype(np.uint8), "L")
        .filter(ImageFilter.MaxFilter(3))
        .filter(ImageFilter.GaussianBlur(0.55)), dtype=np.float32) / 255.0
    ink = np.clip(np.maximum(ink, spread * 0.55), 0, 1)

    # a little grit so edges are never mathematically clean
    ink = np.clip(ink - rng.normal(0.0, 0.035, shape).astype(np.float32) * (ink > 0.05), 0, 1)

    # --- the sheet ---------------------------------------------------------
    if sheets:
        sheet = paper_scan.scanned_paper(shape, seed=seed * 7919, gutter=gutter,
                                         age=age, sheets=sheets, leaf=leaf,
                                         verso=verso).astype(np.float32)
    else:
        sheet = paper.book_paper(shape, seed=seed * 7919, gutter=gutter,
                                 age=age).astype(np.float32)

    # --- show-through from the reverse ------------------------------------
    if prev_ink is not None and prev_ink.shape == shape:
        through = np.asarray(
            Image.fromarray((prev_ink[:, ::-1] * 255).astype(np.uint8), "L")
            .filter(ImageFilter.GaussianBlur(1.6)), dtype=np.float32) / 255.0
        sheet -= (through * 15.0)[:, :, None] * np.array([0.55, 0.75, 1.0])

    # --- lay the ink down --------------------------------------------------
    # warm near-black; iron-gall and lampblack both brown with age
    ink_col = np.array([38.0, 30.0, 26.0])
    out = sheet * (1.0 - ink[:, :, None]) + ink_col[None, None, :] * ink[:, :, None]
    out = np.clip(out, 0, 255).astype(np.uint8)

    img = Image.fromarray(out, "RGB")

    # --- the sheet was not fed square --------------------------------------
    angle = rng.normal(0.0, 0.16)
    scale = 1.0 + rng.normal(0.0, 0.0022)
    img = img.rotate(angle, resample=Image.BICUBIC, expand=False,
                     fillcolor=(214, 202, 176))
    if abs(scale - 1.0) > 1e-4:
        nw, nh = int(w * scale), int(h * scale)
        img = img.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGB", (w, h), (214, 202, 176))
        canvas.paste(img, ((w - nw) // 2 + int(rng.normal(0, w * 0.0015)),
                           (h - nh) // 2 + int(rng.normal(0, h * 0.0015))))
        img = canvas

    return img, ink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--pages", default=None, help="e.g. 1-12")
    ap.add_argument("--age", type=float, default=1.0,
                    help="0.4 lightly shelved, 1.0 default, 1.8 buried")
    ap.add_argument("--fade", type=float, default=FADE,
                    help="how much of the press's under-inking to keep: "
                         "1.0 the full starve (faintest type at 0.56 of "
                         "density, hard to read), 0.5 the default, 0.0 evenly "
                         "inked")
    ap.add_argument("--paper-dir", default=None,
                    help="directory of photographed sheets to use as the "
                         "ground; falls back to procedural paper if empty")
    args = ap.parse_args()

    first = last = None
    if args.pages:
        parts = args.pages.split("-")
        first = int(parts[0])
        last = int(parts[-1])

    first_page = first or 1
    with tempfile.TemporaryDirectory() as tmp:
        pages = rasterize(args.src, args.dpi, tmp, first, last)
        if not pages:
            sys.exit("pdftoppm produced no pages")
        # Each finished page is written straight out as a JPEG and dropped.
        # Holding 120 pages of RGB in a list is about a gigabyte before the
        # float32 working arrays are counted, and it is what killed the first
        # whole-book run at page 68 of 120.
        sheets = paper_scan.find_sheets(args.paper_dir) if args.paper_dir else []
        if args.paper_dir:
            # Closed explicitly: an open PIL handle on a file inside the
            # TemporaryDirectory stops Windows deleting it, and the whole run
            # ends in a PermissionError after the PDF has already been written.
            with Image.open(pages[0]) as probe:
                page_aspect = probe.size[1] / probe.size[0]
            paper_scan.report(sheets, page_aspect)
            if not sheets:
                print("   no scans found — using procedural paper")

        made, prev, n_plates = [], None, 0
        for i, p in enumerate(pages):
            n0 = (first_page - 1) + i
            if is_plate(p):
                img = age_plate_page(p, seed=2000 + i)
                prev = None          # a plate bleeds nothing through
                n_plates += 1
                label = "plate    "
            else:
                gutter = "left" if (i % 2 == 0) else "right"   # recto / verso
                # A physical leaf carries two pages. Page indices 0 and 1 are
                # the two sides of leaf 0, and the verso is the recto seen
                # from behind — so it gets the same scan, mirrored.
                img, prev = age_page(p, seed=1000 + i, prev_ink=prev,
                                     gutter=gutter, age=args.age,
                                     sheets=sheets, leaf=n0 // 2,
                                     verso=bool(n0 % 2), fade=args.fade)
                label = "aged page"
            leaf = Path(tmp) / f"aged-{i:04d}.jpg"
            # The dpi tag matters: img2pdf sizes each page from the image's own
            # resolution metadata and silently falls back to 96 without it,
            # which would give a 11.5in-wide page instead of 5.5in.
            img.save(leaf, "JPEG", quality=88, optimize=True,
                     dpi=(args.dpi, args.dpi))
            made.append(str(leaf))
            img = None
            print(f"   {label} {i+1}/{len(pages)}", flush=True)

        print(f"   {n_plates} plate(s) passed through, "
              f"{len(pages) - n_plates} sheet(s) aged")

        # img2pdf embeds the JPEGs without re-encoding and streams, so peak
        # memory is one page rather than the whole book.
        with open(args.dst, "wb") as fh:
            img2pdf.convert(made, outputstream=fh)
    print(f"   -> {args.dst}")


if __name__ == "__main__":
    main()

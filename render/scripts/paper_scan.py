#!/usr/bin/env python
"""Use photographed sheets of real paper as the ground, instead of noise.

`paper.book_paper` builds a sheet out of fractal noise. It is good at the
things noise is good at — broad mottle, fibre, an even scatter of foxing — and
it cannot do the things that actually make old paper look old: the way a stain
has a hard tide line and a soft centre, the way damage clusters, the way a
sheet remembers being folded. A photograph of real paper has all of that for
free.

What a photograph does NOT know is that it is a page in a bound book, and that
is the whole difficulty. Two things have to be imposed on it:

  The gutter edge does not exist.  In a bound book you see the fore-edge, the
  head and the tail. You never see the spine edge of the leaf: it is sewn into
  the binding. A scan with four ragged, darkened, torn edges reads as a loose
  leaf lying on a table, and in a two-page spread two of those ragged edges
  meet in the middle of the book, which nothing bound has ever looked like.
  So the scan is cropped INTO — the torn edges are thrown away — and the
  directional tanning is put back procedurally, heaviest at the fore-edge.

  A leaf has two sides.  Pages 3 and 4 are the same piece of paper. Their
  stains are the same stains seen from the other side, so the verso is the
  recto mirrored, with the gutter and the tanning reversed. This also halves
  how many sheets are needed, and is the detail that makes a repeated sheet
  read as a book rather than as a repeat.
"""
import numpy as np
from PIL import Image, ImageFilter

import paper

# How far to crop inside the photographed leaf, as a fraction of each side.
# Enough to lose the torn edge, the darkened rim and the white surround.
INSET = 0.055

_CACHE = {}


def find_sheets(dirpath):
    """Every image in the directory, in name order, so page N is stable."""
    from pathlib import Path
    d = Path(dirpath)
    if not d.is_dir():
        return []
    return sorted(p for p in d.iterdir()
                  if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".tif",
                                          ".tiff", ".webp"))


def _prepared(path, shape):
    """Crop into the leaf, then cover-crop to the page aspect and resize."""
    key = (str(path), shape)
    if key in _CACHE:
        return _CACHE[key]

    img = Image.open(path).convert("RGB")
    w, h = img.size
    dx, dy = int(w * INSET), int(h * INSET)
    img = img.crop((dx, dy, w - dx, h - dy))

    # Cover-crop rather than stretch. Stretching a sheet of paper to a
    # different aspect skews the fibre and the stains, and paper grain is one
    # of the few textures where the eye notices immediately.
    th, tw = shape
    want = tw / th
    w, h = img.size
    have = w / h
    if have > want:
        nw = int(round(h * want))
        x = (w - nw) // 2
        img = img.crop((x, 0, x + nw, h))
    elif have < want:
        nh = int(round(w / want))
        y = (h - nh) // 2
        img = img.crop((0, y, w, y + nh))

    img = img.resize((tw, th), Image.LANCZOS)
    a = np.asarray(img, dtype=np.float32)
    _CACHE[key] = a
    return a


def cover_ratio(path):
    """How much of a scan survives the crop to a given page aspect, and the
    aspect of the leaf itself. Reported by the build so a mismatch is visible
    rather than silently cropped away."""
    img = Image.open(path)
    w, h = img.size
    dx, dy = int(w * INSET), int(h * INSET)
    return (w - 2 * dx) / (h - 2 * dy)


def scanned_paper(shape, seed, gutter="left", age=1.0,
                  sheets=(), leaf=0, verso=False):
    """A sheet of the real thing, made into a page of a bound book.

    Same contract as paper.book_paper: returns uint8 (h, w, 3).
    """
    if not sheets:
        return paper.book_paper(shape, seed, gutter=gutter, age=age)

    a = _prepared(sheets[leaf % len(sheets)], shape).copy()
    if verso:
        # The other side of the same leaf.
        a = a[:, ::-1, :]

    rng = np.random.default_rng(seed)
    h, w = shape

    # --- vary a reused sheet ------------------------------------------------
    # With a dozen scans and two hundred pages every sheet comes round many
    # times. A slow tonal drift and a shifted mottle break the recurrence
    # without touching the structure that makes the scan worth having.
    a *= rng.uniform(0.965, 1.030)
    drift = paper.fbm(shape, rng, octaves=3, cells=2) - 0.5
    a += (drift * 13.0 * age)[:, :, None] * np.array([1.0, 0.95, 0.84])

    # --- put the book physics back -----------------------------------------
    # The scan was cropped inside its own edges, so it now carries no edge
    # tone at all. A leaf in a book tans at the fore-edge, head and tail,
    # where air and daylight and fingers reach it, and stays clean at the
    # gutter.
    edge = paper._edge_field(shape, gutter=gutter, strength=1.0, falloff=2.2)
    a -= (edge * 26.0 * age)[:, :, None] * np.array([0.30, 0.62, 1.0])

    # A little extra grime in the outer corner, which is where a reader's
    # thumb actually lands.
    thumb = np.zeros(shape, dtype=np.float32)
    cy = int(h * rng.uniform(0.42, 0.72))
    cx = 0 if gutter == "right" else w - 1
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((yy - cy) / (h * 0.22)) ** 2 + ((xx - cx) / (w * 0.30)) ** 2)
    thumb = np.clip(1.0 - r, 0, 1) ** 2
    a -= (thumb * 11.0 * age)[:, :, None] * np.array([0.5, 0.75, 1.0])

    return np.clip(a, 0, 255).astype(np.uint8)


def report(sheets, page_aspect):
    """One line per scan, saying what the crop costs. `page_aspect` is
    height/width of the trim."""
    if not sheets:
        return
    print(f"   {len(sheets)} paper scan(s); page is 1:{page_aspect:.3f}")
    for s in sheets:
        img = Image.open(s)
        a = img.size[1] / img.size[0]
        # After the inset the leaf keeps its aspect; the cover-crop then eats
        # the long dimension.
        loss = 1.0 - min(a / page_aspect, page_aspect / a)
        flag = "" if loss < 0.02 else f"  <- {loss * 100:.0f}% cropped away"
        print(f"     {s.name}  {img.size[0]}x{img.size[1]}  1:{a:.3f}{flag}")

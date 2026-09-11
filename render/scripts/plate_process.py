#!/usr/bin/env python
"""Turn a photograph of a wet-plate negative into a plate as a book prints it.

This is the step that was missing. What comes out of the image generator is a
photograph OF A PLATE: hand-cut edges, collodion pour ridges, bare corners,
varnish crazing, the whole physical object lying on a copy stand. That is a
museum scan, and it is a way of looking at a 19th-century object that belongs
entirely to the 21st.

A book of 1898 could not print any of it. The negative is masked to a
rectangle in the printing frame, and every edge of the physical plate falls
outside the image area before the process starts. The book shows the picture.
The artifact stays in the photographer's drawer.

Two processes, both correct for the date:

  photogravure  Intaglio, continuous tone, no screen. The prestige process:
                printed from an etched copper plate on damp rag paper and
                tipped into the book on its own leaf. Velvety warm brown-black,
                no true black and no paper-white anywhere inside the image, and
                a PLATE MARK — the embossed rectangle where the edge of the
                copper bit into the paper. That mark is the single strongest
                signal that a page was printed from an intaglio plate, and no
                amount of tonal work substitutes for it.

  halftone      Relief, screened. The new process in 1898 and the one taking
                over trade publishing, because it printed on the same press as
                the type. A visible dot screen at 85–100 lines, tonal range
                flattened at both ends, shadows blocking up and highlights
                dropping out entirely. Cheaper, coarser, and the more probable
                choice for a modest New Orleans imprint.

Both are monochrome. Neither preserves the plate's edges.
"""
import numpy as np
from PIL import Image, ImageFilter

import paper

# Paper inside the plate mark — near white, faintly warm. The ageing pass
# tones the whole leaf afterwards, so this must not be tinted far here or the
# warmth compounds.
PAPER = np.array([252.0, 249.0, 243.0])

# Photogravure ink. Warm brown-black: iron-gall and copper-plate inks both sit
# well short of neutral, and a gravure shadow is never a true black.
INK = np.array([46.0, 34.0, 25.0])


# --------------------------------------------------------------- cropping

def trim_plate_edge(img, crop=None, inset=0.04):
    """Crop away the physical edges of the collodion plate.

    `crop` is an explicit (left, top, right, bottom) in fractions of the side,
    and is what plates.json should carry for anything the automatic pass gets
    wrong. Chipped corners and pour ridges are deliberately irregular, and no
    detector is going to beat looking at the picture.

    Failing that: a plate's edge is bare glass or a hand-cut margin, so it sits
    well away from the tone of the picture — much lighter, usually. Walking in
    from each side while the line's mean tone departs from the interior finds
    it without assuming the edge is white. `inset` then takes a little more off
    all round, because the outermost surviving lines are half-damaged rather
    than clean, and a printer masking a negative left himself margin anyway.
    """
    w0, h0 = img.size
    if crop is not None:
        l, t, r, b = crop
        return img.crop((int(w0 * l), int(h0 * t),
                         int(w0 * (1 - r)), int(h0 * (1 - b))))

    a = np.asarray(img.convert("L"), dtype=np.float32) / 255.0
    h, w = a.shape

    def scan(prof, limit):
        core = prof[len(prof) // 5: -len(prof) // 5]
        base = float(np.median(core))
        lo = 0
        while lo < limit and abs(prof[lo] - base) > 0.11:
            lo += 1
        hi = len(prof) - 1
        while hi > len(prof) - 1 - limit and abs(prof[hi] - base) > 0.11:
            hi -= 1
        return lo, hi

    t, b = scan(a.mean(axis=1), int(h * 0.14))
    l, r = scan(a.mean(axis=0), int(w * 0.14))

    di, dj = int(h * inset), int(w * inset)
    return img.crop((l + dj, t + di, r + 1 - dj, b + 1 - di))


# ----------------------------------------------------------- tone handling

def _grey(img):
    """Orthochromatic monochrome. The plate is already effectively monochrome;
    this only guarantees it, since neither process prints colour."""
    return np.asarray(img.convert("L"), dtype=np.float32) / 255.0


# Per-channel bend applied after the ink/paper mix. A straight linear blend
# between a warm ink and a warm paper still lands the MIDTONES near neutral,
# which is what made the first gravure read as a grey digital photograph
# rather than as brown ink. Lifting red and holding blue back warms the middle
# of the scale without moving either end, which is where the warmth of a real
# photogravure actually lives.
WARMTH = (0.93, 1.0, 1.12)


def _duotone(g, ink=INK, paper=PAPER, warmth=WARMTH):
    """One ink on one paper: every tone is a mix of exactly those two."""
    g = np.clip(g, 0, 1)[:, :, None]
    out = paper[None, None, :] * g + ink[None, None, :] * (1.0 - g)
    out = out / 255.0
    for c, gamma in enumerate(warmth):
        if gamma != 1.0:
            out[:, :, c] = out[:, :, c] ** gamma
    return out * 255.0


def _scurve(g, amount):
    """Contrast about mid grey. The wet-plate sources are deliberately flat —
    veiled, low microcontrast — and etching a copper plate from a flat
    negative is precisely where a printer put the contrast back."""
    return np.clip(0.5 + (g - 0.5) * amount, 0, 1)


# ------------------------------------------------------------ photogravure

def photogravure(img, margin=0.085, platemark=0.035, grain=0.9):
    """Etched copper, printed on damp rag paper, tipped in on its own leaf."""
    g = _grey(img)

    # Intaglio has a long, nearly straight tone scale and reaches neither end.
    # A gravure shadow holds ink but is not black; a gravure highlight carries
    # a faint tone and is never the paper. Compressing to [0.055, 0.945] is
    # what stops the reproduction from reading as a digital image.
    g = _scurve(g, 1.28)
    g = 0.055 + g * (0.945 - 0.055)

    # Aquatint grain: the rosin ground that lets an etched plate hold tone at
    # all. It is strongest in the midtones, because the extremes are either
    # fully bitten or not bitten, and it is fine enough to read as texture
    # rather than as noise.
    if grain > 0:
        rng = np.random.default_rng(7)
        n = rng.normal(0.0, 1.0, g.shape).astype(np.float32)
        tooth = 4.0 * g * (1.0 - g)     # peaks at mid grey, zero at both ends
        g = np.clip(g + n * tooth * (grain / 255.0) * 3.2, 0, 1)

    # No digital acutance. A gravure resolves beautifully and is still soft at
    # the level of the individual dot.
    img_g = Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8), "L")
    img_g = img_g.filter(ImageFilter.GaussianBlur(0.5))
    g = np.asarray(img_g, dtype=np.float32) / 255.0

    out = _duotone(g)
    h, w = g.shape

    # --- lay it on the leaf, with the plate mark ---------------------------
    m = int(round(w * margin))
    H, W = h + 2 * m, w + 2 * m
    leaf = np.empty((H, W, 3), dtype=np.float32)
    leaf[:, :] = PAPER
    leaf[m:m + h, m:m + w] = out

    # The plate mark is an emboss, not a rule: the copper edge pressed a
    # trough into damp paper and the paper heaped very slightly on either
    # side. In a scan that reads as a fine dark line with a fine light line
    # just outside it — which is why drawing it as a plain border never
    # convinces.
    gap = int(round(w * platemark))
    y0, x0 = m - gap, m - gap
    y1, x1 = m + h + gap, m + w + gap
    if y0 > 1 and x0 > 1:
        def band(yy0, yy1, xx0, xx1, delta):
            leaf[yy0:yy1, xx0:xx1] += delta

        for d, delta in ((0, -16.0), (1, -9.0), (-1, 5.0), (-2, 3.0)):
            band(y0 + d, y0 + d + 1, x0 + d, x1 - d, delta)      # top
            band(y1 - d - 1, y1 - d, x0 + d, x1 - d, delta)      # bottom
            band(y0 + d, y1 - d, x0 + d, x0 + d + 1, delta)      # left
            band(y0 + d, y1 - d, x1 - d - 1, x1 - d, delta)      # right

    return Image.fromarray(np.clip(leaf, 0, 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------- halftone

def halftone(img, lines=90, ppi=430, angle=45.0, margin=0.0):
    """Screened relief block, printed with the type.

    `lines` is the screen ruling and `ppi` the resolution the plate is being
    reproduced at on the page, which together fix the cell size. 85–100 lines
    is right for 1898: finer rulings existed but needed coated stock, and a
    book printed on antique wove could not hold them.
    """
    g = _grey(img)

    # A halftone loses both ends. The screen cannot hold a dot small enough
    # for a pale highlight, so highlights drop out to bare paper; and the
    # shadow dots join and fill, so shadows block up to a flat solid.
    g = _scurve(g, 1.15)
    g = np.clip((g - 0.05) / 0.90, 0, 1)
    g = 0.05 + g * 0.93

    # Screen at 2x and average down, so a dot has an edge rather than a step.
    up = 2
    h, w = g.shape
    big = np.asarray(
        Image.fromarray((g * 255).astype(np.uint8), "L")
        .resize((w * up, h * up), Image.BICUBIC), dtype=np.float32) / 255.0

    cell = (ppi / lines) * up
    yy, xx = np.mgrid[0:h * up, 0:w * up].astype(np.float32)
    th = np.deg2rad(angle)
    u = (xx * np.cos(th) + yy * np.sin(th)) / cell
    v = (-xx * np.sin(th) + yy * np.cos(th)) / cell

    # Distance from the centre of the nearest cell, in cell units: 0 at the
    # centre, 0.5 at the edge, 0.707 at the corner.
    du = (u % 1.0) - 0.5
    dv = (v % 1.0) - 0.5
    dist = np.sqrt(du * du + dv * dv)

    # A dot must cover the fraction of the cell that the tone calls for, so
    # its radius follows from the AREA: pi*r^2 = coverage, r = sqrt(c/pi).
    # Taking the radius as sqrt(coverage) instead — the obvious-looking form,
    # and the first version here — overinks by pi: mid grey printed at 78%
    # coverage and the whole plate went to mud. Past c = 0.785 the circles
    # run past the cell edges and merge on their own, which is exactly how a
    # real screen blocks up in the shadows.
    radius = np.sqrt(np.clip(1.0 - big, 0, 1) / np.pi)
    edge = 0.9 / cell                    # about one output pixel of softness
    dot = np.clip((dist - radius) / edge + 0.5, 0, 1)

    small = np.asarray(
        Image.fromarray((np.clip(dot, 0, 1) * 255).astype(np.uint8), "L")
        .resize((w, h), Image.LANCZOS), dtype=np.float32) / 255.0

    # Letterpress ink on the same sheet as the type: neutral, and it does sit
    # near black, unlike a gravure.
    out = _duotone(small, ink=np.array([26.0, 24.0, 23.0]))

    if margin > 0:
        m = int(round(w * margin))
        leaf = np.empty((h + 2 * m, w + 2 * m, 3), dtype=np.float32)
        leaf[:, :] = PAPER
        leaf[m:m + h, m:m + w] = out
        out = leaf

    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


# ----------------------------------------------------------- mounted print

def mounted_print(img, margin=0.10, tilt=0.5, halo=1.0, seed=3):
    """A photographic print pasted down on the leaf, not ink printed into it.

    This is the other way an illustrated book of the period carried a
    photograph, and for an expensive one it was the older and better way: an
    actual albumen or silver print, trimmed and pasted to a stub or to the
    leaf itself, one at a time, by hand. It is why books of the 1870s and
    1880s with real photographs cost what they cost.

    It differs from `photogravure` in what the reader is looking at. A gravure
    is ink in paper and lies flat in the page. A pasted print is an OBJECT on
    the page: it has its own edge, it sits very slightly proud, it was never
    quite square, and — the detail that dates a genuine one — its chemistry
    bled into the mount over the following century and left a halo.

    What this does NOT do is add photo corners. Gummed corners are a snapshot
    album technology of roughly 1905 onward; a print in a book of 1898 was
    pasted down flush. Corners also assert a different book — someone's album,
    assembled by hand — which is the found-album frame, and cannot be true on
    the same page as a plate mark.
    """
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    h, w, _ = a.shape

    m = int(round(w * margin))
    H, W = h + 2 * m, w + 2 * m
    leaf = np.empty((H, W, 3), dtype=np.float32)
    leaf[:, :] = PAPER

    rng = np.random.default_rng(seed)

    # The halo: a century of the print's own chemistry migrating outward into
    # the mount. Warmest and strongest right at the edge, dying away within
    # about a third of an inch. Nothing else reads as convincingly old.
    if halo > 0:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dx = np.maximum(np.maximum(m - xx, xx - (m + w - 1)), 0)
        dy = np.maximum(np.maximum(m - yy, yy - (m + h - 1)), 0)
        d = np.sqrt(dx * dx + dy * dy)
        band = np.exp(-d / (w * 0.035)) * halo
        band *= 0.75 + 0.5 * paper.fbm((H, W), rng, octaves=3, cells=5)
        leaf -= (band * 30.0)[:, :, None] * np.array([0.15, 0.55, 1.0])

    # The print sits proud of the mount, so its edge casts a hairline.
    sh = max(1, int(round(w * 0.004)))
    leaf[m + sh:m + h + sh, m + sh:m + w + sh] -= 26.0

    leaf[m:m + h, m:m + w] = a

    out = Image.fromarray(np.clip(leaf, 0, 255).astype(np.uint8), "RGB")

    # Pasted by hand, so never quite square.
    if tilt:
        out = out.rotate(rng.normal(0.0, tilt), resample=Image.BICUBIC,
                         expand=False,
                         fillcolor=tuple(int(v) for v in PAPER))
    return out


# ---------------------------------------------------------------- as found

def as_is(img, inset=0.015, aspect=None, **_):
    """No reproduction process: the source image, whole, as the whole page.

    For a source that already IS the finished leaf — a print on its album
    mount, photographed. It carries its own paper, its own tone and its own
    edges, so it is not laid on the book's paper and not aged again; it is
    printed to the trim and becomes the leaf.

    `inset` shaves the outermost fraction of each side, which is where the
    scan's own white surround and the ragged outer edge live. `aspect`
    (height/width) then cover-crops to the page: nothing is stretched, because
    a leaf stretched to a different aspect skews everything printed on it.
    """
    img = img.convert("RGB")
    w, h = img.size
    if inset:
        dx, dy = int(w * inset), int(h * inset)
        img = img.crop((dx, dy, w - dx, h - dy))
        w, h = img.size
    if aspect:
        have = h / w
        if have < aspect:            # too wide: take it off the sides
            nw = int(round(h / aspect))
            x = (w - nw) // 2
            img = img.crop((x, 0, x + nw, h))
        elif have > aspect:          # too tall: take it off top and bottom
            nh = int(round(w * aspect))
            y = (h - nh) // 2
            img = img.crop((0, y, w, y + nh))
    return img


PROCESSES = {"photogravure": photogravure, "halftone": halftone,
             "mounted_print": mounted_print,
             "as_is": as_is}


def process(img, name="photogravure", trim=True, **kw):
    if trim:
        img = trim_plate_edge(img)
    return PROCESSES[name](img, **kw)

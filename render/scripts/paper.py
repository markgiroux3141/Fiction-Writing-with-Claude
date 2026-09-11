"""Procedural grounds: 1881 book paper and older parchment.

Everything here returns RGB uint8 numpy arrays at the caller's pixel size.
No external assets — the textures are generated so they can be regenerated
at any resolution and reseeded per page.
"""
import numpy as np
from PIL import Image, ImageFilter


# ---------------------------------------------------------------- noise

def _value_noise(shape, cells, rng):
    """Bicubic-upsampled random grid. One octave."""
    h, w = shape
    gh, gw = max(2, int(cells * h / max(h, w))), max(2, int(cells * w / max(h, w)))
    grid = rng.random((gh, gw)).astype(np.float32)
    img = Image.fromarray((grid * 255).astype(np.uint8), "L").resize((w, h), Image.BICUBIC)
    return np.asarray(img, dtype=np.float32) / 255.0


def fbm(shape, rng, octaves=5, cells=4, gain=0.5, lacunarity=2.0):
    """Fractal sum of value noise, normalised to 0..1."""
    total = np.zeros(shape, dtype=np.float32)
    amp, c, norm = 1.0, cells, 0.0
    for _ in range(octaves):
        total += amp * _value_noise(shape, int(c), rng)
        norm += amp
        amp *= gain
        c *= lacunarity
    total /= norm
    total -= total.min()
    mx = total.max()
    return total / mx if mx > 0 else total


def _blobs(shape, rng, count, rmin, rmax, softness=0.55):
    """Sparse soft radial blobs, 0..1 mask. Used for foxing and stains."""
    h, w = shape
    mask = np.zeros(shape, dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for _ in range(count):
        cx, cy = rng.random() * w, rng.random() * h
        r = rng.uniform(rmin, rmax)
        # anisotropic so blooms are not perfect circles
        ax, ay = r * rng.uniform(0.7, 1.4), r * rng.uniform(0.7, 1.4)
        d = np.sqrt(((xx - cx) / ax) ** 2 + ((yy - cy) / ay) ** 2)
        mask = np.maximum(mask, np.clip(1.0 - d, 0, 1) ** (1.0 / softness))
    return mask


def _edge_field(shape, gutter="left", strength=1.0, falloff=1.5):
    """0 in the middle, 1 at the trimmed edges. Gutter edge stays cleaner,
    because the fore-edge is what fingers and daylight actually reach."""
    h, w = shape
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    x = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    ey = np.minimum(y, 1 - y) * 2
    ex = np.minimum(x, 1 - x) * 2
    if gutter == "left":
        ex = np.where(x < 0.5, np.clip(x * 2 * 2.4, 0, 1), ex)
    elif gutter == "right":
        ex = np.where(x > 0.5, np.clip((1 - x) * 2 * 2.4, 0, 1), ex)
    field = 1.0 - np.minimum(ey, ex)
    return np.clip(field ** falloff * strength, 0, 1)


# ---------------------------------------------------------------- grounds

def book_paper(shape, seed, gutter="left", age=1.0):
    """Machine-made wove rag paper, lightly foxed. Subtle by design:
    this sits under 10pt text and must not compete with it."""
    rng = np.random.default_rng(seed)
    h, w = shape

    base = np.array([228.0, 216.0, 190.0], dtype=np.float32)
    img = np.repeat(np.repeat(base[None, None, :], h, 0), w, 1)

    # broad tonal mottle
    mottle = fbm(shape, rng, octaves=4, cells=3)
    img += ((mottle - 0.5) * 30.0 * age)[:, :, None] * np.array([1.0, 0.94, 0.82])

    # fine fibre grain
    grain = rng.normal(0.0, 2.6, shape).astype(np.float32)
    grain = np.asarray(
        Image.fromarray(np.clip(grain + 128, 0, 255).astype(np.uint8), "L")
        .filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) - 128.0
    img += grain[:, :, None]

    # a few visible fibres/flecks pressed into the sheet
    flecks = _blobs(shape, rng, int(28 * age), h * 0.0012, h * 0.004, softness=0.9)
    img -= (flecks * 26.0)[:, :, None] * np.array([0.7, 0.8, 1.0])

    # foxing: iron-gall rust blooms, denser toward the edges. This is the
    # single most recognisable mark of a 19th-c. sheet that has sat damp.
    fox_field = 0.30 + 0.70 * _edge_field(shape, gutter, 1.0)
    fox = _blobs(shape, rng, int(rng.integers(26, 52) * age),
                 h * 0.005, h * 0.034) * fox_field
    fox *= 0.30 + 0.70 * fbm(shape, rng, octaves=3, cells=8)
    img -= (fox * 82.0 * age)[:, :, None] * np.array([0.12, 0.52, 0.96])

    # a scatter of small hard specks — dust ground into the surface
    specks = (rng.random(shape) < 0.00035 * age).astype(np.float32)
    specks = np.asarray(
        Image.fromarray((specks * 255).astype(np.uint8), "L")
        .filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255.0
    img -= (specks * 190.0)[:, :, None] * np.array([0.5, 0.72, 1.0])

    # edge tanning from light and handling
    tan = _edge_field(shape, gutter, 1.0) * (0.45 + 0.55 * fbm(shape, rng, 3, 5))
    img -= (tan * 62.0 * age)[:, :, None] * np.array([0.22, 0.58, 1.0])

    # damp stain running in from one edge, with a darker tide line at its rim
    if rng.random() < 0.55:
        stain = _blobs(shape, rng, 1, h * 0.14, h * 0.34, softness=0.30)
        stain *= np.clip(_edge_field(shape, gutter, 1.0) * 1.6, 0, 1)
        stain = np.clip(stain, 0, 1)
        tide = np.clip(1.0 - np.abs(stain - 0.42) * 7.0, 0, 1) * (stain > 0.05)
        img -= (stain * 40.0)[:, :, None] * np.array([0.18, 0.58, 1.0])
        img -= (tide * 26.0)[:, :, None] * np.array([0.16, 0.55, 1.0])

    return np.clip(img, 0, 255).astype(np.uint8)


def parchment(shape, seed):
    """Animal skin. Far more aggressive than book paper: high-contrast
    mottling, grease translucency, follicle speckle, scraped patches."""
    rng = np.random.default_rng(seed)
    h, w = shape

    base = np.array([214.0, 194.0, 156.0], dtype=np.float32)
    img = np.repeat(np.repeat(base[None, None, :], h, 0), w, 1)

    # skin is unevenly thick — this is the dominant feature
    thick = fbm(shape, rng, octaves=6, cells=2)
    img += ((thick - 0.5) * 62.0)[:, :, None] * np.array([1.0, 0.92, 0.75])

    # greasy translucent patches where the skin was scraped thin
    thin = _blobs(shape, rng, 7, h * 0.06, h * 0.20, softness=0.3)
    img += (thin * 22.0)[:, :, None] * np.array([1.0, 0.98, 0.9])

    # hair follicles, in drifting clusters
    fol_field = _blobs(shape, rng, 5, h * 0.08, h * 0.24, softness=0.4)
    dots = (rng.random(shape) < 0.0016 * (0.25 + fol_field)).astype(np.float32)
    dots = np.asarray(
        Image.fromarray((dots * 255).astype(np.uint8), "L")
        .filter(ImageFilter.GaussianBlur(0.7)), dtype=np.float32) / 255.0
    img -= (dots * 150.0)[:, :, None] * np.array([0.55, 0.75, 1.0])

    # grain and dirt
    img += rng.normal(0.0, 3.4, shape).astype(np.float32)[:, :, None]
    dirt = fbm(shape, rng, octaves=5, cells=14)
    img -= (np.clip(dirt - 0.55, 0, 1) * 60.0)[:, :, None] * np.array([0.4, 0.7, 1.0])

    # heavy edge darkening — this leaf has been handled at the margins
    edge = _edge_field(shape, gutter="none", strength=1.0)
    edge = np.clip(edge * (0.6 + 0.8 * fbm(shape, rng, 4, 6)), 0, 1)
    img -= (edge * 96.0)[:, :, None] * np.array([0.35, 0.68, 1.0])

    return np.clip(img, 0, 255).astype(np.uint8)


def torn_edge_alpha(shape, seed, bite=0.022, tears=2):
    """Alpha mask with a deckled perimeter and a couple of deeper tears.

    Two noise scales: a slow one for the overall wander of the edge, and a
    fast one for the fibrous fray. Amplitudes are small on purpose — a leaf
    loses a few percent of its margin, not a third of its text block. Deeper
    damage is placed deliberately by `tears` rather than left to the noise.
    """
    rng = np.random.default_rng(seed)
    h, w = shape

    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    x = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    # normalised distance to the nearest edge, corrected for aspect
    ar = w / float(h)
    dist = np.minimum(np.minimum(x, 1 - x) * ar, np.minimum(y, 1 - y))

    slow = (fbm(shape, rng, octaves=3, cells=3) - 0.5) * bite * 1.6
    fast = (fbm(shape, rng, octaves=3, cells=48) - 0.5) * bite * 0.55
    inset = bite * 0.55 + slow + fast

    # a few deeper bites, each a soft blob straddling the perimeter
    if tears:
        bites = _blobs(shape, rng, tears, h * 0.05, h * 0.13, softness=0.5)
        edge_only = np.clip(1.0 - dist / (bite * 4.0), 0, 1)
        inset = inset + bites * edge_only * bite * 3.2

    alpha = (dist > inset).astype(np.float32)

    # close pinholes the noise may have punched inside the sheet
    a = Image.fromarray((alpha * 255).astype(np.uint8), "L")
    a = a.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    a = a.filter(ImageFilter.GaussianBlur(max(1.0, h * 0.0012)))
    return np.asarray(a, dtype=np.float32) / 255.0

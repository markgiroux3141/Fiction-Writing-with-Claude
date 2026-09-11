#!/usr/bin/env python
"""Launcher icons for the Android app.

    python scripts/build_icons.py --android ../app/android/app/src/main/res

By default the icon is an UNTITLED board — see anonymous_board. The app is a
reader that holds whatever books are on the device, so branding it with one
book's cover would name the wrong thing the moment a second book arrives.

`--cover <image>` cuts the icon from a real cover instead. That takes the TOP
of the board rather than scaling the whole 2:3 board into a square, which
would letterbox it into a stamp, or cropping the middle, which keeps the
mounted print and loses the title.

Adaptive foregrounds are inset into the safe circle, because Android clips an
icon to whatever shape the launcher uses and anything running to the edge
loses its ends.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

SIZES = [192, 512]


def square_crop(cover):
    """The top of the board, squared off."""
    w, h = cover.size
    # Start a little below the head so the crop is not all margin, and take a
    # full-width square. On the 1024x1536 board that is the border, the title,
    # the rule beneath it and the head of the print.
    top = int(h * 0.035)
    return cover.crop((0, top, w, top + w))


# Android launcher densities: mdpi is 1x, and an adaptive icon's foreground
# is a 108dp canvas of which only the middle 72dp is guaranteed to survive
# whatever mask the launcher applies.
DENSITIES = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
LEGACY_DP = 48
ADAPTIVE_DP = 108
SAFE = 72 / 108


# Lighter than the book's own boards, deliberately. The first version used the
# cover's cloth (#302B23) and came out with a luma range of 29–50 out of 255:
# in a launcher full of saturated icons that is a black square, and blind
# stamping — which is only ever a shade darker than the cloth around it — has
# no contrast left to be seen by. So the cloth is raised to a mid brown and the
# centre device is GILT rather than blind, which is also what a binder did when
# a board had to carry something at a glance.
CLOTH = (0x54, 0x4A, 0x3A)
GILT = (0xC8, 0xAC, 0x72)


def anonymous_board(size):
    """An untitled bookcloth board: the default icon.

    The app is a reader, not a book, so its icon must not be one book's cover.
    This is the same object with the lettering taken off — dark cloth, a fine
    weave, and the blind-stamped double rule and centre lozenge a Victorian
    binder pressed into a board that carried no title.

    Blind stamping is an emboss, not printing: every line is a dark trough
    with a lighter ridge along one side. Drawn as flat strokes it reads as a
    drawing of a book instead of a book, which at 48 px is the difference
    between an object and a logo.
    """
    import numpy as np
    from PIL import ImageFilter

    a = np.zeros((size, size, 3), dtype=np.float32)
    a[:, :] = CLOTH

    # A fine woven grain: noise softened, plus a cross-hatch at the weave's
    # own pitch, scaled so the weave stays a texture rather than a moiré.
    rng = np.random.default_rng(7)
    n = rng.normal(0.0, 4.5, (size, size)).astype(np.float32)
    n = np.asarray(
        Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8), "L")
        .filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) - 128.0
    pitch = size / 256.0 * 1.9
    yy = np.arange(size, dtype=np.float32)[:, None]
    xx = np.arange(size, dtype=np.float32)[None, :]
    weave = (np.sin(yy * pitch) + np.sin(xx * pitch)) * 1.5
    a += (n + weave)[:, :, None]

    def trough(y0, y1, x0, x1):
        """One blind-stamped line: pressed dark, with a ridge above/left."""
        y0, y1 = max(0, int(y0)), min(size, int(y1))
        x0, x1 = max(0, int(x0)), min(size, int(x1))
        if y1 <= y0 or x1 <= x0:
            return
        t = max(1, (y1 - y0) if (y1 - y0) < (x1 - x0) else (x1 - x0))
        a[y0:y1, x0:x1] *= 0.60
        a[max(0, y0 - t):y0, max(0, x0 - t):x1] *= 1.28

    def rule(inset):
        i = size * inset
        t = max(1.0, size * 0.012)
        trough(i, i + t, i, size - i)                    # head
        trough(size - i - t, size - i, i, size - i)      # tail
        trough(i, size - i, i, i + t)                    # left
        trough(i, size - i, size - i - t, size - i)      # right

    rule(0.085)
    rule(0.135)

    # The centre lozenge, in gilt. A diamond survives being shrunk to a
    # launcher icon; lettering does not, and blind stamping does not either.
    cy = cx = size / 2.0
    r = size * 0.22
    t = max(1.0, size * 0.030)
    d = np.abs(yy - cy) / r + np.abs(xx - cx) / r     # 1.0 on the diamond
    band = np.abs(d - 1.0) < (t / r)
    # Gilt is leaf on an embossed line, so it is neither flat nor clean: it
    # varies, and it sits in a trough that shades one side.
    leaf = np.asarray(GILT, dtype=np.float32)[None, None, :]
    speck = rng.normal(1.0, 0.055, (size, size, 1)).astype(np.float32)
    a[band] = (leaf * speck)[band]
    # A blind trough just outside the gilt, so the device is pressed in rather
    # than painted on.
    outer = (np.abs(d - (1.0 + t / r * 1.25)) < (t / r * 0.7)) & ~band
    a[outer] *= 0.70

    # Handled boards go dark at the edges and darker at the corners — gently,
    # because a heavy vignette on an icon this small just eats the border.
    ey = np.minimum(yy, size - 1 - yy) / (size * 0.5)
    ex = np.minimum(xx, size - 1 - xx) / (size * 0.5)
    vign = np.clip(np.minimum(ey, ex) * 3.2, 0, 1) ** 0.55
    a *= (0.86 + 0.14 * vign)[:, :, None]

    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def cloth_colour(base):
    """The board's own dark cloth, for icon and splash grounds."""
    return base.resize((8, 8), Image.LANCZOS).getpixel((1, 1))


def circle_mask(img):
    from PIL import ImageDraw
    out = img.copy().convert("RGBA")
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, img.size[0] - 1, img.size[1] - 1), fill=255)
    out.putalpha(mask)
    return out


def build_android(base, res):
    """Launcher icons and a splash that is the board's cloth, not white."""
    res = Path(res)
    cloth = cloth_colour(base)

    for name, scale in DENSITIES.items():
        d = res / f"mipmap-{name}"
        d.mkdir(parents=True, exist_ok=True)

        legacy = int(LEGACY_DP * scale)
        base.resize((legacy, legacy), Image.LANCZOS).save(
            d / "ic_launcher.png", "PNG", optimize=True)
        circle_mask(base.resize((legacy, legacy), Image.LANCZOS)).save(
            d / "ic_launcher_round.png", "PNG", optimize=True)

        # Adaptive foreground: the crop inside the safe circle, on cloth, so
        # a round or squircle mask cannot cut the title off the board.
        full = int(ADAPTIVE_DP * scale)
        inner = int(full * SAFE)
        fg = Image.new("RGB", (full, full), cloth)
        fg.paste(base.resize((inner, inner), Image.LANCZOS),
                 ((full - inner) // 2, (full - inner) // 2))
        fg.save(d / "ic_launcher_foreground.png", "PNG", optimize=True)
        print(f"   mipmap-{name}: {legacy}px legacy, {full}px adaptive")

    (res / "values").mkdir(parents=True, exist_ok=True)
    (res / "values" / "ic_launcher_background.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        f'    <color name="ic_launcher_background">#{cloth[0]:02X}{cloth[1]:02X}{cloth[2]:02X}</color>\n'
        '</resources>\n', encoding="utf-8")
    print(f"   ic_launcher_background = #{cloth[0]:02X}{cloth[1]:02X}{cloth[2]:02X}")

    # Every splash Capacitor generated is a white sheet. Overwrite them with
    # the page ground, so launching the app is a dark room rather than a
    # flashbulb followed by a dark room.
    ground = (0x14, 0x12, 0x0f)
    n = 0
    for sp in res.glob("drawable*/splash.png"):
        w, h = Image.open(sp).size
        Image.new("RGB", (w, h), ground).save(sp, "PNG", optimize=True)
        n += 1
    print(f"   {n} splash sheet(s) repainted to the page ground")


def main():
    ap = argparse.ArgumentParser(
        description="Launcher icons for the Android app, cut from a cover.")
    ap.add_argument("--android", required=True, metavar="RES_DIR",
                    help="android/app/src/main/res")
    ap.add_argument("--cover", default=None,
                    help="image to cut the icon from; defaults to an untitled "
                         "board, so the icon says 'a book' rather than naming "
                         "one of the books the reader happens to hold")
    args = ap.parse_args()

    if args.cover:
        src = Path(args.cover)
        if not src.exists():
            sys.exit(f"no cover at {src}")
        base = square_crop(Image.open(src).convert("RGB"))
    else:
        base = anonymous_board(1024)

    build_android(base, args.android)


if __name__ == "__main__":
    main()

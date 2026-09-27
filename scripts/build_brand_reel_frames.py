#!/usr/bin/env python3
"""Generate the still frames for the Gen Ateliér logo-reveal reel.

Directly mirrors the reference video: a single fixed logo lockup
(icon + wordmark, same position/size every frame) flashed across a
torn-paper reveal, a cracked-stone reveal (both real photo textures
from Weave), and the brand's own flat colour palette. No mockups, no
zoom/pan -- hard cuts only, done in the stitch script.

Usage:
    python3 scripts/build_brand_reel_frames.py
Writes 1080x1920 PNGs to assets/frames/.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
LOGO_SRC = ROOT / "assets" / "logo" / "logo-white-src.webp"
TEXTURES = ROOT / "assets" / "textures"
FRAMES_DIR = ROOT / "assets" / "frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

# Gen Ateliér palette (from brand guidelines PDF)
OXBLOOD = (111, 39, 39)
BONE = (238, 238, 230)
CHARCOAL = (47, 47, 47)
SKY = (119, 163, 198)
INK_MUTED = (94, 94, 88)
LINE = (214, 214, 204)
DEEP_SKY = (63, 112, 151)

MANROPE_SEMI = "/usr/share/fonts/truetype/manrope/Manrope-SemiBold.ttf"
GARAMOND_ITALIC = "/usr/share/fonts/opentype/ebgaramond/EBGaramond12-Italic.otf"

# Fixed lockup geometry, as fractions of the 1080x1920 canvas -- identical
# on every single frame, matching the reference's one repeated template.
ICON_WIDTH_FRAC = 0.17
ICON_CENTER_Y_FRAC = 0.487
WORDMARK_CENTER_Y_FRAC = 0.548
WORDMARK_SIZE_FRAC = 0.026
WORDMARK_TRACKING_FRAC = 0.006


def font(path, size):
    return ImageFont.truetype(path, size)


def load_logo_mark():
    im = Image.open(LOGO_SRC).convert("RGBA")
    bbox = im.split()[-1].getbbox()
    return im.crop(bbox)


def recolor(mask_rgba, rgb):
    alpha = mask_rgba.split()[-1]
    solid = Image.new("RGBA", mask_rgba.size, (*rgb, 0))
    solid.putalpha(alpha)
    return solid


def scaled_logo(logo, target_w):
    ratio = target_w / logo.width
    return logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)


def tracked_text(draw, xy, text, fnt, fill, tracking=0):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, xy[1]), ch, font=fnt, fill=fill, anchor="lm")
        x += w + tracking


LOGO_MARK = load_logo_mark()
LOGO_CHARCOAL = recolor(LOGO_MARK, CHARCOAL)
LOGO_BONE = recolor(LOGO_MARK, BONE)
ICON_W = int(W * ICON_WIDTH_FRAC)


def apply_fixed_lockup(bg_rgba: Image.Image, light_on_dark: bool) -> Image.Image:
    """Composite the SAME icon + wordmark, at the SAME position/size, on
    top of any background. light_on_dark picks bone-on-dark or
    charcoal-on-light so it reads, but geometry never changes."""
    logo = scaled_logo(LOGO_BONE if light_on_dark else LOGO_CHARCOAL, ICON_W)
    cx = W / 2
    cy = H * ICON_CENTER_Y_FRAC
    bg_rgba.alpha_composite(logo, (int(cx - logo.width / 2), int(cy - logo.height / 2)))
    draw = ImageDraw.Draw(bg_rgba)
    fill = BONE if light_on_dark else CHARCOAL
    fnt = font(MANROPE_SEMI, int(W * WORDMARK_SIZE_FRAC))
    tracked_text(draw, (cx, H * WORDMARK_CENTER_Y_FRAC), "GEN ATELIÉR", fnt, fill,
                 tracking=W * WORDMARK_TRACKING_FRAC)
    return bg_rgba


def solid_with_vignette(rgb, w=W, h=H, strength=0.22):
    img = Image.new("RGB", (w, h), rgb)
    noise = Image.effect_noise((w, h), 8).convert("L")
    img = Image.blend(img, ImageOps.colorize(noise, black=(0, 0, 0), white=(255, 255, 255)), 0.03)
    vign = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vign)
    vd.ellipse([-w * 0.35, -h * 0.25, w * 1.35, h * 1.25], fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(260))
    dark = Image.new("RGB", (w, h), tuple(max(0, int(c * (1 - strength))) for c in rgb))
    return Image.composite(img, dark, vign)


def fit_texture(path, w=W, h=H, crop_x_frac=0.5):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    x0 = int((im.width - w) * crop_x_frac)
    y0 = (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def save(img, name):
    img.convert("RGB").save(FRAMES_DIR / f"{name}.png", quality=95)
    print("wrote", name)


# 01: torn-paper reveal (real photo texture from Weave), two near-identical
# holds -- same crop, same lockup -- matching the reference's repeated frame.
paper = fit_texture(TEXTURES / "paper_tear_oxblood_raw.png", crop_x_frac=0.5)
for tag in ("a", "b"):
    frame = paper.copy().convert("RGBA")
    apply_fixed_lockup(frame, light_on_dark=True)
    save(frame, f"01_paper_{tag}")

# 02: cracked-stone reveal (real photo texture from Weave)
stone = fit_texture(TEXTURES / "stone_crack_raw.png", crop_x_frac=0.5)
for tag in ("a", "b"):
    frame = stone.copy().convert("RGBA")
    apply_fixed_lockup(frame, light_on_dark=True)
    save(frame, f"02_stone_{tag}")

# 03-08: the logo flashing across the brand's flat colour palette --
# identical lockup, background colour is the only thing that changes.
swatches = [
    (OXBLOOD, True, "03_color_oxblood"),
    (CHARCOAL, True, "04_color_charcoal"),
    (INK_MUTED, True, "05_color_ink"),
    (BONE, False, "06_color_bone"),
    (SKY, False, "07_color_sky"),
    (DEEP_SKY, True, "08_color_deepsky"),
]
for rgb, light_on_dark, name in swatches:
    frame = solid_with_vignette(rgb).convert("RGBA")
    apply_fixed_lockup(frame, light_on_dark=light_on_dark)
    save(frame, name)

# 09: end hold, charcoal, same lockup
frame = solid_with_vignette(CHARCOAL).convert("RGBA")
apply_fixed_lockup(frame, light_on_dark=True)
save(frame, "09_endcard")

print("done")

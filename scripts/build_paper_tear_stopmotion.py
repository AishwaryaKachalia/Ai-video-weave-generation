#!/usr/bin/env python3
"""Generate a 10-frame stop-motion paper-tear sequence: charcoal-black
paper on a white background, tearing open frame by frame along a jagged
line to reveal the Gen Ateliér logo underneath, at the same fixed
position used throughout the reel.

Usage:
    python3 scripts/build_paper_tear_stopmotion.py
Writes 1080x1920 PNGs to assets/frames/tear/tear_01.png .. tear_10.png
"""
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
LOGO_SRC = ROOT / "assets" / "logo" / "logo-white-src.webp"
PAPER_SRC = ROOT / "assets" / "textures" / "paper_charcoal_raw.png"
OUT_DIR = ROOT / "assets" / "frames" / "tear"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
N_FRAMES = 10

WHITE = (255, 255, 255)
CHARCOAL = (47, 47, 47)

MANROPE_SEMI = "/usr/share/fonts/truetype/manrope/Manrope-SemiBold.ttf"

# Same fixed lockup geometry used across the whole reel.
ICON_WIDTH_FRAC = 0.17
ICON_CENTER_Y_FRAC = 0.487
WORDMARK_CENTER_Y_FRAC = 0.548
WORDMARK_SIZE_FRAC = 0.026
WORDMARK_TRACKING_FRAC = 0.006

random.seed(42)


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


def base_canvas_with_logo():
    img = Image.new("RGBA", (W, H), (*WHITE, 255))
    logo = scaled_logo(recolor(LOGO_MARK, CHARCOAL), int(W * ICON_WIDTH_FRAC))
    cx, cy = W / 2, H * ICON_CENTER_Y_FRAC
    img.alpha_composite(logo, (int(cx - logo.width / 2), int(cy - logo.height / 2)))
    draw = ImageDraw.Draw(img)
    fnt = font(MANROPE_SEMI, int(W * WORDMARK_SIZE_FRAC))
    tracked_text(draw, (cx, H * WORDMARK_CENTER_Y_FRAC), "GEN ATELIÉR", fnt, CHARCOAL,
                 tracking=W * WORDMARK_TRACKING_FRAC)
    return img


def fit_texture(path, w, h):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    x0 = (im.width - w) // 2
    y0 = (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def jagged_centerline(w, h, amplitude=26, step=34, seed=1):
    rnd = random.Random(seed)
    pts = []
    x = w / 2
    y = 0
    while y <= h:
        x += rnd.uniform(-amplitude, amplitude)
        x = max(w * 0.35, min(w * 0.65, x))
        pts.append((x, y))
        y += step
    pts.append((pts[-1][0], h))
    return pts


def build_half_masks(centerline, w, h):
    left_pts = [(0, 0)] + centerline + [(0, h)]
    right_pts = [(w, 0)] + centerline + [(w, h)]
    left_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(left_mask).polygon(left_pts, fill=255)
    right_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(right_mask).polygon(right_pts, fill=255)
    return left_mask, right_mask


def with_edge_shadow(rgb_img, mask, edge_px=10, darken=0.55):
    """Darken a thin band just inside the mask's jagged boundary so the
    torn edge reads as a cut, not a flat cut-out."""
    eroded = mask.filter(ImageFilter.MinFilter(edge_px * 2 + 1))
    band = ImageChops.subtract(mask, eroded)
    band = band.filter(ImageFilter.GaussianBlur(3))
    dark = Image.new("RGB", rgb_img.size, (0, 0, 0))
    shaded = Image.blend(rgb_img, dark, darken)
    out = rgb_img.copy()
    out.paste(shaded, (0, 0), band)
    return out


LOGO_MARK = load_logo_mark()
paper = fit_texture(PAPER_SRC, W, H)
centerline = jagged_centerline(W, H)
left_mask_base, right_mask_base = build_half_masks(centerline, W, H)

paper_shadowed_left = with_edge_shadow(paper, left_mask_base)
paper_shadowed_right = with_edge_shadow(paper, right_mask_base)

left_rgba = Image.new("RGBA", (W, H), (0, 0, 0, 0))
left_rgba.paste(paper_shadowed_left, (0, 0), left_mask_base)
right_rgba = Image.new("RGBA", (W, H), (0, 0, 0, 0))
right_rgba.paste(paper_shadowed_right, (0, 0), right_mask_base)

MAX_DX = 215


def eased(t):
    return 1 - (1 - t) ** 2  # ease-out: opens fast, settles


for i in range(N_FRAMES):
    t = i / (N_FRAMES - 1)
    dx = int(MAX_DX * eased(t))
    rnd = random.Random(100 + i)
    jitter_l = (rnd.randint(-2, 2), rnd.randint(-2, 2))
    jitter_r = (rnd.randint(-2, 2), rnd.randint(-2, 2))

    frame = base_canvas_with_logo()
    frame.alpha_composite(left_rgba, (-dx + jitter_l[0], jitter_l[1]))
    frame.alpha_composite(right_rgba, (dx + jitter_r[0], jitter_r[1]))

    out_path = OUT_DIR / f"tear_{i + 1:02d}.png"
    frame.convert("RGB").save(out_path, quality=95)
    print("wrote", out_path.name)

print("done")

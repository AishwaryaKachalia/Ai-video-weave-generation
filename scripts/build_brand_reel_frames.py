#!/usr/bin/env python3
"""Generate the still frames for the Gen Ateliér logo-reveal reel.

Mirrors the reference video's actual structure: a torn/folded-paper
reveal into the logo, then the logo cycling across flat colour-block
backgrounds (the reference's real content is its colour rotation, not
mockups) -- using Gen Ateliér's own logo mark and brand palette from
the supplied brand guidelines PDF.

Usage:
    python3 scripts/build_brand_reel_frames.py
Writes 1080x1920 PNGs to assets/frames/.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
LOGO_SRC = ROOT / "assets" / "logo" / "logo-white-src.webp"
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
MANROPE_LIGHT = "/usr/share/fonts/truetype/manrope/Manrope-Light.ttf"
GARAMOND_ITALIC = "/usr/share/fonts/opentype/ebgaramond/EBGaramond12-Italic.otf"

random.seed(7)


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


def paste_centered(bg, fg, cx, cy):
    bg.alpha_composite(fg, (int(cx - fg.width / 2), int(cy - fg.height / 2)))


def tracked_text(draw, xy, text, fnt, fill, tracking=0):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, xy[1]), ch, font=fnt, fill=fill, anchor="lm")
        x += w + tracking


def paper_texture(base_rgb, w=W, h=H, fold_count=4, seed=0):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), base_rgb)
    fold_xs = sorted(rnd.randint(int(w * 0.1), int(w * 0.9)) for _ in range(fold_count))
    shade = Image.new("L", (w, h), 128)
    sd = ImageDraw.Draw(shade)
    prev = 0
    for fx in fold_xs + [w]:
        sd.rectangle([prev, 0, fx, h], fill=rnd.randint(108, 148))
        sd.line([(fx, 0), (fx, h)], fill=rnd.choice([90, 170]), width=2)
        prev = fx
    shade = shade.filter(ImageFilter.GaussianBlur(18))
    img = Image.blend(img, ImageOps.colorize(shade, black=(0, 0, 0), white=(255, 255, 255)), 0.18)
    noise = Image.effect_noise((w, h), 10).convert("L")
    img = Image.blend(img, ImageOps.colorize(noise, black=(0, 0, 0), white=(255, 255, 255)), 0.05)
    vign = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vign)
    vd.ellipse([-w * 0.3, -h * 0.2, w * 1.3, h * 1.2], fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (w, h), tuple(max(0, c - 40) for c in base_rgb))
    return Image.composite(img, dark, vign)


def solid_with_vignette(rgb, w=W, h=H, strength=0.25):
    img = Image.new("RGB", (w, h), rgb)
    noise = Image.effect_noise((w, h), 8).convert("L")
    img = Image.blend(img, ImageOps.colorize(noise, black=(0, 0, 0), white=(255, 255, 255)), 0.035)
    vign = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vign)
    vd.ellipse([-w * 0.35, -h * 0.25, w * 1.35, h * 1.25], fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(260))
    dark = Image.new("RGB", (w, h), tuple(max(0, int(c * (1 - strength))) for c in rgb))
    return Image.composite(img, dark, vign)


LOGO_MARK = load_logo_mark()
LOGO_WHITE = LOGO_MARK
LOGO_CHARCOAL = recolor(LOGO_MARK, CHARCOAL)
LOGO_OXBLOOD = recolor(LOGO_MARK, OXBLOOD)
LOGO_BONE = recolor(LOGO_MARK, BONE)


def scaled_logo(logo, target_w):
    ratio = target_w / logo.width
    return logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)


def save(img, name):
    img.convert("RGB").save(FRAMES_DIR / f"{name}.png", quality=95)
    print("wrote", name)


# 1-2: torn/folded paper reveal, oxblood
for tag, seed in [("a", 1), ("b", 1)]:
    bg = paper_texture(OXBLOOD, fold_count=3, seed=seed).convert("RGBA")
    paste_centered(bg, scaled_logo(LOGO_BONE, int(W * 0.34)), W * 0.5, H * 0.46)
    save(bg, f"01_paper_oxblood_{tag}")

# 3-4: torn/folded paper reveal, bone
for tag, seed in [("a", 2), ("b", 3)]:
    bg = paper_texture(BONE, fold_count=4, seed=seed).convert("RGBA")
    paste_centered(bg, scaled_logo(LOGO_CHARCOAL, int(W * 0.34)), W * 0.5, H * 0.46)
    save(bg, f"02_paper_bone_{tag}")

# phone mockup: clean device silhouette + splash screen, no gimmicky hand
def phone_mockup(fill_screen):
    img = solid_with_vignette((20, 20, 20), strength=0.05).convert("RGBA")
    draw = ImageDraw.Draw(img)
    pw, ph = int(W * 0.6), int(W * 0.6 * 2.05)
    px, py = (W - pw) // 2, int(H * 0.5 - ph * 0.5)
    draw.rounded_rectangle([px - 16, py - 16, px + pw + 16, py + ph + 16], radius=70, fill=(8, 8, 8))
    draw.rounded_rectangle([px - 16, py - 16, px + pw + 16, py + ph + 16], radius=70, outline=(60, 60, 60), width=2)
    screen = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(screen)
    screen.paste(Image.new("RGB", (pw, ph), (0, 0, 0)), (0, 0))
    fill_screen(screen, sdraw, pw, ph)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=52, fill=255)
    img.paste(screen, (px, py), mask)
    # notch
    nw, nh = int(pw * 0.32), int(ph * 0.022)
    draw.rounded_rectangle([px + pw / 2 - nw / 2, py + 14, px + pw / 2 + nw / 2, py + 14 + nh],
                            radius=nh, fill=(8, 8, 8))
    return img


def splash_screen(screen, sdraw, pw, ph):
    sdraw.rectangle([0, 0, pw, ph], fill=OXBLOOD)
    logo = scaled_logo(LOGO_BONE, int(pw * 0.4))
    screen.alpha_composite(logo, (int(pw / 2 - logo.width / 2), int(ph * 0.42 - logo.height / 2)))
    tracked_text(sdraw, (pw / 2, ph * 0.58), "GEN ATELIÉR", font(MANROPE_SEMI, int(pw * 0.072)), BONE, tracking=4)


bg = phone_mockup(splash_screen)
save(bg, "03_phone_splash_a")
bg = phone_mockup(splash_screen)
save(bg, "03_phone_splash_b")


def home_screen(screen, sdraw, pw, ph):
    sdraw.rectangle([0, 0, pw, ph], fill=(245, 245, 240))
    sdraw.text((pw * 0.08, ph * 0.045), "9:41", font=font(MANROPE_SEMI, int(pw * 0.055)), fill=CHARCOAL, anchor="lm")
    cols, rows = 4, 5
    margin = pw * 0.09
    cell = (pw - margin * 2) / cols
    icon_size = int(cell * 0.62)
    highlight = 6
    idx = 0
    for r in range(rows):
        for c in range(cols):
            idx += 1
            cx = margin + c * cell + cell / 2
            cy = ph * 0.14 + r * cell * 1.18 + cell / 2
            if idx == highlight:
                sdraw.rounded_rectangle([cx - icon_size / 2, cy - icon_size / 2, cx + icon_size / 2, cy + icon_size / 2],
                                         radius=icon_size * 0.26, fill=OXBLOOD)
                logo = scaled_logo(LOGO_BONE, int(icon_size * 0.6))
                screen.alpha_composite(logo, (int(cx - logo.width / 2), int(cy - logo.height / 2)))
            else:
                sdraw.rounded_rectangle([cx - icon_size / 2, cy - icon_size / 2, cx + icon_size / 2, cy + icon_size / 2],
                                         radius=icon_size * 0.26, fill=(214, 214, 204))
    tracked_text(sdraw, (pw / 2, ph * 0.14 + rows * cell * 1.18 + cell * 0.55), "GEN ATELIÉR",
                 font(MANROPE_SEMI, int(pw * 0.06)), CHARCOAL, tracking=3)


bg = phone_mockup(home_screen)
save(bg, "04_phone_home")

# hang tag mockup on sky, laid flat (brand's own stationery motif)
img = solid_with_vignette(SKY, strength=0.22).convert("RGBA")
draw = ImageDraw.Draw(img)
tw, th = int(W * 0.46), int(W * 0.46 * 1.5)
tag = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
tdraw = ImageDraw.Draw(tag)
tdraw.rectangle([20, 20, tw + 20, th + 20], fill=BONE)
hole_r = 15
hx, hy = tw / 2 + 20, 20 + 36
tdraw.ellipse([hx - hole_r, hy - hole_r, hx + hole_r, hy + hole_r], fill=SKY)
logo_t = scaled_logo(LOGO_CHARCOAL, int(tw * 0.42))
tag.alpha_composite(logo_t, (int(tw / 2 + 20 - logo_t.width / 2), int(th * 0.38)))
tdraw.line([(30, th * 0.78), (tw + 10, th * 0.78)], fill=LINE, width=2)
tdraw.text((tw / 2 + 20, th * 0.86), "size: just right", font=font(GARAMOND_ITALIC, int(tw * 0.1)),
           fill=CHARCOAL, anchor="mm")
tag = tag.rotate(-5, expand=True, resample=Image.BICUBIC)
paste_centered(img, tag, W * 0.5, H * 0.42)
save(img, "05_hangtag")

# real product hero, using existing product photography, with wordmark
candidates = ["Wrap Trouser Black.png", "Flap Trouser Black.png", "Wrap Trouser Beige.png"]
product_path = next((ROOT / c for c in candidates if (ROOT / c).exists()), None)
if product_path:
    prod = Image.open(product_path).convert("RGBA")
    canvas = solid_with_vignette(BONE, strength=0.12).convert("RGBA")
    scale = min(W * 0.86 / prod.width, H * 0.78 / prod.height)
    prod_r = prod.resize((int(prod.width * scale), int(prod.height * scale)), Image.LANCZOS)
    paste_centered(canvas, prod_r, W * 0.52, H * 0.48)
    draw = ImageDraw.Draw(canvas)
    tracked_text(draw, (W / 2, H * 0.93), "GEN ATELIÉR", font(MANROPE_SEMI, int(W * 0.05)), CHARCOAL, tracking=6)
    save(canvas, "06_product_hero")

# 7: brand colour palette reveal card
img = Image.new("RGBA", (W, H), (*BONE, 255))
draw = ImageDraw.Draw(img)
pad = int(W * 0.07)
gap = int(W * 0.04)
card_w = (W - pad * 2 - gap * 3) / 4
card_h = int(H * 0.42)
top = int(H * 0.28)
cards = [
    (OXBLOOD, "Oxblood", "#6F2727", BONE),
    (BONE, "Bone", "#EEEEE6", CHARCOAL),
    (CHARCOAL, "Charcoal", "#2F2F2F", BONE),
    (SKY, "Sky", "#77A3C6", CHARCOAL),
]
f_label = font(MANROPE_SEMI, int(W * 0.022))
f_name = font(GARAMOND_ITALIC, int(W * 0.045))
f_hex = font(MANROPE_SEMI, int(W * 0.02))
for i, (rgb, name_txt, hexcode, txtcol) in enumerate(cards):
    x0 = pad + i * (card_w + gap)
    if rgb == BONE:
        draw.rectangle([x0, top, x0 + card_w, top + card_h], fill=rgb, outline=LINE, width=2)
    else:
        draw.rectangle([x0, top, x0 + card_w, top + card_h], fill=rgb)
    draw.text((x0 + card_w * 0.12, top + card_h * 0.08), "COLOUR", font=f_label, fill=txtcol)
    draw.text((x0 + card_w * 0.12, top + card_h * 0.7), name_txt, font=f_name, fill=txtcol)
    draw.text((x0 + card_w * 0.12, top + card_h * 0.86), hexcode, font=f_hex, fill=txtcol)
f_top = font(MANROPE_LIGHT, int(W * 0.065))
draw.text((W / 2, top - H * 0.07), "the palette", font=f_top, fill=CHARCOAL, anchor="mm")
save(img, "07_palette_card")

# 8-13: logo cycling across flat colour-block backgrounds
swatches = [
    (OXBLOOD, LOGO_BONE, "08_swatch_oxblood"),
    (CHARCOAL, LOGO_BONE, "09_swatch_charcoal"),
    (INK_MUTED, LOGO_BONE, "10_swatch_ink"),
    (BONE, LOGO_CHARCOAL, "11_swatch_bone"),
    (SKY, LOGO_CHARCOAL, "12_swatch_sky"),
    (DEEP_SKY, LOGO_BONE, "13_swatch_deepsky"),
]
for rgb, logo, name in swatches:
    im = solid_with_vignette(rgb, strength=0.2).convert("RGBA")
    paste_centered(im, scaled_logo(logo, int(W * 0.4)), W * 0.5, H * 0.5)
    save(im, name)

# 14: end card
img = solid_with_vignette(CHARCOAL, strength=0.3).convert("RGBA")
draw = ImageDraw.Draw(img)
paste_centered(img, scaled_logo(LOGO_BONE, int(W * 0.3)), W * 0.5, H * 0.42)
tracked_text(draw, (W / 2, H * 0.52), "GEN ATELIÉR", font(MANROPE_SEMI, int(W * 0.05)), BONE, tracking=8)
draw.text((W / 2, H * 0.575), "made for how you move", font=font(GARAMOND_ITALIC, int(W * 0.045)),
          fill=LINE, anchor="mm")
save(img, "14_endcard")

print("done")

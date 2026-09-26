#!/usr/bin/env python3
"""Final renderer: exact-measured reference choreography + real images.

Replays the same 37 measured placement events (scripts/motion_prototype.py)
verbatim — identical box coordinates, identical 5fps tick timing, identical
order — but each of the 9 source slots is now either a real photo
(cover-fit into the measured card region, on a paper-texture backdrop) or,
until it's supplied, the flat placeholder color from the prototype.

Usage:
    python3 scripts/render_final.py --out output/final.mp4
"""
import argparse
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

W, H = 720, 1280
FPS = 30
TICK_FRAMES = 6

# Measured envelope of every event box across the whole reference (see
# motion_prototype.py) — the region each source image is cover-fit into;
# everything outside is paper-texture backdrop.
CARD_REGION = (28, 250, 691, 1103)

PLACEHOLDER_COLORS = {
    "A": (58, 102, 106), "B": (196, 93, 76), "C": (214, 163, 62),
    "D": (74, 82, 99), "E": (117, 76, 105), "F": (176, 96, 44),
    "G": (47, 92, 140), "H": (67, 126, 79), "I": (163, 45, 51),
}

EVENTS = [
    (1, [127, 279, 377, 631], "B"),
    (2, [142, 271, 601, 967], "B"),
    (2, [130, 484, 354, 763], "A"),
    (3, [116, 662, 378, 1016], "B"),
    (3, [392, 255, 619, 608], "B"),
    (4, [115, 531, 585, 779], "C"),
    (5, [115, 250, 619, 655], "D"),
    (6, [117, 278, 614, 1011], "C"),
    (7, [135, 284, 598, 1005], "E"),
    (7, [86, 628, 138, 987], "D"),
    (8, [118, 326, 454, 1045], "D"),
    (9, [235, 359, 679, 1078], "D"),
    (10, [126, 623, 636, 1031], "E"),
    (11, [99, 288, 579, 651], "E"),
    (12, [99, 288, 636, 1052], "E"),
    (13, [341, 646, 583, 988], "D"),
    (13, [115, 717, 333, 1004], "D"),
    (14, [353, 280, 587, 727], "D"),
    (15, [88, 746, 645, 1018], "F"),
    (16, [28, 670, 488, 804], "F"),
    (17, [108, 329, 691, 734], "F"),
    (18, [79, 280, 583, 514], "E"),
    (19, [77, 306, 530, 1039], "F"),
    (20, [304, 316, 611, 1027], "E"),
    (21, [72, 600, 586, 1066], "G"),
    (22, [133, 316, 638, 729], "G"),
    (23, [132, 364, 391, 1069], "H"),
    (23, [117, 368, 171, 625], "H"),
    (24, [328, 375, 613, 1070], "H"),
    (25, [64, 878, 367, 1042], "I"),
    (25, [330, 952, 533, 1103], "I"),
    (26, [102, 834, 551, 983], "I"),
    (27, [102, 732, 602, 944], "I"),
    (28, [52, 502, 465, 808], "I"),
    (28, [407, 570, 544, 817], "I"),
    (29, [105, 366, 403, 675], "I"),
    (29, [338, 446, 581, 818], "I"),
]


def make_paper_texture(w, h, seed=3):
    rng = np.random.default_rng(seed)
    base = np.full((h, w, 3), (237, 231, 219), dtype=np.float64)

    fine = rng.normal(0, 1.5, (h, w, 1))
    base += fine

    coarse = rng.normal(0, 10, (h // 24 + 1, w // 24 + 1, 1))
    coarse_up = Image.fromarray((coarse[..., 0] + 128).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    coarse_up = np.array(coarse_up).astype(np.float64)[..., None] - 128
    base += coarse_up

    # a handful of long faint fiber streaks, like pressed paper pulp
    fiber = np.zeros((h, w), dtype=np.float64)
    for _ in range(60):
        y = rng.integers(0, h)
        x0 = rng.integers(0, w)
        length = rng.integers(30, 140)
        angle = rng.uniform(-0.3, 0.3)
        strength = rng.uniform(4, 10)
        for t in range(length):
            xx = int(x0 + t)
            yy = int(y + t * angle)
            if 0 <= xx < w and 0 <= yy < h:
                fiber[yy, xx] += strength
    fiber_img = Image.fromarray(np.clip(fiber, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    base -= np.array(fiber_img).astype(np.float64)[..., None] * 0.5

    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt(((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2)
    vignette = 1.0 - np.clip(dist * 0.35, 0, 0.10)
    base *= vignette[..., None]

    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    img = img.filter(ImageFilter.GaussianBlur(2.2))
    return img


def cover_fit(im, w, h):
    src_w, src_h = im.size
    scale = max(w / src_w, h / src_h)
    nw, nh = round(src_w * scale), round(src_h * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = (nh - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def load_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def make_placeholder_card(letter, color, cw, ch):
    canvas = Image.new("RGB", (cw, ch), color)
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", round(ch * 0.28))
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((cw - tw) / 2 - bbox[0], (ch - th) / 2 - bbox[1]), letter, fill=(255, 255, 255), font=font)
    return canvas


def build_source_frame(letter, image_path, paper_texture):
    x0, y0, x1, y1 = CARD_REGION
    cw, ch = x1 - x0, y1 - y0
    canvas = paper_texture.copy()

    if image_path is not None:
        card_content = cover_fit(load_rgb(image_path), cw, ch)
    else:
        card_content = make_placeholder_card(letter, PLACEHOLDER_COLORS[letter], cw, ch)

    border = 10
    bordered = Image.new("RGB", (cw + border * 2, ch + border * 2), (255, 253, 250))
    bordered.paste(card_content, (border, border))

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([x0 - border + 6, y0 - border + 12, x1 + border + 6, y1 + border + 12], fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))

    base = canvas.convert("RGBA")
    base.alpha_composite(shadow)
    base.paste(bordered, (x0 - border, y0 - border))
    return base.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("output/final.mp4"))
    parser.add_argument("--image", action="append", default=[], metavar="LETTER=PATH",
                         help="Assign a real image to a slot, e.g. --image A=photo.jpg. Repeatable.")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    slot_images = {}
    for spec in args.image:
        letter, path = spec.split("=", 1)
        slot_images[letter] = Path(path)

    paper = make_paper_texture(W, H)
    source_frames = {
        letter: build_source_frame(letter, slot_images.get(letter), paper)
        for letter in PLACEHOLDER_COLORS
    }

    canvas = source_frames["A"].copy()
    by_tick = {}
    for tick, box, source in EVENTS:
        by_tick.setdefault(tick, []).append((box, source))
    max_tick = max(by_tick)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        idx = 0

        def save(img):
            nonlocal idx
            img.save(tmp_dir / f"f_{idx:05d}.png")
            idx += 1

        for _ in range(TICK_FRAMES):
            save(canvas)

        for tick in range(1, max_tick + 1):
            for box, source in by_tick.get(tick, []):
                x0, y0, x1, y1 = box
                piece = source_frames[source].crop((x0, y0, x1, y1))
                canvas.paste(piece, (x0, y0))
            for _ in range(TICK_FRAMES):
                save(canvas)

        subprocess.run(
            ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp_dir / "f_%05d.png"),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.out)],
            check=True,
        )
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

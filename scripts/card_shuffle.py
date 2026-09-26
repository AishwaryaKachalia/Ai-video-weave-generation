#!/usr/bin/env python3
"""Render a "photo-card shatter" transition edit from a list of still images.

Recreates the reference mechanic: static camera, each beat is a still image
held on screen, and the cut to the next beat happens by splitting the
outgoing image into four quadrants that shatter outward toward the corners
(with a soft drop shadow), revealing the next image sitting beneath.

Each beat is styled one of two ways:
  - "card":      contained on a cream backdrop with a bordered photo-card
                 look (for studio/catalog-style product shots).
  - "fullbleed": cover-cropped to fill the whole frame (for macro/lifestyle
                 shots that already read as full-frame photography).

Usage:
    python3 scripts/card_shuffle.py config.json --out output/my-edit.mp4

config.json:
{
  "width": 1080, "height": 1920, "fps": 30,
  "background": [238, 233, 226],
  "transition_s": 0.3,
  "beats": [
    {"image": "Flap Trouser Black.png", "style": "card", "hold_s": 0.45},
    {"image": "hero/flap-trouser-grey-v1.png", "style": "fullbleed", "hold_s": 0.8}
  ]
}
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

CORNERS = {
    "tl": (-1, -1),
    "tr": (1, -1),
    "bl": (-1, 1),
    "br": (1, 1),
}


def ease_in_cubic(t: float) -> float:
    return t ** 3


def load_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def fit_cover(im: Image.Image, w: int, h: int) -> Image.Image:
    src_w, src_h = im.size
    scale = max(w / src_w, h / src_h)
    new_w, new_h = round(src_w * scale), round(src_h * scale)
    im = im.resize((new_w, new_h), Image.LANCZOS)
    x0 = (new_w - w) // 2
    y0 = (new_h - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def prepare_fullbleed(im: Image.Image, w: int, h: int) -> Image.Image:
    return fit_cover(im, w, h)


def prepare_card(im: Image.Image, w: int, h: int, bg_color: tuple) -> Image.Image:
    canvas = Image.new("RGB", (w, h), bg_color)
    card_w = round(w * 0.82)
    card_h = round(h * 0.82)
    src_w, src_h = im.size
    scale = min(card_w / src_w, card_h / src_h)
    new_w, new_h = round(src_w * scale), round(src_h * scale)
    resized = im.resize((new_w, new_h), Image.LANCZOS)

    border = 18
    card = Image.new("RGB", (new_w + border * 2, new_h + border * 2), (255, 253, 250))
    card.paste(resized, (border, border))

    cx, cy = w // 2, h // 2
    cw, ch = card.size
    x0, y0 = cx - cw // 2, cy - ch // 2

    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    pad = 14
    sd.rectangle([x0 + pad, y0 + pad + 10, x0 + cw + pad, y0 + ch + pad + 10], fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(shadow)
    canvas = canvas.convert("RGB")
    canvas.paste(card, (x0, y0))
    return canvas


def prepare_beat(beat: dict, base_dir: Path, w: int, h: int, bg_color: tuple) -> Image.Image:
    im = load_rgb(base_dir / beat["image"])
    if beat.get("style", "card") == "fullbleed":
        return prepare_fullbleed(im, w, h)
    return prepare_card(im, w, h, bg_color)


def quadrant_boxes(w: int, h: int):
    hw, hh = w // 2, h // 2
    return {
        "tl": (0, 0, hw, hh),
        "tr": (hw, 0, w, hh),
        "bl": (0, hh, hw, h),
        "br": (hw, hh, w, h),
    }


def shatter_frame(outgoing: Image.Image, incoming: Image.Image, t: float, w: int, h: int) -> Image.Image:
    eased = ease_in_cubic(t)
    max_travel_x = w * 0.85
    max_travel_y = h * 0.85

    frame = incoming.convert("RGBA")
    boxes = quadrant_boxes(w, h)

    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)

    pieces = []
    for name, (bx0, by0, bx1, by1) in boxes.items():
        dx, dy = CORNERS[name]
        ox = round(dx * eased * max_travel_x)
        oy = round(dy * eased * max_travel_y)
        piece = outgoing.crop((bx0, by0, bx1, by1))
        pieces.append((piece, bx0 + ox, by0 + oy, bx1 - bx0, by1 - by0))
        sd.rectangle([bx0 + ox + 6, by0 + oy + 10, bx0 + ox + (bx1 - bx0) + 6, by0 + oy + (by1 - by0) + 10],
                     fill=(0, 0, 0, int(70 * (1 - eased) + 20)))

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(16))
    frame.alpha_composite(shadow_layer)

    for piece, px, py, pw, ph in pieces:
        frame.paste(piece, (px, py))

    return frame.convert("RGB")


def render(config: dict, base_dir: Path, out_path: Path) -> None:
    w = config.get("width", 1080)
    h = config.get("height", 1920)
    fps = config.get("fps", 30)
    bg = tuple(config.get("background", [238, 233, 226]))
    transition_s = config.get("transition_s", 0.3)
    beats = config["beats"]

    prepared = [prepare_beat(b, base_dir, w, h, bg) for b in beats]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        frame_idx = 0

        def save(img: Image.Image):
            nonlocal frame_idx
            img.save(tmp_dir / f"f_{frame_idx:05d}.png")
            frame_idx += 1

        for i, (beat, img) in enumerate(zip(beats, prepared)):
            hold_frames = max(round(beat.get("hold_s", 0.45) * fps), 1)
            for _ in range(hold_frames):
                save(img)

            if i < len(prepared) - 1:
                trans_frames = max(round(transition_s * fps), 1)
                nxt = prepared[i + 1]
                for f in range(trans_frames):
                    t = (f + 1) / trans_frames
                    save(shatter_frame(img, nxt, t, w, h))

        subprocess.run(
            ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(tmp_dir / "f_%05d.png"),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_path)],
            check=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    config = json.loads(args.config.read_text())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    render(config, args.base_dir, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

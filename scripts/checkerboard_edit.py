#!/usr/bin/env python3
"""Full-bleed checkerboard edit: one image per frame, no border, no margin.

Each source image cover-fits the ENTIRE canvas — no card, no background,
no border. A transition between consecutive images is a clean two-stage
checkerboard hard-cut:
  stage 1: top-left + bottom-right quadrants cut to the new image
  stage 2: top-right + bottom-left quadrants also cut to the new image
           (now the whole frame is the new image, single and coherent)
Never more than two images (old, new) appear in one frame, and both are
always full crops of the SAME two pictures — no unrelated third source.

Usage:
    python3 scripts/checkerboard_edit.py --out output/checkerboard.mp4 \
        --image photo1.jpg --image photo2.jpg --image photo3.jpg ...
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

W, H = 720, 1280
FPS = 30

HOLD_S = 1.0        # each completed image sits alone before the next transition starts
STAGE_S = 0.35       # how long stage 1 (TL+BR only) holds before stage 2 completes it


def cover_fit(im: Image.Image, w: int, h: int) -> Image.Image:
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


def quadrants(w, h):
    hw, hh = w // 2, h // 2
    return {"tl": (0, 0, hw, hh), "tr": (hw, 0, w, hh), "bl": (0, hh, hw, h), "br": (hw, hh, w, h)}


def checkerboard_stage(old_img, new_img, quads_to_new):
    frame = old_img.copy()
    boxes = quadrants(W, H)
    for name in quads_to_new:
        box = boxes[name]
        frame.paste(new_img.crop(box), box[:2])
    return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("output/checkerboard.mp4"))
    parser.add_argument("--image", action="append", required=True, help="Repeatable, in order.")
    parser.add_argument("--hold", type=float, default=HOLD_S)
    parser.add_argument("--stage", type=float, default=STAGE_S)
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    frames_full = [cover_fit(load_rgb(Path(p)), W, H) for p in args.image]

    hold_frames = round(args.hold * FPS)
    stage_frames = round(args.stage * FPS)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        idx = 0

        def save(img):
            nonlocal idx
            img.save(tmp_dir / f"f_{idx:05d}.png")
            idx += 1

        for i, img in enumerate(frames_full):
            for _ in range(hold_frames):
                save(img)
            if i < len(frames_full) - 1:
                nxt = frames_full[i + 1]
                stage1 = checkerboard_stage(img, nxt, ["tl", "br"])
                for _ in range(stage_frames):
                    save(stage1)
                stage2 = checkerboard_stage(img, nxt, ["tl", "br", "tr", "bl"])
                for _ in range(stage_frames):
                    save(stage2)

        subprocess.run(
            ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp_dir / "f_%05d.png"),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.out)],
            check=True,
        )
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

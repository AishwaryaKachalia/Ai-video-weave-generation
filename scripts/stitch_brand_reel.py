#!/usr/bin/env python3
"""Stitch assets/frames/*.png into the final Gen Ateliér logo-reveal reel.

Hard cuts only -- no zoom, no pan, no crossfade -- matching the reference
video's flash-cut pace. Every frame already carries the logo at the exact
same fixed position/size; this script only decides how long each frame
holds before the next hard cut.

Usage:
    python3 scripts/stitch_brand_reel.py --out output/gen-atelier-reveal.mp4
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAMES = ROOT / "assets" / "frames"
W, H, FPS = 1080, 1920, 30

# (frame stem, duration_s) -- hard cut to the next, no motion within a hold.
SEQUENCE = [
    ("01_paper_a", 0.20),
    ("01_paper_b", 0.20),
    ("02_stone_a", 0.20),
    ("02_stone_b", 0.20),
    ("03_color_oxblood", 0.18),
    ("04_color_charcoal", 0.18),
    ("05_color_ink", 0.16),
    ("06_color_bone", 0.16),
    ("07_color_sky", 0.16),
    ("08_color_deepsky", 0.16),
    ("03_color_oxblood", 0.14),
    ("06_color_bone", 0.14),
    ("04_color_charcoal", 0.14),
    ("07_color_sky", 0.14),
    ("09_endcard", 0.90),
]


def build_clip(stem, duration, tmp_dir, idx):
    src = FRAMES / f"{stem}.png"
    dst = tmp_dir / f"{idx:03d}-{stem}.mp4"
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(src), "-t", str(duration),
        "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(dst),
    ]
    subprocess.run(cmd, check=True)
    return dst


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        clips = [build_clip(stem, dur, tmp_dir, i) for i, (stem, dur) in enumerate(SEQUENCE)]
        list_file = tmp_dir / "list.txt"
        list_file.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
             "-c", "copy", str(args.out)],
            check=True,
        )
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

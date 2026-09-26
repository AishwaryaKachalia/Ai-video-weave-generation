#!/usr/bin/env python3
"""Stitch assets/frames/*.png into the final Gen Ateliér logo-reveal reel,
matching the reference video's fast-cut, colour-cycling pace.

Usage:
    python3 scripts/stitch_brand_reel.py --out output/gen-atelier-reveal.mp4
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAMES = ROOT / "assets" / "frames"
W, H, FPS = 1080, 1920, 30

# (frame stem, duration_s, zoom start, zoom end)
SEQUENCE = [
    ("01_paper_oxblood_a", 0.20, 1.00, 1.05),
    ("01_paper_oxblood_b", 0.20, 1.05, 1.10),
    ("02_paper_bone_a", 0.20, 1.00, 1.05),
    ("02_paper_bone_b", 0.20, 1.05, 1.10),
    ("03_phone_splash_a", 0.28, 1.00, 1.05),
    ("03_phone_splash_b", 0.22, 1.05, 1.09),
    ("04_phone_home", 0.45, 1.00, 1.05),
    ("05_hangtag", 0.42, 1.00, 1.05),
    ("06_product_hero", 0.60, 1.00, 1.05),
    ("07_palette_card", 1.05, 1.00, 1.04),
    ("08_swatch_oxblood", 0.24, 1.00, 1.06),
    ("09_swatch_charcoal", 0.24, 1.00, 1.06),
    ("10_swatch_ink", 0.22, 1.00, 1.06),
    ("11_swatch_bone", 0.22, 1.00, 1.06),
    ("12_swatch_sky", 0.22, 1.00, 1.06),
    ("13_swatch_deepsky", 0.22, 1.00, 1.06),
    ("08_swatch_oxblood", 0.15, 1.06, 1.10),
    ("11_swatch_bone", 0.15, 1.06, 1.10),
    ("09_swatch_charcoal", 0.15, 1.06, 1.10),
    ("12_swatch_sky", 0.15, 1.06, 1.10),
    ("14_endcard", 1.30, 1.00, 1.05),
]


def build_clip(stem, duration, z0, z1, tmp_dir, idx):
    src = FRAMES / f"{stem}.png"
    dst = tmp_dir / f"{idx:03d}-{stem}.mp4"
    frames = max(round(duration * FPS), 1)
    fm1 = max(frames - 1, 1)
    ease = f"(1-pow(1-min(on/{fm1},1),3))"
    z_expr = f"{z0}+({z1}-{z0})*{ease}"
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"zoompan=z='{z_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H},"
        f"fps={FPS}"
    )
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
        clips = [
            build_clip(stem, dur, z0, z1, tmp_dir, i)
            for i, (stem, dur, z0, z1) in enumerate(SEQUENCE)
        ]
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

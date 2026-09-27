#!/usr/bin/env python3
"""Stitch assets/frames/tear/tear_*.png into a stop-motion clip.
Hard holds per frame, no interpolation -- genuine stop-motion look.

Usage:
    python3 scripts/stitch_paper_tear_stopmotion.py --out output/paper-tear-stopmotion.mp4
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAMES = ROOT / "assets" / "frames" / "tear"
W, H, FPS = 1080, 1920, 30
HOLD_S = 0.12  # per-frame hold; stop-motion pace


def build_clip(src, duration, tmp_dir, idx):
    dst = tmp_dir / f"{idx:03d}.mp4"
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
    parser.add_argument("--hold", type=float, default=HOLD_S)
    parser.add_argument("--end-hold", type=float, default=0.9)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    frames = sorted(FRAMES.glob("tear_*.png"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        clips = []
        for i, f in enumerate(frames):
            dur = args.end_hold if i == len(frames) - 1 else args.hold
            clips.append(build_clip(f, dur, tmp_dir, i))
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

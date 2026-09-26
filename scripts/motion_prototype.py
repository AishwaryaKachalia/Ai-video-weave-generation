#!/usr/bin/env python3
"""Placeholder-only replay of the reference's EXACT measured choreography.

This does not invent a transition pattern. It replays the literal sequence
of change events measured by diffing the reference video frame-by-frame
(scripts/reference_events.json): the same box pixel coordinates, the same
5fps (6-frame) tick cadence, the same order, the same which-events-share-a-
tick grouping. Each event is colored by which of the 9 source photos it
belongs to in the reference (bottle, rose-petal, text-card, lipstick-bullet,
rose-bloom, berry-cluster, round-object, tube, lips) — flat colors only,
no real images, per instruction: nail the motion first, images come later.

Usage:
    python3 scripts/motion_prototype.py --out output/motion_prototype.mp4
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
FPS = 30
TICK_FRAMES = 6  # 0.2s per tick, matches the measured 5fps cadence

SOURCES = {
    "A": (58, 102, 106),   # bottle (initial frame)
    "B": (196, 93, 76),    # rose petal macro
    "C": (214, 163, 62),   # text/wordmark card
    "D": (74, 82, 99),     # lipstick bullet
    "E": (117, 76, 105),   # rose bloom
    "F": (176, 96, 44),    # berry / floral cluster
    "G": (47, 92, 140),    # round object (compact/balm)
    "H": (67, 126, 79),    # lipstick tube
    "I": (163, 45, 51),    # lips
}

# (tick, box_px[x0,y0,x1,y1], source) — measured directly from the
# reference video by frame-differencing; tick*0.2s = timestamp; a tick
# repeated twice means two pieces landed in the same 0.2s window.
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


def make_source_frame(letter, color):
    canvas = Image.new("RGB", (W, H), color)
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", round(H * 0.22))
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((W - tw) / 2 - bbox[0], (H - th) / 2 - bbox[1]), letter, fill=(255, 255, 255), font=font)
    return canvas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("output/motion_prototype.mp4"))
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    source_frames = {letter: make_source_frame(letter, color) for letter, color in SOURCES.items()}

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

#!/usr/bin/env python3
"""Software light-reveal: dark silhouette still -> lit still, with a soft light front sweeping left to right
and a slow lateral camera drift (no zoom, no rotation). The can never changes, so packaging stays exact.
Usage: python3 scripts/reveal_sweep.py dark.png lit.png out.mp4 [seconds]"""
import subprocess, sys
import numpy as np
from PIL import Image

dark_p, lit_p, out, secs = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
W, H, FPS, S = 1080, 1920, 30, 1.18
sw, sh = int(W * S), int(H * S)
A = np.asarray(Image.open(dark_p).convert("RGB").resize((sw, sh), Image.LANCZOS), np.float32)
B = np.asarray(Image.open(lit_p).convert("RGB").resize((sw, sh), Image.LANCZOS), np.float32)
n = int(secs * FPS)
xs = (np.arange(sw, dtype=np.float32) / sw)[None, :, None]
ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
                       "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / (n - 1)
    e = t * t * (3 - 2 * t)                      # ease in/out
    hold = 0.18                                  # stay dark for the first moments
    p = -0.25 + (1.5) * np.clip((e - hold) / (1 - hold), 0, 1)
    m = np.clip((p - xs) / 0.28, 0, 1)
    m = m * m * (3 - 2 * m)
    frame = A * (1 - m) + B * m
    ox = int((sw - W) * e)                       # left -> right drift
    oy = (sh - H) // 2
    ff.stdin.write(np.clip(frame[oy:oy + H, ox:ox + W], 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
print("wrote", out)

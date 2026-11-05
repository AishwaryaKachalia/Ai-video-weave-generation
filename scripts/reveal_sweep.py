#!/usr/bin/env python3
"""Software light-reveal: dark silhouette still -> lit still. The camera and the can are LOCKED; only the light moves:
a hot light front sweeps left to right with a bright specular streak, flare glow and a haze pulse.
The can never changes, so packaging stays exact.
Usage: python3 scripts/reveal_sweep.py dark.png lit.png out.mp4 [seconds]"""
import subprocess, sys
import numpy as np
from PIL import Image

dark_p, lit_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
secs = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
W, H, FPS = 1080, 1920, 30
A = np.asarray(Image.open(dark_p).convert("RGB").resize((W, H), Image.LANCZOS), np.float32)
B = np.asarray(Image.open(lit_p).convert("RGB").resize((W, H), Image.LANCZOS), np.float32)
lumA, lumB = A.mean(2), B.mean(2)
body = np.clip((lumB - lumA) / 60.0, 0, 1)[:, :, None]          # where the can body gets lit
n = int(secs * FPS)
xs = (np.arange(W, dtype=np.float32) / W)[None, :, None]
warm = np.array([1.0, 0.82, 0.55], np.float32)[None, None, :]
ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
                       "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / (n - 1)
    s = np.clip((t - 0.08) / 0.62, 0, 1)                         # sweep runs 0.4s .. 3.5s
    s = s * s * (3 - 2 * s)
    p = -0.2 + 1.4 * s
    m = np.clip((p - xs) / 0.22, 0, 1)
    m = m * m * (3 - 2 * m)
    frame = A * (1 - m) + B * m
    d = (xs - p)                                                  # distance to the light front
    streak = np.exp(-(d / 0.045) ** 2) * (0.4 < 1) * (1 if 0 < s < 1 else 0)
    flare = np.exp(-(d / 0.20) ** 2) * (1 if 0 < s < 1 else 0)
    frame = frame + B * streak * body * 0.95 + warm * 38 * flare * body + warm * 14 * flare   # hot streak on the can + soft glow
    pulse = 0.5 + 0.5 * np.sin(t * 9.0)                          # slow haze breathing
    frame = frame + warm * 6 * pulse * (1 - body)
    ff.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
print("wrote", out)

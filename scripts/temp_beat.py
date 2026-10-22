#!/usr/bin/env python3
"""Generate a temp 20s guide track for the HIFI teaser (kick/hat/snare/bass/riser).

Usage: python3 scripts/temp_beat.py out.wav
Not final music: replace with the real UK garage / electronic / hip-hop hybrid.
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100
ROOT = Path(__file__).resolve().parent.parent
cfg = json.loads((ROOT / "shots/hifi-teaser.edit.json").read_text())["audio"]
BPM, DROP, (BO0, BO1), FINAL = cfg["bpm"], cfg["drop"], cfg["blackout"], cfg["final_hit"]
N = 20 * SR
out = np.zeros(N, np.float32)
rng = np.random.default_rng(3)


def add(sig, t, gain=1.0):
    i = int(t * SR)
    if i >= N:
        return
    j = min(N, i + len(sig))
    out[i:j] += sig[: j - i] * gain


def kick(d=0.28):
    t = np.arange(int(d * SR)) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def hat(d=0.05):
    t = np.arange(int(d * SR)) / SR
    n = rng.normal(0, 1, len(t))
    n = np.diff(n, prepend=0)
    return n * np.exp(-t * 90) * 0.35


def snare(d=0.2):
    t = np.arange(int(d * SR)) / SR
    return (rng.normal(0, 1, len(t)) * np.exp(-t * 22) * 0.6 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.4)


def sub(freq, d, decay=3.0):
    t = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * decay)


def riser(d):
    t = np.arange(int(d * SR)) / SR
    n = rng.normal(0, 1, len(t))
    k = int(SR * 0.002)
    lp = np.convolve(n, np.ones(k) / k, mode="same")
    return lp * (t / d) ** 2.2 * 0.9


beat = 60.0 / BPM
bass_notes = [49.0, 49.0, 58.27, 43.65]  # G1 G1 Bb1 F1

# 0 -> drop: building kick + hats
t = 0.0
bar = 0
while t < DROP - 0.01:
    prog = t / DROP
    add(kick(), t, 0.35 + 0.35 * prog)
    for k in range(2):
        add(hat(), t + k * beat / 2, 0.25 + 0.35 * prog)
    t += beat
add(riser(DROP - 1.2), 1.2, 0.5)

# drop at 6.0: sub boom then four-on-the-floor with bass line
add(sub(41.2, 1.4, 2.2), DROP, 1.0)
t = DROP
i = 0
while t < BO0 - 0.01:
    add(kick(), t, 0.95)
    add(hat(), t + beat / 2, 0.55)
    add(sub(bass_notes[(i // 2) % 4], beat * 0.9, 4.0), t + beat / 2, 0.55)
    if i % 2 == 1 and t > 13.0:
        add(snare(), t, 0.7)
    if t > 13.0:
        add(hat(), t + beat / 4, 0.4)
        add(hat(), t + 3 * beat / 4, 0.4)
    t += beat
    i += 1

# silence for blackout, then final heavy hit and tail
out[int(BO0 * SR): int(BO1 * SR)] = 0
add(sub(36.7, 2.6, 1.6), FINAL, 1.2)
add(kick(0.4), FINAL, 1.0)
add(snare(0.35), FINAL, 0.8)

out = np.tanh(out * 0.9)
out = out / max(1e-6, np.abs(out).max()) * 0.8
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", sys.argv[1])

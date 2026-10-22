#!/usr/bin/env python3
"""Film-look post pass for Hi-Fi frames: warm grade, lifted blacks, halation, grain.

Usage: python3 scripts/film_post.py in.png out.png [--grain 0.045] [--halation 0.35] [--warmth 0.06]
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter


def film_post(img, grain=0.045, halation=0.35, warmth=0.06, seed=7):
    rng = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0

    # Soft contrast: gentle S-curve blended toward original, lifted blacks, creamy highlights.
    s = a * a * (3 - 2 * a)
    a = 0.65 * a + 0.35 * s
    a = 0.04 + a * 0.93

    # Warm amber grade: pull blue down, red/green up slightly, de-purple the shadows.
    a[..., 0] *= 1 + warmth
    a[..., 1] *= 1 + warmth * 0.35
    a[..., 2] *= 1 - warmth * 1.1
    lum = a.mean(axis=2, keepdims=True)
    shadow = np.clip(1 - lum * 2.2, 0, 1)
    a[..., 0] += shadow[..., 0] * 0.012
    a[..., 1] += shadow[..., 0] * 0.008

    # Slight desaturation for a muted film palette.
    a = lum + (a - lum) * 0.92
    a = np.clip(a, 0, 1)

    # Halation: warm glow bleeding from bright areas.
    pil = Image.fromarray((a * 255).astype(np.uint8))
    bright = np.clip((a - 0.72) / 0.28, 0, 1)
    glow = Image.fromarray((bright * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(max(img.size) / 180)
    )
    g = np.asarray(glow, dtype=np.float32) / 255.0
    tint = np.array([1.0, 0.55, 0.28], dtype=np.float32)
    a = 1 - (1 - a) * (1 - g * tint * halation)

    # Grain: luminance-weighted, slightly soft, strongest in mids.
    h, w = a.shape[:2]
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    n = np.asarray(
        Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(0.8)
        ),
        dtype=np.float32,
    )
    n = (n - 128) / 40
    lum = a.mean(axis=2, keepdims=True)
    amp = grain * (0.4 + 1.2 * (1 - np.abs(lum - 0.45) * 1.6).clip(0, 1))
    chroma = rng.normal(0, 0.35, (h, w, 3)).astype(np.float32)
    a = a + (n[..., None] + chroma * 0.4) * amp

    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--grain", type=float, default=0.045)
    p.add_argument("--halation", type=float, default=0.35)
    p.add_argument("--warmth", type=float, default=0.06)
    args = p.parse_args()
    out = film_post(Image.open(args.src), args.grain, args.halation, args.warmth)
    out.save(args.dst)
    print("saved", args.dst)

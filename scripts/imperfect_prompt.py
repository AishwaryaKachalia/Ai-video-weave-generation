#!/usr/bin/env python3
"""Append flaws-first imperfection variables to a scene prompt.
Usage: python3 scripts/imperfect_prompt.py "scene text" [--seed N]
Banks live in config/skills/imperfection-prompts.md."""
import random, re, sys
from pathlib import Path

md = (Path(__file__).resolve().parent.parent / "config/skills/imperfection-prompts.md").read_text()
bank = {k: [s.strip().rstrip(".") for s in re.search(rf"^{k}: (.+)$", md, re.M).group(1).split(",")]
        for k in ("SURFACE", "AIR", "HUMAN", "LIGHT", "CAMERA")}
args = sys.argv[1:]
seed = int(args[args.index("--seed") + 1]) if "--seed" in args else random.randrange(10**6)
scene = args[0]
r = random.Random(seed)
parts = [r.choice(bank["LIGHT"]), r.choice(bank["SURFACE"]), r.choice(bank["AIR"]),
         r.choice(bank["HUMAN"]), r.choice(bank["CAMERA"])]
print(scene.rstrip(".") + ". " + ". ".join(p[0].upper() + p[1:] for p in parts) + ".")

#!/usr/bin/env python3
"""Append flaws-first imperfection variables to scene prompts (single or batch).
Single: python3 scripts/imperfect_prompt.py "scene text" [--seed N]
Batch:  python3 scripts/imperfect_prompt.py --batch scenes.txt [--out prompts.json] [--seed N]
        scenes.txt = one scene per line (blank lines / # comments ignored).
Each scene gets a different flaw set (seed+index); no flaw repeats until a bank runs out.
Banks live in config/skills/imperfection-prompts.md."""
import json, random, re, sys
from pathlib import Path

md = (Path(__file__).resolve().parent.parent / "config/skills/imperfection-prompts.md").read_text()
bank = {k: [s.strip().rstrip(".") for s in re.search(rf"^{k}: (.+)$", md, re.M).group(1).split(",")]
        for k in ("LIGHT", "SURFACE", "AIR", "HUMAN", "CAMERA")}
args = sys.argv[1:]
opt = lambda n: args[args.index(n) + 1] if n in args else None
seed = int(opt("--seed") or random.randrange(10**6))
scenes = ([l.strip() for l in Path(opt("--batch")).read_text().splitlines() if l.strip() and not l.startswith("#")]
          if "--batch" in args else [args[0]])
r = random.Random(seed)
pools = {k: [] for k in bank}


def pick(k):
    if not pools[k]:
        pools[k] = r.sample(bank[k], len(bank[k]))  # shuffle: no repeats within a cycle
    return pools[k].pop()


res = []
for s in scenes:
    p = [pick(k) for k in bank]
    res.append({"scene": s, "prompt": s.rstrip(".") + ". " + ". ".join(x[0].upper() + x[1:] for x in p) + "."})
if opt("--out"):
    Path(opt("--out")).write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(f"wrote {len(res)} prompts -> {opt('--out')}")
for x in res:
    print(x["prompt"] + "\n")

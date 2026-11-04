#!/usr/bin/env python3
"""Apply the text saved in the editor page to an edit list, so renders follow the user's words.

Usage: python3 scripts/apply_editor_text.py base.edit.json saved.json out.edit.json

saved.json is the `teaser/text` document from the editor page's database (either the bare
document or the {id, data, version} wrapper). The hook words fill the plain "hard" text items
in order; every other line is rebuilt from the saved items (text, timing, colour, place, size,
motion). Motion falls back to the base cut's motion for the same line when none was saved.
"""
import json
import sys

base_p, saved_p, out_p = sys.argv[1:4]
e = json.load(open(base_p))
s = json.load(open(saved_p))
s = s.get("data", s)

hook_items = [t for t in e["text"] if t.get("hard")]
for t, w in zip(hook_items, s["hook"]):
    t["lines"] = [w]

old_body = [t for t in e["text"] if not t.get("hard")]
body = []
for idx, it in enumerate(s["items"]):
    prev = old_body[idx] if idx < len(old_body) else {}
    t = {"t0": it["t0"], "t1": it["t1"], "lines": it.get("lines", []), "pos": it["pos"], "size": it["size"]}
    if it.get("color") and it["color"] != "white":
        t["color"] = it["color"]
    if it.get("y0") is not None and it["pos"] in ("top", "at"):
        t["y0"] = it["y0"]
    if it.get("count"):
        t["count"] = it["count"]
    else:
        t["anim"] = it.get("anim") or prev.get("anim") or "fade"
    body.append(t)
e["text"] = hook_items + body

if s.get("blanks"):
    print(f"NOTE: {len(s['blanks'])} extra blank(s) saved but not applied by this script (they change the cut).")
json.dump(e, open(out_p, "w"), indent=2, ensure_ascii=False)
print(f"applied: {len(hook_items)} hook words + {len(body)} text items -> {out_p}")

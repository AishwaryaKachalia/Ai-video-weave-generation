#!/usr/bin/env python3
"""Assemble the HIFI 20s investor teaser from shots/hifi-teaser.edit.json.

Usage: python3 scripts/build_teaser.py out.mp4 [--audio temp.wav] [--no-text]
Clips are read from clips/hifi/web/. Output is 1920x1080, 24fps, H.264/AAC.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "assets/fonts/Anton-Regular.ttf"
CLIPS = ROOT / "clips/hifi/web"


def run(cmd):
    subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)


def frame_counts(edit, fps):
    """Round every cut to whole frames, then fix each beat to its exact length so cuts never drift."""
    n = [max(1, round(c["d"] * fps)) for c in edit["cuts"]]
    for bi, b in enumerate(edit["beats"], start=1):
        idx = [i for i, c in enumerate(edit["cuts"]) if c["beat"] == bi]
        diff = round((b["end"] - b["start"]) * fps) - sum(n[i] for i in idx)
        longest = max(idx, key=lambda i: n[i])
        n[longest] += diff
    return n


def render_cut(cut, out, w, h, fps, frames):
    if cut["clip"] is None:
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s={w}x{h}:r={fps}", "-frames:v", str(frames),
             "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)])
        return
    sp = cut.get("speed", 1.0)
    vf = (f"setpts=PTS/{sp},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps},"
          f"setsar=1,format=yuv420p")
    if cut.get("dim"):
        vf += f",eq=brightness=-{cut['dim'] * 0.35:.2f}:saturation=1.1"
    run(["ffmpeg", "-y", "-ss", str(cut.get("ss", 0)), "-t", f"{(frames / fps) * sp + 0.2:.3f}", "-i", str(CLIPS / cut["clip"]),
         "-an", "-vf", vf, "-frames:v", str(frames), "-c:v", "libx264", "-crf", "14", "-preset", "fast", str(out)])


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def text_filters(edit, w, h):
    pal = {k: v.replace("0x", "#") for k, v in edit["palette"].items()}
    pal["white"] = "#FFFFFF"
    fs = []
    for item in edit["text"]:
        base = item["size"] * h
        n = len(item["lines"])
        color = pal.get(item.get("color", "white"), "#FFFFFF")
        for i, line in enumerate(item["lines"]):
            if item["pos"] == "bottom":
                y = f"h*0.86-{(n - i) * 1.02}*{base:.1f}+{base:.1f}*0.2"
            elif item["pos"] == "center":
                y = f"(h-text_h)/2"
            elif item["pos"] in ("left", "right"):
                y = f"h*0.5-{n * 0.55 * base:.1f}+{i * 1.05 * base:.1f}"
            elif item["pos"] == "upper":
                y = f"h*0.30"
            else:  # lower
                y = f"h*0.62"
            x = {"left": "w*0.05", "right": "w*0.65"}.get(item["pos"], "(w-text_w)/2")
            t0, t1 = item["t0"], item["t1"]
            # punch-in: 125% -> 100% over 0.22s, then fade out over the last 0.15s
            size = f"{base:.1f}*(1+0.25*max(0\\,1-(t-{t0})/0.22))"
            alpha = f"min(1\\,min((t-{t0})/0.08\\,({t1}-t)/0.15))"
            fs.append(
                f"drawtext=fontfile='{FONT}':text='{esc(line)}':fontsize='{size}':fontcolor='{color}':"
                f"alpha='{alpha}':x='{x}':y='{y}':shadowcolor=black@0.55:shadowx=3:shadowy=3:"
                f"enable='between(t,{t0},{t1})'")
    return ",".join(fs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--audio")
    ap.add_argument("--no-text", action="store_true")
    a = ap.parse_args()
    edit = json.loads((ROOT / "shots/hifi-teaser.edit.json").read_text())
    w, h, fps = edit["ratio_16x9"]["w"], edit["ratio_16x9"]["h"], edit["fps"]
    tmp = Path(tempfile.mkdtemp())
    parts = []
    counts = frame_counts(edit, fps)
    for i, cut in enumerate(edit["cuts"]):
        p = tmp / f"c{i:02d}.mp4"
        render_cut(cut, p, w, h, fps, counts[i])
        parts.append(p)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = tmp / "joined.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)])
    vf = "null" if a.no_text else text_filters(edit, w, h)
    for f in edit.get("flash", []):
        vf += f",drawbox=x=0:y=0:w=iw:h=ih:color=white@0.85:t=fill:enable='between(t,{f['t0']},{f['t1']})'"
    vf += ",fade=t=in:st=0:d=0.06"
    cmd = ["ffmpeg", "-y", "-i", str(joined)]
    if a.audio:
        cmd += ["-i", a.audio]
    cmd += ["-vf", vf, "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-r", str(fps)]
    if a.audio:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", "20", "-shortest"]
    else:
        cmd += ["-an", "-t", "20"]
    cmd += [a.out]
    subprocess.run(cmd, check=True)
    total = sum(counts) / fps
    print(f"cuts={len(parts)} total={total:.2f}s -> {a.out}")


if __name__ == "__main__":
    main()

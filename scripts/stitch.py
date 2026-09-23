#!/usr/bin/env python3
"""Stitch Weave-generated clips into a final video, ordered by a shot list.

Usage:
    python3 scripts/stitch.py shots/my-scene.shot-list.json --out output/my-scene.mp4

Reads clips from clips/<shot-id>.mp4 (override with --clips-dir). Each shot
entry is trimmed from its optional start_s (default 0) for duration_s, then
normalized to a common resolution/fps (raw Weave outputs vary in size) before
joining — the same source clip's id can appear in multiple shot entries with
different start_s/duration_s to reuse different moments of one clip as
separate cuts. Shots whose transition_in is "cut" (the default) are joined
with a hard cut; if any shot uses "crossfade" or "fade_from_black", the whole
timeline is re-encoded with ffmpeg's xfade/fade filters instead of the fast
concat demuxer.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_CROSSFADE_S = 0.5
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920
TARGET_FPS = 25
PUNCH_IN_RATE = 0.0025
PUNCH_IN_MAX = 1.08


def load_shots(shot_list_path: Path) -> list[dict]:
    data = json.loads(shot_list_path.read_text())
    shots = sorted(data["shots"], key=lambda s: s["order"])
    return shots


def resolve_clip_paths(shots: list[dict], clips_dir: Path) -> list[Path]:
    paths = []
    missing = []
    for shot in shots:
        p = clips_dir / f"{shot['id']}.mp4"
        if not p.exists():
            missing.append(str(p))
        paths.append(p)
    if missing:
        sys.exit("Missing clips:\n  " + "\n  ".join(missing))
    return paths


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def normalize_and_trim(shots: list[dict], clip_paths: list[Path], tmp_dir: Path, punch_in: bool = False) -> list[Path]:
    out_paths = []
    for i, (shot, src) in enumerate(zip(shots, clip_paths)):
        dst = tmp_dir / f"{i:03d}-{shot['id']}.mp4"
        start_s = shot.get("start_s", 0)
        zoom = shot.get("zoom", 1.0)
        focus_y = shot.get("focus_y", 0.5)  # 0 = crop toward top of frame, 1 = toward bottom
        # "increase"+crop fills the frame (no letterbox bars) so a punched-in
        # zoom variant of the same clip reads as a distinct tighter framing,
        # not a repeat of the wide pass.
        vf = (
            f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={TARGET_WIDTH}:{TARGET_HEIGHT},fps={TARGET_FPS}"
        )
        zoom_to = shot.get("zoom_to")
        if zoom_to is not None:
            # Explicit eased zoom move (ease-out cubic) from zoom -> zoom_to,
            # like a hand doing a smooth pinch gesture rather than a constant
            # linear crawl.
            focus_y_to = shot.get("focus_y_to", focus_y)
            frames = max(round(shot["duration_s"] * TARGET_FPS), 1)
            fm1 = max(frames - 1, 1)
            ease = f"(1-pow(1-min(on/{fm1},1),3))"
            z_expr = f"{zoom}+({zoom_to}-{zoom})*{ease}"
            fy_expr = f"({focus_y}+({focus_y_to}-{focus_y})*{ease})"
            vf += (
                f",zoompan=z='{z_expr}':d=1"
                f":x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*{fy_expr}':s={TARGET_WIDTH}x{TARGET_HEIGHT}"
            )
        elif punch_in:
            # Slow constant zoom-in from this shot's base zoom level, so held/
            # near-static shots still carry motion energy.
            zoom_max = zoom * PUNCH_IN_MAX
            vf += (
                f",zoompan=z='if(eq(on,0),{zoom},min(zoom+{PUNCH_IN_RATE},{zoom_max}))':d=1"
                f":x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*{focus_y}':s={TARGET_WIDTH}x{TARGET_HEIGHT}"
            )
        cmd = ["ffmpeg", "-y"]
        if start_s:
            cmd += ["-ss", str(start_s)]
        cmd += ["-i", str(src), "-t", str(shot["duration_s"]),
                "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(dst)]
        subprocess.run(cmd, check=True)
        out_paths.append(dst)
    return out_paths


def simple_concat(clip_paths: list[Path], out_path: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve()}'\n")
        list_file = f.name
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
             "-c", "copy", str(out_path)],
            check=True,
        )
    finally:
        Path(list_file).unlink(missing_ok=True)


def crossfade_concat(shots: list[dict], clip_paths: list[Path], out_path: Path) -> None:
    durations = [probe_duration(p) for p in clip_paths]
    inputs = []
    for p in clip_paths:
        inputs += ["-i", str(p)]

    filters = []
    v_label = "0:v"
    offset = durations[0]
    for i in range(1, len(clip_paths)):
        shot = shots[i]
        fade = DEFAULT_CROSSFADE_S if shot.get("transition_in") == "crossfade" else 0
        offset -= fade
        next_v = f"v{i}"
        filters.append(
            f"[{v_label}][{i}:v]xfade=transition=fade:duration={fade}:offset={offset}[{next_v}]"
        )
        v_label = next_v
        offset += durations[i]

    filter_complex = ";".join(filters)
    subprocess.run(
        ["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex,
         "-map", f"[{v_label}]", str(out_path)],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shot_list", type=Path)
    parser.add_argument("--clips-dir", type=Path, default=Path("clips"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--punch-in", action="store_true",
                         help="Add a slow constant zoom-in to every clip for extra motion energy.")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    shots = load_shots(args.shot_list)
    clip_paths = resolve_clip_paths(shots, args.clips_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        normalized = normalize_and_trim(shots, clip_paths, Path(tmp), punch_in=args.punch_in)

        needs_crossfade = any(s.get("transition_in") in ("crossfade", "fade_from_black") for s in shots[1:])
        if needs_crossfade:
            crossfade_concat(shots, normalized, args.out)
        else:
            simple_concat(normalized, args.out)

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

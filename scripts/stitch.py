#!/usr/bin/env python3
"""Stitch Weave-generated clips into a final video, ordered by a shot list.

Usage:
    python3 scripts/stitch.py shots/my-scene.shot-list.json --out output/my-scene.mp4

Reads clips from clips/<shot-id>.mp4 (override with --clips-dir). Each clip is
trimmed to its shot's duration_s and normalized to a common resolution/fps
(raw Weave outputs vary in size) before joining. Shots whose transition_in is
"cut" (the default) are joined with a hard cut; if any shot uses "crossfade"
or "fade_from_black", the whole timeline is re-encoded with ffmpeg's
xfade/fade filters instead of the fast concat demuxer.
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


def normalize_and_trim(shots: list[dict], clip_paths: list[Path], tmp_dir: Path) -> list[Path]:
    vf = (
        f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={TARGET_WIDTH}:{TARGET_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={TARGET_FPS}"
    )
    out_paths = []
    for shot, src in zip(shots, clip_paths):
        dst = tmp_dir / f"{shot['id']}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(src), "-t", str(shot["duration_s"]),
             "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(dst)],
            check=True,
        )
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
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    shots = load_shots(args.shot_list)
    clip_paths = resolve_clip_paths(shots, args.clips_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        normalized = normalize_and_trim(shots, clip_paths, Path(tmp))

        needs_crossfade = any(s.get("transition_in") in ("crossfade", "fade_from_black") for s in shots[1:])
        if needs_crossfade:
            crossfade_concat(shots, normalized, args.out)
        else:
            simple_concat(normalized, args.out)

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

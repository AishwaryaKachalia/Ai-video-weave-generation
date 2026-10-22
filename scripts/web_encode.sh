#!/usr/bin/env bash
# Re-encode a clip to a lightweight, widely playable MP4 (H.264 High/4.1, yuv420p, AAC, faststart).
# Usage: scripts/web_encode.sh in.mp4 out.mp4 [16x9|9x16]
set -euo pipefail
in="$1"; out="$2"; ratio="${3:-16x9}"
if [ "$ratio" = "9x16" ]; then vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"; else vf="scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"; fi
ffmpeg -v error -y -i "$in" -vf "$vf,format=yuv420p" -r 24 -c:v libx264 -profile:v high -level 4.1 -crf 20 -preset medium -movflags +faststart -c:a aac -b:a 128k -ar 44100 -ac 2 "$out"

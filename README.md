# AI Video Weave Generation

A 3-stage pipeline for turning a reference image into a generated video, using
Figma Weave for clip generation.

## Pipeline

1. **Look & Product** (`config/look-bible.md`)
   Define the visual style and product before generating anything: tone, color,
   camera language, product details, constraints. This is the shared context
   every later prompt is written against.

2. **Frame-by-Frame Analysis** (`shots/*.json`)
   Given a reference image (or video), break it into a shot list — one entry
   per clip to generate. Each shot captures what's in frame, camera motion,
   duration, and the prompt to send to Weave. Schema: `schema/shot-list.schema.json`.

3. **Generate + Edit**
   - Generate: run each shot through Figma Weave (via the Figma MCP tools —
     `weave_find_model` / `weave_run_model` or `weave_list_tools` /
     `weave_run_tool`) and save outputs into `clips/<shot-id>.mp4`.
   - Edit: stitch the clips into the final cut with `scripts/stitch.py`, which
     reads `shots/*.json` for ordering/timing and concatenates via ffmpeg.

## Layout

```
config/    look-bible.md          — stage 1 output (style + product spec)
shots/     <name>.shot-list.json  — stage 2 output (per-clip breakdown)
clips/     <shot-id>.mp4          — stage 3 output (raw Weave generations, gitignored)
output/    <name>.mp4             — stage 4 output (final stitched video, gitignored)
schema/    shot-list.schema.json  — shot list format
scripts/   stitch.py              — clip concatenation/assembly
```

## Usage

```bash
# 1. Fill out config/look-bible.md by hand or in conversation with Claude.

# 2. Produce a shot list from a reference image (done in a Claude Code session,
#    validated against schema/shot-list.schema.json):
shots/my-scene.shot-list.json

# 3. Generate each shot's clip via Figma Weave MCP tools, saving to
#    clips/<shot-id>.mp4 (shot-id matches the shot list).

# 4. Stitch the final video:
python3 scripts/stitch.py shots/my-scene.shot-list.json --out output/my-scene.mp4
```

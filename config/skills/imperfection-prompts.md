# Skill: imperfection-first prompting (HIFI)

Load before writing ANY still or video prompt. Goal: kill the "too clean" AI look.

## Rules
1. No tech-jargon quality words. Banned: photorealistic, 4k, 8k, ultra-detailed, cinematic, masterpiece, hyperreal, sharp focus, HDR.
2. Every prompt = scene + light source & direction + 3 flaws (one each from SURFACE, AIR, HUMAN) + 1 camera flaw. Describe what is physically there, in tactile words.
3. Flaws must be specific and local ("scuff on the left sneaker toe"), never generic ("imperfect").
4. Faces stay stable: imperfection goes in skin/hair/clothes/environment, never in motion of faces. Keep face-safe video rules from the look bible.
5. Rotate flaws between shots so no two shots share the same set.
6. Can accuracy and look bible rules still win over any flaw. Never alter the can artwork.

## Banks
SURFACE: micro-scratches on glass, fingerprints smudged on a can, condensation beading unevenly, creased leather showing years of use, frayed hem, scuffed sneaker toe, chipped nail polish, sweat-darkened collar, wrinkled cotton, peeling sticker residue, rain-spotted metal, dust on a dark jacket.
AIR: airborne dust drifting through light shafts, cigarette-free haze from a smoke machine, warm street dust, faint steam, tiny moths around a bulb, powder colour hanging in the air.
HUMAN: flyaway hairs catching backlight, uneven skin with pores and a small shine on the forehead, one person mid-blink, laugh lines, a crooked smile, slightly mismatched jewellery, tired eyes after a long night, a stray bindi sticker, a shirt tag sticking out.
LIGHT: late afternoon light bleeding from upper left, mixed warm tungsten and cool phone glow, one blown-out window, light spilling unevenly across half a face, shadows gone muddy brown instead of black.
CAMERA: handheld drift, soft focus slipping off the nearest face, a thumb-smudge halo on the lens, film grain heavier in the shadows, slight light leak on one edge, horizon not quite level, motion smear on the fastest hand.

## Node chain (Weave)
Base still (Nano Banana, flaws-first prompt) -> image-to-video engines in parallel with the SAME frame and the SAME motion prompt:
- Kling 3 (complex physical movement)
- Seedance 2.5 and Luma Ray 3.2 (skin, light, texture realism)
- Runway Gen-3 Turbo only for the movement test
Pick the winner per shot by looking at skin, light and texture on a frame-zoom, not the whole clip.
Add a final film pass in code (`scripts/film_post.py`): grain, gate weave, halation, slight chroma wobble.

## Build prompts
Single: `python3 scripts/imperfect_prompt.py "<scene>" --seed 3`
Batch: `python3 scripts/imperfect_prompt.py --batch scenes.txt --out prompts.json` (one scene per line; every scene gets a different flaw set).

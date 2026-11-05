# Skill: HIFI prompt craft (stills + video)

Load before writing ANY still or video prompt. Built from published guides (Glif Kling 3, Luma field guide, Seedance guides, Nano Banana realism guides) plus our own failures. Most guides are third-party, so treat them as starting points and judge by looking at frames.

## Core principle
AI looks too clean when the prompt names quality ("4k, photorealistic, cinematic") instead of physical things. Describe the real light source, what is worn/scuffed/damp, what the air holds, and how a person with a camera would shoot it badly. One flowing description, not a keyword list.

## Universal rules
1. Banned words: photorealistic, 4k/8k, ultra-detailed, masterpiece, hyperreal, sharp focus, HDR, "looks realistic", "dramatic lighting".
2. Name real light: direction + softness + source ("tungsten bulbs strung overhead, spill from camera left"), not "moody".
3. Tactile detail: condensation, sweat sheen, fabric weave, creased leather, dust, steam, powder in air.
4. Camera as a person: handheld drift, soft focus slipping, thumb-smudge halo, light leak, grain heavier in shadows. Lens/film words describe a look, they do not prove realism.
5. Specific beats vague: "bangles swing, dupatta lifts" not "moves"; "late sun from upper left" not "nice light".
6. Skin: ask for natural skin variation, pores, small forehead shine, flyaway hair. Never "smooth/perfect/flawless". Avoid beauty-filter and over-sharpening.
7. Prompt length: 1-3 flowing sentences for video; more length rarely helps, more specificity does.
8. Never re-describe the still in video prompts; describe only motion, camera and secondary motion.
9. Rotate flaws between shots; no two shots share a set.
10. Look bible wins: can artwork never altered, no cans in public, faces facing correct way, Mumbai/Gen Z rules.

## Stills (Nano Banana)
Format: [shot type + framing + viewpoint] of [who, doing what, expression] in [specific place]. [Light: direction, source, softness]. [3 flaws: surface, air, human]. [camera flaw]. Set aspect ratio in the param AND prompt. End with "No visible text except on the can, no border". For product: state exact can artwork from the look bible. Check after: light direction consistent, hands/teeth/eyes, can text, dead-straight horizon, skin too smooth.

## Video, general (all engines)
Structure: CAMERA (specific move) + SUBJECT motion (action verbs with body part) + ENVIRONMENT secondary motion (hair, fabric, dust, smoke, reflections) + LIGHT behaviour + PACING word (slow, lingering). Describe the shot's evolution beginning to end or it freezes. Negative prompts help Kling/Runway slightly; Luma Ray is positive-only: do not use negatives there.
Face safety (our rule): tight crops, few large faces, calm motion, "faces stay stable, no hand crossing faces, no new people", no zoom/flare/brightness change. Trim after ~2.5s.

## Per engine
- **Kling 3 / 3 Turbo**: one flowing 1-3 sentence shot; open with camera setup; motion terms: handheld drift, shoulder-cam sway, dolly push-in, slow tracking, rack focus, locked-off; name real light sources and exact colours; add tactile detail; film stock words (35mm warm grain) shift the whole look; avoid "moves/goes" and still-image prompts. Elements = face consistency. Best for complex physical movement.
- **Seedance 2.5 / 2.0**: write a clear creative brief: subject, scene, action, lighting, camera language, style, constraints (e.g. "realistic skin texture, no facial distortion"). Use concrete camera vocabulary, never "cinematic camera". For >8s split into timed segments. May block identifiable real faces on references; AI faces from our stills usually pass. Strong on texture and audio; costliest.
- **Luma Ray 3.2**: [Subject] + [Location] + [Vibe] + [Camera & movement] + [Lighting] + [Style/era]. Positive-only. Describe secondary consequences: wind in hair, fabric, dust kicked up, reflections. Image-to-video keeps the still's look, so spend words on motion. Cheap, good realism check.
- **Runway Gen-3 Turbo**: deprecated in Weave; skip.

## Banks
SURFACE: micro-scratches on glass, fingerprints smudged on a can, condensation beading unevenly, creased leather showing years of use, frayed hem, scuffed sneaker toe, chipped nail polish, sweat-darkened collar, wrinkled cotton, peeling sticker residue, rain-spotted metal, dust on a dark jacket.
AIR: airborne dust drifting through light shafts, cigarette-free haze from a smoke machine, warm street dust, faint steam, tiny moths around a bulb, powder colour hanging in the air.
HUMAN: flyaway hairs catching backlight, uneven skin with pores and a small shine on the forehead, one person mid-blink, laugh lines, a crooked smile, slightly mismatched jewellery, tired eyes after a long night, a stray bindi sticker, a shirt tag sticking out.
LIGHT: late afternoon light bleeding from upper left, mixed warm tungsten and cool phone glow, one blown-out window, light spilling unevenly across half a face, shadows gone muddy brown instead of black.
CAMERA: handheld drift, soft focus slipping off the nearest face, a thumb-smudge halo on the lens, film grain heavier in the shadows, slight light leak on one edge, horizon not quite level, motion smear on the fastest hand.

## Node chain (Weave)
Base still (Nano Banana, flaws-first) -> same frame + same motion prompt into Kling 3 (physical motion) and Luma Ray 3.2 / Seedance 2.5 (skin, light, texture). Pick the winner per shot from a frame-zoom on skin, light and texture, not the whole clip. Run the final film pass in code (`scripts/film_post.py`): grain, gate weave, halation.
Spend rule: quote cost, get explicit approval, then run. Never generate while the user is still shaping the skill/plan.

## Build prompts
Single: `python3 scripts/imperfect_prompt.py "<scene>" --seed 3`
Batch: `python3 scripts/imperfect_prompt.py --batch scenes.txt --out prompts.json` (one scene per line; every scene gets a different flaw set).
The script only adds flaws; still write camera/motion lines by hand per the engine rules above.

## Sources
Glif Kling 3 guide, Luma Video Models Field Guide, Luma "How to prompt Seedance 2.0", VEED/Artlist/localbanana Nano Banana realism guides.

## Can realism (HARD RULE, from user feedback)
A can must look photographed, not pasted on. Always: (1) cast its shadow in the SAME direction, length and softness as the other objects in the scene; (2) put highlights where other glass/brass objects catch light and add one hot-spot from the scene's actual light source (flash, window, diyas); (3) make it behave like metal: stretched vertical reflections of the surroundings, a bright specular band down the curve, darker far edge, shiny rim and tab reflecting the room, label ink slightly glossy not glowing; (4) ground it with a contact shadow and a wet ring; (5) match grain, softness for its depth and colour cast of the rest of the photo. Never pass the can as a flat layer; if a can looks fake, edit only the cans and say which light direction to follow.

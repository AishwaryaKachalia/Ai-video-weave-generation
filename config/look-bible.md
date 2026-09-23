# Look & Product Bible

Fill this out before generating any shots. Every Weave prompt should be
writable by pulling directly from this doc.

## Product catalog

Two SKUs, each in multiple colorways — see `products/<sku>/`. Pick one
SKU/colorway per generation and only reference that folder's images.

### Flap Trouser (`products/flap-trouser/`)
- **What is it**: Wide-leg trousers, high-waisted, with a draped flap panel on the FRONT of BOTH legs (symmetric, not asymmetric/single-leg) and a completely PLAIN waistband — no belt loops, no monogram, no tag/logo of any kind, anywhere on the waistband. Do not include any branding on the waistband in any prompt — every attempt to include it (even just a small tab) has been misrendered as a belt loop. Plain fabric only.
- **Colorways**: `black.png` (pinstripe charcoal — primary), `blue.png`, `grey.png`. Real-world reference: `black-realworld.jpg`.
- **GARMENT MECHANICS — FINAL, confirmed correct by user, read carefully before every generation**:
  - There are two triangular panels, one on each leg.
  - **Two edges are fixed and stitched, zero movement, ever**: the top edge is stitched to the waistband; the OUTER edge is stitched flush along the leg's true side seam, from waistband to hem. This outer edge must NEVER deviate from the leg's natural straight silhouette line — the leg's outline against the background/other leg stays completely smooth and straight at all times, as if the panel were fused to the leg. It must NOT poke, flare, or stick out past the leg's true silhouette, at rest or in motion.
  - **One edge is free, with only a little movement**: the inner diagonal edge (running from near the waistband down to a point) is the only unstitched part. It reads as a diagonal fold/seam line on the surface of the leg, not as a separate edge that opens away from the leg. Only very subtle movement here, never billowing.
  - **Only visible from the front.** The back view (`grey.png` top-right panel) is completely flat pinstripe with no flap, drape, or panel of any kind. Any shot where her back is to camera (walking away, etc.) must show plain flat trousers — no flap.
  - Confirmed-correct reference still: `shots/frames/flap-trouser-grey/platform-stand.png` — use this as a visual anchor alongside `products/flap-trouser/grey.png` when generating any shot that shows the flap.
- **Key features to showcase**: the front drape panel (both legs), the pinstripe texture (black colorway), wide-leg silhouette.
- **What must never be wrong**: exact pattern/colorway, the flap panel shape and its stitched-down construction, the completely plain waistband (NO belt loops, NO monogram/tag/logo anywhere on it), zip fly hardware, the plain/flat back view. Must render pixel-faithful to the supplied photos — no redesigning the garment.

### Wrap Trouser (`products/wrap-trouser/`)
- **What is it**: Cropped wide-leg trousers with a front arched wrap panel overlay, button waistband detail, elastic back waist, side vents at the hem.
- **Colorways**: `beige.png`, `black.png`, `olive.png`.
- **Key features to showcase**: the arched wrap panel, button waistband detail, cropped wide-leg silhouette, side hem vents.
- **What must never be wrong**: exact wrap panel shape and stitching, button placement, colorway, cropped hem/vent construction. Must render pixel-faithful to the supplied photos — no redesigning the garment.

## Look

### Campaign: SoBo Wrap Trouser (Wrap Trouser, beige)

- **Reference**: `reference/wrap-trouser-beige-sobo-reference.mp4` — 13.3s street-style reel, 4 posed segments joined by whip-pan taxi wipes (see `shots/wrap-trouser-beige-sobo.reference-breakdown.md`).
- **Visual style**: bright sunlit candid street-style content — the opposite of the moody-urban look below. High-key natural daylight, saturated (not desaturated) color, minimal grain, crisp/clean editorial-casual "influencer" feel. Mostly static or gently handheld full-body/medium compositions; no walking-motion-blur shots.
- **Location**: South Bombay (SoBo) — colonial-era stone architecture (arches, columns, wrought-iron lamps), tree-lined streets, generic heritage-building street corners. Avoid naming or showing specific identifiable landmarks/signage; keep it a generic composite SoBo street.
- **Transition device**: between each of the 4 posed segments, a fast-moving **kaali peeli taxi** (black-and-yellow Mumbai taxi, Premier Padmini-style) whips through frame close to camera, fully motion-blurred, as a wipe transition — replaces the reference's yellow NYC cab wipe. Each wipe is its own short full-frame insert shot (~0.5s), not a crossfade.
- **Model**: same Indian model constraint as below — consistent face/hair across all 4 segments (single continuous "character", not an outfit-change reel — she wears the Wrap Trouser beige throughout; only pose/backdrop/top styling shifts between segments).
- **Duration / aspect ratio**: 9:16 vertical, ~13-14s total (match reference), Instagram Reel.

### Campaign: Flap Trouser street-fashion film (moody urban editorial)

- **Reference**: `05999f36-instappa-post-DVi7d97jdVL.mp4` — 23s fashion/streetwear reel, 13 shots (see `shots/reference-breakdown.md`).
- **Visual style**: moody urban editorial street-fashion film. Handheld/gimbal energy, shallow depth of field, quick cuts, macro detail inserts mixed with full-body movement shots.
- **Color palette**: desaturated teal-green shadows, warm/golden skin tones, muted urban backdrop (concrete, glass, foliage).
- **Lighting**: natural daylight exterior (soft overcast to golden hour), practical/interior light for train and reflection shots, warm highlights on skin against cooler ambient.
- **Camera language**: mix of extreme close-up macro (eyes, feet, product texture), medium walking shots with slight motion blur, and wide environmental shots (billboards, train platform). Frequent shallow-focus foreground/background falloff.
- **Texture/material notes**: film-grain-ish, slightly soft/glowy highlights, not clinical-sharp — an editorial, lived-in city texture.

## Constraints (all campaigns)

- **Platform**: Instagram Reel, 9:16 vertical. Duration per-campaign (see each Look subsection above).
- **Model**: Indian model, styled to match the given reference's cast look.
- **Things to avoid**: any alteration to a garment's cut, pattern, drape, or branding; over-sharpened/clinical CGI look; mismatched lighting between shots; harsh contrast/crushed blacks; culturally on-the-nose backdrops (Bollywood-style movie posters, heavy Hindi/Marathi text hoardings, named/identifiable landmarks) — keep backdrops neutral/generic Indian urban (generic architecture/texture), not a caricature.

## Video/motion notes

- **Pace**: match each shot's actual motion from its reference — real-time human motion, never an unintended slow-motion look unless the reference shot itself is a held/static beat. Saying "not slow motion" alone has not been enough — every motion prompt must give a concrete fast timeframe (e.g. "the head turn completes in under 1 second, a quick snap reaction" / "the smile forms in half a second, immediate not gradual") so the model doesn't stretch a small action across the full clip length.

### Flap Trouser campaign (moody urban editorial)
- **Grade**: soft natural contrast, no harsh sharp lines or crushed blacks — gentler tonal falloff than a typical AI-render default.
- **Backgrounds**: neutral urban Indian streetscape — worn architecture and generic signage are fine, but avoid movie-poster billboards or dense identifiable text as a focal background element.

### SoBo Wrap Trouser campaign
- **Grade**: bright, high-key, saturated color — clean daylight-editorial, not moody/desaturated.
- **Backgrounds**: generic South Bombay colonial-heritage streetscape (stone arches, columns, wrought-iron lamps, tree-lined) — no named landmarks or identifiable signage.
- **Taxi wipes**: each wipe clip is a fast-moving black-and-yellow "kaali peeli" Mumbai taxi passing very close to camera, filling/streaking across the frame, heavily motion-blurred, ~0.5s. Same taxi styling every time (consistency anchor).

## Consistency anchors

Short phrases to repeat across every shot prompt so clips feel like one video.

**Flap Trouser campaign:**
- "Indian model, moody urban editorial street-fashion film"
- "desaturated teal shadows, warm skin tones, shallow depth of field"
- "wearing [exact product from products/<sku>/<colorway>.png] — garment unchanged from reference"
- "flap panel hinged at waistband/inner seam, subtle natural sway only, not visible from behind — waistband completely plain fabric, no belt loops, no monogram, no tag or logo of any kind"
- "handheld gimbal energy, soft natural daylight"

**SoBo Wrap Trouser campaign:**
- "Indian model, bright sunlit candid street-style content, South Bombay colonial-heritage backdrop"
- "wearing the Wrap Trouser, beige colorway, from products/wrap-trouser/beige.png — arched wrap panel, button waistband, cropped wide-leg — garment unchanged from reference"
- "same face/hair/styling as the previous segment — one continuous model across the whole video"
- "high-key natural daylight, saturated color, clean crisp editorial-casual look, minimal grain"
- (taxi-wipe shots only) "black-and-yellow kaali peeli Mumbai taxi whipping past camera, full-frame motion blur, no model, no text/signage legible"

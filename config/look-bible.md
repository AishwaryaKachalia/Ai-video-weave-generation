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

- **Reference**: `05999f36-instappa-post-DVi7d97jdVL.mp4` — 23s fashion/streetwear reel, 13 shots (see `shots/reference-breakdown.md`).
- **Visual style**: moody urban editorial street-fashion film. Handheld/gimbal energy, shallow depth of field, quick cuts, macro detail inserts mixed with full-body movement shots.
- **Color palette**: desaturated teal-green shadows, warm/golden skin tones, muted urban backdrop (concrete, glass, foliage).
- **Lighting**: natural daylight exterior (soft overcast to golden hour), practical/interior light for train and reflection shots, warm highlights on skin against cooler ambient.
- **Camera language**: mix of extreme close-up macro (eyes, feet, product texture), medium walking shots with slight motion blur, and wide environmental shots (billboards, train platform). Frequent shallow-focus foreground/background falloff.
- **Texture/material notes**: film-grain-ish, slightly soft/glowy highlights, not clinical-sharp — an editorial, lived-in city texture.

## Constraints

- **Duration / aspect ratio**: 9:16 vertical, ~20-25s total (match reference).
- **Platform**: Instagram Reel.
- **Model**: Indian model, styled to match the reference's editorial street-cast look.
- **Things to avoid**: any alteration to the trousers' cut, pattern, drape, or branding; over-sharpened/clinical CGI look; mismatched lighting between shots; harsh contrast/crushed blacks; culturally on-the-nose backdrops (Bollywood-style movie posters, heavy Hindi/Marathi text hoardings) — keep backdrops neutral urban Indian (generic architecture/texture), not a caricature.

## Video/motion notes

- **Grade**: soft natural contrast, no harsh sharp lines or crushed blacks — gentler tonal falloff than a typical AI-render default.
- **Pace**: match each shot's actual motion from the reference (see `shots/reference-breakdown.md` and the per-shot notes below) — real-time human motion, never an unintended slow-motion look unless the reference shot itself is a held/static beat. Saying "not slow motion" alone has not been enough — every motion prompt must give a concrete fast timeframe (e.g. "the head turn completes in under 1 second, a quick snap reaction" / "the smile forms in half a second, immediate not gradual") so the model doesn't stretch a small action across the full clip length.
- **Backgrounds**: neutral urban Indian streetscape — worn architecture and generic signage are fine, but avoid movie-poster billboards or dense identifiable text as a focal background element.

## Alternate look: Still-Life Product Flat-Lay

A separate look from the fashion-film reference above, used for standalone
product/detail hero stills (not part of the main video edit).

- **Reference**: `style-refs/flatlay-tray-glove-ref.webp` — a knit glove folded on
  an oval brushed-pewter tray, near-black warm-brown backdrop, gold jewelry
  props (ring, antique key) resting on/beside the garment, soft single-source
  top light with a gentle falloff shadow, close overhead/45° framing.
- **Visual style**: minimal, moody studio still-life. Warm near-black backdrop,
  one muted-metal prop surface (tray), one or two small gold jewelry props for
  scale/luxury cues. No model, no environment — garment is the only subject.
- **Lighting**: single soft diffused top-left light source, soft shadow falloff
  to the right, no harsh specular highlights, warm neutral color temperature.
- **Camera**: static overhead or steep 45° angle, macro-to-medium framing,
  shallow depth of field so the tray edge and backdrop soften slightly.
- **Consistency anchors for this look**:
  - "minimal moody studio still-life, warm near-black backdrop"
  - "oval brushed-pewter tray, soft single top-light with gentle shadow falloff"
  - "one or two small gold jewelry props (ring/antique key) resting on the fabric for scale"
  - "garment is EXACTLY [colorway] from [product photo] — pixel-faithful, unchanged"
  - (Flap Trouser) "plain waistband, no belt loops, no monogram, no tag/logo of any kind"

## Consistency anchors

Short phrases to repeat across every shot prompt so clips feel like one video:

- "Indian model, moody urban editorial street-fashion film"
- "desaturated teal shadows, warm skin tones, shallow depth of field"
- "wearing [exact product from products/<sku>/<colorway>.png] — garment unchanged from reference"
- (Flap Trouser only) "flap panel hinged at waistband/inner seam, subtle natural sway only, not visible from behind — waistband completely plain fabric, no belt loops, no monogram, no tag or logo of any kind"
- "handheld gimbal energy, soft natural daylight"

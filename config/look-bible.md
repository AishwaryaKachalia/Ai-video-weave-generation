# Look & Product Bible

Fill this out before generating any shots. Every Weave prompt should be
writable by pulling directly from this doc.

## Product catalog

Two SKUs, each in multiple colorways — see `products/<sku>/`. Pick one
SKU/colorway per generation and only reference that folder's images.

### Flap Trouser (`products/flap-trouser/`)
- **What is it**: Wide-leg trousers, high-waisted, with a draped flap panel on the FRONT of BOTH legs (symmetric, not asymmetric/single-leg) and a completely PLAIN waistband — no belt loops, no monogram, no tag/logo of any kind, anywhere on the waistband. Do not include any branding on the waistband in any prompt — every attempt to include it (even just a small tab) has been misrendered as a belt loop. Plain fabric only.
- **Colorways**: `black.png` (pinstripe charcoal — primary), `blue.png`, `grey.png`. Real-world reference: `black-realworld.jpg`.
- **GARMENT MECHANICS — critical, verified against the product photo (corrected repeatedly — read carefully)**:
  - **Shape**: the flap is a STRAIGHT-EDGED TRIANGULAR panel — like an actual triangle, tapering to a point near the knee/ankle. Its edges are straight lines, not curves. It must NOT be drawn as a curved, rounded, bell-shaped, or curtain-like drape — video generations keep rendering it as soft curved drapery, which is wrong. Tailored and structured, straight lines only.
  - **Attachment**: fully stitched down at the waistband AND down the entire side seam of the leg — structurally attached, not free-hanging fabric. It stays close and flat against the leg, following the leg's straight lines.
  - **Movement**: because it's attached along the side seam, it has only very minimal, subtle movement with a stride — it must NOT flap, billow, flare outward, curve away from the leg, or separate from the leg silhouette at any point, even walking. Video generations keep letting it swing/billow like loose fabric — it must not.
  - **Only visible from the front.** The back view (`grey.png` top-right panel) is completely flat pinstripe with no flap, drape, or panel of any kind. Any shot where her back is to camera (walking away, etc.) must show plain flat trousers — no flap.
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

## Consistency anchors

Short phrases to repeat across every shot prompt so clips feel like one video:

- "Indian model, moody urban editorial street-fashion film"
- "desaturated teal shadows, warm skin tones, shallow depth of field"
- "wearing [exact product from products/<sku>/<colorway>.png] — garment unchanged from reference"
- (Flap Trouser only) "flap panel hinged at waistband/inner seam, subtle natural sway only, not visible from behind — waistband completely plain fabric, no belt loops, no monogram, no tag or logo of any kind"
- "handheld gimbal energy, soft natural daylight"

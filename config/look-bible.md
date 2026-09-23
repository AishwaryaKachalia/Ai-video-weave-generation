# Look & Product Bible

Fill this out before generating any shots. Every Weave prompt should be
writable by pulling directly from this doc.

## Product catalog

Two SKUs, each in multiple colorways — see `products/<sku>/`. Pick one
SKU/colorway per generation and only reference that folder's images.

### Flap Trouser (`products/flap-trouser/`)
- **What is it**: Wide-leg trousers, high-waisted, with a draped flap panel on the FRONT of BOTH legs (symmetric, not asymmetric/single-leg), belt loops, zip fly, and a small embossed "BB" monogram tab on the waistband.
- **Colorways**: `black.png` (pinstripe charcoal — primary), `blue.png`, `grey.png`. Real-world reference: `black-realworld.jpg`.
- **GARMENT MECHANICS — critical, verified against the product photo**:
  - The flap is fully stitched down: anchored at the waistband (top) AND along the outer side seam of the leg. It is NOT a loose/free-hanging piece of fabric.
  - Because it's captured along the side seam, **it does not move independently of the leg at all** — no flutter, no billow, no swing, no flare, in any shot, walking or static. It reads as a decorative layered/pleated panel, not a flag or cape. Treat it as bonded to the leg fabric.
  - **Only visible from the front.** The back view (`grey.png` top-right panel) is completely flat pinstripe with no flap, drape, or panel of any kind. Any shot where her back is to camera (walking away, etc.) must show plain flat trousers — no flap.
- **Key features to showcase**: the front drape panel (both legs), the pinstripe texture (black colorway), wide-leg silhouette, the branded waistband tab.
- **What must never be wrong**: exact pattern/colorway, the flap panel shape and its stitched-down, non-moving construction, the "BB" monogram tab, waistband/belt-loop construction, zip fly hardware, the plain/flat back view. Must render pixel-faithful to the supplied photos — no redesigning the garment.

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
- **Things to avoid**: any alteration to the trousers' cut, pattern, drape, or branding; over-sharpened/clinical CGI look; mismatched lighting between shots.

## Consistency anchors

Short phrases to repeat across every shot prompt so clips feel like one video:

- "Indian model, moody urban editorial street-fashion film"
- "desaturated teal shadows, warm skin tones, shallow depth of field"
- "wearing [exact product from products/<sku>/<colorway>.png] — garment unchanged from reference"
- (Flap Trouser only) "flap panel stitched down at waistband and side seam, zero independent movement — not visible from behind"
- "handheld gimbal energy, soft natural daylight"

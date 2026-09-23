# Look & Product Bible

Fill this out before generating any shots. Every Weave prompt should be
writable by pulling directly from this doc.

## Product catalog

Two SKUs, each in multiple colorways — see `products/<sku>/`. Pick one
SKU/colorway per generation and only reference that folder's images.

### Flap Trouser (`products/flap-trouser/`)
- **What is it**: Wide-leg trousers, high-waisted, with an asymmetric draped/flap panel over the front left leg, belt loops, zip fly, and a small embossed "BB" monogram tab on the waistband.
- **Colorways**: `black.png` (pinstripe charcoal — primary), `blue.png`, `grey.png`. Real-world reference: `black-realworld.jpg`.
- **Key features to showcase**: the draped asymmetric front panel, the pinstripe texture (black colorway), wide-leg silhouette/drape from the waist down, the branded waistband tab.
- **What must never be wrong**: exact pattern/colorway, the asymmetric drape panel shape, the "BB" monogram tab, waistband/belt-loop construction, zip fly hardware. Must render pixel-faithful to the supplied photos — no redesigning the garment.

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
- "handheld gimbal energy, soft natural daylight"

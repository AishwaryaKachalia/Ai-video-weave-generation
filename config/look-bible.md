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

## Consistency anchors

Short phrases to repeat across every shot prompt so clips feel like one video:

- "Indian model, moody urban editorial street-fashion film"
- "desaturated teal shadows, warm skin tones, shallow depth of field"
- "wearing [exact product from products/<sku>/<colorway>.png] — garment unchanged from reference"
- (Flap Trouser only) "flap panel hinged at waistband/inner seam, subtle natural sway only, not visible from behind — waistband completely plain fabric, no belt loops, no monogram, no tag or logo of any kind"
- "handheld gimbal energy, soft natural daylight"

## Look B — South Bombay Coffee Run (Wrap Trouser Beige)

A second, distinct look used only for the Wrap Trouser Beige colorway —
paparazzi/CCTV street-style rather than Look A's moody handheld editorial.

- **Reference**: `95af09bc-instappa-post-DVwNp5mAHMg.mp4` — 10.68s single
  continuous overhead shot (see `shots/reference-breakdown-wrap-trouser-beige.md`).
  Camera angle/framing must match this reference exactly: fixed top-down
  overhead shot, not an eye-level portrait.
- **Visual style**: realistic candid phone-shot street style — shot-on-iPhone
  texture, natural un-graded color, visible handheld motion and phone-camera
  noise/grain. NOT a polished cinematic AI render: no dramatic golden-hour
  glow, no airbrushed/glossy skin, no artificial warm color cast. Neutral
  daylight white balance, true-to-life color.
- **Setting**: South Bombay Fort/Kala Ghoda heritage streetscape — colonial-era
  stone building facade, arcade of stone arches, columns with carved
  capitals, sandstone/brick tones, parked cars at the curb. Architecture
  inspiration only — no readable signage, text, or brand names anywhere in
  frame (the mood reference includes a real store's signage; omit it).
- **Wardrobe**: brown ruched bandeau-style top (`style-refs/top-brown-ruched-bandeau.png`)
  — sweetheart neckline, thin straps, ruched draped fabric, sleeveless —
  worn with Wrap Trouser Beige (`Wrap Trouser Beige.png`) — exact front wrap
  panel and button waistband shape unchanged, fabric reads as a **flowy
  nylon-blend drape**, not stiff structured cotton — soft movement in the
  wrap panel and hem, slight natural sheen. **No belt** — this garment has no
  belt loops, so nothing sits at the waist. Chic, aesthetic, elevated styling
  (not overly polished/red-carpet, but not plain either). Footwear: **brown
  boots** (ankle or knee-high leather boots, not black). Delicate gold
  jewelry, hair down.
- **Model**: fair-toned Indian skin tone, dark hair, warm brown eyes, defined
  features, gold hoop earrings — face styled in the spirit of
  `style-refs/face-ref-fair-toned.webp` (similar look/coloring/features, not
  a literal copy of that specific person).
- **Props**: a to-go coffee cup in one hand; a brown structured handbag in
  the other is optional (present in the source video — include it only if
  it reads clean in frame; keep bag color coordinated with the boots, not
  black).
- **Lighting/grade**: natural daylight, soft realistic contrast, true color —
  explicitly avoid golden/amber AI-glow grading. Not the teal-shadow grade
  of Look A either.
- **Duration / aspect ratio**: 9:16 vertical, ~10-11s total (match reference).
- **Things to avoid**: any belt or belt loops on the trousers, black boots,
  stiff/structured trouser drape, golden cinematic AI glow, readable
  signage/brand text/logos, movie-poster or dense-text backdrops,
  over-sharpened CGI look.

### Consistency anchors (Look B only)

- "Indian model, fair-toned skin, dark hair, South Bombay street-style, realistic shot-on-iPhone candid photo, not a cinematic AI render"
- "brown ruched bandeau top tucked into Wrap Trouser Beige — exact wrap panel and button waistband shape unchanged, flowy nylon-blend drape, no belt, no belt loops"
- "brown leather boots"
- "black leather flat loafers, not heeled boots"
- "fixed top-down overhead angle, matching the reference video framing exactly"
- "South Bombay Fort/Kala Ghoda heritage stone building, arches and columns, no readable signage or text"
- "natural daylight, true color, no golden/amber AI glow"

# Product Accuracy

The product is the client's asset, so it must look exactly like it does in real life.
If a generated product is wrong, the ad fails, however good the animation is.

## Product spec (fill in for each SKU in the bible)

| Field | Example |
|---|---|
| SKU / name | Glow Serum 30 ml |
| Reference images | front, back, ¾, cap off, logo close-up (IDs/paths) |
| Shape and proportions | cylindrical glass bottle, height ≈ 3× width, dropper cap ≈ 25% of height |
| Size in hand | fits in palm, about the length of an index finger |
| Colours (hex if supplied) | frosted amber glass, matte black cap, white label |
| Materials and finish | frosted glass, matte cap, gloss label |
| Logo and typography | wordmark centred on label, serif, black |
| Label layout | logo top-third, product name below, small text bottom |
| Must never change | logo, label colour, cap colour, bottle shape |
| Allowed stylisation | Rendered in the scene's style (e.g. clay texture) only if the CS approves; otherwise keep it photographic/clean |

## Rules

1. **Never invent packaging details.** If you don't know what the back of the box
   looks like, don't show the back.
2. **Always attach the reference** for any shot where the product is visible, and say
   what it's for in the prompt.
3. **Describe the product with the spec text** as well as attaching the image. Two
   signals hold better than one.
4. **Readable text is the weakest point** for generators. Don't rely on the model to
   render small label copy. Plan for one of:
   - Product shown at a size or angle where the logo shape reads but small text doesn't
     matter.
   - **Composite in the edit**: overlay the real packshot (or a cleaned still) on hero
     moments. This is the most reliable option for the end card.
   - A hero insert shot generated from the real packshot as the first frame, with a
     gentle camera move only (no hand interaction, no rotation that reveals unseen
     sides).
5. **Limit product motion.** Rotating products and hands opening caps produce
   warping. Prefer a static product with a moving camera, or a cut to a hero insert.
6. **The style lock applies to product stylisation too.** In a 2D or clay ad, agree
   with the CS at Gate 1 whether the product is stylised or kept realistic. Mixing
   both is a valid choice, but it has to be deliberate.

## Product QC (every frame where it appears)

- Silhouette and proportions match
- Colours and materials match
- Logo is present, in the right place, and not misspelled or warped
- Label layout is correct (or legibly suppressed)
- Scale relative to hands and body is right
- No extra or invented elements (stickers, extra caps, wrong variants)

**If it fails twice** with the reference attached → stop re-rolling. Flag it to the
user with the fallback you recommend (composite, insert shot, or smaller in frame).
Log it in the bible as a known product risk.

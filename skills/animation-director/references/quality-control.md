# Quality Control

A generation that exists has not passed. Review every still and clip against the
brief before it's approved.

## The 7 checks

| # | Check | Question | Applies to |
|---|---|---|---|
| 1 | Script accuracy | Does it clearly show what this line says, including every literal obligation? | still + clip |
| 2 | Character consistency | Does it match the hero reference: face, hair, outfit, signature identifiers, style? | still + clip (check the last frame too) |
| 3 | Product accuracy | Shape, colours, logo, label, scale. See `product-accuracy.md` | still + clip |
| 4 | Animation quality | Natural motion for the style? No morphing, melting hands, limb pops, flicker or sliding feet? | clip |
| 5 | Visual continuity | Consistent with the ledger (positions, props, state, light) and the neighbouring shots? | still + clip |
| 6 | Technical compliance | 9:16, key content in 4:5 safe zone, resolution, no watermark or stray text, correct length | still + clip |
| 7 | Edit readiness | Usable at its slot: enough handles, clean start and end, reads at the speed it's shown? | clip |

Mark each **PASS / FIX / FAIL** in the bible.
- **PASS**: approved and locked.
- **FIX**: a targeted correction is needed (see below).
- **FAIL**: the concept doesn't work for this shot. Restage it in the storyboard.

## Failure → smallest fix

| Problem | First fix | If it persists |
|---|---|---|
| Face/outfit drift in a still | Image-edit the still with the hero ref attached, naming only the wrong detail | Raise the character's size in frame; simplify the pose |
| Wrong product | Image-edit with the product ref and spec text | Composite / insert-shot fallback, and flag it to the user |
| Extra character or object | Image-edit to remove; add explicit negatives | Re-roll the still with simplified environment |
| Clip adds unwanted actions | Shorten the motion prompt to one verb; add "no other movement" | Lower the duration; make the camera static |
| Character morphs mid-clip | Reduce motion amplitude; static camera | Shorter clip; use an end frame; cut away earlier |
| Hands/fingers broken | Hide or frame out the hands; avoid grip actions | Restage so the hands aren't the focus |
| Clip drifts off-style | Add a style-motion phrase (e.g. "stepped stop-motion feel") | Try the alternate model on that shot only |
| Timing doesn't fit the slot | Trim/speed in the edit | Generate a second camera move on the same still |

Rules:
- Change **one variable per retry** and log it.
- **Two failed attempts on the same fix** → stop, change approach (restage or use a
  fallback) and tell the user if it affects the creative.
- Never regenerate approved shots to fix a neighbour. Adapt the neighbour.

## Approval gates

| Gate | What's approved | Who |
|---|---|---|
| 1 | Style lock, character sheets and hero refs, product reproduction | User / CS |
| 2 | Storyboard, plan (A/B/Hybrid), credit estimate | User / CS |
| 3 | Rough cut / final cut | User / CS |

Between gates, make routine production decisions yourself and report them in a short
summary. Ask for per-shot approval only if the user wants that level of control.

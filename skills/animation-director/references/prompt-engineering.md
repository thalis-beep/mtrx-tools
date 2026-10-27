# Prompt Engineering

Two different prompts per scene, each with a different job:
- **First-frame prompt (image)** describes **one frozen moment** in full: who, where,
  what's visible, the composition, the style.
- **Image-to-video prompt (motion)** describes **only what changes**: one action, a
  camera move, pacing, and what must stay fixed. The image already carries the look,
  so don't re-describe it at length.

## A. First-frame prompt anatomy

Order matters. Put composition and identity first and the quality tail last.

```
1. FORMAT + COMPOSITION  vertical 9:16 frame, [shot size], [angle], [subject placement],
                         all key action inside the central 4:5 safe area, top and bottom
                         of frame are background only
2. STYLE LOCK            [paste STYLE block verbatim]
3. CHARACTER(S)          [paste CHAR_<ID> verbatim] + pose + expression + what they hold
4. PRODUCT               [paste PRODUCT_<SKU> spec text], position, scale, "match reference exactly"
5. ENVIRONMENT           location, set dressing, time of day (from continuity ledger)
6. LIGHTING + PALETTE    key direction, colour temperature, mood
7. CONTINUITY NOTES      state carried from previous shot (props, wardrobe, mess, etc.)
8. REFERENCE ROLES       "reference 1 = character identity; reference 2 = product exact design"
9. NEGATIVES             no text, no watermark, no extra characters, no extra limbs/fingers,
                         no distorted anatomy, no invented logos, [shot-specific]
```

Tips:
- Show the **start pose of the action** in the first frame, not its end. A hand
  reaching toward the bottle animates better than a hand already gripping it.
- Leave **room to move**. If the camera will push in or the character will walk, give
  them space in the frame.
- One focal point per frame.
- Only name colours and props that matter. Unneeded detail invites drift.

## B. Image-to-video prompt anatomy

```
1. ACTION        [subject] [single verb phrase], start → end, e.g. "lifts the bottle from
                 the counter to chest height and smiles"
2. SEQUENCE      if needed, 2 beats max with timing: "first 2 s ..., then ..."
3. EXPRESSION    how the face changes, if at all
4. CAMERA        one move: static / slow push-in / slow pull-out / gentle pan left /
                 orbit 15° / handheld subtle. Include speed.
5. PACING        slow / natural / snappy; overall duration
6. LOCKS         keep character design, outfit, product shape and label unchanged;
                 background stays still; same lighting
7. RESTRICTIONS  no new objects, no new characters, no scene change, no text, no
                 morphing, no camera cuts
```

Rules that keep video models reliable:
- **One primary action per clip.** Models invent extra actions when given several.
- **Concrete verbs**: "turns head left and smiles", not "reacts happily".
- **Name what stays still.** Unmentioned things get animated.
- **Camera and subject motion together should be modest.** A big subject action
  should get a static or slow camera.
- **Avoid**: hands manipulating small objects, opening packaging, writing, eating
  close-ups, fast spins, crowds, characters walking toward camera for many seconds,
  hair or cloth physics when the face matters most.
- **For transformations** (before → after): use a start frame + end frame if the
  model supports it (Kling 3.0 `start_image` + `end_image`). Otherwise cut on a
  motivated beat (flash, whip, product splash) between two clips.
- Keep prompts **short**: 40–90 words for motion. Long motion prompts lose control.

## C. Style modules

Write one STYLE block per production and reuse it verbatim. Starting points to adapt
to the CS references:

| Style | STYLE block starter |
|---|---|
| 2D cartoon | clean 2D cartoon animation style, bold uniform outlines, flat cel colours with one soft shadow tone, simple shapes, expressive faces, limited palette of [colours] |
| 3D stylised (feature-animation feel) | stylised 3D animated film look, appealing exaggerated proportions, soft subsurface skin, rounded forms, soft global illumination, gentle rim light |
| Claymation / stop-motion | handmade claymation, visible fingerprint texture and slight imperfections in clay, miniature practical set, soft tabletop lighting, shallow depth of field |
| Pixel art | crisp [32/64]-bit pixel art, limited palette, no anti-aliasing, clean pixel clusters, side-on or ¾ view |
| Cinematic CGI | photoreal cinematic CGI, physically based materials, filmic contrast, anamorphic depth of field |
| Paper cut-out | layered paper cut-out animation, visible paper grain and cut edges, soft drop shadows between layers |

In video prompts for stop-motion or claymation, add "stepped stop-motion feel, slight
frame-to-frame jitter" so the motion matches the style. For pixel art, add "no smooth
interpolation, sprite-like motion".

Don't use living artists' names or studio names as style shortcuts. Describe the
qualities instead.

## D. Safe-zone clause (paste into every first-frame prompt)

> vertical 9:16 composition; all characters, faces, hands, product and key action kept
> inside the central 4:5 area; top and bottom 15% of frame contain only background

## E. Motion vocabulary that executes reliably

- **Character**: turns head, looks up/down, smiles, frowns, sighs (shoulders drop),
  nods, raises hand, points, lifts object, puts object down, steps forward one step,
  sits down, stands up, waves, jumps (cartoon), blinks.
- **Camera**: static; slow push-in; slow pull-out; gentle pan; slow tilt up/down;
  small orbit (≤30°); subtle handheld.
- **Environment**: lights turn on, leaves sway, steam rises, sparkles appear,
  background colour shifts (good for before/after), particles drift.

## F. Iteration discipline

When a result is wrong, change **one variable** per retry: either the prompt wording,
the reference set, or the seed/model. Note what changed in the bible so the fix can
be repeated.

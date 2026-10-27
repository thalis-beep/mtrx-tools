# Storyboard and Continuity

## Scene fields (all required)

1. Scene # and timestamp (`EST` if estimated)
2. Exact script line or audio section, verbatim
3. Storytelling purpose: one sentence on what the viewer must understand
4. Characters (and which variant) and products
5. Camera: shot size, angle, lens feel, composition, environment
6. Action and emotion, start state → end state
7. First-frame requirements: what must be visible in frame 1
8. Animation instructions: the single action plus the camera move
9. Duration (generated length, and the trimmed length used in the edit)
10. Transition into the next scene

## Shot economy

- **Fewer, stronger shots.** If one shot says it, don't use two.
- One shot = **one clear action**. Two actions means two shots, or one simpler action.
- Generate clips slightly longer than needed (for example 5 s for a 3.5 s slot) so the
  edit has handles. Don't generate 10 s when 5 s will do.
- Reuse when you can. An establishing still can be the first frame of two shots with
  different camera moves, and a reaction shot can be reused if the script repeats.
- Product hero shots can usually be **one strong still plus a subtle camera move**,
  which is cheap and reliable and keeps the product accurate.

## Shot sizes and when to use them

| Size | Use |
|---|---|
| Wide / establishing | New location, scale, the start of a transformation |
| Medium | Character action with a product, two-character interaction |
| Close-up | Emotion, the moment a line lands |
| Extreme close-up / insert | Product details, texture, the moment of use |

Vary shot size between consecutive shots so the cuts feel intentional.

## Continuity rules

Keep a **continuity ledger** in the bible and update it after every approved shot.
Record:
- Where each character is (screen left/right, standing/sitting) and which way they face
- What each character is holding, and in which hand
- Wardrobe state (jacket on/off, hair up/down) and before/after state
- Product state (closed/open, full/used, cap on/off)
- Environment state (time of day, lights on, mess cleaned)
- Actions already completed. Nothing un-happens unless the script says so

Rules:
- **Screen direction**: keep characters on the same side across a conversation
  (180° rule) unless a shot motivates the change.
- **Light and palette**: same key-light direction and colour temperature within a
  location.
- **Match on action**: if shot N ends mid-gesture, shot N+1 begins where that gesture
  ends.
- **Clip end → next first frame**: when two shots must flow continuously, use the
  approved last frame (or a still derived from it) as the reference for the next
  first frame.

## Transitions

| Transition | When |
|---|---|
| Hard cut | Default. Use for most cuts, on the beat or VO phrase |
| Match cut (shape/motion) | Joining two locations or before/after states |
| Whip pan / motion blur | High-energy music sections. Add in the edit, don't generate it |
| Push-in into object → reveal | Moving into the product or a detail |
| Morph / transformation | Only when the script describes a transformation. Use start + end frames if the model supports them |

Prefer transitions done **in the edit** over transitions generated inside a clip.
They're more reliable and cheaper.

## 4:5 safe-zone composition (9:16 frame)

- Keep faces, hands doing the action, product and any key text inside the centred
  1080×1350 area.
- The top 285 px and bottom 285 px should hold only background or extensions of the
  environment, because platform UI (captions, buttons, username) covers them.
- State this in every first-frame prompt (see the prompt-engineering safe-zone clause).

# Worked Example: from a CS script to scene cards

A fictional brand and product, used to show the method end to end. Abridged.

## CS script (input)

> **Brand:** Puffle Hair Mist (fictional) · **Style:** 3D stylised, warm and playful ·
> **Length:** about 15 s · **Audio:** VO (final file to come)
> **Character:** Nora, late 20s, curly hair that goes flat by midday.
> VO:
> 1. "By noon, my curls give up."
> 2. "One spritz of Puffle…"
> 3. "…and they're back. Bouncy all day."
> 4. "Puffle. Curls that keep up."
> Product: 150 ml teal spray bottle, white cap, coral wordmark (refs attached).

## 1. Analysis (excerpt)

- **Concept**: flat curls → one spritz → bounce, with the product as the turning point.
- **Literal obligations**: "noon" (time cue), "curls give up" (flat curls, deflated
  mood), "one spritz" (the spray action), "back / bouncy" (before→after
  transformation), the product name on the end line.
- **Red flags**: a hand pressing the spray nozzle is a hand-plus-product interaction,
  which is risky. Stage it as a mist burst seen from the side with the hand mostly out
  of frame. Label legibility on the end card → composite the real packshot.

### Beat map
| Beat | Time | Audio | Obligations | Emotion | Visual idea |
|---|---|---|---|---|---|
| B1 | 0.0–2.4 EST | "By noon, my curls give up." | noon, flat curls | deflated | Office window with midday sun; Nora's curls sag; she blows a strand off her face |
| B2 | 2.4–4.6 EST | "One spritz of Puffle…" | spray, product | hopeful | Side CU: bottle at hair height, mist burst |
| B3 | 4.6–8.8 EST | "…and they're back. Bouncy all day." | transformation, bounce | delighted | Curls spring up (start/end frames); she shakes her head, curls bounce |
| B4 | 8.8–12.0 EST | "Puffle. Curls that keep up." | product name | confident | Hero: Nora smiles past camera, product foreground (composite end card) |

## 2. Locks (excerpt)

```
STYLE = stylised 3D animated film look, appealing slightly exaggerated proportions, soft
subsurface skin, rounded forms, warm soft global illumination with gentle rim light,
palette of warm cream, teal and coral accents
```
```
CHAR_NORA = Nora, stylised 3D woman in her late twenties with adult proportions, oval face
with defined cheekbones, warm brown eyes, thick dark brows, medium-deep brown skin,
shoulder-length dark brown 3C curls with a coral claw clip on the right side, mustard
ribbed knit sweater, small gold hoop earrings; signature identifiers: coral claw clip,
mustard sweater, gold hoops
CHAR_NORA_FLAT = CHAR_NORA except: curls limp and flattened against her head, clip slipping
```
```
PRODUCT_PUFFLE150 = tall slim teal spray bottle with a white fine-mist cap about one fifth
of its height, coral "Puffle" wordmark centred vertically on the front, matte finish,
matches the reference exactly
```

## 3. Storyboard (excerpt)

| # | Time | Line | Purpose | Camera | Action | Gen/used | Transition | Plan |
|---|---|---|---|---|---|---|---|---|
| S01 | 0.0–2.4 | "By noon, my curls give up." | Establish the problem | Medium, eye level, Nora at desk, window centre-back | Blows a limp strand upward; it flops back | 5 / 2.4 s | cut | A std |
| S02 | 2.4–4.6 | "One spritz of Puffle…" | Introduce the product as the turning point | Side CU at head height | Mist bursts from the bottle into the curls | 5 / 2.2 s | match cut on mist | A pro |
| S03 | 4.6–8.8 | "…and they're back…" | Payoff transformation | Medium CU, front | Curls spring from flat to full (start=FLAT, end=NORA) | 5 / 4.2 s | cut | A pro |
| S04 | 8.8–12.0 | "Puffle. Curls that keep up." | Brand + CTA | Medium, product foreground left | Nora smiles, small head turn; slow push-in | 5 / 3.2 s | end card composite | A std |

## 4. Scene card: S03 (excerpt)

**A. First-frame (start) prompt**
```
Vertical 9:16 frame, medium close-up, eye level, Nora centred; all characters, faces,
hands, product and key action kept inside the central 4:5 area, top and bottom 15% of
the frame background only. <STYLE>. <CHAR_NORA_FLAT>, facing camera, eyes closed,
hopeful half-smile. Soft office background with a bright midday window, warm light from
camera left. Continuity: mist droplets still sparkling in the air from S02. Use
reference 1 for Nora's face, hair, clip and sweater. No text, no watermark, no extra
characters, no extra fingers, no distorted anatomy.
```
End frame: the same prompt with `<CHAR_NORA>` (full bouncy curls) and eyes open,
delighted smile. Generate it as an image-edit of the start frame so everything else
stays identical.

**B. Image-to-video prompt** (Kling 3.0 pro, start + end frame, 5 s, sound off)
```
Nora's flat curls spring up into full bouncy curls from the roots outward while she opens
her eyes and breaks into a delighted smile. Camera: static. Pacing: snappy spring in the
first 2 seconds, then a gentle settle. Keep her face, sweater, clip and earrings unchanged;
background and lighting stay the same. No new objects, no scene change, no text, no cuts.
```

## 5. Budget (from `scripts/example-plan.json`)

```
$ python3 scripts/estimate_credits.py scripts/example-plan.json
TOTAL 73.62 (hero subset 24.00) · balance 13187.72 → Recommendation: Plan A
```

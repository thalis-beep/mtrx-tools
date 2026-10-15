---
workflow: general-video
flow: automation
storyboard: no
message: "BLACK FRIDAY — UP TO 30% OFF + FREE BEANIE WITH EVERY ORDER."
aspect: "9:16"
length: 6s
audio: sound design only (scripts/make_sfx.py -> assets/sfx.wav), no voice
---

## Intent
UndrDog Hemp, Project 008: The Polo (Midnight Black). Premium menswear Black Friday spot.
Black / charcoal / off-white with restrained orange; Anton (condensed display) + Barlow Condensed labels.

0.0–1.2 hook: polo lit out of darkness, BLACK / FRIDAY slams in behind it, light sweep across the knit.
1.2–3.3 deal: speed-ramp push + light-sweep cut, UP TO / 30% digit roll (largest element) / OFF.
3.3–5.0 gift: polo slides left, beanie lands right, FREE BEANIE / WITH EVERY ORDER.
5.0–6.0 end frame: logo, BLACK FRIDAY, UP TO 30% OFF, + FREE BEANIE WITH EVERY ORDER, products; hold.

## Assets still needed (the sandbox could not reach undrdog.com)
The render uses neutral, clearly labelled placeholders. Drop in the official files and re-render:
- Midnight Black polo, front, transparent PNG -> replace `assets/polo-placeholder.svg` (img src + `#polo-sweep` mask)
- Official promotional beanie, transparent PNG -> replace `assets/beanie-placeholder.svg` (img src + `#beanie-sweep` mask)
- Official UndrDog logo (SVG/PNG) -> replace the `#logo` wordmark text with an `<img>`
Then set `--ph-tag: none` and run `npm run check && npm run render`.

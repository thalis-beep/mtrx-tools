---
workflow: general-video
flow: automation
storyboard: no
message: "BLACK FRIDAY — UP TO 30% OFF + FREE BEANIE WITH EVERY ORDER."
aspect: "9:16"
length: 6s
audio: quiet sound design only (scripts/make_sfx.py -> assets/sfx.wav)
---

## Intent
Simpler, minimal follow-up to `../undrdog-black-friday`: one poster-style frame that stays on screen.
Feedback on the first cut was that the information moved too fast to read.

Layout: black header band (logo, BLACK FRIDAY) over a warm off-white stage; UP TO / 30% OFF as the
largest element; the polo centred; a FREE BEANIE WITH EVERY ORDER card with the beanie; a small footer.
Motion: everything settles in once (all copy readable by ~0.9s), then only a slow push-in on the polo
and one soft sheen each on the polo and the beanie. Nothing leaves the screen.

## Assets
- `assets/polo.png`: client polo reference (`assets/polo-source.jpg`) cut out with `scripts/cutout.py`.
- `assets/beanie.png`: client beanie, same cutout as the first spot.
- Still needed: the official UndrDog logo. `#logo` is a plain wordmark placeholder.

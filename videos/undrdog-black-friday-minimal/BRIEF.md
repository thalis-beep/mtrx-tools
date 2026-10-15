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

Layout: dark charcoal gradient set (as in the first spot) with a soft spotlight and rim light on the
polo; logo and BLACK FRIDAY with a short orange rule; UP TO / 30% OFF as the
largest element; the polo centred; a FREE BEANIE WITH EVERY ORDER card with the beanie; a small footer.
Motion: everything settles in once (all copy readable by ~0.9s), then only a slow push-in on the polo
and one soft sheen each on the polo and the beanie. Nothing leaves the screen.

## Safe zones
All information sits inside the centred 4:5 zone (1080x1350, y 285-1635), within 60 px side
margins, and clear of the approximate action rail (x > 960) and caption area (y > 1600).
Only background colour bleeds to the 9:16 edges. Check with `../../overlays/safe-zone-9x16-4x5.png`;
`renders/*-safezone-preview.mp4` is the spot with that overlay burned in (review only, not for posting).

## Assets
- `assets/polo.png`: client polo reference (`assets/polo-source.jpg`) cut out with `scripts/cutout.py`.
- `assets/beanie.png`: client beanie, same cutout as the first spot.
- Still needed: the official UndrDog logo. `#logo` is a plain wordmark placeholder.

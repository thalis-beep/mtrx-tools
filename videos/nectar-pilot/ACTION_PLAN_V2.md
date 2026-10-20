# Nectar "Alive Again" — V2 action plan (from Frame.io review of V1)

Source: `review/frameio-comments-v1.csv` (33 comments). Timecodes mapped to shots via `shot_timing.json`.
Animation model for V2: **MiniMax H3** (images stay GPT Image 2.5, 4:5 → outpaint 9:16).

Legend — **S** = new still + animate · **A** = re-animate existing still · **E** = edit/audio/captions only · ✅ = already fixed after V1 · ❓ = needs confirmation

| # | TC | Comment | Plan | Type |
|---|---|---|---|---|
| 1 | 0:00 | would cut this | Drop the 3s intro; start on the hook. Trim the song's instrumental intro to match | E |
| 2 | 0:03 | make struggle clearer, can't pick up kid | Dad bends, grips grandson, strains hard, can't lift him at all — boy's feet never leave the grass | S |
| 2 | 0:06 | don't throw the kid; kid sad dad can't lift him | End on the boy's disappointed face as dad gives up, hand on back | S |
| 3 | 0:08 | show him trying to lift something else | Dad tries to lift a bag of charcoal / cooler, can't, grabs his back | S |
| 4 | 0:12 | facial expressions all over the place | Same still, re-animate with one clear pained-tired expression | A |
| 5 | 0:16 | friends working out, he can't keep up | Backyard/garage: buddies lifting & doing push-ups, dad drops out exhausted | S |
| 5 | 0:19 | (editor) family turns toward him, shocked | ❓ conflicts with the strategist note — see question 2 | ❓ |
| 6 | 0:22 | winded going UP + fix what's circled | New angle clearly going up (side/behind), fix the distorted reaching arm | S |
| 7 | 0:25 | don't cover his face | Caption sits on his face → move captions per shot so they never cover faces (+ keep re-animation) | E |
| 9–10 | 0:34 | wife should look away; better: walking, fit guy passes on wife's side, she stares | Merge 9+10 into one walking shot: couple on sidewalk, fit man jogs past on her side, her head turns to follow him, dad notices | S |
| 12 | 0:43 | show him slumped on couch instead | Replace closet shot with dad slumped on couch, remote in hand | S |
| 16–17 | 0:58 | dark nighttime, consistent light | Re-light porch scenes 16 + 17 to night (dark sky, porch light only) | S |
| 17 | 1:07 | son shouldn't walk away then back | New animation: son walks straight up and sits | S |
| 22 | 1:25 | son should look at what he pours; pour less | Son looks down at bottle, short pour | S |
| 24 | 1:30 | remove this guy (circled) | ❓ which person — see question 1 | S |
| 26–27 | 1:36 | music gets quiet, +3 dB | Measured: 1:32–1:45 is 3–4 dB below the rest → +3 dB with smooth ramps | E |
| 27 | 1:41 | make this green too (circled) | ❓ probably the callout boxes (navy → green) — see question 1. (Shot 27 itself already replaced after V1) | E ❓ |
| 28 | 1:49 | too much pour; show pour + mix | ✅ shorter pour done; add stir/mix end (pour → stir) | A |
| 29 | 1:54 | facial expressions off | Re-animate, calm determined "why not" | A |
| 30 | 1:57 | show him at a mirror checking himself out | New mirror still (early progress, small proud smile) | S |
| 31 | 1:59 | should show him going up | New angle: clearly climbing up the stairs | S |
| 32 | 2:03 | determined, fast look | Re-animate workbench with focused, quick energy | A |
| 33 | 2:06 | "and still have" | Captions split this phrase badly ("work and still / have energy") → phrase-aware caption grouping | E |
| 34 | 2:10 | show him actually fixing something | Close action: tightening a railing bolt / hammering, visible result | S |
| 35 | 2:12 | show him throwing the ball | Start frame = dad mid-throw, kids reacting | S |
| 36 | 2:15 | throw the beers in the trash | Dad drops the beer cans into the trash can, satisfied | S |
| 37 | 2:21 | show him flexing | Mirror: dad flexes his arm, proud grin | S |
| 40 | 2:34 | facial expressions off | Re-animate dinner, warm natural looks | A |
| 41 | 2:35 | female voice + lip sync | Wife sings "you look good lately…" on screen, lip-synced (MiniMax audio reference) — needs female vocal, see question 3 | S |
| 43 | 2:43 | show them as they are now, not old | ✅ redone after V1 with the current-look couple | — |
| 45 | 2:54 | show older guy here | Bench man → 50s, same age as dad | S |
| 46 | 2:56 | same guy here too | Same 50s man in the crowd shot | S |
| all | 3:08 | too slow; closer to the reference | See question 4 (pace) | E |

## Totals
- New stills + animation: ~20 shots · re-animate only: ~6 · edit/audio/captions: 6
- Estimated credits: stills ~40 + outpaint ~40 + MiniMax ~10–15/clip
  - only changed shots (~26): **~350–400 credits**
  - all 47 shots on MiniMax for consistent acting: **~600–700 credits**

## Open questions
1. Circled annotations: which person to remove in shot 24, and what to make green in shot 27?
2. Shot 5: strategist (friends working out) vs editor (family turns toward him, shocked) — which, or both?
3. Female line (2:35–2:40): regenerate just that section in Suno with a female voice (Replace Section)?
4. Pace: cut intro, shorten 16s end card to ~5s, more/faster cuts, optionally speed the song up ~8% (pitch kept)?

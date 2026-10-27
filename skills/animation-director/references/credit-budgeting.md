# Credit Budgeting and the Plan Decision

**Never assume a balance or a price.** Read the balance (`balance`) and quote the
cost of each configuration you'll use (`get_cost:true`). If you can't, ask the user
for both.

## 1. Count the work

From the storyboard:
- `S` = scene stills (first frames)
- `L` = lock assets: style tests + character sheets + hero refs + product check
- `C` = clips, with duration and quality tier for each
- `H` = hero shots (hook, product hero, end card), which may use a higher tier

## 2. Apply revision buffers

Plan for retries up front. These are starting multipliers. Adjust them in
`house-lessons.md` as the team learns its real retry rates.

| Asset | Expected attempts per approved asset |
|---|---|
| Lock assets (sheets, style tests) | 2.0 |
| Scene stills | 1.5 |
| Simple clips (static camera, small action) | 1.5 |
| Complex clips (character + product interaction, transformations) | 2.5 |

## 3. Compute

```
total = Σ(lock_cost × 2.0) + Σ(still_cost × 1.5) + Σ(clip_cost × attempts) + finishing (upscales)
```

`scripts/estimate_credits.py` does this from a small JSON file of the storyboard.
Put the result in `templates/credit-estimate.md`.

## 4. Decide

| Condition | Recommendation |
|---|---|
| balance ≥ total × 1.2 | **Plan A** |
| balance ≥ total, but < total × 1.2 | **Plan A**, with draft tiers and the user told the margin is thin |
| locks + hero shots ≤ balance < total | **Hybrid**: Higgsfield for the locks and hero or hardest shots, Plan B for the rest |
| balance < locks | **Plan B** (or ask for a top-up) |
| User budget cap set | Treat the cap as the balance |

For Hybrid, rank shots by **difficulty × importance**: the hook, product hero,
transformations and multi-character shots go in Higgsfield first. Reuse the
Higgsfield-approved character and product references as the reference images for the
external tools, so the two halves look like one film.

## 5. Report to the user (plain words)

> 14 scenes → about 230 credits with revision buffer (locks 12, stills 32, clips 176,
> finishing 10). Balance: 13,187. **Recommend Plan A.** Hero shots in Kling pro, the
> rest std, all silent.

Re-check the balance before the animation phase and before any large batch.

## Cost snapshot (example only: re-quote before use)

Quoted on this team's account on 2026-10-27, 9:16, silent:

| Config | Credits |
|---|---|
| `gpt_image_2_5` 1k, quality medium | 0.5 / image |
| `nano_banana_pro` 1k | 2 / image |
| `kling3_0` std 5 s | 6.25 |
| `kling3_0` std 10 s | 12.5 |
| `kling3_0` pro 5 s | 7.5 |
| `kling3_0_turbo` 720p 5 s | 7.5 |
| `seedance_2_5` 720p 5 s | 35 |

Takeaways that are likely to hold: **video costs about 10× more than stills, so QC
stills hard before animating**. Clip length scales roughly linearly with cost. Some
models (Seedance) cost several times more than others, so save them for shots that
really need them.

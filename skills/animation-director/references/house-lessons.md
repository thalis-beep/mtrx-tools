# House Lessons (MTRX team)

This file holds what the team has learned on its own productions: what worked, what
failed, real retry rates, preferred models, CS preferences. **Read it at the start of
every job. Add to it at the end of every job.** It overrides the general defaults
elsewhere in this skill when the two conflict.

> **Status: seed version.** When this skill was built, no record of earlier MTRX
> animation productions was available to the author, so the entries below are the
> starting defaults built into this skill. Replace or confirm them as real
> productions accumulate. Date and initial each entry.

## Defaults confirmed by the team
- 9:16 delivery, 4:5 safe zone, 1K stills: *from the original skill brief, 2026-10-27*

## Model preferences
<!-- e.g. "2026-11-03 (JR): kling3_0 std holds clay style better than turbo; use turbo only for drafts." -->

## Prompt patterns that work
<!-- Copy exact phrasings that fixed recurring problems. -->

## Known failure modes
<!-- e.g. "Bottle labels warp when the character rotates the product — always cut to an insert." -->

## Real retry rates
<!-- Update the multipliers in credit-budgeting.md once you have data. -->
| Asset | Planned | Actual (avg of last N jobs) |
|---|---|---|
| Lock assets | 2.0 | |
| Scene stills | 1.5 | |
| Simple clips | 1.5 | |
| Complex clips | 2.5 | |

## CS / client preferences
<!-- Brand-specific rules, recurring characters, approved style blocks to reuse. -->

## Post-job retro template
```
Job: <name>  Date: <yyyy-mm-dd>  Editor: <initials>  Plan: A/B/Hybrid
Credits: estimated <n> / actual <n>
What worked:
What failed and the fix:
Add to defaults? (y/n + what):
```

## Job log
```
Job: DN Creatine V1 (bloating, claymation)  Date: 2026-10-27  Plan: A
What failed and the fix:
- Style-reference frames taken from a competitor ad leaked its character (bearded man) into scenes
  with no people. Fix: only use frames with NO characters as style refs, or use our own approved
  stills as refs; add "absolutely no people/humans" to object and environment shots.
- Insert shots (clock, glass) came back with the hero character added, because the kitchen ref had
  her in it. Fix: say "object-only insert, no people" explicitly.
- Higgsfield sometimes rejects a generate_video batch item with a preset recommendation
  ("IN THE DARK"). Fix: resubmit the same item with declined_preset_id.
- The script described the product as "blue"; the real pack is white. Always follow the real reference and flag it.
What worked:
- gpt_image_2_5 1k high (1.5 cr) with refs: strong identity hold; editing the hero ref made a
  perfect before/after variant.
- The clay-rendered product pouch matched logo/layout well; only small print was wrong.
```

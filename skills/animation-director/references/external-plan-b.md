# Plan B: External AI Production Package

Plan B is the same production with a different place to generate. All of the
analysis, locks, storyboard and QC still apply. The difference is that you hand the
editor a package they can run in other tools without having to reconstruct any
creative direction.

## Package contents

1. **Production bible**: analysis, style lock, character and product locks,
   storyboard, continuity ledger (`templates/production-bible.md`).
2. **Lock prompts**: the character sheet prompt and hero-reference prompt for each
   character and variant, and the product check prompt. **Run these first** and get
   approval before the scene prompts.
3. **Scene cards** (`templates/scene-card.md`), one per scene:
   - **A. First-frame image prompt**: complete and copy-ready, with the style,
     character and product blocks pasted in full (no "see above").
   - **B. Image-to-video prompt**: copy-ready, with the duration and settings for the
     target tool.
   - **C. Scene info**: number, verbatim script line, timing, which references to
     attach, editing notes.
4. **Generation order and reference plan**: which approved image goes into which
   generation as a reference.
5. **QC checklist and edit timeline**.

**Every prompt must stand alone.** The editor will paste one card at a time.

## Adapting to the target tool

Ask which tools the editor uses. Then adapt the prompts using the patterns below,
**without changing the creative content**. Tool features change often, so if you're
unsure what a tool currently supports, say so and use the generic format.

| Tool type | Adaptation |
|---|---|
| Natural-language image models with reference upload (GPT Image, Nano Banana / Gemini, Flux Kontext-style editors) | Full sentences in the anatomy order. Say "Use image 1 for … image 2 for …". Aspect ratio in the settings plus in the text |
| Tag/weight-style image tools (Midjourney-style) | Shorter descriptive phrases; aspect via parameter (e.g. `--ar 9:16`); character/style reference via the tool's reference features; put negatives in its no-parameter |
| Image-to-video tools (Kling, Runway, Luma, Veo, Hailuo, Pika-style) | Upload the approved still as the first/start frame. Use the motion prompt only (action + camera + locks). Set duration and 9:16 in the settings. Turn generated audio off if possible. Use end-frame features for transformations where they exist |
| Tools without negative prompts | Phrase restrictions positively inside the prompt: "the background remains completely still" |

Generic format to use when the tool is unknown:

```
[IMAGE PROMPT — paste into image tool]
<full first-frame prompt>
Settings: aspect 9:16 · ~1K resolution · attach: <ref list>

[VIDEO PROMPT — paste into image-to-video tool, start frame = approved image above]
<motion prompt>
Settings: duration <n> s · 9:16 · audio off · camera: <move>
```

## Keeping consistency across tools

- Generate **all** characters' hero references in **one** tool and reuse them in
  every external tool, ideally Higgsfield in a Hybrid job.
- Use the same image tool for every scene still. Switching image tools mid-job is the
  biggest cause of style drift.
- Ask the editor to return the stills (or describe any deviations) before animating,
  so you can QC them. Offer to review uploads.
- Give file names: `S03_first.png`, `S03_clip_v1.mp4`, which keeps the edit simple.

## Hybrid jobs

- Mark each scene card **[A] Higgsfield** or **[B] External**.
- [A] cards include the Higgsfield model and parameters. [B] cards include the
  external-tool settings.
- External scenes use the Higgsfield-approved references as uploads.

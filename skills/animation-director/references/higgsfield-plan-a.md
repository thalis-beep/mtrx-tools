# Plan A: Producing in Higgsfield

This assumes the Higgsfield connector (MCP) is connected. Tool names below are the
connector's. If a tool is missing in your client, list the step for the user to
run manually in the Higgsfield web app, with the exact prompt and settings.

> The model catalogue and parameters change. Before each production, confirm model IDs,
> durations, aspect ratios and media roles with `models_explore {action:"get", model_id}`.
> The table below is a starting point that was correct when this skill was written.

## Setup

1. `balance`: read the live credits and plan. Record them in the bible.
2. `get_preferences`: if `auto_create_project` is true (or the user wants a project),
   `create_project` and reuse its `default_folder_id` as `folder_id` on **every**
   generation in this job.
3. Upload references:
   - Local or readable files: `media_upload` → PUT the file → `media_confirm`.
   - Web URLs: `media_import_url`.
   - Unreadable chat attachments: `media_upload_widget`, as the only tool call in that
     turn.
   - Record every `media_id` in the bible's asset register (character refs, product
     refs, location refs).

## Model choice (starting defaults)

| Step | Default model | Why / notes |
|---|---|---|
| Style tests, character sheets, scene stills with references | `gpt_image_2_5` | Strong reference following and editing. Params: `resolution:"1k"`, `quality:"medium"` (raise only for hero shots), refs as role `image_references`. Supports 9:16 and 4:5 |
| Alternative stills / text-heavy frames | `nano_banana_pro` | **Defaults to 2K. Always pass `resolution:"1k"`.** Refs as `image_references` |
| Product packshot or product-led stills | `marketing_studio_image` | Use when the shot is mainly the product. Pass the product photo as `image` |
| Image-to-video, default | `kling3_0` | `start_image` (+ optional `end_image` for transformations), `mode:"std"`, **`sound:"off"`**, 3–15 s, 9:16 |
| Image-to-video, hero shots | `kling3_0` with `mode:"pro"` | Higher quality, for hook, product hero and end card |
| Image-to-video, fast/cheap drafts | `kling3_0_turbo` | `start_image` only, 720p |
| Complex multi-reference or longer shots | `seedance_2_5` | Much more expensive. Check the mode (`omni_reference`) and roles with `models_explore` first. Set `generate_audio:false` |

Not sure? Call `models_explore {action:"recommend", query:"image-to-video, stylised
<style>, single character action, 9:16", type:"video", input:"image"}`.

## Run order

1. **Style test** (Gate 1 input): 1–2 stills of a key scene in the proposed style.
   Cheap, and it settles the look before you spend on anything else.
2. **Character sheets**: one per recurring character (see `character-consistency.md`).
   Then a single-pose hero reference per character and variant.
3. **Product check still**: one still with the product reference to test how
   accurately it reproduces. Flag problems now (see `product-accuracy.md`).
4. → **Gate 1 approval.**
5. **Scene stills**: `generate_image_batch` for independent scenes (up to 12 per batch).
   Attach the character, product and location references to each item. Then
   `jobs_wait` (timeout ≤ 15 s per call, repeat until done) → `show_generation_by_ids`
   once for the set.
6. **QC the stills.** Fix failures with image-edit (pass the failed still's `job_id`
   as a reference and describe only the correction).
7. **Animate**: `generate_video_batch`, one item per approved still, with the still's
   `job_id` as `start_image`. Use `jobs_wait` → `show_generation_by_ids`.
8. **QC the clips.** Re-roll only the failing clips.
9. **Optional finishing**: `upscale_video` on the final selects only (not drafts).
   For assembly, soundtrack and burned captions, load
   `get_workflow_instructions {workflow:"video-montage"}`.

## Credit discipline in Higgsfield

- **Preflight every new configuration** with `get_cost:true` (it submits nothing). Use
  the quote in the budget and never assume a price.
- `count` 2–4 (variants of the same prompt) only where choice really matters, such as
  the character sheet or hook frame. Default `count:1`.
- Keep clip `sound:"off"` / `generate_audio:false`. The CS audio is the soundtrack.
- Draft at std/720p and upgrade only the finals that need it.
- Don't pass `use_unlim` unless the user explicitly asks to use unlimited or
  free-trial generations.
- On a transport timeout, **don't resubmit blindly**. The job may have been accepted.
  Check with `show_generations` / `jobs_wait` first.

## Gotchas

- Pass `aspect_ratio:"9:16"` explicitly. Some models (Marketing Studio) default to 16:9.
- `medias[].value` must be a `media_id` or `job_id`, never a URL.
- Use the role names each model declares (`image_references`, `start_image`,
  `end_image`, `image`). Check `models_explore get` when unsure.
- If a call returns a `recovery_tool`, call it straight away.
- Multi-panel character sheets used as references can leak multiple figures into a
  scene. Use a single-pose hero reference.

## Run log (keep in the bible)

| Scene | Step | Model + key params | Refs (media/job IDs) | Job ID | Credits | QC result | Notes |
|---|---|---|---|---|---|---|---|

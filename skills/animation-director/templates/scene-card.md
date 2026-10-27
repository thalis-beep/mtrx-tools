# Scene <NN>: <short title>   [A Higgsfield | B External]

## C. Scene info
| Field | Value |
|---|---|
| Timestamp | 0.0–0.0 (EST?) |
| Script line | "<verbatim>" |
| Purpose | |
| Cast / variant | |
| Product | |
| Duration | generate <n> s · use <n> s |
| Transition in / out | |
| Continuity in | (state carried from previous scene) |
| Continuity out | (state this scene leaves) |
| References to attach | 1. <char hero ref> 2. <product ref> 3. <location ref> |
| Edit notes | (speed, overlay, composite, caption) |

## A. First-frame image prompt
```
Vertical 9:16 frame, <shot size>, <angle>, <placement>; all characters, faces, hands,
product and key action kept inside the central 4:5 area, top and bottom 15% of the frame
background only.
<STYLE block verbatim>
<CHAR block verbatim>, <pose — the START of the action>, <expression>, <holding …>.
<PRODUCT block verbatim>, <position, scale>, matching the reference exactly.
<Environment>, <lighting + palette>.
Continuity: <carried state>.
Use reference 1 for the character's face, hair and outfit; reference 2 for the product's
exact shape, colours and label.
No text, no watermark, no extra characters, no extra fingers or limbs, no distorted
anatomy, no invented logos<, shot-specific negatives>.
```
Settings: aspect 9:16 · 1K · model/tool: <…> · refs: <…>

## B. Image-to-video prompt
```
<Subject> <single action, start → end>. <Expression change, if any>.
Camera: <one move + speed>. Pacing: <slow/natural/snappy>, <n> seconds.
Keep the character design, outfit, product shape and label unchanged; background and
lighting stay the same. No new objects or characters, no scene change, no text, no cuts,
no morphing.
```
Settings: duration <n> s · 9:16 · audio off · start frame = approved S<NN> still
<· end frame = … (transformations only)> · model/tool: <…>

## QC
| 1 Script | 2 Character | 3 Product | 4 Motion | 5 Continuity | 6 Technical | 7 Edit-ready |
|---|---|---|---|---|---|---|
| | | | | | | |

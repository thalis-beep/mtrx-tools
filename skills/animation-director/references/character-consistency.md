# Character Consistency

Consistency comes from three things used together: **one master description reused
verbatim**, **one approved reference image attached to every generation**, and **one
locked style block**. Leave any of them out and the character drifts.

## 1. Master description (write once, paste everywhere)

Write it as a single dense paragraph in this slot order. Earlier tokens carry more
weight:

```
[NAME/ID] — [style treatment], [age band + build + height feel], [face shape, jaw,
nose, eyes (shape + colour), brows, mouth], [skin tone], [hair: colour, length, style,
finish, parting], [wardrobe head-to-toe: top → layer → bottom → shoes → accessories],
[distinctive marks/props], [default expression/personality read]
```

Rules:
- Be **specific, not adjectival**: write "mustard-yellow cropped puffer with silver
  zip", not "cool jacket".
- Give **2–3 signature identifiers** that survive any angle or size, such as a hair
  shape, a colour-blocked garment, or a prop. Viewers recognise these first.
- Don't use names of real people or existing IP. Original designs only.
- Adults should read as adults. Specify mature proportions when the style tends to
  make faces too young.
- Store the paragraph in the bible as `CHAR_<ID>`. **Paste it verbatim** into every
  prompt for that character. Don't paraphrase.

## 2. Reference sheet (Gate 1)

Generate one sheet per recurring character before any scene still:
- **Turnaround** (front, ¾, side, back) on a plain background, in the locked style.
  This is the default.
- Add an **expression row** when the script's emotional arc is wide.
- Use 16:9 or 3:2 for sheets, and 1K unless detail is lost.
- Higgsfield has a dedicated `character-sheet` workflow. Load it with
  `get_workflow_instructions {workflow:"character-sheet"}` and use its slot structure
  and negative tail, swapping in our style lock.

Then **crop or generate one clean single-pose hero image** of the character (front or
¾, neutral pose, plain background). This is the reference attached to every scene
still. Multi-panel sheets used as references sometimes make models paste multiple
figures into a scene. If that happens, switch to the single-pose reference.

Get user approval of the sheet before continuing. After approval, the design is frozen.

## 3. Variants (before/after, outfits, ages)

- Define each variant as a **diff** from the master: `CHAR_MIA_AFTER = CHAR_MIA except:
  hair glossy and voluminous, posture upright, expression confident`.
- Keep the 2–3 signature identifiers **unchanged** across variants so the viewer knows
  it's the same person.
- Make a separate hero reference image for each variant, generated from the master
  reference (image-edit/reference mode) and not from scratch.

## 4. Using references in scene stills

- Attach the character hero reference, plus the product reference, plus (if a
  location repeats) the approved location still.
- In the prompt, name what each reference is for: "use reference 1 for the
  character's face, hair and outfit; reference 2 for the bottle's exact shape and
  label".
- Keep the character **large enough in frame** for the model to honour the face. In
  wide shots, faces drift. Rely on the signature identifiers and keep wides short.
- **Multi-character shots**: attach one reference per character, describe positions
  explicitly ("Mia on the left, Leo on the right"), and avoid physical contact unless
  the script needs it.

## 5. Drift checks (run on every still)

Compare against the hero reference: face shape, eye colour, hair shape and colour,
every wardrobe item, accessories, skin tone, proportions and style treatment. Any
mismatch fails QC → fix by image-edit with the reference attached. Don't re-roll from
text alone.

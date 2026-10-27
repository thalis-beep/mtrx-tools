# Audio Sync and Editing

The audio is the spine of the edit. Plan the visuals to the audio, not the other way
round.

## With final audio

1. Get timestamps for every VO phrase or lyric line. If a transcription tool is
   available, use word-level timestamps. Otherwise, listen and log them by hand.
2. Lock the beat map to the real times, replacing all `EST` values.
3. For music, also mark: tempo/BPM, downbeats, section changes (intro, verse, chorus,
   drop, outro) and energy peaks.

## Voiceover-driven cuts

- **Cut on the phrase, show on the word.** The visual for an obligation ("the bottle")
  should be on screen *when the word is heard*, ideally 0.1–0.3 s before it.
- Lead the hook visually: the first frame must be arresting before the first word lands.
- Hold the product hero shot long enough to register (≥ 1.5 s).
- Avoid cutting in the middle of a word.

## Music-driven cuts

- Cut on beats or bars. Fast sections can cut every 1–2 beats, slower sections every
  bar or phrase.
- Change scene or visual idea at section changes.
- Match motion energy to musical energy: small actions in verses, bigger moves and
  transformations on the chorus or drop.
- Lyric obligations still apply. When a lyric names something, show it on that line.

## Retiming when the audio changes

Preserve approved assets first:
1. Re-transcribe and rebuild the beat map with new times.
2. Map each existing approved clip to its new slot. Trim or extend with the handles,
   adjust speed (±10% is usually invisible), or hold on the last frame.
3. Only lines that are **new or changed in meaning** need new shots.
4. If a slot got longer than any clip, first try a second camera move on the same
   approved still. That's cheaper than a new scene.
5. Update the edit timeline and note what changed.

## Captions and on-screen text

- Add text **in the edit**, not in generated images, so it's legible, editable and
  correctly spelled.
- Keep it inside the 4:5 safe zone and clear of platform UI.
- For burned captions in Higgsfield, use the `video-montage` workflow. Otherwise
  deliver an SRT and caption notes.

## Edit handoff

Fill in `templates/edit-timeline.md`: clip file, in/out points, the audio range it
covers, transition, and notes (speed changes, overlays, composites, captions). Add the
end card and any legal or disclaimer text the CS specified.

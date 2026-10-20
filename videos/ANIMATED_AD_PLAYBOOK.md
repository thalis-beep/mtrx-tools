# Animated music ad playbook

How MTRX cartoon musical ads are made with this repo, and the house style learned from the
editor's final cut of Nectar "Alive Again" V2 (`MTRX_DNCR5_Al_SA_RSANM4_Th_V1_9-16_2.prproj`).
Read this before starting the next one.

## Pipeline

1. Script → song (Suno, lyrics verbatim from the script) → `tools/analyze_song.py` (Whisper words
   + beats) → `tools/align_lyrics.py` (script spelling, monotonic timing).
2. Storyboard: one shot per sung phrase, `timing.json` with song_start/song_end per shot.
3. Stills: GPT Image 2.5 at 1K, generated at 4:5 so everything sits in the safe zone, then outpainted
   to 9:16. Review sheets with the 4:5 box go to the client before any animation.
4. Animation (see Models and credits), QC every clip as a frame strip, retake failures.
5. Captions: `tools/captions_png.py --phrases` (hand-phrased, verified word for word),
   callouts and title: `tools/graphics_png.py`.
6. `tools/assemble.py edit.json OUT` → preview MP4 with burned-in overlays and a Premiere package
   (`tools/premiere_otio.py`: shots V1, captions V2, graphics V3, song A1).
7. Delivery: MP4 under 100 MB (2-pass) and the Premiere package split into zips under 100 MB,
   committed to the branch and shared as GitHub raw links (chat attachments did not download).

## House style (from the editor's cut)

Timing and cuts
- Start the edit on the first sung word. Whisper put the first word of "Alive Again" 0.9 s early
  (2.32 s vs the real 3.23 s), which left dead air and an early first caption. Check the vocal onset
  on a demucs vocal stem before setting `song_in`; start ~0.05 s before it, with a short audio fade-in.
- Cut on the phrase, not on the beat grid. The editor moved most cuts to land 0.1–0.3 s before the
  line the shot illustrates (only 11 of 47 cuts sit on a beat; every one of ours did).
- Trim into the action. Generated clips open slowly on the still; the editor skipped 0.2–2.2 s into
  many clips. Choose each clip's in-point where the motion is already happening.
- Short cross dissolves (0.3–0.7 s) only at scene or time jumps (BBQ → workout, café → shop window,
  graph → brain); hard cuts everywhere else.
- Slow push-ins (scale keyframed 100 → 105–108 %) on emotional beats, static punch-ins (104–129 %)
  to tighten loose framing.
- End on the client's own CTA video (with its audio) instead of a generated end card and title; fade
  the song out over ~3.4 s underneath it. Ask the client for the CTA file up front.

Captions
- No blank gaps: each caption stays up until the next one starts (now the default in
  `captions_png.py`).
- Highlight key words: brand mention in light blue `#4ACAFF` ("NECTAR'S A"), product claims in
  green `#3DFF3D` ("IS NON-GMO", "CALLED BIOPERINE"). In `phrases.txt`: `#3DFF3D is non-GMO,`.
- When a callout shows the same words, drop that caption and let the callout take its place
  (ZERO SUGAR, ZERO CALORIES). In `phrases.txt`: `~zero sugar,`.

Callouts
- Green box `#34AE33`, white text, one short line (no sub-line), one at a time at y ≈ 0.25
  (now the default in `graphics_png.py`).

Shots
- The editor replaced the lift-struggle opening and the jogger/wife-look beat with Grok Imagine
  clips: MiniMax H3 under-acted interaction and reaction beats. For beats that hinge on a reaction
  between characters, test a second model before settling.
- Water stays clear in pour shots: lock start and end frames, or reuse an approved pour.

## Models and credits

| Model | Resolution | Cost | Notes |
|---|---|---|---|
| MiniMax H3 (`minimax_h3`) | 2K only | 10 cr / 5 s | used for Nectar V2; rejects 4 s jobs despite listing them, use ≥ 5 s |
| MiniMax H3 Max (`minimax_h3_max`) | 768p / 480p | 12.5 / 7.5 cr per 5 s | 768p costs more than H3 2K |
| MiniMax Hailuo 2.3 (`minimax_hailuo`) | 768 (≈720p) | 6 cr / 6 s | half H3's cost per second; 6 or 10 s; start + end frames |
| Grok Video 1.5 (`grok_video_v15`) | 720p | 27 cr / 6 s | what the editor used for the replaced shots |
| Kling 3.0 Pro (`kling3_0`) | — | 1.5 cr / s | V1 model |

Default for the next video: 720p-class MiniMax, i.e. Hailuo 2.3 at 768, after a 2–3 shot test
against H3 so the client can compare the acting.

Nectar V2 spend: 591 credits (MiniMax 508, stills 39, outpaints 44).

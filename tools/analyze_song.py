#!/usr/bin/env python3
"""Word-level transcription + beat grid for a song.

Usage: analyze_song.py song.mp3 OUT_DIR [whisper_model]
Writes OUT_DIR/words_raw.json ([{word,start,end,prob}]) and OUT_DIR/beats.json.
"""
import json
import sys
from pathlib import Path

import librosa
from faster_whisper import WhisperModel

song, out = sys.argv[1], Path(sys.argv[2])
model_name = sys.argv[3] if len(sys.argv) > 3 else "medium.en"
out.mkdir(parents=True, exist_ok=True)

y, sr = librosa.load(song, sr=22050, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
(out / "beats.json").write_text(json.dumps(
    {"tempo": float(tempo[0] if hasattr(tempo, "__len__") else tempo),
     "beats": [round(float(b), 3) for b in beats]}, indent=1))

model = WhisperModel(model_name, device="cpu", compute_type="int8")
audio16 = librosa.load(song, sr=16000, mono=True)[0]
segments, _ = model.transcribe(audio16, language="en", word_timestamps=True, vad_filter=False,
                               beam_size=5, condition_on_previous_text=True)
words = []
for seg in segments:
    for w in seg.words:
        words.append({"word": w.word.strip(), "start": round(w.start, 3),
                      "end": round(w.end, 3), "prob": round(w.probability, 3)})
(out / "words_raw.json").write_text(json.dumps(words, indent=1))
print(f"tempo {tempo}, {len(beats)} beats, {len(words)} words")

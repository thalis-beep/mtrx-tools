#!/usr/bin/env python3
"""Align the script's lyric words to Whisper word timings (script spelling wins).

Usage: align_lyrics.py lyrics.txt words_raw.json words.json
lyrics.txt: plain lyric text (section tags in [] are ignored).
"""
import difflib
import json
import re
import sys

lyr_text = re.sub(r"\[[^\]]*\]", " ", open(sys.argv[1]).read())
script = lyr_text.split()
heard = json.load(open(sys.argv[2]))


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower().replace("’", "'"))


a = [norm(w) for w in script]
b = [norm(w["word"]) for w in heard]
out = [None] * len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1):
            h = heard[j1 + k]
            out[i1 + k] = {"word": script[i1 + k], "start": h["start"], "end": h["end"]}
    elif tag == "replace" and j2 > j1:
        # spread the script words evenly over the heard span
        s, e = heard[j1]["start"], heard[j2 - 1]["end"]
        n = i2 - i1
        for k in range(n):
            out[i1 + k] = {"word": script[i1 + k], "start": s + (e - s) * k / n, "end": s + (e - s) * (k + 1) / n}
# fill words with no match by interpolating between neighbours
for i, w in enumerate(out):
    if w is None:
        prev = next((out[j]["end"] for j in range(i - 1, -1, -1) if out[j]), 0.0)
        nxt = next((out[j]["start"] for j in range(i + 1, len(out)) if out[j]), prev + 0.4)
        out[i] = {"word": script[i], "start": prev, "end": max(prev + 0.05, min(nxt, prev + 0.4))}
json.dump([{**w, "start": round(w["start"], 3), "end": round(w["end"], 3)} for w in out],
          open(sys.argv[3], "w"), indent=0)
print(f"{len(out)} words aligned")

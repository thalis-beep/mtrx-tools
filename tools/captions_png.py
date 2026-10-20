#!/usr/bin/env python3
"""Render word-timed captions as transparent PNG overlays (TikTok-style).

Usage: captions_png.py words.json OUT_DIR [--until SECONDS] [--y 0.64] [--positions positions.json]
                       [--phrases phrases.txt]

words.json: [{word, start, end}] on the song timeline (script spelling).
Writes OUT_DIR/cap_###.png (1080x1920, transparent) and OUT_DIR/captions.json
([{png, text, start, end}]) for the assembler and the Premiere caption track.
positions.json (optional): [{"start": s, "end": e, "y": 0.5}] overrides the caption
height for shots where the default would cover a face.
phrases.txt (optional): one caption per line, in lyric order. Each line takes its words from
words.json and must match them exactly, so no word can go missing or change; without it the
captions are grouped automatically.
"""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = Path(__file__).parent / "fonts" / "TikTokSans-Bold.ttf"
W, H = 1080, 1920
SIZE = 68          # matches the reference: caption ~70% of frame width for 3 words
STROKE = 8
TRACKING = -3      # reference letters sit tight together
MAX_WIDTH = 900    # stays inside the 4:5 safe zone with margin
# words a caption should not end on, so phrases stay together ("and still have")
WEAK_END = {"a", "an", "the", "and", "or", "to", "of", "in", "on", "my", "his", "her", "your",
            "i", "i'd", "i'm", "with", "for", "at", "that", "who", "so", "just", "is", "was",
            "be", "being", "still", "some", "from", "by", "up", "their", "every", "each", "after"}


def clean(w):
    return re.sub(r"[^\w'’-]", "", w.lower())


def chunk(words, max_words=3, gap=0.3):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        ends_phrase = w["word"].rstrip().endswith((",", ".", "?", "!"))
        pause = nxt is None or nxt["start"] - w["end"] > gap
        full = len(cur) >= max_words
        weak = clean(w["word"]) in WEAK_END and not ends_phrase
        if nxt is None or ends_phrase or pause or (full and not weak) or len(cur) >= max_words + 1:
            out.append(cur)
            cur = []
    return out


def from_phrases(words, lines):
    groups, i = [], 0
    for line in lines:
        n = len(line.split())
        got = words[i:i + n]
        if [clean(t) for t in line.split()] != [clean(w["word"]) for w in got]:
            raise SystemExit(f"phrase {line!r} does not match sung words "
                             f"{' '.join(w['word'] for w in got)!r} at {words[i]['start']:.2f}s")
        groups.append((line, got))
        i += n
    if i != len(words):
        raise SystemExit(f"{len(words) - i} sung words not covered, from {words[i]['word']!r}")
    return groups


def render(text, y_frac, path, font):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = SIZE
    while True:
        f = ImageFont.truetype(str(font), size)
        advances = [f.getlength(ch) + TRACKING for ch in text]
        tw = sum(advances) - TRACKING + 2 * STROKE
        if tw <= MAX_WIDTH or size <= 48:
            break
        size -= 2
    asc, desc = f.getmetrics()
    x = (W - tw) / 2 + STROKE
    y = int(H * y_frac) - (asc + desc) // 2
    # strokes first, then fills, so tightly tracked letters don't cut into each other
    for pass_stroke in (True, False):
        cx = x
        for ch, adv in zip(text, advances):
            if pass_stroke:
                d.text((cx, y), ch, font=f, fill=(0, 0, 0, 255), stroke_width=STROKE,
                       stroke_fill=(0, 0, 0, 255))
            else:
                d.text((cx, y), ch, font=f, fill=(255, 255, 255, 255))
            cx += adv
    img.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words")
    ap.add_argument("out")
    ap.add_argument("--until", type=float, default=None)
    ap.add_argument("--y", type=float, default=0.645)
    ap.add_argument("--positions", default=None)
    ap.add_argument("--phrases", default=None)
    a = ap.parse_args()
    words = json.loads(Path(a.words).read_text())
    if a.until:
        words = [w for w in words if w["start"] < a.until]
    pos = json.loads(Path(a.positions).read_text()) if a.positions else []
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    caps = []
    if a.phrases:
        lines = [x.strip() for x in Path(a.phrases).read_text().splitlines() if x.strip()]
        groups = from_phrases(words, lines)
    else:
        groups = [(" ".join(w["word"] for w in g), g) for g in chunk(words)]
    for i, (line, g) in enumerate(groups):
        start = g[0]["start"]
        nxt = groups[i + 1][1][0]["start"] if i + 1 < len(groups) else None
        end = nxt if nxt is not None and nxt - g[-1]["end"] < 0.6 else g[-1]["end"] + 0.25
        text = line.upper().replace("’", "'")
        text = re.sub(r"[.,!?]+(?=\s|$)", "", text)   # reference shows no trailing punctuation
        y = next((p["y"] for p in pos if p["start"] <= start < p["end"]), a.y)
        name = f"cap_{i + 1:03d}.png"
        render(text, y, out / name, FONT)
        caps.append({"png": name, "text": text, "start": round(start, 3), "end": round(end, 3)})
    (out / "captions.json").write_text(json.dumps(caps, indent=1))
    print(f"{len(caps)} captions -> {out}")


if __name__ == "__main__":
    main()

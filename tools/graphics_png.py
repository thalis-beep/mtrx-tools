#!/usr/bin/env python3
"""Render callouts and the end title as transparent PNG overlays, in the caption font.

Usage: graphics_png.py graphics.json OUT_DIR

graphics.json: [{"type": "callout", "text": "ZERO SUGAR", "sub": "optional small line",
                 "start": 89.5, "end": 91.3, "y": 0.22},
                {"type": "title", "lines": ["Nectar Creatine", "For men who want a change."],
                 "start": 159.4, "end": 164.85, "y": 0.2}]
Writes OUT_DIR/gfx_##.png (1080x1920) and OUT_DIR/graphics.json ([{png, text, start, end, pop}])
in the same form as captions.json, so the assembler and the Premiere export treat both alike.
Callouts are marked "pop" so the assembler scales them in.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = Path(__file__).parent / "fonts" / "TikTokSans-Bold.ttf"
W, H = 1080, 1920
NAVY = (30, 42, 82, 255)
TITLE_STROKE = (18, 26, 48, 255)


def callout(text, sub, y_frac):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(FONT), 84)
    fs = ImageFont.truetype(str(FONT), 40)
    tw = d.textlength(text, font=f)
    sw = d.textlength(sub, font=fs) if sub else 0
    asc, desc = f.getmetrics()
    h = asc + desc + (52 if sub else 0)
    bw, bh = max(tw, sw) + 72, h + 36
    x0, y0 = (W - bw) / 2, H * y_frac - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=22, fill=NAVY)
    d.text(((W - tw) / 2, y0 + 18), text, font=f, fill=(255, 255, 255, 255))
    if sub:
        d.text(((W - sw) / 2, y0 + 18 + asc + desc + 4), sub, font=fs, fill=(255, 255, 255, 230))
    return img


def title(lines, y_frac):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = H * y_frac
    for i, line in enumerate(lines):
        size = 96 if i == 0 else 64
        while True:
            f = ImageFont.truetype(str(FONT), size)
            if d.textlength(line, font=f) <= 940 or size <= 40:
                break
            size -= 2
        tw = d.textlength(line, font=f)
        d.text(((W - tw) / 2, y), line, font=f, fill=(255, 255, 255, 255),
               stroke_width=8 if i == 0 else 6, stroke_fill=TITLE_STROKE)
        asc, desc = f.getmetrics()
        y += asc + desc + 14
    return img


def main(spec, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    events = []
    for i, g in enumerate(json.loads(Path(spec).read_text()), 1):
        name = f"gfx_{i:02d}.png"
        if g["type"] == "callout":
            callout(g["text"], g.get("sub"), g.get("y", 0.22)).save(out / name)
            text, pop = g["text"], True
        else:
            title(g["lines"], g.get("y", 0.2)).save(out / name)
            text, pop = " / ".join(g["lines"]), False
        events.append({"png": name, "text": text, "start": g["start"], "end": g["end"], "pop": pop})
    (out / "graphics.json").write_text(json.dumps(events, indent=1))
    print(f"{len(events)} graphics -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])

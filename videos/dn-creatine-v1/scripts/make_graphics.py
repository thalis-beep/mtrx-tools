"""Build caption PNGs + SRT from word timestamps, plus title / icon / guarantee graphics.
Usage: python3 make_graphics.py words.json OUT_DIR
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
words = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(f"{out}/captions", exist_ok=True)
os.makedirs(f"{out}/graphics", exist_ok=True)

# ---------- caption chunking: split at punctuation/pauses into phrases, then balance each ----------
toks = []
for w in words:  # re-join hyphen fragments ("30" + "-day")
    if w["w"].startswith("-") and toks:
        toks[-1] = {**toks[-1], "w": toks[-1]["w"] + w["w"], "e": w["e"]}
    else:
        toks.append(dict(w))
phrases, cur = [], []
for i, w in enumerate(toks):
    cur.append(w)
    nxt = toks[i + 1] if i + 1 < len(toks) else None
    if w["w"][-1] in ",.?!" or not nxt or nxt["s"] - w["e"] > 0.35:
        phrases.append(cur); cur = []
MAXC = 18
chunks = []
for ph in phrases:
    n = len(" ".join(x["w"] for x in ph))
    k = max(1, -(-n // MAXC))  # pieces needed
    target = n / k
    piece = []
    for w in ph:
        trial = " ".join(x["w"] for x in piece + [w])
        if piece and len(trial) > target + 4 and len(chunks) >= 0 and k > 1:
            chunks.append(piece); piece = []
        piece.append(w)
    chunks.append(piece)

caps = []
for i, c in enumerate(chunks):
    s = c[0]["s"]
    e = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else c[-1]["e"] + 0.6
    if e - c[-1]["e"] > 0.6:  # don't hold through long pauses
        e = c[-1]["e"] + 0.4
    txt = " ".join(x["w"] for x in c).upper().replace(" -", "-")
    txt = txt.rstrip(",.")  # brand style: no trailing commas/periods
    caps.append({"i": i + 1, "s": round(s, 3), "e": round(e, 3), "t": txt})

def outlined(draw, xy, text, font, fill, stroke, sw):
    draw.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor="mm")

def fit_font(text, size, maxw, path=ANTON):
    while True:
        f = ImageFont.truetype(path, size)
        if f.getlength(text) <= maxw or size <= 16: return f
        size -= 4

CAP_Y = 1330  # lower third, inside the 4:5 safe zone (285..1635)
for c in caps:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = fit_font(c["t"], 120, 940)
    outlined(d, (W / 2, CAP_Y), c["t"], f, "white", "black", 9)
    c["png"] = f"captions/cap_{c['i']:03d}.png"
    im.save(f"{out}/{c['png']}")

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
with open(f"{out}/captions.srt", "w") as fh:
    for c in caps:
        fh.write(f"{c['i']}\n{ts(c['s'])} --> {ts(c['e'])}\n{c['t']}\n\n")

# ---------- graphics ----------
G = []
def gfx(name, s, e, draw_fn):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(im), im)
    im.save(f"{out}/graphics/{name}.png")
    G.append({"name": name, "png": f"graphics/{name}.png", "s": s, "e": e})

def title(d, im):
    outlined(d, (W / 2, 335), "WHY CREATINE", ImageFont.truetype(ANTON, 104), "white", "black", 8)
    outlined(d, (W / 2, 440), "MAKES YOU BLOAT", ImageFont.truetype(ANTON, 82), "white", "black", 7)
gfx("title_why_bloat", 2.55, 8.15, title)

NAVY, PINK, GREEN = (31, 42, 92), (242, 167, 195), (46, 160, 90)
badges = [(["NON-GMO"], 42.42), (["VEGAN"], 43.56), (["NO ARTIFICIAL", "INGREDIENTS"], 44.38),
          (["BIOPERINE", "HELPS NUTRIENT", "ABSORPTION"], 46.84)]
BW, BH = 470, 190
slots = [(55, 330), (555, 330), (55, 540), (555, 540)]
for k, ((lines, t0), (x, y)) in enumerate(zip(badges, slots)):
    def draw_badge(d, im, lines=lines, x=x, y=y):
        d.rounded_rectangle((x + 6, y + 8, x + BW + 6, y + BH + 8), 40, fill=(0, 0, 0, 90))
        d.rounded_rectangle((x, y, x + BW, y + BH), 40, fill="white", outline=PINK, width=8)
        cx, cy, r = x + 80, y + BH / 2, 50
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN)
        d.line([(cx - 24, cy + 2), (cx - 6, cy + 22), (cx + 26, cy - 20)], fill="white", width=12, joint="curve")
        tx, maxw = x + 150, BW - 175
        fonts = [fit_font(lines[0], 66 if len(lines) == 1 else 56, maxw)] + [fit_font(l, 36, maxw) for l in lines[1:]]
        heights = [f.size * 1.08 for f in fonts]
        ty = cy - sum(heights) / 2
        for l, f, h in zip(lines, fonts, heights):
            d.text((tx, ty + h / 2), l, font=f, fill=NAVY, anchor="lm"); ty += h
    gfx(f"icon_{k+1}_{lines[0].split()[0].lower().replace('-', '')}", t0 - 0.05, 51.0, draw_badge)

def guarantee(d, im):
    outlined(d, (W / 2, 350), "30-DAY MONEY-BACK", ImageFont.truetype(ANTON, 108), "white", "black", 9)
    outlined(d, (W / 2, 475), "GUARANTEE", ImageFont.truetype(ANTON, 132), "white", "black", 10)
gfx("guarantee", 65.0, 70.6, guarantee)

json.dump({"captions": caps, "graphics": G}, open(f"{out}/overlays.json", "w"), indent=1)
print(len(caps), "captions;", len(G), "graphics")
for c in caps: print(f"{c['s']:6.2f}-{c['e']:6.2f}  {c['t']}")

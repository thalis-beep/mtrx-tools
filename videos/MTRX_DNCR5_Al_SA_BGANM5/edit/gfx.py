# Builds the V1 graphics (1080x1920 RGBA overlays and full-frame cards) with PIL.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gfx")
W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w, s): return ImageFont.truetype(F % w, s)
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
NAVY, CREAM, AMBER = (24, 32, 66), (250, 245, 236), (242, 170, 60)

def card(h):
    """Rounded translucent card in the lower-middle safe area; returns (img, draw, top-left)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, y0 = 70, 1560 - h
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 10, W - x0, y0 + h + 10], 40, fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, W - x0, y0 + h], 40, fill=CREAM + (238,))
    return im, d, x0, y0

def centered(d, y, text, f, fill):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill)

# ATP graphic 1: creatine drops after 40
im, d, x0, y0 = card(470)
centered(d, y0 + 40, "After 40, creatine levels drop", font("Bold", 50), NAVY)
cx0, cy0, cx1, cy1 = x0 + 90, y0 + 140, W - x0 - 70, y0 + 380
d.line([cx0, cy1, cx1, cy1], fill=NAVY + (120,), width=3)
pts = [(0, .1), (.35, .12), (.5, .2), (.65, .45), (.8, .7), (1, .85)]
xy = [(cx0 + p * (cx1 - cx0), cy0 + q * (cy1 - cy0)) for p, q in pts]
poly = xy + [(cx1, cy1), (cx0, cy1)]
d.polygon(poly, fill=(248, 222, 178, 255))
d.line(xy, fill=AMBER, width=10, joint="curve")
for (px, py) in (xy[0], xy[-1]): d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=AMBER)
xa = cx0 + .5 * (cx1 - cx0)
d.line([xa, cy0 - 10, xa, cy1], fill=NAVY + (90,), width=3)
for lab, p in (("20", 0), ("40", .5), ("60+", 1)):
    f = font("SemiBold", 34); w = d.textlength(lab, font=f)
    d.text((cx0 + p * (cx1 - cx0) - w / 2, cy1 + 14), lab, font=f, fill=NAVY)
d.text((cx0, cy0 - 30), "CREATINE", font=font("SemiBold", 28), fill=NAVY + (170,))
im.save(f"{D}/atp1.png")

# ATP graphic 2: creatine -> ATP -> muscles + brain
im, d, x0, y0 = card(470)
centered(d, y0 + 40, "Creatine is your cells' fuel", font("Bold", 50), NAVY)
def pill(cx, cy, text, fill, tc):
    f = font("Bold", 40); w = d.textlength(text, font=f)
    d.rounded_rectangle([cx - w / 2 - 34, cy - 40, cx + w / 2 + 34, cy + 40], 40, fill=fill)
    d.text((cx - w / 2, cy - 25), text, font=f, fill=tc)
row = y0 + 190
pill(300, row, "CREATINE", NAVY, CREAM)
d.text((475, row - 38), "→", font=font("Bold", 60), fill=NAVY)
pill(720, row, "ATP ENERGY", AMBER, NAVY)
row2 = y0 + 340
for cx, emo, lab in ((380, "💪", "Muscles"), (700, "🧠", "Brain")):
    e = Image.new("RGBA", (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), emo, font=EMOJI, embedded_color=True)
    e = e.resize((80, 80), Image.LANCZOS); im.alpha_composite(e, (int(cx - 150), int(row2 - 40)))
    d.text((cx - 55, row2 - 26), lab, font=font("Bold", 44), fill=NAVY)
im.save(f"{D}/atp2.png")

# Callout pills (stacked, appear one at a time over the product hero)
calls = ["Zero sugar", "Zero calories", "Non-GMO", "Plant-based", "Keto & paleo-friendly"]
for i in range(len(calls)):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for j, t in enumerate(calls[: i + 1]):
        f = font("Bold", 38); w = d.textlength("✓  " + t, font=f)
        y = 290 + j * 86
        d.rounded_rectangle([W / 2 - w / 2 - 32, y, W / 2 + w / 2 + 32, y + 72], 36, fill=CREAM + (240,), outline=AMBER, width=4)
        d.text((W / 2 - w / 2, y + 14), "✓  " + t, font=f, fill=NAVY)
    im.save(f"{D}/callout{i + 1}.png")

# "3 months later" title card
im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
centered(d, 900, "3 months later", font("Medium", 76), (245, 240, 230))
im.save(f"{D}/title_3months.png")

# Closing black cards: lines accumulate one at a time
lines = ["For all the moms out there...", "Listen to your body.", "And your daughters.", "Get Nectar Creatine today."]
for i in range(len(lines)):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    for j, t in enumerate(lines[: i + 1]):
        f = font("SemiBold" if j < 3 else "Bold", 62); y = 690 + j * 130
        w = d.textlength(t, font=f) + (95 if j == 2 else 0)
        d.text(((W - w) / 2, y), t, font=f, fill=(245, 240, 230) if j < 3 else AMBER)
        if j == 2:
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), "😉", font=EMOJI, embedded_color=True)
            e = e.resize((72, 72), Image.LANCZOS); im.paste(e, (int((W - w) / 2 + w - 75), y - 2), e)
    im.save(f"{D}/black{i + 1}.png")

# End card: real pouch photo + 30-day guarantee
im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
bag = Image.open(os.environ["BAG"]).convert("RGB")
bag = bag.resize((760, int(760 * bag.height / bag.width)), Image.LANCZOS)
m = Image.new("L", bag.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, *bag.size], 36, fill=255)
by = 300; im.paste(bag, ((W - bag.width) // 2, by), m)
centered(d, by + bag.height + 70, "Nectar Creatine Variety Pack", font("Bold", 56), CREAM)
gy = by + bag.height + 175
f = font("Bold", 46); t = "30-DAY MONEY-BACK GUARANTEE"; w = d.textlength(t, font=f)
d.rounded_rectangle([(W - w) / 2 - 40, gy, (W + w) / 2 + 40, gy + 96], 48, fill=AMBER)
d.text(((W - w) / 2, gy + 20), t, font=f, fill=NAVY)
im.save(f"{D}/endcard.png")
print("ok")

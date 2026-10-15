"""Draw a reusable 9:16 safe-zone guide overlay (transparent PNG, 1080x1920).

Zones (top to bottom of priority):
  - 4:5 safe zone, 1080x1350, centred (y 285-1635): all information goes here,
    so the ad survives a 4:5 crop in feed placements.
  - Title-safe margin, 60 px inside the 4:5 zone's sides: keeps type off the edges.
  - Approximate platform UI (Reels / TikTok / Shorts): header, right action rail,
    caption + CTA area. Exact sizes vary by app and device, so these are hatched as cautions.
Outside the 4:5 zone is tinted so it reads as "background only".

usage: python3 make_safe_zone_overlay.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SAFE = (0, 285, 1080, 1635)          # 4:5 zone
TITLE = (60, 285, 1020, 1635)        # title-safe columns inside it
HEADER = (0, 0, 1080, 220)           # account / platform header (approx.)
FOOTER = (0, 1600, 1080, 1920)       # caption, audio, CTA, nav (approx.)
RAIL = (960, 1000, 1080, 1600)       # like / comment / share rail (approx.)
CYAN = (0, 229, 255)
RED = (255, 72, 72)
WHITE = (255, 255, 255)

FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
f_big = ImageFont.truetype(FONT, 30)
f_med = ImageFont.truetype(FONT, 22)
f_small = ImageFont.truetype(FONT_MED, 18)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def hatch(base, box, color, step=22, width=2):
    """Diagonal hatching clipped to box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    for k in range(-h, w, step):
        d.line([(k, h), (k + h, 0)], fill=color, width=width)
    base.alpha_composite(tile, (x0, y0))


def dashed_rect(d, box, color, dash=16, gap=10, width=2):
    x0, y0, x1, y1 = box
    for a, b, horiz, fixed in [(x0, x1, True, y0), (x0, x1, True, y1), (y0, y1, False, x0), (y0, y1, False, x1)]:
        p = a
        while p < b:
            q = min(p + dash, b)
            d.line([(p, fixed), (q, fixed)] if horiz else [(fixed, p), (fixed, q)], fill=color, width=width)
            p = q + gap


def tag(d, xy, text, font, fg, bg, anchor="la", pad=(10, 6)):
    l, t, r, b = d.textbbox(xy, text, font=font, anchor=anchor)
    d.rounded_rectangle([l - pad[0], t - pad[1], r + pad[0], b + pad[1]], radius=6, fill=bg)
    d.text(xy, text, font=font, fill=fg, anchor=anchor)


# 1. tint everything outside the 4:5 zone
tint = layer()
td = ImageDraw.Draw(tint)
td.rectangle([0, 0, W, SAFE[1]], fill=(0, 0, 0, 120))
td.rectangle([0, SAFE[3], W, H], fill=(0, 0, 0, 120))
img = Image.alpha_composite(img, tint)

# 2. platform UI cautions (hatched red)
ui = layer()
ud = ImageDraw.Draw(ui)
for box in (HEADER, FOOTER, RAIL):
    ud.rectangle(box, fill=(*RED, 38))
    hatch(ui, box, (*RED, 70))
    ud.rectangle(box, outline=(*RED, 170), width=2)
img = Image.alpha_composite(img, ui)

# 3. guides
g = layer()
gd = ImageDraw.Draw(g)
gd.rectangle(SAFE, outline=(*CYAN, 255), width=4)
dashed_rect(gd, TITLE, (*WHITE, 150))
cx, cy = W // 2, (SAFE[1] + SAFE[3]) // 2
gd.line([(cx - 26, cy), (cx + 26, cy)], fill=(*CYAN, 200), width=2)
gd.line([(cx, cy - 26), (cx, cy + 26)], fill=(*CYAN, 200), width=2)
for y in (SAFE[1], SAFE[3]):                        # corner ticks for quick alignment
    for x in (0, W):
        sx = 1 if x == 0 else -1
        sy = 1 if y == SAFE[1] else -1
        gd.line([(x, y), (x + sx * 70, y)], fill=(*CYAN, 255), width=8)
        gd.line([(x + sx * 4, y), (x + sx * 4, y + sy * 70)], fill=(*CYAN, 255), width=8)
img = Image.alpha_composite(img, g)

# 4. labels
t = layer()
d = ImageDraw.Draw(t)
# labels sit just outside the zone so they never cover the artwork being checked
tag(d, (W - 24, SAFE[1] - 18), "4:5 SAFE ZONE  ·  1080 × 1350", f_med, (0, 0, 0, 255), (*CYAN, 235), anchor="rd")
tag(d, (W - 24, SAFE[3] + 18), "KEEP ALL TEXT, OFFER & LOGO INSIDE", f_small, (0, 0, 0, 255), (*CYAN, 235), anchor="ra")
tag(d, (TITLE[0] + 10, cy), "60px", f_small, (*WHITE, 255), (0, 0, 0, 170), anchor="lm")
tag(d, (TITLE[2] - 10, cy), "60px", f_small, (*WHITE, 255), (0, 0, 0, 170), anchor="rm")
tag(d, (W // 2, 110), "PLATFORM HEADER (approx.)", f_med, (*WHITE, 255), (*RED, 220), anchor="mm")
tag(d, (W // 2, 1790), "CAPTION · AUDIO · CTA · NAV (approx.)", f_med, (*WHITE, 255), (*RED, 220), anchor="mm")
rail = Image.new("RGBA", (500, 60), (0, 0, 0, 0))
rd = ImageDraw.Draw(rail)
tag(rd, (250, 30), "ACTION RAIL (approx.)", f_small, (*WHITE, 255), (*RED, 220), anchor="mm")
rail = rail.rotate(90, expand=True)
t.alpha_composite(rail, ((RAIL[0] + RAIL[2]) // 2 - 30, (RAIL[1] + RAIL[3]) // 2 - 250))
tag(d, (24, SAFE[1] - 20), "BACKGROUND ONLY", f_small, (*WHITE, 230), (0, 0, 0, 0), anchor="ld")
tag(d, (24, SAFE[3] + 20), "BACKGROUND ONLY", f_small, (*WHITE, 230), (0, 0, 0, 0), anchor="la")
tag(d, (W - 24, H - 24), "9:16  ·  1080 × 1920", f_small, (*WHITE, 230), (0, 0, 0, 160), anchor="rd")
img = Image.alpha_composite(img, t)

out = sys.argv[1] if len(sys.argv) > 1 else "safe-zone-9x16-4x5.png"
img.save(out, optimize=True)
print(out, img.size)

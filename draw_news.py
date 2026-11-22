#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Written from scratch in the build session for news-image-20261122.
No network, no external assets: every pixel is drawn here with PIL.
Run: python3 draw_news.py  -> writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (18, 35, 63)
RED = (179, 32, 44)
GOLD = (201, 162, 39)
TEAL = (14, 107, 107)
MUTED = (90, 86, 76)
SKY = (24, 38, 66)
ORANGE = (232, 122, 42)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, width, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 132], fill=NAVY)
d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=font(SERIF, 54),
       fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 80), "S U N D A Y   2 2   N O V E M B E R   2 0 2 6",
       font=font(SANS_B, 24), fill=GOLD, anchor="ma")
d.rectangle([0, 132, W, 136], fill=GOLD)

# ---- lead story: Middle East ----
y = 146
d.text((24, y), "MIDDLE EAST  •  ESCALATION", font=font(SANS_B, 23), fill=RED)
y = para(d, 24, 176, "Iran strikes US bases\nin Bahrain and Kuwait",
         font(SERIF, 44), INK, 560, leading=52)
y = para(d, 24, y + 8,
         "IRGC missiles and drones hit US Patriot radars; "
         "Washington warns Tehran as Gulf tensions hit a new high.",
         font(SANS, 22), MUTED, 560, leading=30)

# lead illustration: night sky, missile arcs, radar dome
ix0, iy0, ix1, iy1 = 612, 146, 1000, 430
d.rectangle([ix0, iy0, ix1, iy1], fill=SKY)
d.rectangle([ix0, iy0, ix1, iy1], outline=NAVY, width=2)
# stars
for (sx, sy, r) in [(650, 200, 2), (700, 185, 2), (760, 210, 3), (830, 190, 2),
                    (900, 205, 2), (960, 185, 3), (680, 240, 2), (940, 240, 2)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
# missile trails
d.arc([640, 210, 900, 420], 200, 330, fill=ORANGE, width=5)
d.arc([700, 230, 960, 430], 200, 330, fill=(255, 200, 90), width=4)
d.ellipse([868, 300, 884, 316], fill=(255, 230, 150))
d.ellipse([928, 322, 942, 336], fill=(255, 230, 150))
# ground + radar dome + buildings
d.rectangle([ix0, 380, ix1, iy1], fill=(12, 20, 38))
d.rectangle([640, 340, 700, 380], fill=(40, 55, 85))
d.rectangle([720, 320, 760, 380], fill=(40, 55, 85))
d.pieslice([800, 310, 880, 390], 180, 360, fill=(120, 130, 150))
d.rectangle([836, 360, 844, 380], fill=(120, 130, 150))
d.rectangle([900, 350, 970, 380], fill=(40, 55, 85))
d.text((ix0 + 10, iy1 - 30), "GULF  •  US BASES UNDER FIRE",
       font=font(SANS_B, 17), fill=(255, 255, 255))

d.line([24, 446, 1000, 446], fill=(200, 192, 172), width=2)

# ---- row 2: Ukraine | Peru ----
def story(x, y, w, kicker, kcolor, head, body, art, art_h=64,
          head_size=28, body_size=19):
    d.text((x, y), kicker, font=font(SANS_B, 20), fill=kcolor)
    art(x, y + 28, w, art_h)
    yy = para(d, x, y + 28 + art_h + 10, head, font(SERIF, head_size),
              INK, w, leading=head_size + 6)
    para(d, x, yy + 6, body, font(SANS, body_size), MUTED, w,
         leading=body_size + 6)


def art_explosion(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 48, 44))
    cx, cy = x + w // 2 - 60, y + h // 2
    for r, c in [(28, ORANGE), (19, (255, 200, 90)), (10, (255, 240, 180))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 26, 24))
    d.text((x + 8, y + 6), "KYIV  •  LVIV  •  BALTIC SEA",
           font=font(SANS_B, 15), fill=(255, 255, 255))


def art_quake(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 160))
    d.polygon([(x, y + h), (x + 90, y + 8), (x + 170, y + h)], fill=(120, 100, 80))
    d.polygon([(x + 130, y + h), (x + 250, y + 2), (x + 360, y + h)],
              fill=(90, 76, 60))
    d.polygon([(x + 300, y + h), (x + 400, y + 14), (x + w, y + h)],
              fill=(120, 100, 80))
    d.arc([x + 30, y - 6, x + w - 30, y + 60], 0, 180, fill=RED, width=4)
    d.arc([x + 70, y + 6, x + w - 70, y + 72], 0, 180, fill=RED, width=3)


story(24, 462, 472, "UKRAINE  •  WAR SPILLS OVER", RED,
      "Missiles hit Lviv; drones strike Baltic ship",
      "Two killed in Lviv; debris crashes in Poland; Finland "
      "tightens security.",
      art_explosion)
story(528, 462, 472, "PERU  •  EARTHQUAKE", TEAL,
      "Magnitude 6.9 quake shakes the Andes",
      "Strong tremor rattles the Andes; no damage or casualties "
      "reported.",
      art_quake)

d.line([24, 700, 1000, 700], fill=(200, 192, 172), width=2)

# ---- row 3: COP31 | EU-Indonesia trade ----
def art_climate(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 90, 84))
    d.ellipse([x + w // 2 - 22, y + 6, x + w // 2 + 22, y + 50], fill=(140, 210, 190))
    d.arc([x + w // 2 - 29, y - 1, x + w // 2 + 29, y + 57], 0, 360,
          fill=(255, 255, 255), width=3)
    d.rectangle([x + 40, y + h - 22, x + 90, y + h], fill=(240, 240, 240))
    d.rectangle([x + 110, y + h - 22, x + 150, y + h], fill=(240, 240, 240))


def art_trade(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 120))
    # EU circle of stars
    cx, cy = x + 110, y + h // 2
    for i in range(12):
        import math
        a = math.radians(i * 30)
        sx, sy = cx + 30 * math.cos(a), cy + 22 * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 60))
    # Indonesia red-white flag
    fx = x + 260
    d.rectangle([fx, y + 8, fx + 130, y + 29], fill=(200, 30, 40))
    d.rectangle([fx, y + 29, fx + 130, y + 50], fill=(255, 255, 255))


story(24, 716, 472, "CLIMATE  •  COP31", TEAL,
      "Fossil-fuel fight leaves COP31 in deadlock",
      "Negotiators split over phase-out language as the summit "
      "runs into trouble.",
      art_climate, art_h=58, head_size=27)
story(528, 716, 472, "TRADE  •  EU–INDONESIA", NAVY,
      "EU and Indonesia sign deal after ten years",
      "Pact scraps 98.5% of tariffs between Brussels and "
      "Southeast Asia's largest economy.",
      art_trade, art_h=58, head_size=27)

# ---- ticker band ----
d.rectangle([0, 946, W, 996], fill=NAVY)
d.text((24, 958), "ALSO TODAY:",
       font=font(SANS_B, 19), fill=GOLD)
d.text((185, 958),
       "Mexico arrests cartel boss 'El Chapo Isidro'; 11 die in Sinaloa  •  "
       "Hong Kong votes",
       font=font(SANS, 18), fill=(255, 255, 255))
d.text((24, 978),
       "Trump meets Xi in Shenzhen  •  Bolsonaro in ICU  •  Myanmar quake 4.1",
       font=font(SANS, 18), fill=(200, 205, 215))

d.text((W // 2, 1004), "22 NOVEMBER 2026  •  THE DAY IN ONE IMAGE",
       font=font(SANS_B, 16), fill=MUTED, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, "bytes:", len(open("entry.png", "rb").read()))

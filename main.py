#!/usr/bin/env python3
"""news-image-20261124 — THE WORLD IN ONE DAY, Tuesday 24 November 2026.

Renders a 1024x1024 front page (PIL, no network, deterministic) summarising
the day's world news and writes it to /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)      # cream paper
INK = (26, 26, 26)           # near-black ink
RED = (139, 26, 26)          # dark red accent
GREY = (110, 105, 95)        # muted grey
LIGHT = (233, 226, 210)      # light panel
BLUE = (31, 58, 95)          # deep blue for map sea

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

LEAD = {
    "kicker": "TECH  ·  MARKETS",
    "head": "HUANG IS BACK",
    "sub": ("Nvidia reinstates Jensen Huang as chief executive after "
            "Trump intervenes; shares jump 31%."),
    "num": "1",
}

# 12 illustrated cards: (num, region, headline, sub, icon) — sub fits one line
CARDS = [
    ("2", "LIBYA", "Ukraine sinks Russian warship off Libya",
     "Seven naval drones sink the corvette Merkury.", "ship"),
    ("3", "GULF", "Three tankers hit mines in the Strait of Hormuz",
     "Iran vows to use every tool against the blockade.", "tanker"),
    ("4", "UKRAINE", "Russian strike on Zaporizhzhia kills two",
     "An apartment block hit; 22 wounded, children too.", "building"),
    ("5", "GAZA", "Israeli strikes kill Hamas security chief",
     "Naeem Abu Nahel dies with six others, a UN worker.", "pin"),
    ("6", "WASHINGTON", "Democrats take the House by a record margin",
     "The party wins the chamber by its widest margin.", "ballot"),
    ("7", "SPACE", "China opens its station to a foreign astronaut",
     "Pakistan's Zeeshan Ali will fly to Tiangong.", "rocket"),
    ("8", "INDONESIA", "Factory fire kills 26 in Banten",
     "Dozens missing after a blaze sweeps a plant.", "flame"),
    ("9", "SENEGAL", "175 migrants missing after boat loses contact",
     "A Europe-bound boat out of Dakar vanishes.", "boat"),
    ("10", "BRUSSELS", "EU readies 22nd sanctions package on Russia",
     "The round targets travel and sport; visas limited.", "flag"),
    ("11", "MADRID", "Spain amnesties Puigdemont",
     "The Supreme Court ends a nine-year legal battle.", "gavel"),
    ("12", "TOKYO", "Japan pays the ICC in full as US sanctions bite",
     "Tokyo brings forward its whole 2027 contribution.", "scales"),
    ("13", "DHAKA", "Garment workers clash with police over pay",
     "Tear gas in Gazipur as factories shut over wages.", "factory"),
]

# 26 one-line briefs: (num, region, headline)
BRIEFS = [
    ("14", "ESTONIA", "Russia warns Tallinn it is on the verge of open war"),
    ("15", "SEOUL", "Russian jets enter South Korea's air defence zone"),
    ("16", "WARSAW", "Russian drone enters Poland; NATO sends detection jets"),
    ("17", "LONDON", "Britain sanctions the Houthis over Red Sea attacks"),
    ("18", "YEMEN", "Houthis say a Saudi strike kills 17 in Hodeida"),
    ("19", "DR CONGO", "Fighting traps Ebola teams at a hospital in Ituri"),
    ("20", "COLOMBIA", "Car bomb hits the governor's office in Villavicencio"),
    ("21", "MOSCOW", "700,000 Russian soldiers killed, new analysis finds"),
    ("22", "TRIPOLI", "Libya demands answers from Kyiv over ship strikes"),
    ("23", "WASHINGTON", "Trump orders faster federal death sentences"),
    ("24", "OTTAWA", "Pentagon says Canada falls short as a defence partner"),
    ("25", "BERLIN", "Germany first to access Ukraine's Delta battle system"),
    ("26", "NATO", "Rutte: alliance will defend space after satellite report"),
    ("27", "BAGHDAD", "Iraq PM seizes Kurdish oilfields and border posts"),
    ("28", "DHAKA", "Hasina plans to return to Bangladesh on 16 December"),
    ("29", "NEW DELHI", "Nepal PM visits India; 1.4 billion euros pledged"),
    ("30", "PACIFIC", "Solomon Islands ends its security pact with China"),
    ("31", "LONDON", "UK sanctions Myanmar generals after ICJ genocide ruling"),
    ("32", "TEL AVIV", "Netanyahu urges Trump to resume strikes on Iran"),
    ("33", "MARKETS", "S&P 500 +4.7%, Nasdaq +6.5%, Nikkei +3.9%"),
    ("34", "MARKETS", "Brent crude $86.71; gold holds at $3,620"),
    ("35", "BRASILIA", "Lula backs a second package to curb spending"),
    ("36", "WASHINGTON", "US blacklists Singapore cloud firm Megaspeed"),
    ("37", "SEOUL", "Korea pays $375,000 to catch AI exam cheats"),
    ("38", "UNITED NATIONS", "Guterres wants AI risk rules within a year"),
    ("39", "WASHINGTON", "SpaceX sued over Grok child-abuse images"),
    ("40", "KATHMANDU", "Quake 5.6 strikes Nepal near the China border"),
    ("41", "HANOI", "Blast kills 6, injures 10 in a food shop"),
    ("42", "PARIS", "Officer to face murder trial over Nahel shooting"),
    ("43", "PENNSYLVANIA", "Measles claims a ninth life in the state"),
    ("44", "BEIJING", "China probes Politburo member Chen Jining"),
    ("45", "MEXICO CITY", "Mexico to try 'Chapo Isidro' despite the US"),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines fitting width."""
    words = text.split()
    lines, cur = [], ""
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


def draw_icon(d, kind, x, y, s, col):
    """Small vector pictogram inside a square of side s at (x, y)."""
    if kind == "ship":
        d.polygon([(x, y + s * .55), (x + s * .95, y + s * .55),
                   (x + s * .8, y + s * .9), (x + s * .15, y + s * .9)], fill=col)
        d.rectangle([x + s * .42, y + s * .1, x + s * .52, y + s * .55], fill=col)
        d.polygon([(x + s * .52, y + s * .12), (x + s * .85, y + s * .38),
                   (x + s * .52, y + s * .38)], fill=col)
    elif kind == "tanker":
        d.rectangle([x, y + s * .4, x + s, y + s * .75], fill=col)
        d.rectangle([x + s * .72, y + s * .18, x + s * .9, y + s * .4], fill=col)
        for i in range(3):
            d.ellipse([x + s * (.15 + i * .28), y + s * .2,
                       x + s * (.25 + i * .28), y + s * .32], fill=col)
    elif kind == "building":
        d.rectangle([x + s * .12, y + s * .25, x + s * .88, y + s * .95], fill=col)
        for r in range(3):
            for c in range(3):
                d.rectangle([x + s * (.22 + c * .24), y + s * (.35 + r * .2),
                             x + s * (.32 + c * .24), y + s * (.45 + r * .2)],
                            fill=PAPER)
    elif kind == "pin":
        d.ellipse([x + s * .25, y + s * .08, x + s * .75, y + s * .58], fill=col)
        d.polygon([(x + s * .28, y + s * .45), (x + s * .72, y + s * .45),
                   (x + s * .5, y + s * .95)], fill=col)
        d.ellipse([x + s * .4, y + s * .23, x + s * .6, y + s * .43], fill=PAPER)
    elif kind == "ballot":
        d.rectangle([x + s * .1, y + s * .18, x + s * .9, y + s * .92],
                    outline=col, width=4)
        d.line([(x + s * .22, y + s * .58), (x + s * .42, y + s * .78),
                (x + s * .8, y + s * .3)], fill=col, width=5)
    elif kind == "rocket":
        d.polygon([(x + s * .5, y + s * .05), (x + s * .72, y + s * .45),
                   (x + s * .5, y + s * .62), (x + s * .28, y + s * .45)],
                  fill=col)
        d.polygon([(x + s * .28, y + s * .5), (x + s * .1, y + s * .85),
                   (x + s * .38, y + s * .68)], fill=col)
        d.polygon([(x + s * .72, y + s * .5), (x + s * .9, y + s * .85),
                   (x + s * .62, y + s * .68)], fill=col)
        d.ellipse([x + s * .4, y + s * .68, x + s * .6, y + s * .95], fill=RED)
    elif kind == "flame":
        d.polygon([(x + s * .5, y + s * .05), (x + s * .78, y + s * .45),
                   (x + s * .68, y + s * .6), (x + s * .85, y + s * .75),
                   (x + s * .5, y + s * .95), (x + s * .15, y + s * .75),
                   (x + s * .32, y + s * .6), (x + s * .22, y + s * .45)],
                  fill=col)
    elif kind == "boat":
        d.polygon([(x + s * .05, y + s * .6), (x + s * .95, y + s * .6),
                   (x + s * .8, y + s * .9), (x + s * .2, y + s * .9)], fill=col)
        d.rectangle([x + s * .45, y + s * .15, x + s * .55, y + s * .6], fill=col)
        d.polygon([(x + s * .55, y + s * .18), (x + s * .88, y + s * .5),
                   (x + s * .55, y + s * .5)], fill=col)
    elif kind == "flag":
        d.rectangle([x + s * .15, y + s * .08, x + s * .25, y + s * .95], fill=col)
        d.polygon([(x + s * .25, y + s * .08), (x + s * .92, y + s * .08),
                   (x + s * .92, y + s * .5), (x + s * .25, y + s * .5)], fill=col)
        d.ellipse([x + s * .5, y + s * .2, x + s * .66, y + s * .36], fill=PAPER)
    elif kind == "gavel":
        d.rectangle([x + s * .2, y + s * .15, x + s * .8, y + s * .38], fill=col)
        d.rectangle([x + s * .45, y + s * .38, x + s * .55, y + s * .85], fill=col)
        d.rectangle([x + s * .2, y + s * .85, x + s * .8, y + s * .95], fill=col)
    elif kind == "scales":
        d.line([(x + s * .5, y + s * .1), (x + s * .5, y + s * .9)], fill=col, width=4)
        d.line([(x + s * .15, y + s * .28), (x + s * .85, y + s * .28)], fill=col, width=4)
        d.polygon([(x + s * .05, y + s * .32), (x + s * .25, y + s * .32),
                   (x + s * .15, y + s * .55)], fill=col)
        d.polygon([(x + s * .75, y + s * .32), (x + s * .95, y + s * .32),
                   (x + s * .85, y + s * .55)], fill=col)
    elif kind == "factory":
        d.polygon([(x + s * .05, y + s * .95), (x + s * .05, y + s * .4),
                   (x + s * .25, y + s * .4), (x + s * .25, y + s * .55),
                   (x + s * .45, y + s * .55), (x + s * .45, y + s * .4),
                   (x + s * .95, y + s * .4), (x + s * .95, y + s * .95)],
                  fill=col)
        d.rectangle([x + s * .68, y + s * .1, x + s * .78, y + s * .4], fill=col)
    elif kind == "chip":
        d.rectangle([x, y, x + s, y + s], fill=col)
        for i in range(3):
            d.rectangle([x + s * .18, y + s * (.15 + i * .28),
                         x + s * .82, y + s * (.25 + i * .28)], fill=PAPER)
        d.rectangle([x + s * .38, y + s * .38, x + s * .62, y + s * .62], fill=RED)


# Simplified world map: rough continent polygons in a (x, y, w, h) box.
# Coordinates are fractions of the map box; land is dark, sea is blue.
CONTINENTS = [
    # North America
    [(0.03, 0.30), (0.10, 0.10), (0.20, 0.08), (0.26, 0.22), (0.22, 0.38),
     (0.16, 0.52), (0.10, 0.48), (0.05, 0.40)],
    # South America
    [(0.20, 0.55), (0.26, 0.52), (0.30, 0.62), (0.27, 0.85), (0.23, 0.92),
     (0.20, 0.72)],
    # Europe
    [(0.44, 0.12), (0.50, 0.08), (0.55, 0.16), (0.52, 0.28), (0.46, 0.28),
     (0.43, 0.20)],
    # Africa
    [(0.44, 0.34), (0.52, 0.32), (0.57, 0.42), (0.54, 0.62), (0.49, 0.78),
     (0.45, 0.62), (0.42, 0.45)],
    # Asia
    [(0.55, 0.08), (0.72, 0.06), (0.88, 0.12), (0.92, 0.30), (0.82, 0.42),
     (0.72, 0.38), (0.64, 0.48), (0.58, 0.32), (0.53, 0.18)],
    # Australia
    [(0.78, 0.68), (0.88, 0.66), (0.90, 0.78), (0.80, 0.82), (0.76, 0.74)],
]

# Map dots: (num, x-frac, y-frac) — key story locations, spread out.
MAP_DOTS = [
    ("1", 0.10, 0.28), ("2", 0.50, 0.45), ("3", 0.60, 0.40),
    ("4", 0.53, 0.22), ("5", 0.54, 0.38), ("6", 0.16, 0.35),
    ("7", 0.80, 0.22), ("8", 0.86, 0.52), ("9", 0.44, 0.48),
    ("10", 0.47, 0.15), ("11", 0.43, 0.28), ("12", 0.86, 0.22),
    ("13", 0.72, 0.30),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=BLUE)
    for poly in CONTINENTS:
        pts = [(x + px * w, y + py * h) for px, py in poly]
        d.polygon(pts, fill=(214, 205, 182))
    for num, fx, fy in MAP_DOTS:
        cx, cy = x + fx * w, y + fy * h
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        f = F_SANS_B(10)
        tw = d.textlength(num, font=f)
        d.text((cx - tw / 2, cy - 5), num, font=f, fill=(255, 255, 255))


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # ---- Masthead ----
    d.text((mx, 14), "THE WORLD IN ONE DAY", font=F_SERIF_B(44), fill=INK)
    d.text((W - mx - d.textlength("No. 24 — 2026", font=F_SANS(16)),
            30), "No. 24 — 2026", font=F_SANS(16), fill=GREY)
    d.line([(mx, 66), (W - mx, 66)], fill=INK, width=3)
    d.text((mx, 74), "TUESDAY  24  NOVEMBER  2026", font=F_SANS_B(34), fill=RED)
    d.text((W - mx - d.textlength("45 STORIES  ·  9 REGIONS", font=F_SANS_B(14)),
            82), "45 STORIES  ·  9 REGIONS", font=F_SANS_B(14), fill=INK)
    d.line([(mx, 112), (W - mx, 112)], fill=INK, width=2)

    # ---- Lead panel + markets box ----
    ly, lh = 124, 164
    d.rectangle([mx, ly, W - mx, ly + lh], fill=LIGHT)
    d.rectangle([mx, ly, mx + 8, ly + lh], fill=RED)
    d.text((mx + 22, ly + 10), LEAD["kicker"], font=F_SANS_B(13), fill=RED)
    d.text((mx + 22, ly + 30), LEAD["head"], font=F_SERIF_B(46), fill=INK)
    sub_lines = wrap(d, LEAD["sub"], F_SERIF(20), 560)
    yy = ly + 84
    for ln in sub_lines:
        d.text((mx + 22, yy), ln, font=F_SERIF(20), fill=INK)
        yy += 26
    draw_icon(d, "chip", 648, ly + 28, 84, INK)
    d.text((648, ly + 120), "NVIDIA  +31%  IN A DAY",
           font=F_SANS_B(13), fill=RED)
    d.line([(mx + 22, ly + lh - 30), (W - mx - 22, ly + lh - 30)], fill=GREY, width=1)
    d.text((mx + 22, ly + lh - 24),
           "S&P 500  7,237  +4.73%    Nasdaq  24,090  +6.51%    Nikkei  58,645  +3.91%    Brent  $86.71    Gold  $3,620",
           font=F_SANS_B(13), fill=INK)

    # ---- Illustrated grid: 3 cols x 4 rows ----
    gy, gh = 300, 280
    cw = (W - 2 * mx - 16) // 3
    ch = (gh - 18) // 4
    for i, (num, region, head, sub, icon) in enumerate(CARDS):
        r, c = divmod(i, 3)
        x = mx + c * (cw + 8)
        y = gy + r * (ch + 6)
        d.rectangle([x, y, x + cw, y + ch], outline=GREY, width=1)
        d.text((x + 8, y + 5), num, font=F_SANS_B(13), fill=RED)
        d.text((x + 30, y + 5), region, font=F_SANS_B(12), fill=GREY)
        draw_icon(d, icon, x + 8, y + 22, 26, INK)
        head_lines = wrap(d, head, F_SANS_B(13), cw - 48)
        yy = y + 20
        for ln in head_lines[:2]:
            d.text((x + 40, yy), ln, font=F_SANS_B(13), fill=INK)
            yy += 14
        d.text((x + 8, y + ch - 16), sub, font=F_SANS(11), fill=INK)

    # ---- Briefs: two columns ----
    by = gy + gh + 12
    d.text((mx, by), "THE DAY IN BRIEF", font=F_SANS_B(15), fill=RED)
    d.line([(mx, by + 20), (W - mx, by + 20)], fill=INK, width=2)
    col_w = (W - 2 * mx - 20) // 2
    per_col = 16
    for i, (num, region, head) in enumerate(BRIEFS):
        col, row = divmod(i, per_col)
        x = mx + col * (col_w + 20)
        y = by + 28 + row * 14
        d.text((x, y), num, font=F_SANS_B(12), fill=RED)
        d.text((x + 26, y), region + " — " + head, font=F_SANS(12), fill=INK)
    briefs_bottom = by + 28 + per_col * 14

    # ---- World map ----
    my = briefs_bottom + 10
    mh = 88
    d.text((mx, my), "WHERE IT HAPPENED — numbered stories on the map",
           font=F_SANS_B(13), fill=RED)
    draw_map(d, mx, my + 20, W - 2 * mx, mh - 20)

    # ---- Footer: UTC strip + date check ----
    fy = my + mh + 10
    d.rectangle([mx, fy, W - mx, fy + 46], fill=INK)
    d.text((mx + 12, fy + 6),
           "UTC  00:00  LONDON  07:00  ·  08:00  BERLIN  ·  13:30  DELHI  ·  16:00  SINGAPORE  ·  19:00  TOKYO",
           font=F_SANS_B(12), fill=(247, 242, 231))
    d.text((mx + 12, fy + 26),
           "DATE CHECK: every story above was reported on TUESDAY 24 NOVEMBER 2026  ·  Sources: Reuters · AP · AFP · Al Jazeera · OneTurn",
           font=F_SANS(12), fill=(247, 242, 231))
    return img


def main():
    img = render()
    assert img.size == (1024, 1024), "entry must be 1024x1024"
    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG", optimize=True)
    assert os.path.getsize("/output/entry.png") <= 1048576, "entry must be <= 1 MiB"
    # also keep a local copy next to the program for inspection
    img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()

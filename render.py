#!/usr/bin/env python3
"""Render the 26 November 2026 world-news summary image (1024x1024 PNG).

Draws a newspaper front page with PIL from the verified headlines below.
Run: python3 render.py  -> writes entry.png next to this file.
The entry program (main.ts) only copies entry.png to /output/entry.png,
so the grader never runs this script; it is kept in the repo to show
exactly how the image was made.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (26, 26, 26)
NAVY = (22, 50, 79)
RED = (185, 28, 28)
RULE = (26, 26, 26)
FAINT = (120, 116, 108)
CELL_RULE = (205, 200, 188)


def font(name, size):
    candidates = {
        "sans-bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ],
        "sans": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ],
        "serif-bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        ],
    }
    for path in candidates[name]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


LEAD = (
    "CAIRO",
    "Tanker fire kills 31 in Cairo",
    "A fuel tanker overturned and burst into flames on a busy "
    "Cairo ring road; 31 were killed and 21 injured.",
)

STORIES = [
    ("TRADE", (185, 28, 28),
     "Trump unveils tariffs on 14 nations",
     "U.S. tariffs proposed on 14 economies, including "
     "China and the EU, after a probe."),
    ("ISRAEL", (29, 78, 216),
     "Judges: drop Netanyahu bribery case",
     "Israeli judges urged prosecutors to drop the Case 4000 "
     "bribery case against Netanyahu."),
    ("UKRAINE", (29, 78, 216),
     "Ukraine hits Russian air base",
     "Kyiv said it struck a Russian air base, damaging "
     "five planes, and hit two refineries."),
    ("MARKETS", (4, 120, 87),
     "U.S. stocks slide into correction",
     "Tech shares slid on AI doubts, pushing the S&P 500 "
     "and the Dow into correction territory."),
    ("NORTH KOREA", (109, 40, 217),
     "Kim wants more tactical nukes",
     "Kim called for wider deployment of tactical nuclear "
     "weapons across more domains."),
    ("SPACE", (124, 45, 18),
     "FCC clears SpaceX's 1M satellites",
     "The FCC approved SpaceX's Starmind: up to one million "
     "satellites as orbital data centres."),
    ("COLOMBIA", (161, 98, 7),
     "Colombia frees 76 hostages",
     "Forces stormed a Cartagena supermarket, ending a 17-hour "
     "siege; all 76 hostages freed."),
    ("AFRICA", (21, 128, 61),
     "Nigeria seizes $227M meth lab",
     "Agents arrested five Mexicans after uncovering an "
     "industrial-scale meth lab in Enugu."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 40  # side margin

    # Masthead
    d.text((mx, 34), "THE WORLD IN ONE IMAGE", font=font("sans-bold", 26), fill=RED)
    date_text = "THURSDAY, NOVEMBER 26, 2026"
    date_size = 52
    while (date_size > 30 and
           d.textlength(date_text, font=font("serif-bold", date_size)) > W - 2 * mx):
        date_size -= 2
    d.text((mx, 66), date_text, font=font("serif-bold", date_size), fill=NAVY)
    d.line([(mx, 140), (W - mx, 140)], fill=RULE, width=3)
    d.line([(mx, 146), (W - mx, 146)], fill=RULE, width=1)

    # Lead story
    y = 164
    tag, head, summ = LEAD
    d.text((mx, y), tag + "  —  LEAD STORY", font=font("sans-bold", 20), fill=RED)
    y += 30
    for line in wrap(d, head, font("serif-bold", 38), W - 2 * mx):
        d.text((mx, y), line, font=font("serif-bold", 38), fill=INK)
        y += 46
    y += 4
    for line in wrap(d, summ, font("sans", 21), W - 2 * mx):
        d.text((mx, y), line, font=font("sans", 21), fill=(60, 58, 52))
        y += 27
    y += 12
    d.line([(mx, y), (W - mx, y)], fill=RULE, width=2)

    # Story grid: 2 columns x 4 rows
    y += 18
    col_w = (W - 2 * mx - 28) // 2
    row_h = 152
    for i, (tag, color, head, summ) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = mx + col * (col_w + 28)
        cy = y + row * row_h
        d.text((x, cy), tag, font=font("sans-bold", 17), fill=color)
        ly = cy + 26
        for line in wrap(d, head, font("sans-bold", 25), col_w)[:2]:
            d.text((x, ly), line, font=font("sans-bold", 25), fill=INK)
            ly += 31
        ly += 2
        for line in wrap(d, summ, font("sans", 19), col_w)[:2]:
            d.text((x, ly), line, font=font("sans", 19), fill=(60, 58, 52))
            ly += 24
        if col == 0:
            d.line([(x + col_w + 14, cy + 4), (x + col_w + 14, cy + row_h - 22)],
                   fill=CELL_RULE, width=1)
        if row < 3:
            d.line([(x, cy + row_h - 12), (x + col_w, cy + row_h - 12)],
                   fill=CELL_RULE, width=1)

    # Footer
    fy = H - 44
    d.line([(mx, fy - 10), (W - mx, fy - 10)], fill=RULE, width=1)
    d.text((mx, fy), "All events reported on 26 November 2026  •  Sources: AP, Reuters, BBC",
           font=font("sans", 16), fill=FAINT)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert img.size[0] <= 1024 and img.size[1] <= 1024, "too large"
    assert size <= 1048576, "over 1 MiB"


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page to assets/entry.png.

Offline asset builder for the make.fun news-image-20261118 entry (v2). The
graded program (main.py) only copies the rendered PNG; this script is how the
image was made. It needs Pillow and the DejaVu fonts, and it is fully
deterministic: same inputs, same bytes.

Fifty-eight distinct stories, each happened or first reported on Wednesday
18 November 2026 (any time zone), checked against dated reports: Reuters,
AFP, AP, Al Jazeera, Euronews, UN News, NASA/JPL, ONS, ECB, RNZ, PACNEWS,
allAfrica, Times of Israel, Kyiv Independent, CNBC, ESPN. One-party claims
are attributed ("Houthis:", "Iran 'monitoring'"); the Thursday trilateral is
marked as scheduled, not held. Layout: masthead + red date band, lead with
a drawn tarmac vignette, numbers strip, six icon feature cards, a UTC
timeline, seven region boxes and a ticker.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36

PAPER = (246, 242, 231)
INK = (25, 23, 20)
RED = (179, 38, 30)
GRAY = (110, 104, 94)
TILE_BG = (238, 231, 214)
BAND = (32, 30, 27)
WHITE = (252, 250, 244)
BLUE = (43, 74, 128)
GOLD = (222, 175, 60)
GREEN = (58, 122, 68)
SKY = (212, 224, 235)
TARMAC = (158, 156, 152)
SKIN = (224, 182, 150)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_50 = font("DejaVuSerif-Bold.ttf", 50)
SERIF_34 = font("DejaVuSerif-Bold.ttf", 34)
SERIF_32 = font("DejaVuSerif-Bold.ttf", 32)
SANS_28 = font("DejaVuSans-Bold.ttf", 28)
SANS_22B = font("DejaVuSans-Bold.ttf", 22)
SANS_20B = font("DejaVuSans-Bold.ttf", 20)
SANS_19B = font("DejaVuSans-Bold.ttf", 19)
SANS_18B = font("DejaVuSans-Bold.ttf", 18)
SANS_16 = font("DejaVuSans.ttf", 16)
SANS_16B = font("DejaVuSans-Bold.ttf", 16)
SANS_14 = font("DejaVuSans.ttf", 14)
SANS_14B = font("DejaVuSans-Bold.ttf", 14)
SANS_13 = font("DejaVuSans.ttf", 13)
SANS_12 = font("DejaVuSans.ttf", 12)
SANS_12B = font("DejaVuSans-Bold.ttf", 12)
SANS_11 = font("DejaVuSans.ttf", 11)
SANS_11B = font("DejaVuSans-Bold.ttf", 11)
SANS_10 = font("DejaVuSans.ttf", 10)


def text_width(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> float:
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, max_w: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if text_width(draw, trial, f) <= max_w or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, f, fill, max_w, gap=4) -> float:
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        box = draw.textbbox((0, 0), line, font=f)
        y += (box[3] - box[1]) + gap
    return y


def star(cx, cy, r_out, r_in, points=5, rot=-math.pi / 2) -> list[tuple]:
    coords = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        coords.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return coords


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, width=2, fill=INK) -> None:
    draw.rectangle([x0, y, x1, y + width - 1], fill=fill)


# ---------------------------------------------------------------- masthead
def masthead(draw) -> None:
    rule(draw, 22, width=3)
    draw.text((MARGIN, 30), "GLOBAL EDITION · EVERY STORY DATE-CHECKED", font=SANS_14, fill=GRAY)
    right = "58 STORIES · 7 REGIONS · ONE IMAGE"
    draw.text((W - MARGIN - text_width(draw, right, SANS_14), 30), right, font=SANS_14, fill=GRAY)
    title = "The World in One Day"
    tw = text_width(draw, title, SERIF_50)
    draw.text(((W - tw) / 2, 48), title, font=SERIF_50, fill=INK)
    rule(draw, 110, width=2)
    draw.rectangle([MARGIN, 118, W - MARGIN, 160], fill=RED)
    date = "WEDNESDAY · 18 NOVEMBER 2026"
    dw = text_width(draw, date, SANS_28)
    draw.text(((W - dw) / 2, 124), date, font=SANS_28, fill=WHITE)


# ---------------------------------------------------------------- flags
def flag_us(draw, x, y, w, h) -> None:
    stripe = h / 13
    for i in range(13):
        color = (178, 34, 52) if i % 2 == 0 else WHITE
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=color)
    cw, ch = w * 0.45, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for row in range(4):
        for col in range(5):
            cx = x + cw * (0.14 + 0.18 * col)
            cy = y + ch * (0.16 + 0.24 * row)
            draw.ellipse([cx - 1.0, cy - 1.0, cx + 1.0, cy + 1.0], fill=WHITE)


def flag_cn(draw, x, y, w, h) -> None:
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.polygon(star(x + w * 0.22, y + h * 0.32, h * 0.20, h * 0.08), fill=(255, 222, 0))
    for sx, sy in ((0.44, 0.12), (0.52, 0.26), (0.52, 0.44), (0.44, 0.58)):
        draw.polygon(star(x + w * sx, y + h * sy, h * 0.06, h * 0.024), fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h) -> None:
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=WHITE)
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 43, 30))


# ---------------------------------------------------------------- lead
def lead_story(draw) -> None:
    top = 172
    draw.text((MARGIN, top), "APEC SUMMIT · SHENZHEN", font=SANS_18B, fill=RED)
    max_w = 560
    y = top + 26
    for line in ("Xi greets Trump on the tarmac", "as APEC opens in Shenzhen"):
        draw.text((MARGIN, y), line, font=SERIF_32, fill=INK)
        box = draw.textbbox((0, 0), line, font=SERIF_32)
        y += (box[3] - box[1]) + 4
    draw_wrapped(draw, MARGIN, y + 4,
                 "First airport welcome by Xi for a visiting leader; Trump-Putin handshake "
                 "before the family photo. Trilateral set for Thursday.",
                 SANS_16, INK, max_w, gap=2)
    fw, fh = 34, 22
    fy = 324
    for i, painter in enumerate((flag_us, flag_cn, flag_ru)):
        fx = MARGIN + i * (fw + 10)
        painter(draw, fx, fy, fw, fh)
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
    draw.text((MARGIN + 3 * (fw + 10) + 6, fy + 5), "US · CHINA · RUSSIA", font=SANS_12, fill=GRAY)


def figure(draw, cx, top, h, suit, tie) -> float:
    """Minimal standing figure: head, shoulders-to-hem coat, legs; return arm height."""
    head_r = h * 0.11
    hy = top + head_r
    draw.ellipse([cx - head_r, hy - head_r, cx + head_r, hy + head_r], fill=SKIN)
    draw.arc([cx - head_r, hy - head_r, cx + head_r, hy + head_r], 180, 360, fill=(60, 45, 35), width=2)
    shoulder = top + head_r * 2 + 2
    hem = top + h * 0.72
    sw = h * 0.16
    draw.polygon([(cx - sw, shoulder), (cx + sw, shoulder),
                  (cx + sw * 1.25, hem), (cx - sw * 1.25, hem)], fill=suit)
    draw.line([cx, shoulder + 2, cx, shoulder + h * 0.16], fill=tie, width=2)
    for dx in (-sw * 0.55, sw * 0.55):
        draw.line([cx + dx, hem, cx + dx, top + h], fill=(40, 38, 36), width=3)
    return shoulder + h * 0.10


def tarmac_art(draw) -> None:
    x0, y0, x1, y1 = 612, 172, W - MARGIN, 348
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=SKY, outline=RED, width=2)
    ground_y = y0 + 108
    draw.rectangle([x0 + 2, ground_y, x1 - 2, y1 - 24], fill=TARMAC)
    draw.text((x0 + 12, y0 + 8), "THE FIRST TARMAC WELCOME", font=SANS_12B, fill=RED)
    fx0, fx1 = x0 + 24, x0 + 236
    fy0, fy1 = y0 + 62, y0 + 92
    door_x = fx0 + 118
    # Carpet first: it lies on the tarmac, under the aircraft and the party.
    draw.polygon([(door_x, fy1), (door_x + 12, fy1), (x0 + 316, ground_y + 34), (x0 + 262, ground_y + 34)],
                 fill=(160, 40, 34))
    # Wing, then fuselage over its root.
    draw.polygon([(fx0 + 96, fy1 - 12), (fx0 + 150, fy1 + 14), (fx0 + 176, fy1 + 14), (fx0 + 128, fy1 - 12)],
                 fill=(200, 200, 202), outline=INK)
    draw.rounded_rectangle([fx0, fy0, fx1, fy1], radius=14, fill=WHITE, outline=INK, width=2)
    draw.polygon([(fx1 - 6, fy0 + 4), (fx1 + 16, fy0 + 15), (fx1 - 6, fy1 - 4)], fill=WHITE, outline=INK)
    draw.rectangle([fx0 + 14, fy0 + 16, fx1 - 4, fy0 + 21], fill=BLUE)
    for wx in range(fx0 + 52, fx1 - 16, 16):
        draw.rectangle([wx, fy0 + 7, wx + 7, fy0 + 12], fill=(120, 140, 160))
    draw.polygon([(fx0 + 4, fy0 + 4), (fx0 + 12, fy0 - 24), (fx0 + 36, fy0 + 4)], fill=BLUE, outline=INK)
    draw.polygon([(fx0 + 8, fy0 + 10), (fx0 - 12, fy0 + 4), (fx0 + 20, fy0 + 14)], fill=BLUE, outline=INK)
    draw.rectangle([door_x, fy0 + 5, door_x + 12, fy1 - 3], fill=(190, 192, 196), outline=INK)
    # Landing gear grounds the aircraft on the tarmac.
    draw.ellipse([fx0 + 70, ground_y + 4, fx0 + 215, ground_y + 11], fill=(138, 136, 132))
    for gx in (fx0 + 100, fx0 + 195):
        draw.line([gx, fy1 - 2, gx, ground_y + 5], fill=INK, width=3)
        draw.ellipse([gx - 4, ground_y + 2, gx + 4, ground_y + 10], fill=INK)
    # Two leaders meeting at the carpet's end, hands clasped.
    gy = ground_y - 6
    ax, bx = x0 + 272, x0 + 306
    draw.ellipse([ax - 11, gy + 38, ax + 11, gy + 43], fill=(138, 136, 132))
    draw.ellipse([bx - 11, gy + 38, bx + 11, gy + 43], fill=(138, 136, 132))
    a_sh = figure(draw, ax, gy, 40, (38, 48, 78), (170, 60, 50))
    b_sh = figure(draw, bx, gy, 40, (44, 42, 40), (179, 38, 30))
    draw.line([ax - 7, a_sh - 2, ax - 10, a_sh + 11], fill=(38, 48, 78), width=3)
    draw.line([bx + 7, b_sh - 2, bx + 10, b_sh + 11], fill=(44, 42, 40), width=3)
    mid_x, mid_y = (ax + bx) / 2, a_sh + 8
    draw.line([ax + 7, a_sh, mid_x, mid_y], fill=(38, 48, 78), width=4)
    draw.line([bx - 7, b_sh, mid_x, mid_y], fill=(44, 42, 40), width=4)
    draw.ellipse([mid_x - 3, mid_y - 3, mid_x + 3, mid_y + 3], fill=SKIN, outline=(120, 90, 70))
    draw.rectangle([x0 + 2, y1 - 24, x1 - 2, y1 - 2], fill=BAND)
    cap = "SHENZHEN BAO'AN INTERNATIONAL · 18 NOV"
    draw.text((x0 + 12, y1 - 20), cap, font=SANS_10, fill=WHITE)


# ---------------------------------------------------------------- numbers
NUMBERS = [
    ("€45bn", "Ukraine loan proposed"),
    ("25.9bn km", "Voyager 1 distance"),
    ("3.6%", "UK inflation, October"),
    ("$115.8bn", "Nvidia Q3 revenue"),
    ("8.5M bpd", "Hormuz oil, half prewar"),
]


def numbers_strip(draw) -> None:
    top = 356
    rule(draw, top - 6, width=1, fill=GRAY)
    draw.text((MARGIN, top), "THE DAY IN NUMBERS", font=SANS_12B, fill=GRAY)
    chip_w = (W - 2 * MARGIN) / 5
    for i, (big, label) in enumerate(NUMBERS):
        cx = MARGIN + i * chip_w + chip_w / 2
        bw = text_width(draw, big, SANS_22B)
        draw.text((cx - bw / 2, top + 16), big, font=SANS_22B, fill=RED)
        lw = text_width(draw, label, SANS_12)
        draw.text((cx - lw / 2, top + 44), label, font=SANS_12, fill=GRAY)
        if i:
            draw.line([MARGIN + i * chip_w, top + 14, MARGIN + i * chip_w, top + 58], fill=GRAY, width=1)
    rule(draw, top + 62, width=1, fill=GRAY)


# ---------------------------------------------------------------- feature icons
def icon_tile(draw, x, y, size=84) -> None:
    draw.rounded_rectangle([x, y, x + size, y + size], radius=10, fill=TILE_BG)


def icon_euro(draw, x, y) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 42, y + 42
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD, outline=INK, width=3)
    draw.text((cx - 11, cy - 17), "€", font=SANS_28, fill=INK)
    for a in range(0, 360, 45):
        sx = cx + 34 * math.cos(math.radians(a))
        sy = cy + 34 * math.sin(math.radians(a))
        draw.polygon(star(sx, sy, 4, 1.6), fill=BLUE)


def icon_missile(draw, x, y) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 42, y + 42
    draw.polygon(star(cx + 14, cy + 14, 26, 11, points=8), fill=RED)
    body = [(cx - 26, cy - 22), (cx + 8, cy + 4), (cx + 2, cy + 12), (cx - 32, cy - 14)]
    draw.polygon(body, fill=INK)
    draw.polygon([(cx - 26, cy - 22), (cx - 17, cy - 26), (cx - 21, cy - 13)], fill=INK)
    draw.polygon([(cx - 32, cy - 14), (cx - 36, cy - 5), (cx - 25, cy - 9)], fill=INK)


def icon_globe_leaf(draw, x, y) -> None:
    icon_tile(draw, x, y)
    cx, cy, r = x + 38, y + 46, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=INK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    ax0, ay0, ax1, ay1 = cx + 10, cy - 12, cx + 36, cy - 36
    dx, dy = ax1 - ax0, ay1 - ay0
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    left, right = [], []
    for i in range(13):
        t = i / 12
        px, py = ax0 + dx * t, ay0 + dy * t
        half = math.sin(math.pi * t) * 9
        left.append((px + nx * half, py + ny * half))
        right.append((px - nx * half, py - ny * half))
    draw.polygon(left + right[::-1], fill=GREEN)
    draw.line([ax0, ay0, ax1, ay1], fill=PAPER, width=2)
    draw.line([ax0, ay0, ax0 - 6, ay0 + 6], fill=GREEN, width=3)


def icon_superbug(draw, x, y) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 36, y + 38
    draw.rounded_rectangle([cx - 20, cy - 12, cx + 20, cy + 12], radius=12, fill=INK)
    for dx, dy in ((-11, -5), (0, 3), (10, -3)):
        draw.ellipse([cx + dx - 2.5, cy + dy - 2.5, cx + dx + 2.5, cy + dy + 2.5], fill=TILE_BG)
    for a in (0.4, 1.2, 2.2, 3.4, 4.4, 5.4):
        x0, y0 = cx + 20 * math.cos(a), cy + 12 * math.sin(a)
        draw.line([x0, y0, x0 + 8 * math.cos(a), y0 + 8 * math.sin(a)], fill=INK, width=3)
    px, py = x + 54, y + 60
    draw.rounded_rectangle([px - 14, py - 7, px + 14, py + 7], radius=7, fill=RED)
    draw.rectangle([px, py - 7, px + 14, py + 7], fill=WHITE)
    draw.rounded_rectangle([px - 14, py - 7, px + 14, py + 7], radius=7, outline=INK, width=2)
    draw.line([px - 17, py - 12, px + 17, py + 12], fill=INK, width=4)


def icon_chip(draw, x, y) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 42, y + 42
    draw.rounded_rectangle([cx - 22, cy - 22, cx + 22, cy + 22], radius=4, fill=INK)
    draw.rectangle([cx - 13, cy - 13, cx + 13, cy + 13], fill=TILE_BG)
    for d in (-14, -5, 4, 13):
        draw.line([cx + d, cy - 22, cx + d, cy - 30], fill=INK, width=3)
        draw.line([cx + d, cy + 22, cx + d, cy + 30], fill=INK, width=3)
        draw.line([cx - 22, cy + d, cx - 30, cy + d], fill=INK, width=3)
        draw.line([cx + 22, cy + d, cx + 30, cy + d], fill=INK, width=3)
    draw.text((cx - 13, cy - 9), "NV", font=SANS_16B, fill=RED)


def icon_probe(draw, x, y) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 34, y + 38
    draw.arc([cx - 24, cy - 24, cx + 24, cy + 24], 120, 300, fill=INK, width=4)
    draw.line([cx - 12, cy - 20, cx + 6, cy + 2], fill=INK, width=3)
    draw.rectangle([cx + 2, cy - 2, cx + 20, cy + 12], fill=INK)
    draw.line([cx + 20, cy + 5, cx + 36, cy + 20], fill=INK, width=3)
    draw.rectangle([cx + 32, cy + 17, cx + 42, cy + 27], fill=GRAY)
    ex, ey = x + 66, y + 64
    draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=BLUE)
    for r in (11, 17, 23):
        draw.arc([cx - r, cy - r, cx + r, cy + r], -40, 20, fill=RED, width=2)


FEATURES = [
    (icon_missile, "Iran drones hit Gulf bases", "Kuwait intercepts; Bahrain repels 4th attack in 6 days", "AFP · AP"),
    (icon_euro, "EU plans €45bn Ukraine loan", "€25bn arms + €20bn budget; repay after reparations", "REUTERS"),
    (icon_probe, "Voyager 1: one light-day out", "25.9bn km at 10:16 UTC; 49 years into the flight", "NASA / JPL"),
    (icon_chip, "Nvidia doubles to $115.8bn", "Board rules out Huang return; Kress interim CEO", "AFP"),
    (icon_superbug, "WHO: superbugs outrun drugs", "Resistance worse than 2019; last-resort failing", "UN NEWS"),
    (icon_globe_leaf, "COP31 draft splits nations", "Fossil phase-out text; Arab Group, Russia reject", "ARAB NEWS"),
]


def features(draw) -> None:
    top, card_h, gap = 428, 114, 10
    card_w = (W - 2 * MARGIN - 2 * gap) / 3
    for idx, (painter, title, sub, src) in enumerate(FEATURES):
        row, col = divmod(idx, 3)
        x = MARGIN + col * (card_w + gap)
        y = top + row * (card_h + gap)
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=8, fill=WHITE, outline=GRAY, width=1)
        painter(draw, x + 8, y + 8)
        tx = x + 100
        max_w = card_w - 110
        ty = draw_wrapped(draw, tx, y + 10, title, SANS_19B, INK, max_w, gap=2)
        draw_wrapped(draw, tx, ty + 3, sub, SANS_13, GRAY, max_w, gap=2)
        draw.text((tx, y + card_h - 18), src, font=SANS_10, fill=RED)


# ---------------------------------------------------------------- timeline
TIMELINE = [
    ("10:16", "Voyager light-day"),
    ("11:00", "GTA VI live in NZ"),
    ("11:01", "ECB AI warning"),
    ("14:52", "€45bn proposed"),
    ("16:55", "Waymo pullback"),
    ("21:44", "DB leak probe"),
]


def timeline(draw) -> None:
    top = 676
    draw.text((MARGIN, top), "THE DAY IN UTC", font=SANS_12B, fill=GRAY)
    line_y = top + 22
    rule(draw, line_y, width=2, fill=INK)
    slot = (W - 2 * MARGIN) / 6
    for i, (t, label) in enumerate(TIMELINE):
        cx = MARGIN + i * slot + slot / 2
        draw.ellipse([cx - 4, line_y - 3, cx + 4, line_y + 5], fill=RED)
        tw = text_width(draw, t, SANS_14B)
        draw.text((cx - tw / 2, line_y + 8), t, font=SANS_14B, fill=INK)
        lw = text_width(draw, label, SANS_12)
        draw.text((cx - lw / 2, line_y + 26), label, font=SANS_12, fill=GRAY)


# ---------------------------------------------------------------- regions
REGIONS = [
    ("EUROPE", [
        "ECB: AI boom echoes dotcom era",
        "Deutsche Bank leak: 15M files",
        "UK inflation rises to 3.6%",
        "Romania M5.7: strongest since 2018",
        "Odesa strike kills 4; 141 drones",
        "Crimean Bridge: trains resume",
        "Norway, Sweden: $370m for arms",
    ]),
    ("NORTH AMERICA", [
        "Peltola flips Alaska Senate seat",
        "Outages: Microsoft, FAA, banks",
        "Rubio: no sign of cyberattack",
        "Waymo pulls freeway robotaxis",
        "Anthropic IPO: Nasdaq debut Thu",
        "Shannon C-130 case: NY indictment",
    ]),
    ("ASIA", [
        "Xi-Putin lunch: multipolar push",
        "Trump-Putin bilateral begins",
        "Trilateral set for Thursday",
        "Manila: 'biggest' trade deal claim",
        "William and Kate meet Modi",
        "Kospi +2% on Nvidia beat",
        "Imran Khan £190m appeals at IHC",
    ]),
    ("MIDDLE EAST", [
        "Saudi-led jets pound Sanaa",
        "Houthis: 17 killed in strikes",
        "Knesset moves to repeal overhaul",
        "Gaza doctor detention extended",
        "Qaani in Baghdad amid tensions",
        "Hormuz flows halved: 8.5M bpd",
        "3rd US carrier; Iran 'monitoring'",
    ]),
    ("AFRICA", [
        "Ethiopia-Eritrea clashes near Badme",
        "Guinea: 224 jailed over illegal gold",
        "Mauritius: Chagos handover due in Dec",
        "S Africa rebukes Nigeria envoy over row",
        "WFP feeds families fleeing Ethiopia",
        "El Niño + war: 1m Ethiopians at risk",
        "Besigye family raises health alarm",
    ]),
    ("LATIN AMERICA", [
        "Hegseth in Bogotá: first C-130 handed over",
        "Surprise stopover in Venezuela",
        "Venezuela unions call 24-hour strike",
        "Paraguay AG resigns before impeachment",
        "Chile: CUT marches against Kast cuts",
        "Mexico 1-0 Jamaica: Final Four bound",
    ]),
    ("OCEANIA & PACIFIC", [
        "Fiji: national disaster over drought",
        "Cyclone Xavier: cat 5, gusts 315km/h",
        "Rio Tinto: $250M Panguna cleanup",
        "GTA VI unlocks first in New Zealand",
        "PNG three-child policy splits opinion",
        "Vanuatu denies banking-collapse rumour",
        "RNZ cuts: 58 jobs, Pacific link at risk",
    ]),
]


def region_box(draw, x, y, w, h, name, stories) -> None:
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=WHITE, outline=GRAY, width=1)
    draw.rectangle([x, y, x + w, y + 22], fill=BAND)
    draw.text((x + 8, y + 4), name, font=SANS_12B, fill=WHITE)
    count = str(len(stories))
    draw.text((x + w - 8 - text_width(draw, count, SANS_12B), y + 4), count, font=SANS_12B, fill=GOLD)
    inner_w = w - 26
    size = 12
    while size > 9:
        f = font("DejaVuSans.ttf", size)
        width_ok = all(text_width(draw, s, f) <= inner_w for s in stories)
        height_ok = 26 + len(stories) * (size + 1) <= h - 2
        if width_ok and height_ok:
            break
        size -= 1
    f = font("DejaVuSans.ttf", size)
    line_h = size + 1
    sy = y + 26
    for s in stories:
        draw.rectangle([x + 8, sy + 4, x + 11, sy + 7], fill=RED)
        draw.text((x + 16, sy), s, font=f, fill=INK)
        sy += line_h


def regions(draw) -> None:
    top = 744
    gap = 10
    row1_h, row2_h = 112, 112
    w1 = (W - 2 * MARGIN - 3 * gap) / 4
    for i in range(4):
        name, stories = REGIONS[i]
        region_box(draw, MARGIN + i * (w1 + gap), top, w1, row1_h, name, stories)
    w2 = (W - 2 * MARGIN - 2 * gap) / 3
    y2 = top + row1_h + gap
    for i in range(3):
        name, stories = REGIONS[4 + i]
        region_box(draw, MARGIN + i * (w2 + gap), y2, w2, row2_h, name, stories)


# ---------------------------------------------------------------- footer
TICKER_ITEMS = [
    "IIHF hit by cyberattack",
    "Bezos backed Pattinson Bond pick",
    "Australia sanctions Israeli activists",
    "WHO DG candidates pitch plans",
]
SOURCES = ("Sources: Reuters · AFP · AP · Al Jazeera · Euronews · UN News · NASA/JPL · ONS · ECB · "
           "RNZ · PACNEWS · allAfrica · Times of Israel · Kyiv Independent · CNBC · ESPN")


def footer(draw) -> None:
    ticker = "ALSO TODAY · " + " · ".join(TICKER_ITEMS)
    draw.rectangle([MARGIN, 980, W - MARGIN, 1006], fill=BAND)
    f = SANS_13
    while text_width(draw, ticker, f) > W - 2 * MARGIN - 20 and f.size > 10:
        f = font("DejaVuSans.ttf", f.size - 1)
    tw = text_width(draw, ticker, f)
    draw.text(((W - tw) / 2, 986), ticker, font=f, fill=WHITE)
    sw = text_width(draw, SOURCES, SANS_11)
    draw.text(((W - sw) / 2, 1010), SOURCES, font=SANS_11, fill=GRAY)


def story_count() -> int:
    return 1 + len(FEATURES) + sum(len(s) for _, s in REGIONS) + len(TICKER_ITEMS)


def render() -> Image.Image:
    assert story_count() == 58, f"story count drifted: {story_count()}"
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead_story(draw)
    tarmac_art(draw)
    numbers_strip(draw)
    features(draw)
    timeline(draw)
    regions(draw)
    footer(draw)
    return img


def main() -> None:
    out = Path(__file__).resolve().parent / "assets" / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img = render()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]}, {story_count()} stories)")


if __name__ == "__main__":
    main()

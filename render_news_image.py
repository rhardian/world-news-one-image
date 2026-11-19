#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page to assets/entry.png.

Offline asset builder for the make.fun news-image-20261118 entry. The graded
program (main.py) only copies the rendered PNG; this script is how the image
was made. It needs Pillow and the DejaVu fonts, and it is fully deterministic:
same inputs, same bytes.

Stories are the world's top reported news of Wednesday 18 November 2026
(Euronews, NPR, UN News, IPS, Hindustan Times, Newser):
  - APEC Shenzhen: Trump-Xi tarmac welcome, first Trump-Putin meeting since
    2025, first US-China-Russia trilateral.
  - Iran strikes Kuwait and Bahrain, warns off the US.
  - COP31 Antalya deadlock; new global "climate reality check" launched.
  - WHO: antibiotic resistance worse than 2019, last-resort drugs failing.
  - Mary Peltola wins the Alaska Senate race.
  - GTA VI launch hit by glitches.
  - Magnus Carlsen forfeits a Budapest game to protect his rating.
  - Storms Bruna and Charles: record rain and wind in Portugal and Madeira.
  - US defense secretary restores military cooperation in Caracas.
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

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_56 = font("DejaVuSerif-Bold.ttf", 54)
SERIF_40 = font("DejaVuSerif-Bold.ttf", 39)
SANS_30 = font("DejaVuSans-Bold.ttf", 30)
SANS_26 = font("DejaVuSans-Bold.ttf", 25)
SANS_22 = font("DejaVuSans.ttf", 22)
SANS_20 = font("DejaVuSans.ttf", 20)
SANS_20B = font("DejaVuSans-Bold.ttf", 20)
SANS_18 = font("DejaVuSans.ttf", 18)
SANS_16 = font("DejaVuSans.ttf", 16)
SANS_14 = font("DejaVuSans.ttf", 14)


def text_width(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> float:
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, max_w: float) -> list[str]:
    """Greedy word wrap measured with the real font metrics."""
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


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    text: str,
    f: ImageFont.FreeTypeFont,
    fill: tuple,
    max_w: float,
    gap: int = 4,
) -> float:
    """Draw wrapped text top-left anchored; return the y below the last line."""
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        box = draw.textbbox((0, 0), line, font=f)
        y += (box[3] - box[1]) + gap
    return y


def star(cx: float, cy: float, r_out: float, r_in: float, points: int = 5, rot: float = -math.pi / 2) -> list[tuple]:
    coords = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        coords.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return coords


def rule(draw: ImageDraw.ImageDraw, y: float, x0: float = MARGIN, x1: float = W - MARGIN, width: int = 2, fill=INK) -> None:
    draw.rectangle([x0, y, x1, y + width - 1], fill=fill)


# ---------------------------------------------------------------- masthead
def masthead(draw: ImageDraw.ImageDraw) -> None:
    rule(draw, 28, width=3)
    draw.text((MARGIN, 40), "GLOBAL EDITION", font=SANS_16, fill=GRAY)
    right = "ONE IMAGE · ONE DAY"
    draw.text((W - MARGIN - text_width(draw, right, SANS_16), 40), right, font=SANS_16, fill=GRAY)
    title = "The World in One Day"
    tw = text_width(draw, title, SERIF_56)
    draw.text(((W - tw) / 2, 62), title, font=SERIF_56, fill=INK)
    rule(draw, 126, width=2)
    # Date band: the day this image sums up, named plainly.
    draw.rectangle([MARGIN, 138, W - MARGIN, 184], fill=RED)
    date = "WEDNESDAY · 18 NOVEMBER 2026"
    dw = text_width(draw, date, SANS_30)
    draw.text(((W - dw) / 2, 145), date, font=SANS_30, fill=WHITE)


# ---------------------------------------------------------------- lead art
def flag_us(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float) -> None:
    stripe = h / 13
    for i in range(13):
        color = (178, 34, 52) if i % 2 == 0 else WHITE
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=color)
    canton_w, canton_h = w * 0.45, stripe * 7
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=(60, 59, 110))
    for row in range(4):
        for col in range(5):
            cx = x + canton_w * (0.14 + 0.18 * col)
            cy = y + canton_h * (0.16 + 0.24 * row)
            draw.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=WHITE)


def flag_cn(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float) -> None:
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.polygon(star(x + w * 0.22, y + h * 0.32, h * 0.20, h * 0.08), fill=(255, 222, 0))
    for sx, sy in ((0.44, 0.12), (0.52, 0.26), (0.52, 0.44), (0.44, 0.58)):
        draw.polygon(star(x + w * sx, y + h * sy, h * 0.06, h * 0.024), fill=(255, 222, 0))


def flag_ru(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float) -> None:
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=WHITE)
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 43, 30))


def lead_art(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    """Three flags on poles: the US, China and Russia meet at APEC."""
    fw, fh = 132, 84
    positions = [(x, y + 18), (x + 62, y), (x + 124, y + 18)]
    flags = (flag_us, flag_cn, flag_ru)
    for (fx, fy), painter in zip(positions, flags):
        draw.rectangle([fx - 4, fy - 8, fx, fy + fh + 66], fill=(90, 84, 74))
        painter(draw, fx, fy, fw, fh)
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
    caption = "US · CHINA · RUSSIA"
    draw.text((x + 20, y + fh + 78), caption, font=SANS_16, fill=GRAY)


def lead_story(draw: ImageDraw.ImageDraw) -> None:
    top = 202
    lead_art(draw, MARGIN + 4, top + 6)
    tx = 320
    max_w = W - MARGIN - tx
    draw.text((tx, top), "APEC SUMMIT · SHENZHEN", font=SANS_20B, fill=RED)
    y = draw_wrapped(
        draw, tx, top + 32,
        "Trump, Xi and Putin hold first three-way talks",
        SERIF_40, INK, max_w, gap=6,
    )
    draw_wrapped(
        draw, tx, y + 8,
        "Xi greets Trump on the tarmac as APEC opens in China; first Trump-Putin encounter since 2025.",
        SANS_22, INK, max_w, gap=4,
    )
    rule(draw, 420, width=2)


# ---------------------------------------------------------------- tile icons
def icon_tile(draw: ImageDraw.ImageDraw, x: float, y: float, size: float = 100) -> None:
    draw.rounded_rectangle([x, y, x + size, y + size], radius=12, fill=TILE_BG)


def icon_missile(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 50, y + 50
    # Impact burst behind, missile crossing down-right.
    draw.polygon(star(cx + 16, cy + 16, 30, 13, points=8), fill=RED)
    body = [(cx - 30, cy - 26), (cx + 8, cy + 4), (cx + 2, cy + 12), (cx - 36, cy - 18)]
    draw.polygon(body, fill=INK)
    draw.polygon([(cx - 30, cy - 26), (cx - 20, cy - 30), (cx - 24, cy - 16)], fill=INK)
    draw.polygon([(cx - 36, cy - 18), (cx - 40, cy - 8), (cx - 28, cy - 12)], fill=INK)
    draw.line([cx - 44, cy - 34, cx - 32, cy - 24], fill=GRAY, width=3)


def icon_globe_leaf(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    icon_tile(draw, x, y)
    cx, cy, r = x + 46, y + 52, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=INK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    draw.arc([cx - r, cy - r * 1.5, cx + r, cy + r * 0.5], 200, 340, fill=INK, width=2)
    # Leaf over the globe's top-right: lens shape along a diagonal axis.
    ax0, ay0, ax1, ay1 = cx + 12, cy - 14, cx + 42, cy - 42
    dx, dy = ax1 - ax0, ay1 - ay0
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    left, right = [], []
    for i in range(13):
        t = i / 12
        px, py = ax0 + dx * t, ay0 + dy * t
        half = math.sin(math.pi * t) * 11
        left.append((px + nx * half, py + ny * half))
        right.append((px - nx * half, py - ny * half))
    draw.polygon(left + right[::-1], fill=(58, 122, 68))
    draw.line([ax0, ay0, ax1, ay1], fill=PAPER, width=2)
    draw.line([ax0, ay0, ax0 - 7, ay0 + 7], fill=(58, 122, 68), width=3)


def icon_superbug(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 44, y + 46
    draw.rounded_rectangle([cx - 24, cy - 14, cx + 24, cy + 14], radius=14, fill=INK)
    for dx, dy in ((-14, -6), (0, 4), (12, -4)):
        draw.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=TILE_BG)
    for a in (0.4, 1.2, 2.2, 3.4, 4.4, 5.4):
        x0, y0 = cx + 24 * math.cos(a), cy + 14 * math.sin(a)
        draw.line([x0, y0, x0 + 10 * math.cos(a), y0 + 10 * math.sin(a)], fill=INK, width=3)
    # Capsule pill, crossed out: the drugs are losing.
    px, py = x + 62, y + 70
    draw.rounded_rectangle([px - 16, py - 8, px + 16, py + 8], radius=8, fill=RED)
    draw.rectangle([px, py - 8, px + 16, py + 8], fill=WHITE)
    draw.rounded_rectangle([px - 16, py - 8, px + 16, py + 8], radius=8, outline=INK, width=2)
    draw.line([px - 20, py - 14, px + 20, py + 14], fill=INK, width=4)


def icon_ballot(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    icon_tile(draw, x, y)
    bx, by = x + 22, y + 44
    draw.rectangle([bx, by, bx + 56, by + 34], fill=INK)
    draw.rectangle([bx + 12, by + 6, bx + 44, by + 10], fill=TILE_BG)
    # Ballot paper dropping into the slot, with a check.
    draw.rectangle([bx + 16, by - 26, bx + 40, by + 4], fill=WHITE, outline=INK, width=2)
    draw.line([bx + 21, by - 12, bx + 26, by - 6, bx + 36, by - 20], fill=RED, width=3)
    draw.text((bx + 6, by + 14), "AK", font=SANS_16, fill=WHITE)


def icon_controller(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    icon_tile(draw, x, y)
    cx, cy = x + 50, y + 52
    draw.rounded_rectangle([cx - 34, cy - 16, cx + 34, cy + 18], radius=16, fill=INK)
    draw.ellipse([cx - 40, cy - 4, cx - 12, cy + 26], fill=INK)
    draw.ellipse([cx + 12, cy - 4, cx + 40, cy + 26], fill=INK)
    draw.rectangle([cx - 26, cy - 6, cx - 14, cy + 2], fill=TILE_BG)
    draw.rectangle([cx - 22, cy - 10, cx - 18, cy + 6], fill=TILE_BG)
    for dx, dy in ((20, -8), (28, -2), (20, 4), (12, -2)):
        draw.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=RED)


def icon_pawn(draw: ImageDraw.ImageDraw, x: float, y: float) -> None:
    icon_tile(draw, x, y)
    cx, base = x + 50, y + 82
    draw.ellipse([cx - 13, y + 16, cx + 13, y + 42], fill=INK)
    draw.polygon([(cx - 9, y + 40), (cx + 9, y + 40), (cx + 16, base - 10), (cx - 16, base - 10)], fill=INK)
    draw.rounded_rectangle([cx - 24, base - 10, cx + 24, base], radius=4, fill=INK)
    draw.line([cx - 20, y + 24, cx + 20, y + 64], fill=RED, width=4)


# ---------------------------------------------------------------- tiles
TILES = [
    (icon_missile, "Iran strikes Kuwait and Bahrain", "Gulf states hit; Tehran warns off the US"),
    (icon_globe_leaf, "COP31 deadlock in Antalya", "New 'climate reality check' launched as talks stall"),
    (icon_superbug, "WHO: superbugs outrun drugs", "Antibiotic resistance worse than 2019, last-resort drugs failing"),
    (icon_ballot, "Peltola wins Alaska Senate race", "Democrats flip the Alaska seat in the US Senate"),
    (icon_controller, "GTA VI launch hit by glitches", "Rockstar's long-awaited release stumbles on day one"),
    (icon_pawn, "Carlsen forfeits in Budapest", "Chess No. 1 skips a game to protect his sliding rating"),
]


def tiles(draw: ImageDraw.ImageDraw) -> None:
    top, row_h, col_w = 436, 168, 478
    for idx, (painter, title, sub) in enumerate(TILES):
        row, col = divmod(idx, 2)
        x = MARGIN + col * (col_w + 12)
        y = top + row * row_h
        painter(draw, x, y + 4)
        tx = x + 116
        max_w = col_w - 116
        ty = draw_wrapped(draw, tx, y + 6, title, SANS_26, INK, max_w, gap=2)
        draw_wrapped(draw, tx, ty + 4, sub, SANS_20, GRAY, max_w, gap=2)
        if col == 0:
            draw.line([x + col_w + 5, y + 8, x + col_w + 5, y + row_h - 16], fill=GRAY, width=1)
        if row < 2:
            rule(draw, y + row_h - 8, x0=x, x1=x + col_w, width=1, fill=GRAY)


# ---------------------------------------------------------------- footer
def footer(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle([MARGIN, 946, W - MARGIN, 986], fill=BAND)
    ticker = "ALSO TODAY · Storms Bruna & Charles: record rain in Portugal · US-Venezuela military ties restored · iCloud outage"
    tw = text_width(draw, ticker, SANS_16)
    draw.text(((W - tw) / 2, 957), ticker, font=SANS_16, fill=WHITE)
    sources = "Sources: Euronews, NPR, UN News, IPS, Hindustan Times, Newser · compiled 18 Nov 2026"
    sw = text_width(draw, sources, SANS_14)
    draw.text(((W - sw) / 2, 996), sources, font=SANS_14, fill=GRAY)


def render() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead_story(draw)
    tiles(draw)
    footer(draw)
    return img


def main() -> None:
    out = Path(__file__).resolve().parent / "assets" / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img = render()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()

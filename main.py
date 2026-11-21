#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Draws one invented passport spread (1024x1024 PNG) for the mountain
republic of Talsoria, entirely procedurally with PIL. No network, no
external assets: every line, stamp, portrait and letter is drawn here.

Country: REPUBLIC OF TALSORIA -- a small landlocked mountain republic
whose only road out runs over the Drenovik Pass, closed by snow from
31 October to 1 May. Capital: Drenovik.
Holder: Mira Elena Drenov, born 12 Apr 1988 in Drenovik.
Passport issued 14 Mar 2023, expires 13 Mar 2033.
Travel story (all stamps AFTER the issue date):
  Kovar entry  02 Jun 2023, exit 18 Jun 2023 (summer trade fair)
  Brezna entry 05 Sep 2024, exit 21 Sep 2024 (harvest visit)
  Kovar entry  03 May 2025, exit 17 May 2025 (spring, pass just open)
Telling detail: Condition 7 stamp -- the holder must leave Talsoria
via Drenovik Pass before 31 Oct, because the pass closes for winter.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# --- ICAO 9303 MRZ check digits -------------------------------------------
def check_digit(s):
    weights = (7, 3, 1)
    vals = {}
    for i in range(10):
        vals[str(i)] = i
    vals["<"] = 0
    for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = 10 + i
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * weights[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<TALDRENOV<<MIRA<ELENA"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "TS0428173"
    dob = "880412"
    exp = "330313"
    personal = "<" * 14
    line2 = (
        doc + check_digit(doc)
        + "TAL"
        + dob + check_digit(dob)
        + "F"
        + exp + check_digit(exp)
        + personal + check_digit(personal)
    )
    line2 += check_digit(line2)  # composite check digit -> 44 chars
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# --- small drawing helpers -------------------------------------------------
def text(d, xy, s, fpath, size, fill, anchor="la"):
    d.text(xy, s, font=font(fpath, size), fill=fill, anchor=anchor)


def hline(d, x0, x1, y, fill, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def rounded_stamp(d, box, fill, outline, width=3):
    d.rounded_rectangle(box, radius=10, outline=outline, width=width)


def draw_emblem(d, cx, cy, r, ink):
    """Coat of arms of Talsoria: a sun over three mountain peaks in a ring."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=2)
    d.ellipse([cx - 5, cy - r + 8, cx + 5, cy - r + 18], fill=ink)
    # three peaks
    d.polygon([(cx - r + 6, cy + r - 12), (cx - r // 3, cy - 2),
               (cx - 4, cy + r - 12)], fill=ink)
    d.polygon([(cx - r // 3 + 2, cy + r - 12), (cx, cy - r + 16),
               (cx + r // 3 - 2, cy + r - 12)], fill=ink)
    d.polygon([(cx + 4, cy + r - 12), (cx + r // 3, cy - 2),
               (cx + r - 6, cy + r - 12)], fill=ink)
    d.line([(cx - r + 4, cy + r - 12), (cx + r - 4, cy + r - 12)],
           fill=ink, width=2)


def draw_portrait(img, box):
    """Stylised drawn portrait: a woman of the high valleys, dark hair,
    woollen collar, plain studio backdrop with faint guilloche arcs.
    Rendered on its own layer so nothing escapes the photo box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGB", (w, h), (198, 208, 216))
    d = ImageDraw.Draw(layer)
    # backdrop: pale blue-grey with concentric arcs
    cx = w // 2
    for rr in range(30, 260, 26):
        d.arc([cx - rr, 30 - rr, cx + rr, 30 + rr],
              start=200, end=340, fill=(178, 190, 200), width=1)
    # shoulders / jacket
    d.polygon([(8, h), (30, h * 0.72),
               (cx - 26, h * 0.66), (cx + 26, h * 0.66),
               (w - 30, h * 0.72), (w - 8, h)], fill=(58, 62, 78))
    # white collar
    d.polygon([(cx - 26, h * 0.66), (cx, h * 0.78),
               (cx + 26, h * 0.66), (cx + 14, h * 0.62),
               (cx - 14, h * 0.62)], fill=(238, 236, 228))
    # neck
    d.rectangle([cx - 13, h * 0.55, cx + 13, h * 0.70],
                fill=(214, 178, 148))
    # head
    d.ellipse([cx - 34, h * 0.16, cx + 34, h * 0.60],
              fill=(222, 186, 154))
    # hair: dark, parted, framing the face, tied back
    d.pieslice([cx - 40, h * 0.10, cx + 40, h * 0.52],
               start=180, end=360, fill=(42, 32, 26))
    d.polygon([(cx - 40, h * 0.30), (cx - 30, h * 0.16),
               (cx - 26, h * 0.34), (cx - 38, h * 0.42)],
              fill=(42, 32, 26))
    d.polygon([(cx + 40, h * 0.30), (cx + 30, h * 0.16),
               (cx + 26, h * 0.34), (cx + 38, h * 0.42)],
              fill=(42, 32, 26))
    # brows, eyes, nose, mouth -- simple, calm, passport-neutral
    d.line([(cx - 22, h * 0.36), (cx - 8, h * 0.35)],
           fill=(52, 40, 30), width=2)
    d.line([(cx + 8, h * 0.35), (cx + 22, h * 0.36)],
           fill=(52, 40, 30), width=2)
    for ex in (cx - 15, cx + 15):
        d.ellipse([ex - 5, h * 0.385, ex + 5, h * 0.415],
                  outline=(60, 48, 38), width=1)
        d.ellipse([ex - 2, h * 0.395, ex + 2, h * 0.41],
                  fill=(40, 32, 26))
    d.line([(cx, h * 0.42), (cx - 2, h * 0.50)],
           fill=(190, 150, 120), width=2)
    d.line([(cx - 9, h * 0.54), (cx + 9, h * 0.54)],
           fill=(150, 90, 80), width=2)
    # faint cheek shading
    d.ellipse([cx - 30, h * 0.46, cx - 18, h * 0.52],
              fill=(226, 178, 148))
    d.ellipse([cx + 18, h * 0.46, cx + 30, h * 0.52],
              fill=(226, 178, 148))
    d.rectangle([0, 0, w - 1, h - 1], outline=(90, 90, 90), width=2)
    img.paste(layer, (x0, y0))


# --- stamps ----------------------------------------------------------------
def draw_stamp(img, cx, cy, w, h, angle, ink, lines, size=15):
    """A rectangular border-control stamp, drawn on its own layer and
    rotated, so the ink sits at a natural slight angle."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=8,
                        outline=ink + (255,), width=3)
    d.rounded_rectangle([26, 26, 14 + w, 14 + h], radius=6,
                        outline=ink + (255,), width=1)
    f_b = font(SANS_B, size)
    f = font(SANS, size - 2)
    y = 28
    for i, s in enumerate(lines):
        ff = f_b if i == 0 else f
        d.text((20 + w // 2, y), s, font=ff, fill=ink + (255,),
               anchor="ma")
        y += size + 2
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(layer, (cx - layer.width // 2, cy - layer.height // 2))


def draw_condition_stamp(img, cx, cy, w, h, angle):
    """The telling detail: Condition 7, in red ink. Talsoria's only road
    out closes with the snow, so every exit visa carries this condition."""
    ink = (178, 32, 28)
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([20, 20, 20 + w, 20 + h], outline=ink + (255,), width=3)
    d.text((20 + w // 2, 30), "CONDITION 7 — WINTER CLOSURE",
           font=font(SANS_B, 15), fill=ink + (255,), anchor="ma")
    d.text((20 + w // 2, 52),
           "HOLDER MUST LEAVE TALSORIA VIA",
           font=font(SANS, 13), fill=ink + (255,), anchor="ma")
    d.text((20 + w // 2, 70),
           "DRENOVIK PASS BEFORE 31 OCTOBER.",
           font=font(SANS, 13), fill=ink + (255,), anchor="ma")
    d.text((20 + w // 2, 88),
           "NO WINTER EXIT — PASS CLOSED 1 NOV – 30 APR",
           font=font(SANS_B, 11), fill=ink + (255,), anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(layer, (cx - layer.width // 2, cy - layer.height // 2))


def draw_fee_stamp(img, cx, cy, w, h, angle):
    ink = (30, 110, 60)
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=6,
                        outline=ink + (255,), width=2)
    d.text((20 + w // 2, 30), "PASS FEE 40 TALERS",
           font=font(SANS_B, 14), fill=ink + (255,), anchor="ma")
    d.text((20 + w // 2, 50), "PAID 03 MAY 2025",
           font=font(SANS, 12), fill=ink + (255,), anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(layer, (cx - layer.width // 2, cy - layer.height // 2))


# --- pages -----------------------------------------------------------------
PAPER = (247, 242, 230)
INK = (32, 32, 38)
MUTED = (110, 104, 90)
RULE = (150, 142, 122)


def data_page(img, x0, y0, pw, ph):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PAPER,
                outline=(120, 112, 92), width=2)
    mx = x0 + 26
    # header: emblem + country name, two languages
    draw_emblem(d, x0 + 48, y0 + 46, 24, (52, 64, 96))
    text(d, (x0 + 80, y0 + 26), "REPUBLIC OF TALSORIA",
         SERIF_B, 17, (52, 64, 96))
    text(d, (x0 + 80, y0 + 50), "REPUBLIKA TALSORIJA",
         SERIF, 12, MUTED)
    text(d, (x0 + pw - 26, y0 + 26), "PASSPORT", SERIF_B, 17,
         (52, 64, 96), anchor="ra")
    text(d, (x0 + pw - 26, y0 + 50), "PASPORT", SERIF, 12, MUTED,
         anchor="ra")
    hline(d, mx, x0 + pw - 26, y0 + 82, RULE, 1)
    text(d, (x0 + pw // 2, y0 + 92), "IDENTITY  •  IDENTITET",
         SANS, 11, MUTED, anchor="ma")

    # portrait, left; fields, right
    px0, py0 = mx, y0 + 118
    # embossed-style circular control seal overlapping the photo corner
    sx, sy = px0 + 108, py0 + 164
    seal = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
    sdd = ImageDraw.Draw(seal)
    sdd.ellipse([6, 6, 84, 84], outline=(52, 64, 120, 200), width=3)
    sdd.ellipse([14, 14, 76, 76], outline=(52, 64, 120, 200), width=1)
    sdd.polygon([(28, 58), (38, 34), (48, 58)], fill=(52, 64, 120, 200))
    sdd.polygon([(44, 58), (55, 30), (66, 58)], fill=(52, 64, 120, 200))
    sdd.text((45, 62), "DRENOVIK", font=font(SANS_B, 8),
             fill=(52, 64, 120, 220), anchor="ma")
    img.alpha_composite(seal, (sx - 45, sy - 45))
    fx = px0 + 168
    fw = x0 + pw - 26 - fx
    fields = [
        ("Type / Tip", "P"),
        ("Country code / Kod", "TAL"),
        ("Passport No. / Br. pasosa", "TS 0428173"),
        ("Surname / Prezime", "DRENOV"),
        ("Given names / Ime", "MIRA ELENA"),
        ("Nationality / Drzavljanstvo", "TALSORIAN"),
        ("Date of birth / Roden", "12 APR 1988"),
        ("Place of birth / Mjesto rodenja", "DRENOVIK"),
        ("Sex / Pol", "F"),
    ]
    y = py0 + 2
    for label, value in fields:
        text(d, (fx, y), label, SANS, 10, MUTED)
        text(d, (fx, y + 12), value, SANS_B, 14, INK)
        y += 28
    # issue / expiry block -- starts below the portrait and the fields
    y = py0 + 196 + 34
    hline(d, mx, x0 + pw - 26, y, RULE, 1)
    y += 12
    cols = [
        ("Date of issue / Izdato", "14 MAR 2023"),
        ("Date of expiry / Vazi do", "13 MAR 2033"),
        ("Authority / Organ", "MINISTRY OF THE INTERIOR"),
    ]
    cx = mx
    for label, value in cols[:2]:
        text(d, (cx, y), label, SANS, 10, MUTED)
        text(d, (cx, y + 12), value, SANS_B, 14, INK)
        cx += 190
    y += 44
    text(d, (mx, y), cols[2][0], SANS, 10, MUTED)
    text(d, (mx, y + 12), cols[2][1] + " — DRENOVIK", SANS_B, 14, INK)
    # signature
    y += 52
    d.line([(mx, y + 26), (mx + 190, y + 26)], fill=INK, width=1)
    text(d, (mx, y + 30), "Holder's signature / Potpis", SANS, 10, MUTED)
    sig = Image.new("RGBA", (200, 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sig)
    sd.line([(4, 28), (30, 8), (52, 30), (74, 10), (96, 28), (120, 12),
             (150, 26), (180, 14)], fill=(40, 40, 90, 255), width=2)
    sd.line([(60, 34), (150, 34)], fill=(40, 40, 90, 255), width=1)
    img.alpha_composite(sig, (mx, y - 6))
    # endorsements -- fills the lower page and ties holder to the country
    y += 78
    hline(d, mx, x0 + pw - 26, y, RULE, 1)
    y += 12
    text(d, (mx, y), "Endorsements / Zabiljeske", SANS, 10, MUTED)
    y += 16
    text(d, (mx, y), "HOLDER IS A LICENSED MOUNTAIN GUIDE,",
         SANS_B, 13, INK)
    y += 20
    text(d, (mx, y), "AUTHORISED TO LEAD PARTIES OVER DRENOVIK PASS.",
         SANS_B, 13, INK)
    # MRZ
    l1, l2 = mrz_lines()
    my = y0 + ph - 74
    d.rectangle([mx, my - 8, x0 + pw - 26, my + 44], fill=(238, 234, 220))
    text(d, (mx, my), l1, MONO_B, 15, INK)
    text(d, (mx, my + 20), l2, MONO_B, 15, INK)


def visa_page(img, x0, y0, pw, ph):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PAPER,
                outline=(120, 112, 92), width=2)
    mx = x0 + 26
    text(d, (x0 + pw // 2, y0 + 24), "VISAS", SERIF_B, 20,
         (52, 64, 96), anchor="ma")
    text(d, (x0 + pw // 2, y0 + 50), "VIZE  •  STAMPS OF ENTRY AND EXIT",
         SANS, 11, MUTED, anchor="ma")
    hline(d, mx, x0 + pw - 26, y0 + 76, RULE, 1)
    blue = (38, 62, 150)
    purple = (110, 48, 140)
    # travel story, all dates after the 14 Mar 2023 issue date
    draw_stamp(img, x0 + 125, y0 + 165, 190, 92, -6, blue,
               ["KOVAR", "ENTRY", "02 JUN 2023", "GORAZ PASS"])
    draw_stamp(img, x0 + 345, y0 + 165, 190, 92, 5, blue,
               ["KOVAR", "EXIT", "18 JUN 2023", "GORAZ PASS"])
    draw_stamp(img, x0 + 125, y0 + 300, 190, 92, 4, purple,
               ["BREZNA", "ENTRY", "05 SEP 2024", "BISTRICA"])
    draw_stamp(img, x0 + 345, y0 + 300, 190, 92, -5, purple,
               ["BREZNA", "EXIT", "21 SEP 2024", "BISTRICA"])
    draw_stamp(img, x0 + 125, y0 + 435, 190, 92, -3, blue,
               ["KOVAR", "ENTRY", "03 MAY 2025", "GORAZ PASS"])
    draw_stamp(img, x0 + 345, y0 + 435, 190, 92, 6, blue,
               ["KOVAR", "EXIT", "17 MAY 2025", "GORAZ PASS"])
    # the telling detail: winter-closure condition + pass fee
    draw_condition_stamp(img, x0 + pw // 2, y0 + 590, 380, 116, -2)
    draw_fee_stamp(img, x0 + pw // 2, y0 + 700, 210, 74, 3)
    # page number and a quiet footer line
    text(d, (x0 + pw - 26, y0 + ph - 34), "4 — 5", SANS, 11, MUTED,
         anchor="ra")
    text(d, (mx, y0 + ph - 34), "TALSORIA — DRENOVIK PASS",
         SANS, 11, MUTED)


def main():
    img = Image.new("RGBA", (W, H), (58, 66, 82))
    d = ImageDraw.Draw(img)
    # desk vignette
    for i in range(60):
        a = int(10 * (1 - i / 60))
        d.rectangle([i, i, W - i, H - i], outline=(255, 255, 255, a))
    # soft drop shadow under the spread
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([40, 66, 992, 982], fill=(0, 0, 0, 90))
    shadow = shadow.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(10))
    img.alpha_composite(shadow)
    # two pages
    data_page(img, 32, 52, 470, 920)
    visa_page(img, 522, 52, 470, 920)
    # centre gutter shading
    gutter = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gutter)
    gd.rectangle([498, 52, 526, 972], fill=(0, 0, 0, 70))
    img.alpha_composite(gutter)
    img = img.convert("RGB")
    os.makedirs("/output", exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()

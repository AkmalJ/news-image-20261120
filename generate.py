#!/usr/bin/env python3
"""Render the news-image-20261120 entry: one page summing up the world news
of Friday 20 November 2026. Deterministic: same bytes on every run."""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
INK = (18, 18, 18)
RED = (178, 34, 30)
NAVY = (23, 42, 74)
GOLD = (198, 148, 42)
GREEN = (46, 110, 62)
TEAL = (38, 120, 122)
PURPLE = (96, 62, 140)
GREY = (90, 88, 80)
LIGHT = (238, 231, 214)

FD = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FD + "LiberationSerif-Bold.ttf"
SERIF = FD + "LiberationSerif-Regular.ttf"
SERIF_I = FD + "LiberationSerif-Italic.ttf"
SANS_B = FD + "LiberationSans-Bold.ttf"
SANS = FD + "LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, font):
    return d.textlength(s, font=font)


# ---------------------------------------------------------------- data
KICKER_R = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
DEK = ("Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · "
       "An AI sell-off sinks Asia's markets · UK and EU seal a deal")

STATS = [
    ("3", "Dnipro bridges hit in Kyiv"),
    ("300,000+", "people moved before Akvan"),
    ("-6.2%", "Taiwan index, Friday's close"),
    ("100,000", "youth visas a year, UK-EU deal"),
    ("2.3%", "Japan inflation in October"),
    ("118", "Phillips runs against India"),
]

REGIONS = [("Europe", 8, (52, 92, 150)), ("Asia", 9, RED),
           ("Middle East", 4, GOLD), ("Africa", 4, GREEN),
           ("Americas", 4, PURPLE), ("Oceania", 3, TEAL),
           ("Global", 3, (60, 60, 60))]

FEATURES = [
    dict(n=1, label="KYIV, UKRAINE · WAR", art="kyiv",
         tag="Officials' count · Kyiv Independent · BBC",
         head="Russian missiles hit three Kyiv bridges",
         cap="An overnight barrage of more than 110 missiles and more than "
             "400 drones killed at least eight people across Ukraine and "
             "damaged the capital's Dnipro bridges. (Kyiv Independent, BBC)"),
    dict(n=2, label="ODISHA, INDIA · CYCLONE", art="akvan",
         tag="Weather office · IMD · Deccan Herald",
         head="Cyclone Akvan comes ashore in eastern India",
         cap="The storm crossed the coast near Gopalpur from about 8 am after "
             "more than 300,000 people were moved to shelters. No deaths were "
             "reported. (IMD, Deccan Herald)"),
    dict(n=3, label="TAIPEI · SEOUL · TOKYO · MARKETS", art="selloff",
         tag="Closing prices · Exchange data · Reuters",
         head="AI sell-off sinks Asia's stock markets",
         cap="Chip stocks led the fall \u2014 Nvidia about 14% lower, AMD about "
             "13%. Taiwan's index fell 6.2% to end its worst week since 1991; "
             "Seoul lost 5.2% and Tokyo 5.1%. (Exchange closes, Reuters)"),
]

MEDIUMS = [
    dict(n=4, label="BRUSSELS · DIPLOMACY", art="ukeu", strip="Agreed · Reuters",
         head="UK and EU seal a \u201creset\u201d deal",
         cap="Food trade, carbon link, youth visas."),
    dict(n=5, label="ANTALYA · CLIMATE", art="cop", strip="Ongoing · UN News",
         head="COP31 reaches its last day with no deal",
         cap="The draft text leaves out fossil fuels."),
    dict(n=6, label="EASTERN POLAND · SECURITY", art="poland",
         strip="Deliberate provocation · NATO",
         head="Two Russian missiles come down in Poland",
         cap="A suspected drone fell too; NATO jets scrambled."),
    dict(n=7, label="CENTRAL IRAQ · SECURITY", art="iraq",
         strip="Witnessed · Reuters",
         head="Iraqi army enters a militia stronghold",
         cap="Troops deploy to Jurf al-Sakhar."),
    dict(n=8, label="ITALY · LABOUR", art="italy", strip="Reported · Reuters",
         head="General strike over Italy's budget",
         cap="Workers and students march."),
    dict(n=9, label="TOKYO · ECONOMY", art="japan",
         strip="Official data · Reuters",
         head="Japan's inflation picks up to 2.3%",
         cap="A December rate rise stays in view."),
    dict(n=10, label="SEOUL · POLITICS", art="seoul",
         strip="Party decision · Korea Herald",
         head="Korea's ruling party to impeach top judge",
         cap="It follows an overturned conviction."),
    dict(n=11, label="TURKANA, KENYA · ENERGY", art="kenya",
         strip="Ceremony held · allAfrica",
         head="Kenya starts drilling its first oil well",
         cap="First crude is due on 1 December."),
    dict(n=12, label="SAN SALVADOR · POLITICS", art="bukele", strip="Filed · AP",
         head="Bukele files to run for a third term",
         cap="The vote is on 28 February 2027."),
    dict(n=13, label="WELLINGTON · CRICKET", art="cricket",
         strip="Scorecard · ICC",
         head="Phillips hits 118 against India",
         cap="Hundreds v India in all three formats."),
]

BRIEFS = [
    ("Lviv", "A strike on a railway station kills two (BBC)"),
    ("Hormuz", "Tankers catch fire; IEA says energy markets permanently altered"),
    ("Berlin", "School pupils strike against military service"),
    ("New Delhi", "Pakistan minister Malik arrives, first since the 2025 conflict"),
    ("Naypyidaw", "Myanmar's rulers dismiss the genocide ruling (CNN)"),
    ("Beijing", "China holds loan prime rates for an 18th month"),
    ("Seoul", "Kospi ends the week 7.9% lower (Anadolu)"),
    ("Ganjam", "209 mm of rain falls as Akvan crosses (PTI)"),
    ("Lebanon", "Israel strikes a Hezbollah missile factory in the Beqaa"),
    ("Copenhagen", "Parliament ratifies the US security deal on Greenland"),
    ("Abuja", "Court bars new evidence against Tinubu"),
    ("Riyadh", "Saudis down a Houthi missile, then strike Hudaydah and Sanaa"),
    ("Malawi", "Fuel crisis brings night-long petrol queues"),
    ("Africa", "AfDB says 22 countries are in debt distress"),
    ("Las Vegas", "Russell fastest in wet Grand Prix practice"),
    ("New York", "Nasdaq closes 5.28% lower in the rout (Reuters)"),
    ("Tallinn", "Estonia to shut border crossings with Russia after sabotage"),
    ("New York", "Anthropic falls about 9% to $89 (Reuters)"),
    ("Wellington", "Nicholls makes 175 in a stand of 216 (ICC)"),
    ("Sydney", "Australian shares fall 1.6% in the sell-off"),
    ("Antalya", "Panama-led group demands fossil fuels back in the COP31 draft"),
    ("Antalya", "EU official calls the climate draft unacceptable"),
]

DATE_CHECK = (
    "Left out on purpose \u2014 first reported Thursday 19 November: the "
    "Trump-Xi-Putin Shenzhen summit · the World Court's Myanmar (Rohingya) "
    "ruling · Anthropic's $83 IPO debut (Friday's fall is brief 31) · the "
    "Senate's 51-48 Iran war-powers vote · the Crimea Bridge strike · the "
    "Houthi hit on Riyadh's PIF Tower · Tonga's drought emergency · GTA VI's "
    "launch · the $190.4m Van Gogh sale · Voyager 1's light-day · Fiona's "
    "death. Not yet: "
    "BepiColombo enters Mercury orbit (Sat 21) · a final COP31 text · the "
    "ATP Finals final (Sun 22).")

FOOTER_L = ("Every story here happened, or was first reported, on Friday "
            "20 November 2026. Officials' counts are attributed.")
FOOTER_R = "Sources named beside each story · Original drawings"


# ---------------------------------------------------------------- helpers
def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, xy, text, font, fill, width, leading):
    x, y = xy
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, font, bg, fg=(255, 255, 255), pad=5):
    w_ = tw(d, text, font) + pad * 2
    d.rectangle([x, y, x + w_, y + font.size + pad], fill=bg)
    d.text((x + pad, y + pad // 2), text, font=font, fill=fg)
    return w_


def num_badge(d, x, y, n, r=9):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    s = str(n)
    f = F(SANS_B, 11)
    d.text((x + r - tw(d, s, f) / 2, y + r - 7), s, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- scenes
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 48))
    rng = random.Random(7)
    for _ in range(46):  # stars / city sparks
        sx, sy = x + rng.randrange(w), y + rng.randrange(int(h * 0.5))
        d.point((sx, sy), fill=(200, 210, 235))
    river_y = y + int(h * 0.72)
    # two-layer skyline on the far bank, back layer taller and darker
    for bx, bw_, bh, col in ((0.02, 30, 34, (26, 40, 68)), (0.13, 22, 44, (26, 40, 68)),
                             (0.30, 34, 30, (26, 40, 68)), (0.55, 26, 40, (26, 40, 68)),
                             (0.68, 36, 32, (26, 40, 68)), (0.86, 28, 42, (26, 40, 68))):
        d.rectangle([x + int(w * bx), river_y - bh, x + int(w * bx) + bw_, river_y],
                    fill=col)
    for bx, bw_, bh in ((0.06, 20, 24), (0.22, 16, 30), (0.42, 24, 22),
                        (0.60, 18, 27), (0.76, 22, 20), (0.92, 16, 26)):
        x0 = x + int(w * bx)
        d.rectangle([x0, river_y - bh, x0 + bw_, river_y], fill=(34, 52, 84))
        for _ in range(6):  # lit windows
            wx = x0 + 2 + rng.randrange(max(3, bw_ - 5))
            wy = river_y - bh + 3 + rng.randrange(max(3, bh - 6))
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(246, 200, 110))
    d.rectangle([x, river_y, x + w, y + h], fill=(24, 52, 92))
    d.text((x + w - 62, river_y + 8), "DNIPRO", font=F(SANS_B, 10),
           fill=(150, 185, 225))
    for bx in (0.16, 0.47, 0.78):  # three bridges: deck + towers + arc + cables
        cx = x + int(w * bx)
        d.line([cx - 52, river_y, cx + 52, river_y], fill=(150, 170, 205), width=3)
        for tx in (cx - 34, cx + 30):
            d.rectangle([tx, river_y - 34, tx + 5, river_y], fill=(150, 170, 205))
            for ex in (cx - 46, cx - 20, cx + 18, cx + 44):  # cable stays
                d.line([tx + 2, river_y - 33, ex, river_y - 1],
                       fill=(110, 135, 180), width=1)
        d.arc([cx - 48, river_y - 26, cx + 48, river_y + 14], 180, 360,
              fill=(120, 145, 190), width=2)
    for i, fx in enumerate((0.16, 0.47, 0.78)):  # fires + smoke on the decks
        cx, cy = x + int(w * fx), river_y - 2 - (i % 2) * 5
        for s in range(3):  # smoke plume: stacked soft ellipses drifting right
            exx, eyy = cx + 5 + s * 7, cy - 24 - s * 7
            d.ellipse([exx - 6 + s * 2, eyy - 4, exx + 6 + s * 2, eyy + 4],
                      fill=(88, 96, 118))
        d.polygon([(cx - 8, cy), (cx, cy - 20), (cx + 8, cy)], fill=(232, 120, 40))
        d.polygon([(cx - 4, cy), (cx, cy - 11), (cx + 4, cy)], fill=(246, 190, 70))
    for i in range(3):  # missile trails
        sx, sy = x + int(w * (0.55 + 0.14 * i)), y + 8 + i * 5
        ex, ey = x + int(w * (0.28 + 0.2 * i)), river_y - 16
        pts = []
        for t in range(21):
            u = t / 20
            px = sx + (ex - sx) * u
            py = sy + (ey - sy) * u - math.sin(u * math.pi) * 16
            pts.append((px, py))
        d.line(pts, fill=(240, 200, 120), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(250, 220, 150))
    bw = chip(d, x + 8, y + 8, "KYIV", F(SANS_B, 21), RED)
    chip(d, x + 8, y + 40, "3 bridges hit", F(SANS_B, 13), (245, 245, 245), INK)
    chip(d, x + 8, y + 66, "110+ missiles · 400+ drones", F(SANS_B, 10), INK)


def art_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 208, 224))
    land = [(x, y + h), (x, y + int(h * 0.30)), (x + int(w * 0.16), y + int(h * 0.33)),
            (x + int(w * 0.24), y + int(h * 0.30)), (x + int(w * 0.30), y + int(h * 0.38)),
            (x + int(w * 0.37), y + int(h * 0.44)), (x + int(w * 0.33), y + int(h * 0.52)),
            (x + int(w * 0.44), y + int(h * 0.58)), (x + int(w * 0.40), y + h)]
    d.polygon(land, fill=(226, 205, 160))
    for i in range(9):  # hatch texture on the land
        hx = x + 8 + i * 11
        d.line([hx, y + h - 8, hx + 8, y + h - 22], fill=(206, 182, 132), width=2)
    cx, cy = x + int(w * 0.66), y + int(h * 0.52)
    for r, col in ((52, (96, 152, 186)), (44, (70, 130, 170)), (33, (90, 150, 190)),
                   (22, (120, 175, 210)), (12, (240, 246, 250))):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 320, fill=col, width=5)
    rng = random.Random(11)
    for _ in range(26):  # rain streaks under the storm's east side
        rx = cx + rng.randrange(-8, int(w * 0.30))
        ry = cy + rng.randrange(-16, int(h * 0.30))
        d.line([rx, ry, rx - 4, ry + 7], fill=(110, 160, 195), width=2)
    d.line([cx - 52, cy + 30, x + int(w * 0.36), y + int(h * 0.60)],
           fill=RED, width=3)
    d.polygon([(x + int(w * 0.36), y + int(h * 0.60)), (x + int(w * 0.36) + 11,
               y + int(h * 0.60) - 3), (x + int(w * 0.36) + 4, y + int(h * 0.60) + 8)],
              fill=RED)
    gx, gy = x + int(w * 0.20), y + int(h * 0.50)
    d.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=INK)
    d.text((gx - 8, gy + 7), "GOPALPUR", font=F(SANS_B, 10), fill=INK)
    d.text((x + int(w * 0.47), y + 8), "CYCLONE AKVAN", font=F(SANS_B, 17), fill=RED)
    chip(d, x + int(w * 0.47), y + 34, "Landfall · 8 am", F(SANS_B, 12), INK)
    chip(d, x + 8, y + 8, "300,000+ moved", F(SANS_B, 10), INK)


def art_selloff(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 22, 30))
    gx, gy, gw, gh = x + 14, y + 44, int(w * 0.44), int(h * 0.52)
    for i in range(4):
        yy = gy + gh * i // 3
        d.line([gx, yy, gx + gw, yy], fill=(70, 74, 90), width=1)
    pts = [(gx, gy + 4), (gx + gw * 0.3, gy + gh * 0.24), (gx + gw * 0.52, gy + gh * 0.2),
           (gx + gw * 0.74, gy + gh * 0.62), (gx + gw, gy + gh - 2)]
    d.line(pts, fill=(235, 80, 70), width=3)
    d.polygon([(gx + gw, gy + gh - 2), (gx + gw - 10, gy + gh - 12),
               (gx + gw - 1, gy + gh - 14)], fill=(235, 80, 70))
    chip(d, x + 8, y + 8, "AI SELL-OFF", F(SANS_B, 19), RED)
    d.text((x + 10, y + 34), "Asia, Friday's close", font=F(SANS_B, 11),
           fill=(230, 230, 230))
    rows = [("Taipei", "-6.2%"), ("Seoul", "-5.2%"), ("Tokyo", "-5.1%"),
            ("Hong Kong", "-1.9%")]
    tx = x + int(w * 0.60)
    for i, (name, val) in enumerate(rows):
        yy = y + 14 + i * 24
        d.text((tx, yy), name, font=F(SANS_B, 13), fill=(235, 235, 235))
        d.text((tx + 96, yy), val, font=F(SANS_B, 13), fill=(240, 110, 95))


# ---------------------------------------------------------------- medium art
def art_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 7, y + 5), "UK-EU DEAL", font=F(SANS_B, 16), fill=(255, 255, 255))
    d.text((x + 7, y + 22), "100,000", font=F(SANS_B, 19), fill=(255, 255, 255))
    fx, fy, fw, fh = x + w - 62, y + 8, 54, 38  # simplified Union Jack
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(30, 60, 140))
    d.line([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), width=5)
    d.line([fx + fw, fy, fx, fy + fh], fill=(255, 255, 255), width=5)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(255, 255, 255), width=9)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(255, 255, 255), width=9)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=RED, width=4)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=RED, width=4)


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 226, 190))
    d.text((x + 7, y + 5), "COP31: NO DEAL", font=F(SANS_B, 14), fill=INK)
    d.text((x + 7, y + 24), "$120bn", font=F(SANS_B, 17), fill=INK)
    d.text((x + 70, y + 30), "adaptation gap", font=F(SANS, 9), fill=GREY)
    cx, cy = x + w - 50, y + 19
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=(60, 110, 160), width=3)
    d.ellipse([cx - 5, cy - 13, cx + 5, cy + 13], outline=(60, 110, 160), width=2)
    d.line([cx - 13, cy, cx + 13, cy], fill=(60, 110, 160), width=2)
    kx, ky = x + w - 18, y + h - 15  # clock: overtime
    d.ellipse([kx - 11, ky - 11, kx + 11, ky + 11], outline=INK, width=2)
    d.line([kx, ky, kx, ky - 7], fill=INK, width=2)
    d.line([kx, ky, kx + 6, ky + 3], fill=INK, width=2)


def art_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 178))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(150, 128, 84))
    d.text((x + 7, y + 5), "POLAND: MISSILES", font=F(SANS_B, 14), fill=INK)
    d.text((x + 7, y + 24), "JETS SCRAMBLED", font=F(SANS_B, 13), fill=(70, 70, 60))
    d.text((x + 7, y + 43), "Patriots activated", font=F(SANS, 9), fill=(70, 70, 60))
    mx, my = x + w - 56, y + 22  # missile body, nose down-left
    d.polygon([(mx, my + 22), (mx + 12, my + 4), (mx + 22, my), (mx + 16, my + 14),
               (mx + 8, my + 26)], fill=(120, 124, 132))
    d.polygon([(mx + 16, my + 14), (mx + 26, my + 22), (mx + 14, my + 24)], fill=RED)
    for i in range(3):
        d.line([mx + 20 + i * 7, my - 2 - i * 2, mx + 30 + i * 7, my - 6 - i * 2],
               fill=(235, 160, 70), width=2)


def art_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 196, 158))
    d.text((x + 7, y + 5), "IRAQ: ARMY IN", font=F(SANS_B, 15), fill=INK)
    d.text((x + 7, y + 26), "FIRST SINCE 2014", font=F(SANS_B, 11), fill=(96, 82, 58))
    for i, tx in enumerate((x + w - 96, x + w - 58)):  # two trucks
        ty = y + h - 24
        d.rectangle([tx, ty, tx + 30, ty + 12], fill=(96, 100, 74))
        d.rectangle([tx + 22, ty - 7, tx + 30, ty], fill=(96, 100, 74))
        d.ellipse([tx + 4, ty + 10, tx + 12, ty + 18], fill=INK)
        d.ellipse([tx + 20, ty + 10, tx + 28, ty + 18], fill=INK)


def art_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 210))
    d.text((x + 7, y + 5), "ITALY: STRIKE", font=F(SANS_B, 14), fill=INK)
    sx = x + w - 88
    d.rectangle([sx, y + 6, sx + 82, y + 22], fill=RED)
    d.text((sx + 6, y + 9), "SCIOPERO", font=F(SANS_B, 11), fill=(255, 255, 255))
    for i in range(8):  # crowd heads
        hx = x + w - 104 + i * 12
        d.ellipse([hx, y + h - 18, hx + 9, y + h - 9], fill=INK)
        d.rectangle([hx + 1, y + h - 9, hx + 8, y + h - 2], fill=INK)


def art_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 240, 232))
    d.text((x + 7, y + 5), "JAPAN: +2.3%", font=F(SANS_B, 17), fill=INK)
    d.text((x + 7, y + 26), "October CPI · core 2.2%", font=F(SANS_B, 10), fill=GREY)
    bx = x + w - 92
    for i, bh in enumerate((10, 16, 24, 33)):
        d.rectangle([bx + i * 20, y + h - 8 - bh, bx + i * 20 + 13, y + h - 8],
                    fill=(90, 120, 170) if i < 3 else RED)
    d.ellipse([x + w - 34, y + 6, x + w - 14, y + 26], fill=RED)


def art_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 204))
    d.text((x + 7, y + 5), "SEOUL: IMPEACH", font=F(SANS_B, 14), fill=INK)
    d.text((x + 7, y + 25), "THE CHIEF JUSTICE", font=F(SANS_B, 10), fill=(70, 66, 58))
    bx = x + w - 52  # courthouse columns
    d.polygon([(bx, y + 10), (bx + 44, y + 10), (bx + 22, y + 2)], fill=(120, 116, 104))
    for i in range(4):
        d.rectangle([bx + 3 + i * 11, y + 13, bx + 8 + i * 11, y + 34],
                    fill=(150, 146, 134))
    d.rectangle([bx - 2, y + 35, bx + 48, y + 39], fill=(120, 116, 104))
    gx, gy = x + w - 66, y + 44  # gavel
    d.line([gx - 8, gy + 6, gx + 5, gy - 5], fill=(120, 84, 40), width=4)
    d.rectangle([gx + 1, gy - 11, gx + 12, gy - 3], fill=(120, 84, 40))


def art_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 170))
    d.text((x + 7, y + 5), "KENYA: OIL", font=F(SANS_B, 15), fill=INK)
    d.text((x + 7, y + 26), "WELL No. 1", font=F(SANS_B, 11), fill=(96, 76, 44))
    dx, dy = x + w - 62, y + 6  # derrick
    d.polygon([(dx, dy + 40), (dx + 13, dy), (dx + 26, dy + 40)], outline=INK, width=2)
    d.line([dx + 4, dy + 27, dx + 22, dy + 27], fill=INK, width=2)
    d.line([dx + 7, dy + 15, dx + 19, dy + 15], fill=INK, width=2)
    d.ellipse([x + w - 30, y + 8, x + w - 16, y + 22], fill=GOLD)


def art_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 7, y + 5), "BUKELE: 3RD BID", font=F(SANS_B, 15), fill=(255, 255, 255))
    d.text((x + 7, y + 26), "VOTE 28 FEB 2027", font=F(SANS_B, 11), fill=(230, 238, 250))
    bx, by = x + w - 66, y + h - 26  # ballot box + paper
    d.rectangle([bx, by, bx + 44, by + 20], fill=(240, 240, 240))
    d.rectangle([bx + 8, by + 4, bx + 36, by + 7], fill=INK)
    d.polygon([(bx + 14, by - 10), (bx + 32, by - 10), (bx + 28, by + 3),
               (bx + 18, by + 3)], fill=(255, 255, 255))
    d.text((bx + 19, by - 9), "\u2713", font=F(SANS_B, 11), fill=RED)


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=GREEN)
    d.text((x + 7, y + 5), "PHILLIPS: 118", font=F(SANS_B, 17), fill=(255, 255, 255))
    d.text((x + 7, y + 26), "v India · Wellington", font=F(SANS_B, 10),
           fill=(205, 235, 210))
    for i in range(3):  # stumps
        d.rectangle([x + w - 52 + i * 9, y + 12, x + w - 49 + i * 9, y + 34],
                    fill=(240, 220, 150))
    d.ellipse([x + w - 30, y + h - 20, x + w - 18, y + h - 8], fill=RED)
    d.line([x + w - 84, y + h - 8, x + w - 58, y + 14], fill=(210, 180, 120), width=5)


MED_ART = {"ukeu": art_ukeu, "cop": art_cop, "poland": art_poland,
           "iraq": art_iraq, "italy": art_italy, "japan": art_japan,
           "seoul": art_seoul, "kenya": art_kenya, "bukele": art_bukele,
           "cricket": art_cricket}


# ---------------------------------------------------------------- map
MAP_ROWS = [
    "                                                                      ",
    "        ##########                                                    ",
    "      ###############        ##  ####  ########################       ",
    "     #################      ############################ ######       ",
    "      ################      #############################             ",
    "       #############         ##################  ##########           ",
    "        ##########            ################    ########            ",
    "         ########              ##############      ######             ",
    "          ######                ############       #####              ",
    "           #####                 ##########       ####                ",
    "           ######                 ########        ###                 ",
    "            #####                 #########       ##                  ",
    "            ######               ##########                           ",
    "             #####               ##########                           ",
    "             ######               ########                            ",
    "              ####                 ######                             ",
    "              ###                   ####            ##                ",
    "              ##                    ###            ########           ",
    "                                     ##              ######           ",
    "                                                      ##  ##          ",
    "                                                            #  ##     ",
    "                                                                ##    ",
]
PINS = {1: (36, 3), 2: (47, 11), 3: (53, 10), 4: (31, 3), 5: (39, 7),
        6: (34, 4), 7: (42, 8), 8: (33, 6), 9: (57, 8), 10: (54, 7),
        11: (39, 14), 12: (7, 11), 13: (64, 20)}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    rows, cols = len(MAP_ROWS), max(len(r) for r in MAP_ROWS)
    px, py = w / cols, h / rows
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                cx, cy = x + ci * px + px / 2, y + ri * py + py / 2
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=(233, 222, 192))
    for n, (ci, ri) in PINS.items():
        cx, cy = x + ci * px + px / 2, y + ri * py + py / 2
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
        s = str(n)
        f = F(SANS_B, 9)
        d.text((cx - tw(d, s, f) / 2, cy - 5), s, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- compose
def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX, CW = 16, W - 32

    # masthead
    d.text((MX, 10), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=RED)
    kr = F(SANS_B, 12)
    d.text((W - MX - tw(d, KICKER_R, kr), 11), KICKER_R, font=kr, fill=INK)
    d.line([MX, 32, W - MX, 32], fill=INK, width=2)
    size = 88
    while tw(d, "Friday 20 November 2026", F(SERIF_B, size)) > CW:
        size -= 2
    d.text((MX, 38), "Friday 20 November 2026", font=F(SERIF_B, size), fill=INK)
    y = 38 + size + 6
    dk = F(SERIF_I, 16)
    d.text(((W - tw(d, DEK, dk)) / 2, y), DEK, font=dk, fill=(40, 40, 40))
    y += 26

    # numbers strip
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    cw6 = CW / 6
    for i, (num, lab) in enumerate(STATS):
        cx = MX + i * cw6 + 8
        if i:
            d.line([MX + i * cw6, y + 4, MX + i * cw6, y + 44], fill=(170, 160, 140), width=1)
        d.text((cx, y + 4), num, font=F(SERIF_B, 25), fill=INK)
        ly = y + 35
        for ln in lab.split("\n"):
            d.text((cx, ly), ln, font=F(SANS, 9), fill=GREY)
            ly += 11
    y += 54
    d.line([MX, y - 4, W - MX, y - 4], fill=INK, width=1)

    # region bar
    total = sum(c for _, c, _ in REGIONS)
    bx = MX
    for name, cnt, col in REGIONS:
        seg = CW * cnt / total
        d.rectangle([bx, y, bx + seg - 2, y + 17], fill=col)
        lab = "%s %d" % (name, cnt)
        lf = F(SANS_B, 10)
        d.text((bx + (seg - tw(d, lab, lf)) / 2, y + 3), lab, font=lf,
               fill=(255, 255, 255))
        bx += seg
    y += 27

    # features
    fw = int((CW - 24) / 3)
    for i, ft in enumerate(FEATURES):
        fx = MX + i * (fw + 12)
        {"kyiv": art_kyiv, "akvan": art_akvan, "selloff": art_selloff}[ft["art"]](
            d, fx, y, fw, 110)
        chip(d, fx, y + 110 - 17, ft["tag"], F(SANS_B, 9), INK)
        ly = y + 117
        num_badge(d, fx, ly, ft["n"])
        d.text((fx + 24, ly + 1), ft["label"], font=F(SANS_B, 11), fill=RED)
        hy = block(d, (fx, ly + 19), ft["head"], F(SERIF_B, 20), INK, fw, 22)
        block(d, (fx, hy + 1), ft["cap"], F(SERIF, 11), (45, 45, 45), fw, 13.5)
    y += 117 + 19 + 44 + 41 + 6

    # mediums: two rows of five
    mw = int((CW - 40) / 5)
    for row in range(2):
        for col in range(5):
            md = MEDIUMS[row * 5 + col]
            mx = MX + col * (mw + 10)
            MED_ART[md["art"]](d, mx, y, mw, 56)
            chip(d, mx, y + 56 - 14, md["strip"], F(SANS, 8), INK, pad=4)
            ly = y + 61
            num_badge(d, mx, ly, md["n"], r=8)
            d.text((mx + 21, ly), md["label"], font=F(SANS_B, 9), fill=RED)
            hy = block(d, (mx, ly + 16), md["head"], F(SERIF_B, 14), INK, mw, 16)
            block(d, (mx, hy + 1), md["cap"], F(SANS, 9), (45, 45, 45), mw, 12)
        y += 61 + 16 + 32 + 14 + 7

    # bottom block: map + briefs
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 6
    d.text((MX, y), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    bh = "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES"
    d.text((MX + 344, y), bh, font=F(SANS_B, 12), fill=INK)
    y += 18
    draw_map(d, MX, y, 330, 140)
    d.text((MX, y + 144), "Each number is the story with that number on this page.",
           font=F(SANS, 9), fill=GREY)
    hs = ("HOW SURE: the tags on each card \u2014 CONFIRMED means two or more "
          "outlets, OFFICIAL means on the record, REPORTED means one outlet.")
    block(d, (MX, y + 158), hs, F(SANS, 9), GREY, 330, 12)
    # briefs in two columns, cumulative heights so wrapped lines never collide
    bf = F(SANS, 10)
    bfb = F(SANS_B, 10)
    place_cols = [RED, (52, 92, 150), GREEN, TEAL, PURPLE, (150, 96, 20)]
    colw = (CW - 344 - 16) / 2
    col_y = [y, y]
    for i, (place, text) in enumerate(BRIEFS):
        col = 0 if col_y[0] <= col_y[1] else 1
        bx = MX + 344 + col * (colw + 16)
        by = col_y[col]
        num = str(14 + i)
        d.text((bx, by), num, font=F(SANS_B, 10), fill=RED)
        tx = bx + 20
        d.text((tx, by), place, font=bfb, fill=place_cols[i % len(place_cols)])
        tx += tw(d, place, bfb) + 3
        lines = wrap(d, text, bf, bx + colw - tx)
        d.text((tx, by), lines[0] if lines else "", font=bf, fill=(35, 35, 35))
        for j, ln in enumerate(lines[1:]):
            d.text((bx + 20, by + 11.25 * (j + 1)), ln, font=bf, fill=(35, 35, 35))
        col_y[col] = by + 11.25 * len(lines) + 3.0
    y = max(y + 182, max(col_y)) + 6

    # date check (box height follows the wrapped text)
    dc_lines = wrap(d, DATE_CHECK, F(SANS, 10), CW - 88)
    boxh = len(dc_lines) * 13 + 12
    d.rectangle([MX, y, W - MX, y + boxh], outline=RED, width=2)
    d.text((MX + 8, y + 6), "DATE CHECK", font=F(SANS_B, 10), fill=RED)
    ly = y + 6
    for ln in dc_lines:
        d.text((MX + 74, ly), ln, font=F(SANS, 10), fill=(35, 35, 35))
        ly += 13
    y += boxh + 8

    # footer
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    d.text((MX, y + 5), FOOTER_L, font=F(SANS, 9), fill=GREY)
    fr = F(SANS, 9)
    d.text((W - MX - tw(d, FOOTER_R, fr), y + 5), FOOTER_R, font=fr, fill=GREY)
    return img


def main():
    img = compose()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

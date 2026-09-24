#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valeurs rythmiques, silences, clave, tresillo, cinquillo (SVG)."""
from diagrams_chords import (write, svg_open, INK, SOFT, MUTE, RUST, RUSTD,
                             TEAL, GOLD, GREEN, LINE, SAND, PAPER, SERIF, MONO)

PLUM = "#6B3A5B"


# ---------------------------------------------------------------- notes
def note_glyph(cx, cy, kind, col=INK, stem_up=True, scale=1.0):
    """kind : ronde, blanche, noire, croche, double"""
    s = []
    rx, ry = 7.2 * scale, 5.4 * scale
    filled = kind not in ("ronde", "blanche")
    s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
             f'transform="rotate(-18 {cx:.1f} {cy:.1f})" '
             f'fill="{col if filled else "none"}" stroke="{col}" stroke-width="{1.9*scale:.1f}"/>')
    if kind != "ronde":
        sx = cx + rx * 0.88
        sy1 = cy - 1 * scale
        sy2 = cy - 34 * scale
        s.append(f'<line x1="{sx:.1f}" y1="{sy1:.1f}" x2="{sx:.1f}" y2="{sy2:.1f}" '
                 f'stroke="{col}" stroke-width="{1.9*scale:.1f}"/>')
        if kind in ("croche", "double"):
            s.append(f'<path d="M {sx:.1f} {sy2:.1f} C {sx+13*scale:.1f} {sy2+7*scale:.1f}, '
                     f'{sx+13*scale:.1f} {sy2+16*scale:.1f}, {sx+4*scale:.1f} {sy2+23*scale:.1f}" '
                     f'fill="none" stroke="{col}" stroke-width="{2.4*scale:.1f}" stroke-linecap="round"/>')
        if kind == "double":
            s.append(f'<path d="M {sx:.1f} {sy2+9*scale:.1f} C {sx+13*scale:.1f} {sy2+16*scale:.1f}, '
                     f'{sx+13*scale:.1f} {sy2+25*scale:.1f}, {sx+4*scale:.1f} {sy2+32*scale:.1f}" '
                     f'fill="none" stroke="{col}" stroke-width="{2.4*scale:.1f}" stroke-linecap="round"/>')
    return "".join(s)


def rest_glyph(cx, cy, kind, col=INK):
    """pause, demi-pause, soupir, demi-soupir, quart"""
    s = []
    if kind == "pause":        # rectangle sous la ligne
        s.append(f'<rect x="{cx-9}" y="{cy-4}" width="18" height="8" fill="{col}"/>')
        s.append(f'<line x1="{cx-14}" y1="{cy-4}" x2="{cx+14}" y2="{cy-4}" stroke="{col}" stroke-width="1.2"/>')
    elif kind == "demi-pause":
        s.append(f'<rect x="{cx-9}" y="{cy-8}" width="18" height="8" fill="{col}"/>')
        s.append(f'<line x1="{cx-14}" y1="{cy}" x2="{cx+14}" y2="{cy}" stroke="{col}" stroke-width="1.2"/>')
    elif kind == "soupir":     # le « Z » du soupir
        s.append(f'<path d="M {cx-6} {cy-16} C {cx+4} {cy-10}, {cx-6} {cy-4}, {cx+3} {cy+1} '
                 f'C {cx-6} {cy+4}, {cx+2} {cy+10}, {cx+7} {cy+16}" fill="none" stroke="{col}" '
                 f'stroke-width="2.6" stroke-linecap="round"/>')
    elif kind in ("demi-soupir", "quart-soupir"):
        n = 1 if kind == "demi-soupir" else 2
        s.append(f'<line x1="{cx+5}" y1="{cy-15}" x2="{cx-2}" y2="{cy+16}" stroke="{col}" stroke-width="2"/>')
        for k in range(n):
            yy = cy - 12 + k * 11
            s.append(f'<circle cx="{cx-3}" cy="{yy}" r="3.2" fill="{col}"/>')
            s.append(f'<path d="M {cx-3} {yy} C {cx+4} {yy-2}, {cx+7} {yy+3}, {cx+4} {yy+6}" '
                     f'fill="none" stroke="{col}" stroke-width="2"/>')
    return "".join(s)


# =====================================================================
#  ARBRE DES VALEURS RYTHMIQUES
# =====================================================================
def build_note_values():
    W, H = 660, 400
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">LES VALEURS DE NOTES</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">à chaque étage, on coupe la durée en deux — exemple en mesure à 4/4</text>')

    rows = [
        ("ronde",   1, "Ronde",        "4 temps",  INK),
        ("blanche", 2, "Blanche",      "2 temps",  TEAL),
        ("noire",   4, "Noire",        "1 temps",  RUST),
        ("croche",  8, "Croche",       "½ temps",  GOLD),
        ("double", 16, "Double-croche", "¼ temps", PLUM),
    ]
    x0, x1 = 176.0, 630.0
    for k, (kind, n, name, dur, col) in enumerate(rows):
        y = 74 + k * 52
        p.append(f'<text x="14" y="{y+4}" font-size="11.5" font-weight="700" fill="{col}">{name}</text>')
        p.append(f'<text x="14" y="{y+18}" font-size="9.3" fill="{MUTE}">{dur}</text>')
        p.append(f'<text x="118" y="{y+4}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTE}">×{n}</text>')
        seg = (x1 - x0) / n
        for i in range(n):
            xa = x0 + seg * i
            p.append(f'<rect x="{xa+1.5:.1f}" y="{y-13}" width="{seg-3:.1f}" height="28" rx="4" '
                     f'fill="{col}" opacity="{0.16 if k else 0.22}"/>')
            p.append(f'<rect x="{xa+1.5:.1f}" y="{y-13}" width="{seg-3:.1f}" height="28" rx="4" '
                     f'fill="none" stroke="{col}" stroke-width="1"/>')
            sc = 0.62 if n <= 8 else 0.45
            p.append(note_glyph(xa + seg / 2 - 2.5 * sc, y + 4, kind, col, scale=sc))

    # règle des temps
    yb = 74 + 5 * 52 - 12
    p.append(f'<line x1="{x0}" y1="{yb+6}" x2="{x1}" y2="{yb+6}" stroke="{LINE}"/>')
    for i in range(4):
        xa = x0 + (x1 - x0) / 4 * (i + .5)
        p.append(f'<text x="{xa:.1f}" y="{yb+22}" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="11" font-weight="700" fill="{SOFT}">{i+1}</text>')
    p.append(f'<text x="14" y="{yb+22}" font-size="10" fill="{MUTE}">les 4 temps</text>')

    p.append(f'<rect x="14" y="{yb+34}" width="{W-28}" height="30" rx="6" fill="{SAND}" stroke="{LINE}"/>')
    p.append(f'<text x="26" y="{yb+53}" font-size="10" fill="{SOFT}">'
             f'<tspan font-weight="700" fill="{RUSTD}">Le point</tspan> placé après une note ajoute la moitié de sa durée&#160;: '
             f'une blanche pointée = 3 temps, une noire pointée = 1 temps et demi.</text>')
    p.append("</svg>")
    write("valeurs-rythmiques.svg", "".join(p))


# =====================================================================
#  SILENCES
# =====================================================================
def build_rests():
    W, H = 640, 150
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">LES SILENCES</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">à chaque note correspond un silence de même durée — le silence fait partie de la musique</text>')

    items = [("pause", "Pause", "4 temps", "ronde"),
             ("demi-pause", "Demi-pause", "2 temps", "blanche"),
             ("soupir", "Soupir", "1 temps", "noire"),
             ("demi-soupir", "Demi-soupir", "½ temps", "croche"),
             ("quart-soupir", "Quart de soupir", "¼ temps", "double-croche")]
    for k, (kind, name, dur, eq) in enumerate(items):
        cx = 76 + k * 124
        p.append(f'<rect x="{cx-52}" y="58" width="104" height="76" rx="8" fill="#fff" stroke="{LINE}"/>')
        p.append(f'<line x1="{cx-34}" y1="84" x2="{cx+34}" y2="84" stroke="{LINE}" stroke-width="1"/>')
        p.append(rest_glyph(cx, 84, kind, INK))
        p.append(f'<text x="{cx}" y="{116}" text-anchor="middle" font-size="10.3" font-weight="700" fill="{INK}">{name}</text>')
        p.append(f'<text x="{cx}" y="{128}" text-anchor="middle" font-size="9" fill="{MUTE}">{dur} · {eq}</text>')
    p.append("</svg>")
    write("silences.svg", "".join(p))


# =====================================================================
#  GRILLE RYTHMIQUE GÉNÉRIQUE
# =====================================================================
def rhythm_grid(p, ox, oy, cells, w=26.0, h=26.0, beats=4, sub=4,
                label=None, col=RUST, counts=True, accents=None):
    """cells : chaîne de longueur beats*sub, 'X' frappe, '.' rien, 'o' fantôme."""
    n = len(cells)
    for i in range(n):
        xa = ox + w * i
        strong = (i % sub == 0)
        p.append(f'<rect x="{xa:.1f}" y="{oy:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'fill="{"#FFFFFF" if not strong else "#F7F1E6"}" stroke="{LINE}" stroke-width="1"/>')
    for b in range(beats + 1):
        xa = ox + w * sub * b
        p.append(f'<line x1="{xa:.1f}" y1="{oy-3:.1f}" x2="{xa:.1f}" y2="{oy+h+3:.1f}" '
                 f'stroke="{SOFT}" stroke-width="1.7"/>')
    for i, c in enumerate(cells):
        xa = ox + w * i + w / 2
        if c == "X":
            p.append(f'<circle cx="{xa:.1f}" cy="{oy+h/2:.1f}" r="{min(w,h)*0.32:.1f}" fill="{col}"/>')
        elif c == "o":
            p.append(f'<circle cx="{xa:.1f}" cy="{oy+h/2:.1f}" r="{min(w,h)*0.28:.1f}" fill="none" '
                     f'stroke="{col}" stroke-width="1.6" stroke-dasharray="2 2"/>')
    if counts:
        AMP = "&amp;"
        names = ["1", "e", AMP, "a"] if sub == 4 else (["1", AMP] if sub == 2 else ["1", AMP, "a"])
        for i in range(n):
            xa = ox + w * i + w / 2
            lbl = names[i % sub]
            if i % sub == 0:
                lbl = str(i // sub + 1)
            p.append(f'<text x="{xa:.1f}" y="{oy+h+15:.1f}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="9" font-weight="{"700" if i%sub==0 else "400"}" '
                     f'fill="{SOFT if i%sub==0 else MUTE}">{lbl}</text>')
    if label:
        p.append(f'<text x="{ox-12:.1f}" y="{oy+h/2+4:.1f}" text-anchor="end" font-size="10.5" '
                 f'font-weight="700" fill="{INK}">{label}</text>')


# =====================================================================
#  LA CLAVE
# =====================================================================
def build_clave():
    W, H = 700, 330
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">LA CLAVE&#160;: LA CLÉ DE TOUTE LA MUSIQUE CUBAINE</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">5 frappes réparties sur 2 mesures — une cellule «&#160;3&#160;» et une cellule «&#160;2&#160;»</text>')

    ox = 128.0
    w = 33.0
    # Clave son 3-2 : mesure 1 : 1, &de2(pos 6), 4(pos 12) ; mesure 2 : 2(pos 4), 3(pos 8)
    m1_32 = "X..." "..X." "...." "X..."
    m2_32 = "...." "X..." "X..." "...."
    rhythm_grid(p, ox, 74, m1_32, w=w, label="Mesure 1", col=RUST)
    rhythm_grid(p, ox, 74, "", w=w)
    rhythm_grid(p, ox, 140, m2_32, w=w, label="Mesure 2", col=TEAL)

    p.append(f'<text x="{ox+w*8:.1f}" y="66" text-anchor="middle" font-size="11" font-weight="700" fill="{RUST}">côté «&#160;3&#160;» — trois frappes</text>')
    p.append(f'<text x="{ox+w*8:.1f}" y="134" text-anchor="middle" font-size="11" font-weight="700" fill="{TEAL}">côté «&#160;2&#160;» — deux frappes</text>')

    p.append(f'<rect x="14" y="196" width="{W-28}" height="52" rx="7" fill="{SAND}" stroke="{LINE}"/>')
    p.append(f'<text x="28" y="216" font-size="10.5" fill="{SOFT}">'
             f'Lue dans l\'autre sens (mesure 2 d\'abord), la même cellule devient la '
             f'<tspan font-weight="700" fill="{RUSTD}">clave 2-3</tspan>.</text>')
    p.append(f'<text x="28" y="234" font-size="10.5" fill="{SOFT}">'
             f'Compte à voix haute&#160;: «&#160;<tspan font-family="{MONO}" font-weight="700" fill="{RUSTD}">'
             f'UN … et-DEUX … QUATRE | … DEUX … TROIS …</tspan>&#160;»</text>')

    # grille visuelle "où tombent les frappes"
    p.append(f'<text x="14" y="278" font-size="10.5" font-weight="700" fill="{RUSTD}">Repère visuel&#160;:</text>')
    p.append(f'<text x="112" y="278" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}">'
             f'X . . . | . . X . | . . . . | X . . .</text>')
    p.append(f'<text x="112" y="298" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}">'
             f'. . . . | X . . . | X . . . | . . . .</text>')
    p.append(f'<text x="470" y="278" font-size="9.5" fill="{MUTE}">← mesure 1 (3 frappes)</text>')
    p.append(f'<text x="470" y="298" font-size="9.5" fill="{MUTE}">← mesure 2 (2 frappes)</text>')
    p.append("</svg>")
    write("clave-32.svg", "".join(p))


# =====================================================================
#  TRESILLO & CINQUILLO
# =====================================================================
def build_tresillo():
    W, H = 660, 290
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">TRESILLO ET CINQUILLO</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">les deux cellules qui donnent son balancement à la musique cubaine</text>')

    ox, w = 150.0, 30.0
    # tresillo 3+3+2 sur 8 doubles-croches
    rhythm_grid(p, ox, 70, "X..X" "..X.", w=w, beats=2, sub=4, label="Tresillo", col=RUST)
    p.append(f'<text x="{ox+w*8+16:.1f}" y="88" font-size="10" fill="{MUTE}">3 + 3 + 2</text>')

    # cinquillo
    rhythm_grid(p, ox, 136, "X.XX" ".XX.", w=w, beats=2, sub=4, label="Cinquillo", col=TEAL)
    p.append(f'<text x="{ox+w*8+16:.1f}" y="154" font-size="10" fill="{MUTE}">5 frappes</text>')

    p.append(f'<rect x="14" y="196" width="{W-28}" height="80" rx="7" fill="#FBF1DA" stroke="#E7D3A6"/>')
    p.append(f'<text x="28" y="216" font-size="10.5" font-weight="700" fill="#8A5F10">Tu connais déjà le tresillo sans le savoir</text>')
    p.append(f'<text x="28" y="234" font-size="10" fill="{SOFT}">'
             f'C\'est le rythme de la <tspan font-style="italic">habanera</tspan>, celui de «&#160;Hound Dog&#160;», du '
             f'<tspan font-style="italic">Bo Diddley beat</tspan>,</text>')
    p.append(f'<text x="28" y="250" font-size="10" fill="{SOFT}">'
             f'de presque tout le reggaeton, et de la Habanera de <tspan font-style="italic">Carmen</tspan> de Bizet.</text>')
    p.append(f'<text x="28" y="268" font-size="10" fill="{SOFT}">'
             f'Frappe-le sur une table&#160;: <tspan font-family="{MONO}" font-weight="700" fill="{RUSTD}">'
             f'>PAM . . PAM . . PAM .</tspan> — ça y est, tu as le groove.</text>')
    p.append("</svg>")
    write("tresillo-cinquillo.svg", "".join(p))


# =====================================================================
#  ANATOMIE D'UNE MESURE
# =====================================================================
def build_measure():
    W, H = 640, 220
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">ANATOMIE D\'UNE MESURE À 4/4</text>')

    top, gap = 62, 11
    for i in range(5):
        p.append(f'<line x1="70" y1="{top+i*gap}" x2="{W-40}" y2="{top+i*gap}" stroke="{SOFT}" stroke-width="1.1"/>')
    p.append(f'<text x="34" y="{top+46}" font-family="{SERIF}" font-size="62" fill="{INK}">&#119070;</text>')
    p.append(f'<text x="106" y="{top+19}" font-family="{SERIF}" font-size="25" font-weight="700" fill="{RUST}">4</text>')
    p.append(f'<text x="106" y="{top+43}" font-family="{SERIF}" font-size="25" font-weight="700" fill="{RUST}">4</text>')

    # barres de mesure
    for bx in (140, 340, 540):
        p.append(f'<line x1="{bx}" y1="{top}" x2="{bx}" y2="{top+4*gap}" stroke="{INK}" stroke-width="2"/>')
    p.append(f'<line x1="{W-42}" y1="{top}" x2="{W-42}" y2="{top+4*gap}" stroke="{INK}" stroke-width="2"/>')
    p.append(f'<line x1="{W-47}" y1="{top}" x2="{W-47}" y2="{top+4*gap}" stroke="{INK}" stroke-width="5"/>')

    # 4 noires par mesure
    for m, bx in enumerate((140, 340)):
        for i in range(4):
            cx = bx + 28 + i * 43
            p.append(note_glyph(cx, top + 2.5 * gap, "noire", INK, scale=0.82))
            p.append(f'<text x="{cx}" y="{top+4*gap+26}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="10" font-weight="700" fill="{MUTE}">{i+1}</text>')

    def ann(x1, y1, x2, y2, t, sub=None, anchor="middle"):
        s = (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{TEAL}" stroke-width="1" stroke-dasharray="2.5 2.5" fill="none"/>'
             f'<circle cx="{x1}" cy="{y1}" r="2.4" fill="{TEAL}"/>'
             f'<text x="{x2}" y="{y2}" text-anchor="{anchor}" font-size="10.3" font-weight="700" fill="{INK}">{t}</text>')
        if sub:
            s += f'<text x="{x2}" y="{y2+13}" text-anchor="{anchor}" font-size="9" fill="{MUTE}">{sub}</text>'
        return s

    p.append(ann(112, top + 30, 112, 148, "Chiffrage", "4 temps par mesure,", "middle"))
    p.append(f'<text x="112" y="174" text-anchor="middle" font-size="9" fill="{MUTE}">la noire vaut 1 temps</text>')
    p.append(ann(340, top - 4, 340, 40, "Barre de mesure", None, "middle"))
    p.append(ann(W - 46, top + 50, W - 90, 150, "Double barre", "c'est la fin", "middle"))
    p.append(ann(168, top + 34, 230, 176, "Une mesure = 4 noires", None, "middle"))
    p.append("</svg>")
    write("mesure-44.svg", "".join(p))


if __name__ == "__main__":
    print("Rythme :")
    build_note_values()
    build_rests()
    build_clave()
    build_tresillo()
    build_measure()
    print("OK")

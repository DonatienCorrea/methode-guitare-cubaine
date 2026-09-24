#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génération des diagrammes d'accords et des schémas de manche (SVG)."""
import os

OUT = os.path.join(os.path.dirname(__file__), "assets", "img")
os.makedirs(OUT, exist_ok=True)

INK   = "#1F1B18"
SOFT  = "#4E463E"
MUTE  = "#8B8075"
RUST  = "#B94F2C"
RUSTD = "#8E3A1E"
TEAL  = "#1C5057"
GOLD  = "#C68B21"
GREEN = "#3A6F52"
LINE  = "#D9CDB8"
SAND  = "#F5EDE0"
PAPER = "#FFFFFF"

SANS  = "Inter, 'DejaVu Sans', sans-serif"
SERIF = "'EB Garamond', Georgia, serif"
MONO  = "'JetBrains Mono', monospace"
MUSIC = "'Noto Music', serif"


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("  ·", name)


def svg_open(w, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{SANS}"{extra}>')


# =====================================================================
#  DIAGRAMME D'ACCORD
# =====================================================================
def chord_svg(name, frets, fingers, nfrets=4, base=1, barre=None,
              title=True, notes=None, scale=1.0, label_color=INK):
    """
    frets   : liste de 6 valeurs, corde 6 (mi grave) -> corde 1 (mi aigu).
              -1 = corde étouffée (X), 0 = corde à vide (O), n = case n.
    fingers : liste de 6 valeurs, 0 = rien, 1..4 = doigt.
    barre   : (doigt, case, corde_debut_index, corde_fin_index) indices 0..5
    """
    sx, sy = 22.0, 27.0           # espacement cordes / cases
    ml, mr = 20.0, 20.0
    mt = 46.0 if title else 26.0
    mb = 20.0
    W = ml + mr + sx * 5
    H = mt + mb + sy * nfrets

    x = lambda i: ml + sx * i            # i = 0 (corde 6) .. 5 (corde 1)
    y = lambda f: mt + sy * f            # f = 0 (sillet) .. nfrets

    p = [svg_open(f"{W:.0f}", f"{H:.0f}")]

    # titre
    if title:
        p.append(f'<text x="{W/2:.1f}" y="21" text-anchor="middle" font-family="{SERIF}" '
                 f'font-size="21" font-weight="700" fill="{label_color}">{name}</text>')

    # X et O au-dessus
    oy = mt - 11
    for i, fr in enumerate(frets):
        if fr == -1:
            p.append(f'<g stroke="{MUTE}" stroke-width="1.7" stroke-linecap="round">'
                     f'<line x1="{x(i)-4:.1f}" y1="{oy-4:.1f}" x2="{x(i)+4:.1f}" y2="{oy+4:.1f}"/>'
                     f'<line x1="{x(i)-4:.1f}" y1="{oy+4:.1f}" x2="{x(i)+4:.1f}" y2="{oy-4:.1f}"/></g>')
        elif fr == 0:
            p.append(f'<circle cx="{x(i):.1f}" cy="{oy:.1f}" r="4.3" fill="none" '
                     f'stroke="{TEAL}" stroke-width="1.7"/>')

    # sillet ou indication de case
    if base == 1:
        p.append(f'<rect x="{ml-1.5:.1f}" y="{mt-4.5:.1f}" width="{sx*5+3:.1f}" height="4.5" '
                 f'rx="1.4" fill="{INK}"/>')
    else:
        p.append(f'<text x="{ml-8:.1f}" y="{mt+sy*0.66:.1f}" text-anchor="end" '
                 f'font-family="{MONO}" font-size="11" font-weight="700" fill="{RUST}">{base}</text>')

    # cases horizontales
    for f in range(nfrets + 1):
        p.append(f'<line x1="{ml:.1f}" y1="{y(f):.1f}" x2="{ml+sx*5:.1f}" y2="{y(f):.1f}" '
                 f'stroke="#B9AB93" stroke-width="1.35"/>')
    # cordes verticales (plus épaisses vers les graves)
    for i in range(6):
        wdt = 1.9 - i * 0.17
        p.append(f'<line x1="{x(i):.1f}" y1="{mt:.1f}" x2="{x(i):.1f}" y2="{y(nfrets):.1f}" '
                 f'stroke="{SOFT}" stroke-width="{wdt:.2f}"/>')

    # barré
    if barre:
        bf, bc, i0, i1 = barre
        yy = y(bc - base + 1) - sy / 2
        p.append(f'<rect x="{x(i0)-8.5:.1f}" y="{yy-8.5:.1f}" width="{x(i1)-x(i0)+17:.1f}" '
                 f'height="17" rx="8.5" fill="{RUST}"/>')
        p.append(f'<text x="{(x(i0)+x(i1))/2:.1f}" y="{yy+4.4:.1f}" text-anchor="middle" '
                 f'font-size="10.5" font-weight="700" fill="#fff">{bf}</text>')

    # points
    for i, fr in enumerate(frets):
        if fr and fr > 0:
            rel = fr - base + 1
            if barre and fr == barre[1] and barre[2] <= i <= barre[3]:
                continue
            cy = y(rel) - sy / 2
            p.append(f'<circle cx="{x(i):.1f}" cy="{cy:.1f}" r="8.6" fill="{RUST}"/>')
            fg = fingers[i] if fingers else 0
            if fg:
                p.append(f'<text x="{x(i):.1f}" y="{cy+3.9:.1f}" text-anchor="middle" '
                         f'font-size="10.5" font-weight="700" fill="#fff">{fg}</text>')

    # noms de notes sous le diagramme
    if notes:
        for i, n in enumerate(notes):
            col = MUTE if frets[i] == -1 else RUSTD
            p.append(f'<text x="{x(i):.1f}" y="{y(nfrets)+14:.1f}" text-anchor="middle" '
                     f'font-family="{MONO}" font-size="9" font-weight="700" fill="{col}">{n}</text>')

    p.append("</svg>")
    return "".join(p)


CHORDS = {
    # nom            frets (6->1)          doigts               notes
    "Em":  ([0, 2, 2, 0, 0, 0], [0, 2, 3, 0, 0, 0], ["E", "B", "E", "G", "B", "E"]),
    "Am":  ([-1, 0, 2, 2, 1, 0], [0, 0, 2, 3, 1, 0], ["", "A", "E", "A", "C", "E"]),
    "C":   ([-1, 3, 2, 0, 1, 0], [0, 3, 2, 0, 1, 0], ["", "C", "E", "G", "C", "E"]),
    "G":   ([3, 2, 0, 0, 0, 3], [2, 1, 0, 0, 0, 3], ["G", "B", "D", "G", "B", "G"]),
    "G4":  ([3, 2, 0, 0, 3, 3], [2, 1, 0, 0, 3, 4], ["G", "B", "D", "G", "D", "G"]),
    "D":   ([-1, -1, 0, 2, 3, 2], [0, 0, 0, 1, 3, 2], ["", "", "D", "A", "D", "F#"]),
    "A":   ([-1, 0, 2, 2, 2, 0], [0, 0, 1, 2, 3, 0], ["", "A", "E", "A", "C#", "E"]),
    "E":   ([0, 2, 2, 1, 0, 0], [0, 2, 3, 1, 0, 0], ["E", "B", "E", "G#", "B", "E"]),
    "Dm":  ([-1, -1, 0, 2, 3, 1], [0, 0, 0, 2, 3, 1], ["", "", "D", "A", "D", "F"]),
    # accords bonus
    "E7":  ([0, 2, 0, 1, 0, 0], [0, 2, 0, 1, 0, 0], ["E", "B", "D", "G#", "B", "E"]),
    "A7":  ([-1, 0, 2, 0, 2, 0], [0, 0, 2, 0, 3, 0], ["", "A", "E", "G", "C#", "E"]),
    "D7":  ([-1, -1, 0, 2, 1, 2], [0, 0, 0, 2, 1, 3], ["", "", "D", "A", "C", "F#"]),
    "G7":  ([3, 2, 0, 0, 0, 1], [3, 2, 0, 0, 0, 1], ["G", "B", "D", "G", "B", "F"]),
    "B7":  ([-1, 2, 1, 2, 0, 2], [0, 2, 1, 3, 0, 4], ["", "B", "D#", "A", "B", "F#"]),
    "Am7": ([-1, 0, 2, 0, 1, 0], [0, 0, 2, 0, 1, 0], ["", "A", "E", "G", "C", "E"]),
    "Dm7": ([-1, -1, 0, 2, 1, 1], [0, 0, 0, 2, 1, 1], ["", "", "D", "A", "C", "F"]),
    "Em7": ([0, 2, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0], ["E", "B", "D", "G", "B", "E"]),
    "Cmaj7": ([-1, 3, 2, 0, 0, 0], [0, 3, 2, 0, 0, 0], ["", "C", "E", "G", "B", "E"]),
    "Fmaj7": ([-1, -1, 3, 2, 1, 0], [0, 0, 3, 2, 1, 0], ["", "", "F", "A", "C", "E"]),
}


def build_chords():
    for key, (fr, fg, nt) in CHORDS.items():
        label = {"G4": "G", "Em7": "Em7"}.get(key, key)
        write(f"acc-{key}.svg", chord_svg(label, fr, fg, notes=nt))
    # F avec petit barré
    write("acc-F.svg", chord_svg("F", [-1, -1, 3, 2, 1, 1], [0, 0, 3, 2, 1, 1],
                                 barre=(1, 1, 4, 5),
                                 notes=["", "", "F", "A", "C", "F"]))
    # Fa grand barré
    write("acc-Fbarre.svg", chord_svg("F", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1],
                                      barre=(1, 1, 0, 5),
                                      notes=["F", "C", "F", "A", "C", "F"]))


# =====================================================================
#  LÉGENDE : COMMENT LIRE UN DIAGRAMME
# =====================================================================
def build_legend():
    W, H = 700, 300
    sx, sy = 26.0, 32.0
    ml, mt = 258.0, 78.0
    x = lambda i: ml + sx * i
    y = lambda f: mt + sy * f
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

    # diagramme central (accord de Do)
    frets = [-1, 3, 2, 0, 1, 0]
    fing = [0, 3, 2, 0, 1, 0]
    oy = mt - 13
    for i, fr in enumerate(frets):
        if fr == -1:
            p.append(f'<g stroke="{MUTE}" stroke-width="2" stroke-linecap="round">'
                     f'<line x1="{x(i)-4.5}" y1="{oy-4.5}" x2="{x(i)+4.5}" y2="{oy+4.5}"/>'
                     f'<line x1="{x(i)-4.5}" y1="{oy+4.5}" x2="{x(i)+4.5}" y2="{oy-4.5}"/></g>')
        elif fr == 0:
            p.append(f'<circle cx="{x(i)}" cy="{oy}" r="5" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    p.append(f'<rect x="{ml-2}" y="{mt-5.5}" width="{sx*5+4}" height="5.5" rx="1.6" fill="{INK}"/>')
    for f in range(5):
        p.append(f'<line x1="{ml}" y1="{y(f)}" x2="{ml+sx*5}" y2="{y(f)}" stroke="{LINE}" stroke-width="1.4"/>')
    for i in range(6):
        p.append(f'<line x1="{x(i)}" y1="{mt}" x2="{x(i)}" y2="{y(4)}" stroke="{SOFT}" stroke-width="{2.0-i*0.18:.2f}"/>')
    for i, fr in enumerate(frets):
        if fr > 0:
            cy = y(fr) - sy / 2
            p.append(f'<circle cx="{x(i)}" cy="{cy}" r="10" fill="{RUST}"/>')
            p.append(f'<text x="{x(i)}" y="{cy+4.3}" text-anchor="middle" font-size="12" '
                     f'font-weight="700" fill="#fff">{fing[i]}</text>')
    # numéros de corde en bas
    for i in range(6):
        p.append(f'<text x="{x(i)}" y="{y(4)+15}" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="9.5" font-weight="700" fill="{MUTE}">{6-i}</text>')

    def leader(x1, y1, x2, y2, txt, anchor="start", tx=None, ty=None, col=TEAL):
        s = (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="1.1" '
             f'fill="none" stroke-dasharray="2.5 2.5"/>'
             f'<circle cx="{x1}" cy="{y1}" r="2.4" fill="{col}"/>')
        s += (f'<text x="{tx if tx is not None else x2}" y="{ty if ty is not None else y2}" '
              f'text-anchor="{anchor}" font-size="11.5" fill="{INK}">{txt}</text>')
        return s

    # annotations à gauche
    p.append(leader(x(0), oy, 218, 40, "", "end"))
    p.append(f'<text x="218" y="36" text-anchor="end" font-size="11.5" font-weight="700" fill="{INK}">✕ corde à ne pas jouer</text>')
    p.append(f'<text x="218" y="50" text-anchor="end" font-size="10" fill="{MUTE}">on l\'étouffe ou on l\'évite</text>')

    p.append(f'<path d="M{x(3)} {oy} L 496 40" stroke="{TEAL}" stroke-width="1.1" stroke-dasharray="2.5 2.5" fill="none"/>'
             f'<circle cx="{x(3)}" cy="{oy}" r="2.4" fill="{TEAL}"/>')
    p.append(f'<text x="500" y="36" font-size="11.5" font-weight="700" fill="{INK}">○ corde à vide</text>')
    p.append(f'<text x="500" y="50" font-size="10" fill="{MUTE}">jouée sans appuyer</text>')

    p.append(f'<path d="M{ml-4} {mt-3} L 218 96" stroke="{TEAL}" stroke-width="1.1" stroke-dasharray="2.5 2.5" fill="none"/>'
             f'<circle cx="{ml-4}" cy="{mt-3}" r="2.4" fill="{TEAL}"/>')
    p.append(f'<text x="218" y="94" text-anchor="end" font-size="11.5" font-weight="700" fill="{INK}">le sillet de tête</text>')
    p.append(f'<text x="218" y="108" text-anchor="end" font-size="10" fill="{MUTE}">barre épaisse = case 1 juste dessous</text>')

    p.append(f'<path d="M{x(1)+10} {y(3)-sy/2} L 496 152" stroke="{TEAL}" stroke-width="1.1" stroke-dasharray="2.5 2.5" fill="none"/>'
             f'<circle cx="{x(1)+10}" cy="{y(3)-sy/2}" r="2.4" fill="{TEAL}"/>')
    p.append(f'<text x="500" y="148" font-size="11.5" font-weight="700" fill="{INK}">● doigt à poser</text>')
    p.append(f'<text x="500" y="162" font-size="10" fill="{MUTE}">le chiffre = quel doigt</text>')

    p.append(f'<path d="M{ml-4} {y(2)} L 218 176" stroke="{TEAL}" stroke-width="1.1" stroke-dasharray="2.5 2.5" fill="none"/>'
             f'<circle cx="{ml-4}" cy="{y(2)}" r="2.4" fill="{TEAL}"/>')
    p.append(f'<text x="218" y="174" text-anchor="end" font-size="11.5" font-weight="700" fill="{INK}">les cases</text>')
    p.append(f'<text x="218" y="188" text-anchor="end" font-size="10" fill="{MUTE}">de haut en bas : 1, 2, 3, 4</text>')

    p.append(f'<path d="M{x(2)} {y(4)+8} L 496 232" stroke="{TEAL}" stroke-width="1.1" stroke-dasharray="2.5 2.5" fill="none"/>'
             f'<circle cx="{x(2)}" cy="{y(4)+8}" r="2.4" fill="{TEAL}"/>')
    p.append(f'<text x="500" y="228" font-size="11.5" font-weight="700" fill="{INK}">numéro de corde</text>')
    p.append(f'<text x="500" y="242" font-size="10" fill="{MUTE}">6 = mi grave · 1 = mi aigu</text>')

    # main gauche : numérotation des doigts
    p.append(f'<text x="30" y="232" font-size="11.5" font-weight="700" fill="{RUSTD}">Les doigts de la main gauche</text>')
    for k, (num, nm) in enumerate([("1", "index"), ("2", "majeur"), ("3", "annulaire"), ("4", "auriculaire")]):
        cx = 40 + k * 52
        p.append(f'<circle cx="{cx}" cy="{258}" r="12" fill="{RUST}"/>')
        p.append(f'<text x="{cx}" y="{262.5}" text-anchor="middle" font-size="12.5" font-weight="700" fill="#fff">{num}</text>')
        p.append(f'<text x="{cx}" y="{284}" text-anchor="middle" font-size="9" fill="{MUTE}">{nm}</text>')
    p.append(f'<text x="258" y="262" font-size="10.5" fill="{MUTE}">Le pouce (P) reste derrière le manche,</text>')
    p.append(f'<text x="258" y="276" font-size="10.5" fill="{MUTE}">il n\'apparaît jamais sur un diagramme.</text>')

    p.append("</svg>")
    write("diagramme-legende.svg", "".join(p))


# =====================================================================
#  CORDES À VIDE — DOUBLE NOTATION
# =====================================================================
def build_open_strings():
    W, H = 620, 292
    x0, x1 = 128, 560
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="11.5" font-weight="700" fill="{RUSTD}">LES SIX CORDES À VIDE</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">vue de la guitare posée à plat, la corde 6 est celle du haut quand on joue</text>')

    rows = [("6", "Mi grave", "E", "82,4 Hz", 3.4),
            ("5", "La",       "A", "110 Hz",  3.0),
            ("4", "Ré",       "D", "146,8 Hz", 2.6),
            ("3", "Sol",      "G", "196 Hz",  2.1),
            ("2", "Si",       "B", "246,9 Hz", 1.6),
            ("1", "Mi aigu",  "E", "329,6 Hz", 1.1)]
    for k, (num, fr, en, hz, thick) in enumerate(rows):
        y = 66 + k * 31
        p.append(f'<text x="14" y="{y+4}" font-family="{MONO}" font-size="12" font-weight="700" fill="{MUTE}">{num}</text>')
        p.append(f'<text x="34" y="{y+4}" font-family="{SERIF}" font-size="15" font-weight="600" fill="{INK}">{fr}</text>')
        p.append(f'<rect x="96" y="{y-9}" width="22" height="19" rx="4" fill="{RUST}"/>')
        p.append(f'<text x="107" y="{y+4.5}" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">{en}</text>')
        p.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{SOFT}" stroke-width="{thick}" stroke-linecap="round"/>')
        p.append(f'<text x="{x1+10}" y="{y+4}" font-family="{MONO}" font-size="9.5" fill="{MUTE}">{hz}</text>')

    p.append(f'<line x1="{x0-8}" y1="56" x2="{x0-8}" y2="{66+5*31+10}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    p.append(f'<text x="{x0-8}" y="{66+5*31+26}" text-anchor="middle" font-size="9.5" fill="{MUTE}">sillet</text>')
    p.append(f'<text x="14" y="278" font-size="10.5" fill="{SOFT}">Moyen mnémotechnique&#160;: '
             f'<tspan font-weight="700" fill="{RUSTD}">M</tspan>i '
             f'<tspan font-weight="700" fill="{RUSTD}">L</tspan>a '
             f'<tspan font-weight="700" fill="{RUSTD}">R</tspan>é '
             f'<tspan font-weight="700" fill="{RUSTD}">S</tspan>ol '
             f'<tspan font-weight="700" fill="{RUSTD}">S</tspan>i '
             f'<tspan font-weight="700" fill="{RUSTD}">M</tspan>i → '
             f'«&#160;<tspan font-style="italic">Mon Loup Regarde Sous Son Manteau</tspan>&#160;»</text>')
    p.append("</svg>")
    write("cordes-a-vide.svg", "".join(p))


# =====================================================================
#  MANCHE AVEC NOMS DE NOTES (5 premières cases)
# =====================================================================
def build_fretboard_notes():
    nf = 5
    sx, sy = 74.0, 30.0
    ml, mt = 116.0, 78.0
    W = ml + sx * nf + 60
    H = mt + sy * 6 + 56
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="11.5" font-weight="700" fill="{RUSTD}">LE MANCHE, CASE PAR CASE</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">une case = un demi-ton · notation anglo-saxonne (latine en dessous)</text>')

    # touche
    p.append(f'<rect x="{ml}" y="{mt}" width="{sx*nf}" height="{sy*5}" fill="#F6F0E5"/>')
    p.append(f'<rect x="{ml-7}" y="{mt-4}" width="7" height="{sy*5+8}" rx="2" fill="{INK}"/>')
    for f in range(nf + 1):
        xx = ml + sx * f
        p.append(f'<line x1="{xx}" y1="{mt}" x2="{xx}" y2="{mt+sy*5}" stroke="{MUTE}" stroke-width="2"/>')
        if f:
            p.append(f'<text x="{ml+sx*(f-0.5)}" y="{mt-22}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="11" font-weight="700" fill="{RUST}">case {f}</text>')
    p.append(f'<text x="70" y="{mt-22}" text-anchor="middle" font-family="{MONO}" '
             f'font-size="10" font-weight="700" fill="{TEAL}">à vide</text>')

    strings = [
        ("6", ["E", "F", "F♯", "G", "G♯", "A"], ["Mi", "Fa", "Fa♯", "Sol", "Sol♯", "La"]),
        ("5", ["A", "A♯", "B", "C", "C♯", "D"], ["La", "La♯", "Si", "Do", "Do♯", "Ré"]),
        ("4", ["D", "D♯", "E", "F", "F♯", "G"], ["Ré", "Ré♯", "Mi", "Fa", "Fa♯", "Sol"]),
        ("3", ["G", "G♯", "A", "A♯", "B", "C"], ["Sol", "Sol♯", "La", "La♯", "Si", "Do"]),
        ("2", ["B", "C", "C♯", "D", "D♯", "E"], ["Si", "Do", "Do♯", "Ré", "Ré♯", "Mi"]),
        ("1", ["E", "F", "F♯", "G", "G♯", "A"], ["Mi", "Fa", "Fa♯", "Sol", "Sol♯", "La"]),
    ]
    for k, (num, en, fr) in enumerate(strings):
        y = mt + sy * k
        p.append(f'<line x1="{ml-7}" y1="{y}" x2="{ml+sx*nf}" y2="{y}" stroke="{SOFT}" stroke-width="{2.4-k*0.25:.2f}"/>')
        p.append(f'<text x="20" y="{y+4}" font-family="{MONO}" font-size="10" '
                 f'font-weight="700" fill="{MUTE}">{num}</text>')
        # note à vide
        p.append(f'<rect x="53" y="{y-14}" width="34" height="26" fill="{PAPER}"/>')
        p.append(f'<text x="70" y="{y-2}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{TEAL}">{en[0]}</text>')
        p.append(f'<text x="70" y="{y+9}" text-anchor="middle" font-size="8.5" fill="{MUTE}">{fr[0]}</text>')
        for f in range(1, nf + 1):
            cx = ml + sx * (f - 0.5)
            alt = "♯" in en[f]
            col = MUTE if alt else INK
            p.append(f'<rect x="{cx-18}" y="{y-16}" width="36" height="26" fill="#F6F0E5"/>')
            p.append(f'<text x="{cx}" y="{y-6}" text-anchor="middle" font-size="12.5" '
                     f'font-weight="{"500" if alt else "700"}" fill="{col}">{en[f]}</text>')
            p.append(f'<text x="{cx}" y="{y+5}" text-anchor="middle" font-size="8.5" fill="{MUTE}">{fr[f]}</text>')

    yb = mt + sy * 5 + 28
    p.append(f'<text x="14" y="{yb}" font-size="10.5" fill="{SOFT}">'
             f'Repère&#160;: entre <tspan font-weight="700" fill="{RUSTD}">Mi–Fa</tspan> et '
             f'<tspan font-weight="700" fill="{RUSTD}">Si–Do</tspan>, il n\'y a qu\'un demi-ton&#160;:</text>')
    p.append(f'<text x="14" y="{yb+15}" font-size="10.5" fill="{SOFT}">'
             f'une seule case, et aucune note altérée entre les deux.</text>')
    p.append("</svg>")
    write("manche-notes.svg", "".join(p))


# =====================================================================
#  TONS ET DEMI-TONS / GAMME MAJEURE
# =====================================================================
def build_scale():
    W, H = 640, 250
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="11.5" font-weight="700" fill="{RUSTD}">LA GAMME MAJEURE&#160;: UNE RECETTE DE TONS ET DE DEMI-TONS</text>')

    notes = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si", "Do"]
    en = ["C", "D", "E", "F", "G", "A", "B", "C"]
    steps = ["1 ton", "1 ton", "½ ton", "1 ton", "1 ton", "1 ton", "½ ton"]
    x0, dx = 46, 76
    y = 92
    for i in range(8):
        cx = x0 + dx * i
        p.append(f'<circle cx="{cx}" cy="{y}" r="24" fill="{SAND}" stroke="{LINE}"/>')
        p.append(f'<text x="{cx}" y="{y-2}" text-anchor="middle" font-family="{SERIF}" font-size="17" '
                 f'font-weight="700" fill="{INK}">{notes[i]}</text>')
        p.append(f'<text x="{cx}" y="{y+13}" text-anchor="middle" font-family="{MONO}" font-size="10.5" '
                 f'font-weight="700" fill="{RUST}">{en[i]}</text>')
        p.append(f'<text x="{cx}" y="{y-36}" text-anchor="middle" font-family="{MONO}" font-size="10" '
                 f'font-weight="700" fill="{TEAL}">{["I","II","III","IV","V","VI","VII","I"][i]}</text>')
    for i in range(7):
        xa, xb = x0 + dx * i + 26, x0 + dx * (i + 1) - 26
        half = "½" in steps[i]
        col = RUST if half else MUTE
        p.append(f'<path d="M{xa} {y+34} Q {(xa+xb)/2} {y+52} {xb} {y+34}" fill="none" '
                 f'stroke="{col}" stroke-width="{2.2 if half else 1.3}"/>')
        p.append(f'<text x="{(xa+xb)/2}" y="{y+70}" text-anchor="middle" font-size="10.5" '
                 f'font-weight="{"700" if half else "500"}" fill="{col}">{steps[i]}</text>')

    p.append(f'<rect x="14" y="196" width="{W-28}" height="40" rx="7" fill="{SAND}" stroke="{LINE}"/>')
    p.append(f'<text x="30" y="214" font-size="11" font-weight="700" fill="{RUSTD}">La formule, valable pour TOUTES les gammes majeures&#160;:</text>')
    p.append(f'<text x="30" y="229" font-family="{MONO}" font-size="11.5" font-weight="700" fill="{TEAL}">'
             f'ton – ton – ½&#160;ton – ton – ton – ton – ½&#160;ton</text>')
    p.append("</svg>")
    write("gamme-majeure.svg", "".join(p))


# =====================================================================
#  PORTÉE VS TABLATURE
# =====================================================================
def build_staff_vs_tab():
    W, H = 620, 320
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

    # ---- portée
    p.append(f'<text x="14" y="20" font-size="11.5" font-weight="700" fill="{RUSTD}">LA PORTÉE (solfège)</text>')
    top, gap = 44, 11
    for i in range(5):
        p.append(f'<line x1="70" y1="{top+i*gap}" x2="{W-30}" y2="{top+i*gap}" stroke="{SOFT}" stroke-width="1.1"/>')
    # clé de sol dessinée
    p.append(f'<text x="34" y="{top+3*gap}" font-family="{MUSIC}" font-size="{4*gap}" fill="{INK}">&#119070;</text>')
    p.append(f'<text x="104" y="{top+2*gap-2}" text-anchor="middle" font-family="{SERIF}" font-size="24" font-weight="700" fill="{SOFT}">4</text>')
    p.append(f'<text x="104" y="{top+4*gap-1}" text-anchor="middle" font-family="{SERIF}" font-size="24" font-weight="700" fill="{SOFT}">4</text>')

    # notes de Do à Sol (do3 sous la portée)
    seq = [("Do", "C", 5.0), ("Ré", "D", 4.5), ("Mi", "E", 4.0), ("Fa", "F", 3.5),
           ("Sol", "G", 3.0), ("La", "A", 2.5), ("Si", "B", 2.0), ("Do", "C", 1.5)]
    x = 160
    for fr, en, pos in seq:
        cy = top + pos * gap
        if pos >= 5.0:
            p.append(f'<line x1="{x-11}" y1="{top+5*gap}" x2="{x+11}" y2="{top+5*gap}" stroke="{SOFT}" stroke-width="1.1"/>')
        p.append(f'<ellipse cx="{x}" cy="{cy}" rx="6.4" ry="4.8" fill="{INK}" transform="rotate(-18 {x} {cy})"/>')
        if pos > 2:
            p.append(f'<line x1="{x+6.2}" y1="{cy-1}" x2="{x+6.2}" y2="{cy-32}" stroke="{INK}" stroke-width="1.5"/>')
        else:
            p.append(f'<line x1="{x-6.2}" y1="{cy+1}" x2="{x-6.2}" y2="{cy+32}" stroke="{INK}" stroke-width="1.5"/>')
        p.append(f'<text x="{x}" y="{top+76}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{RUSTD}">{en}</text>')
        p.append(f'<text x="{x}" y="{top+89}" text-anchor="middle" font-size="9" fill="{MUTE}">{fr}</text>')
        x += 50

    p.append(f'<line x1="14" y1="152" x2="{W-14}" y2="152" stroke="{LINE}" stroke-dasharray="4 4"/>')

    # ---- tablature
    p.append(f'<text x="14" y="176" font-size="11.5" font-weight="700" fill="{RUSTD}">LA TABLATURE (les mêmes notes)</text>')
    top2, gap2 = 200, 15
    labels = ["e", "B", "G", "D", "A", "E"]
    for i in range(6):
        yy = top2 + i * gap2
        p.append(f'<line x1="70" y1="{yy}" x2="{W-30}" y2="{yy}" stroke="{LINE}" stroke-width="1.1"/>')
        p.append(f'<text x="62" y="{yy+4}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{MUTE}">{labels[i]}</text>')
    for li, ch in enumerate("TAB"):
        p.append(f'<text x="16" y="{top2+22+li*26}" font-family="{SERIF}" font-size="26" font-weight="700" fill="{SOFT}">{ch}</text>')
    # positions : do3=corde5 c3, ré=corde4 c0, mi=c2, fa=c3, sol=corde3 c0, la=c2, si=corde2 c0, do=c1
    tabseq = [(4, "3"), (3, "0"), (3, "2"), (3, "3"), (2, "0"), (2, "2"), (1, "0"), (1, "1")]
    x = 160
    for si, fret in tabseq:
        yy = top2 + si * gap2
        p.append(f'<rect x="{x-8}" y="{yy-7}" width="16" height="14" fill="{PAPER}"/>')
        p.append(f'<text x="{x}" y="{yy+4}" text-anchor="middle" font-family="{MONO}" font-size="11.5" '
                 f'font-weight="700" fill="{RUSTD}">{fret}</text>')
        x += 50
    p.append(f'<text x="14" y="{top2+6*gap2+18}" font-size="10.5" fill="{SOFT}">'
             f'Les 6 lignes = les 6 cordes (la corde 1, la plus aiguë, est en haut). '
             f'Le chiffre = la case à presser. <tspan font-weight="700" fill="{RUSTD}">0</tspan> = corde à vide.</text>')
    p.append("</svg>")
    write("portee-vs-tablature.svg", "".join(p))


if __name__ == "__main__":
    print("Diagrammes d'accords et de manche :")
    build_chords()
    build_legend()
    build_open_strings()
    build_fretboard_notes()
    build_scale()
    build_staff_vs_tab()
    print("OK")

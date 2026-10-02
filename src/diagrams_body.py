#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anatomie de la guitare, posture, mains, accordage (SVG)."""
import math
from diagrams_chords import (write, svg_open, INK, SOFT, MUTE, RUST, RUSTD,
                             TEAL, GOLD, GREEN, LINE, SAND, PAPER, SANS, SERIF, MONO)

WOOD_T = "#E8D3AE"   # table d'harmonie
WOOD_D = "#8A5A33"   # touche / chevalet
WOOD_M = "#B07C48"   # éclisses


def leader(x1, y1, x2, y2, txt, sub=None, anchor="start", col=TEAL, fs=11):
    dx = 6 if anchor == "start" else -6
    s = (f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="1" '
         f'fill="none" stroke-dasharray="2.5 2.5"/>'
         f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="2.6" fill="{col}"/>')
    s += (f'<text x="{x2+dx:.1f}" y="{y2+3.5:.1f}" text-anchor="{anchor}" font-size="{fs}" '
          f'font-weight="650" fill="{INK}">{txt}</text>')
    if sub:
        s += (f'<text x="{x2+dx:.1f}" y="{y2+16:.1f}" text-anchor="{anchor}" font-size="9.3" '
              f'fill="{MUTE}">{sub}</text>')
    return s


# =====================================================================
#  ANATOMIE DE LA GUITARE CLASSIQUE
# =====================================================================
def build_anatomy():
    W, H = 860, 440
    cy = 250.0
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">ANATOMIE DE LA GUITARE CLASSIQUE</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">les mots que tu retrouveras partout dans ce guide</text>')

    nut_x, joint_x, body_end = 178.0, 452.0, 812.0
    scale_len = 580.0

    # ---------- corps
    body = (f"M {joint_x} {cy-78} "
            f"C {joint_x+26} {cy-90}, {joint_x+52} {cy-108}, {joint_x+80} {cy-110} "
            f"C {joint_x+118} {cy-112}, {joint_x+148} {cy-98}, {joint_x+172} {cy-82} "
            f"C {joint_x+200} {cy-104}, {joint_x+222} {cy-132}, {joint_x+272} {cy-132} "
            f"C {joint_x+330} {cy-132}, {body_end} {cy-88}, {body_end} {cy} "
            f"C {body_end} {cy+88}, {joint_x+330} {cy+132}, {joint_x+272} {cy+132} "
            f"C {joint_x+222} {cy+132}, {joint_x+200} {cy+104}, {joint_x+172} {cy+82} "
            f"C {joint_x+148} {cy+98}, {joint_x+118} {cy+112}, {joint_x+80} {cy+110} "
            f"C {joint_x+52} {cy+108}, {joint_x+26} {cy+90}, {joint_x} {cy+78} Z")
    p.append(f'<path d="{body}" fill="{WOOD_T}" stroke="{WOOD_M}" stroke-width="3"/>')
    # filet intérieur
    p.append(f'<path d="{body}" fill="none" stroke="#D9BE93" stroke-width="1" transform="translate(0,0) scale(1)" opacity=".8"/>')

    # ---------- rosace
    rx, ry, rr = joint_x + 118, cy, 54
    p.append(f'<circle cx="{rx}" cy="{ry}" r="{rr+13}" fill="none" stroke="{WOOD_D}" stroke-width="3.2"/>')
    p.append(f'<circle cx="{rx}" cy="{ry}" r="{rr+8}" fill="none" stroke="#C99C63" stroke-width="5"/>')
    p.append(f'<circle cx="{rx}" cy="{ry}" r="{rr+2}" fill="none" stroke="{WOOD_D}" stroke-width="2"/>')
    p.append(f'<circle cx="{rx}" cy="{ry}" r="{rr}" fill="#3A2A1C"/>')
    # motif mosaïque
    for a in range(0, 360, 12):
        ang = math.radians(a)
        p.append(f'<circle cx="{rx+math.cos(ang)*(rr+8):.1f}" cy="{ry+math.sin(ang)*(rr+8):.1f}" '
                 f'r="2" fill="{WOOD_D}"/>')

    # ---------- chevalet
    bx = joint_x + 268
    p.append(f'<rect x="{bx}" y="{cy-34}" width="74" height="68" rx="5" fill="{WOOD_D}"/>')
    p.append(f'<rect x="{bx+24}" y="{cy-30}" width="9" height="60" rx="2" fill="#F3EEE2"/>')  # sillet de chevalet
    for k in range(6):
        yy = cy - 26 + k * 10.4
        p.append(f'<circle cx="{bx+55}" cy="{yy:.1f}" r="2.4" fill="#2E2116"/>')

    # ---------- manche + touche
    p.append(f'<rect x="{nut_x}" y="{cy-36}" width="{joint_x-nut_x+30}" height="72" fill="{WOOD_M}"/>')
    p.append(f'<rect x="{nut_x}" y="{cy-33}" width="{joint_x-nut_x+30}" height="66" fill="#4A3524"/>')
    # frettes
    for n in range(1, 13):
        fx = nut_x + scale_len * (1 - 2 ** (-n / 12.0))
        p.append(f'<line x1="{fx:.1f}" y1="{cy-33}" x2="{fx:.1f}" y2="{cy+33}" stroke="#D7D2C6" stroke-width="2"/>')
    # sillet de tête
    p.append(f'<rect x="{nut_x-6}" y="{cy-37}" width="7" height="74" rx="2" fill="#F3EEE2" stroke="{MUTE}" stroke-width=".8"/>')

    # ---------- tête
    hx0 = 44.0
    p.append(f'<path d="M {nut_x-6} {cy-37} L {hx0+16} {cy-46} '
             f'C {hx0} {cy-46}, {hx0} {cy-46}, {hx0} {cy-32} '
             f'L {hx0} {cy+32} C {hx0} {cy+46}, {hx0} {cy+46}, {hx0+16} {cy+46} '
             f'L {nut_x-6} {cy+37} Z" fill="{WOOD_M}" stroke="{WOOD_D}" stroke-width="2"/>')
    # fentes
    p.append(f'<rect x="{hx0+26}" y="{cy-32}" width="86" height="22" rx="8" fill="#5C3F27"/>')
    p.append(f'<rect x="{hx0+26}" y="{cy+10}" width="86" height="22" rx="8" fill="#5C3F27"/>')
    # mécaniques (axes + boutons)
    for k in range(3):
        xx = hx0 + 40 + k * 30
        p.append(f'<circle cx="{xx}" cy="{cy-21}" r="7" fill="#D8D2C6" stroke="{SOFT}" stroke-width="1"/>')
        p.append(f'<circle cx="{xx}" cy="{cy+21}" r="7" fill="#D8D2C6" stroke="{SOFT}" stroke-width="1"/>')
        p.append(f'<rect x="{xx-4}" y="{cy-56}" width="8" height="16" rx="3" fill="#3A2A1C"/>')
        p.append(f'<line x1="{xx}" y1="{cy-40}" x2="{xx}" y2="{cy-28}" stroke="{SOFT}" stroke-width="2"/>')
        p.append(f'<rect x="{xx-4}" y="{cy+40}" width="8" height="16" rx="3" fill="#3A2A1C"/>')
        p.append(f'<line x1="{xx}" y1="{cy+40}" x2="{xx}" y2="{cy+28}" stroke="{SOFT}" stroke-width="2"/>')

    # ---------- cordes
    for k in range(6):
        y_nut = cy - 26 + k * 10.4
        y_br = cy - 26 + k * 10.4
        thick = 2.3 - k * 0.26
        p.append(f'<line x1="{hx0+40}" y1="{cy-21 if k<3 else cy+21}" x2="{nut_x-4}" y2="{y_nut:.1f}" '
                 f'stroke="#C9BFAE" stroke-width="{thick:.2f}"/>')
        p.append(f'<line x1="{nut_x-4}" y1="{y_nut:.1f}" x2="{bx+28}" y2="{y_br:.1f}" '
                 f'stroke="#D6CCBA" stroke-width="{thick:.2f}"/>')

    # ---------- annotations
    p.append(leader(hx0 + 70, cy - 56, 112, 108, "Tête", "(la « pala »)", "middle"))
    p.append(leader(hx0 + 62, cy + 30, 84, 386, "Mécaniques", "on les tourne pour accorder", "start"))
    p.append(leader(nut_x - 3, cy - 37, 214, 82, "Sillet de tête", "case 0 : la corde à vide part d'ici", "start"))
    p.append(leader(nut_x + 116, cy - 33, 330, 132, "Frettes", "les barrettes de métal", "start"))
    p.append(leader(nut_x + 60, cy + 33, 238, 368, "Touche", "la surface où l'on appuie", "start"))
    p.append(leader(nut_x + 186, cy + 36, 402, 410, "Manche", None, "start"))
    p.append(leader(rx, ry - rr - 13, rx - 36, 106, "Rosace &amp; bouche", "l'ouverture qui projette le son", "start"))
    p.append(leader(joint_x + 306, cy - 126, 840, 64, "Table d'harmonie", "épicéa ou cèdre : le vrai haut-parleur", "end"))
    p.append(leader(body_end - 6, cy + 54, 828, 344, "Éclisses", "les côtés", "end"))
    p.append(leader(bx + 34, cy + 34, 622, 402, "Chevalet", "+ sillet de chevalet", "start"))
    p.append(leader(joint_x + 8, cy + 78, 470, 366, "Talon", "jonction manche / caisse", "start"))

    p.append("</svg>")
    write("anatomie-guitare.svg", "".join(p))


# =====================================================================
#  POSTURE CLASSIQUE
# =====================================================================
def build_posture():
    W, H = 690, 400
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">LA POSITION CLASSIQUE</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">guitare sur la cuisse gauche, repose-pied sous le pied gauche</text>')

    SKIN = "#E3CDB4"
    CLOTH = "#CFC3B2"

    # tabouret
    p.append(f'<rect x="112" y="292" width="176" height="13" rx="4" fill="{SAND}" stroke="{LINE}"/>')
    p.append(f'<line x1="128" y1="305" x2="122" y2="372" stroke="{MUTE}" stroke-width="3.4"/>')
    p.append(f'<line x1="272" y1="305" x2="278" y2="372" stroke="{MUTE}" stroke-width="3.4"/>')
    p.append(f'<line x1="70" y1="372" x2="400" y2="372" stroke="{SOFT}" stroke-width="2.5"/>')

    # repose-pied (sous le pied gauche = à droite de l'image)
    p.append(f'<path d="M 296 348 L 358 338 L 358 330 L 296 340 Z" fill="{WOOD_M}" stroke="{WOOD_D}"/>')
    p.append(f'<line x1="303" y1="346" x2="303" y2="372" stroke="{WOOD_D}" stroke-width="2.6"/>')
    p.append(f'<line x1="351" y1="337" x2="351" y2="372" stroke="{WOOD_D}" stroke-width="2.6"/>')

    # ---- silhouette vue de face
    # jambe droite du joueur (à gauche de l'image), pied au sol
    p.append(f'<path d="M 166 286 L 130 296 L 116 360 L 148 364 L 156 300 Z" fill="{CLOTH}"/>')
    p.append(f'<ellipse cx="130" cy="366" rx="23" ry="7" fill="{SOFT}"/>')
    # jambe gauche du joueur (à droite), relevée sur le repose-pied
    p.append(f'<path d="M 216 286 L 264 300 L 300 330 L 276 346 L 240 316 L 202 304 Z" fill="{CLOTH}"/>')
    p.append(f'<ellipse cx="314" cy="333" rx="24" ry="8" fill="{SOFT}" transform="rotate(-9 314 333)"/>')
    # torse
    p.append(f'<path d="M 172 150 C 160 168, 154 214, 158 254 L 160 296 L 240 296 '
             f'L 244 250 C 248 210, 240 168, 228 150 Z" fill="{CLOTH}"/>')
    # cou + tête
    p.append(f'<rect x="190" y="130" width="20" height="24" fill="{SKIN}"/>')
    p.append(f'<circle cx="200" cy="110" r="29" fill="{SKIN}"/>')
    p.append(f'<path d="M 171 102 C 173 76, 227 76, 229 102 C 225 90, 175 90, 171 102 Z" fill="#6B5B4B"/>')

    # ---- guitare : caisse à gauche, manche vers le haut à droite
    p.append('<g transform="translate(190,268) rotate(-31)">')
    p.append(f'<path d="M -104 0 C -104 -34, -84 -58, -56 -58 C -34 -58, -18 -44, -8 -28 '
             f'C 0 -40, 14 -50, 34 -50 C 62 -50, 80 -28, 80 0 '
             f'C 80 28, 62 50, 34 50 C 14 50, 0 40, -8 28 '
             f'C -18 44, -34 58, -56 58 C -84 58, -104 34, -104 0 Z" '
             f'fill="{WOOD_T}" stroke="{WOOD_M}" stroke-width="2.6"/>')
    p.append(f'<circle cx="-62" cy="0" r="19" fill="#3A2A1C"/>')
    p.append(f'<circle cx="-62" cy="0" r="23.5" fill="none" stroke="{WOOD_D}" stroke-width="2.6"/>')
    p.append(f'<rect x="36" y="-15" width="26" height="30" rx="3" fill="{WOOD_D}"/>')
    p.append(f'<rect x="76" y="-14" width="98" height="28" fill="#4A3524"/>')
    for n in (1, 2, 3, 4, 5, 6, 7):
        fx = 76 + 98 * (1 - 2 ** (-n / 7.5))
        p.append(f'<line x1="{fx:.1f}" y1="-14" x2="{fx:.1f}" y2="14" stroke="#D7D2C6" stroke-width="1.5"/>')
    p.append(f'<rect x="172" y="-16" width="5" height="32" fill="#F3EEE2"/>')
    p.append(f'<rect x="177" y="-18" width="40" height="36" rx="5" fill="{WOOD_M}" stroke="{WOOD_D}" stroke-width="1.6"/>')
    for k in range(3):
        p.append(f'<circle cx="{186+k*13}" cy="-11" r="3.4" fill="#D8D2C6"/>')
        p.append(f'<circle cx="{186+k*13}" cy="11" r="3.4" fill="#D8D2C6"/>')
    for k in range(6):
        yy = -10 + k * 4
        p.append(f'<line x1="36" y1="{yy}" x2="172" y2="{yy}" stroke="#CFC4B1" stroke-width="1"/>')
    p.append('</g>')

    # bras
    p.append(f'<path d="M 234 168 C 262 188, 270 216, 254 238" stroke="{CLOTH}" stroke-width="19" '
             f'fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M 168 170 C 152 200, 176 226, 216 214" stroke="{CLOTH}" stroke-width="18" '
             f'fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M 216 214 C 250 200, 274 184, 294 170" stroke="{CLOTH}" stroke-width="16" '
             f'fill="none" stroke-linecap="round"/>')
    p.append(f'<circle cx="304" cy="164" r="14" fill="{SKIN}" stroke="{MUTE}" stroke-width="1"/>')
    p.append(f'<circle cx="248" cy="246" r="14" fill="{SKIN}" stroke="{MUTE}" stroke-width="1"/>')

    # légende des 4 points de contact
    pts = [("1", 238, 198, "Poitrine / sternum"),
           ("2", 248, 300, "Cuisse gauche · elle porte la guitare"),
           ("3", 262, 240, "Avant-bras droit sur l'éclisse"),
           ("4", 143, 303, "Cuisse droite · appui latéral")]
    for num, cx, cyy, lab in pts:
        p.append(f'<circle cx="{cx}" cy="{cyy}" r="10" fill="{RUST}" stroke="#fff" stroke-width="1.6"/>')
        p.append(f'<text x="{cx}" y="{cyy+3.8}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">{num}</text>')

    lx, ly = 410, 92
    p.append(f'<text x="{lx}" y="{ly}" font-size="11" font-weight="700" fill="{RUSTD}">LES 4 POINTS DE CONTACT</text>')
    for i, (num, _, _, lab) in enumerate(pts):
        yy = ly + 24 + i * 24
        p.append(f'<circle cx="{lx+8}" cy="{yy-4}" r="8.5" fill="{RUST}"/>')
        p.append(f'<text x="{lx+8}" y="{yy-0.6}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">{num}</text>')
        p.append(f'<text x="{lx+24}" y="{yy}" font-size="10.5" fill="{INK}">{lab}</text>')

    p.append(f'<text x="{lx}" y="{ly+128}" font-size="11" font-weight="700" fill="{RUSTD}">À VÉRIFIER</text>')
    checks = ["Manche à ~ 45°, tête à hauteur d'épaule",
              "Dos droit mais pas raide, épaules basses",
              "Pied gauche sur le repose-pied (10–18 cm)",
              "Les deux mains sont libres : si tu lâches",
              "tout, la guitare ne bouge pas"]
    for i, c in enumerate(checks):
        p.append(f'<text x="{lx}" y="{ly+150+i*17}" font-size="10" fill="{SOFT}">{"· " if i<4 else "  "}{c}</text>')

    p.append(f'<text x="{lx}" y="{ly+256}" font-size="9.5" font-style="italic" fill="{MUTE}">Pas de repose-pied&#160;? Un gros livre ou</text>')
    p.append(f'<text x="{lx}" y="{ly+270}" font-size="9.5" font-style="italic" fill="{MUTE}">un coussin de guitare font l\'affaire.</text>')
    p.append("</svg>")
    write("posture.svg", "".join(p))


# =====================================================================
#  MAIN DROITE — P I M A
# =====================================================================
def build_right_hand():
    W, H = 620, 340
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">LA MAIN DROITE&#160;: P · I · M · A</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">chaque doigt a sa corde attitrée — c\'est la base de tout arpège</text>')

    # cordes
    x0, x1 = 300, 548
    ys = [70, 95, 120, 145, 170, 195]
    names = [("6", "Mi", "p"), ("5", "La", "p"), ("4", "Ré", "p"),
             ("3", "Sol", "i"), ("2", "Si", "m"), ("1", "Mi", "a")]
    for k, y in enumerate(ys):
        p.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{SOFT}" stroke-width="{2.6-k*0.3:.2f}"/>')
        num, nm, dg = names[k]
        p.append(f'<text x="{x1+8}" y="{y+4}" font-family="{MONO}" font-size="9.5" fill="{MUTE}">{num} · {nm}</text>')

    # paume stylisée
    p.append(f'<path d="M 96 250 C 72 214, 78 166, 112 146 C 150 124, 212 130, 240 152 '
             f'C 262 170, 262 214, 240 240 C 214 270, 130 282, 96 250 Z" '
             f'fill="#EDDFCE" stroke="#C9B49A" stroke-width="2"/>')

    fingers = [
        ("p", "pulgar",  "pouce",      "#B94F2C", (150, 158), (298, 95),  -1),
        ("i", "índice",  "index",      "#C68B21", (206, 152), (298, 145),  0),
        ("m", "medio",   "majeur",     "#1C5057", (224, 178), (298, 170),  0),
        ("a", "anular",  "annulaire",  "#3A6F52", (232, 208), (298, 195),  0),
    ]
    for letter, esp, fr, col, (fx, fy), (tx, ty), _ in fingers:
        p.append(f'<path d="M {fx} {fy} C {(fx+tx)/2} {fy-10}, {(fx+tx)/2} {ty+8}, {tx} {ty}" '
                 f'stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".92"/>')
        p.append(f'<circle cx="{tx}" cy="{ty}" r="8.5" fill="#fff" stroke="{col}" stroke-width="2.6"/>')
        p.append(f'<text x="{tx}" y="{ty+3.6}" text-anchor="middle" font-family="{SERIF}" font-size="11.5" '
                 f'font-weight="700" fill="{col}">{letter}</text>')

    # tableau de légende
    ly = 250
    p.append(f'<line x1="14" y1="{ly-14}" x2="{W-14}" y2="{ly-14}" stroke="{LINE}"/>')
    cols = [("p", "pulgar", "pouce", "cordes 6·5·4 (basses)", "#B94F2C"),
            ("i", "índice", "index", "corde 3 (sol)", "#C68B21"),
            ("m", "medio", "majeur", "corde 2 (si)", "#1C5057"),
            ("a", "anular", "annulaire", "corde 1 (mi aigu)", "#3A6F52")]
    for k, (l, esp, fr, role, col) in enumerate(cols):
        xx = 22 + k * 150
        p.append(f'<circle cx="{xx+13}" cy="{ly+8}" r="13" fill="{col}"/>')
        p.append(f'<text x="{xx+13}" y="{ly+13}" text-anchor="middle" font-family="{SERIF}" font-size="15" '
                 f'font-weight="700" fill="#fff">{l}</text>')
        p.append(f'<text x="{xx+33}" y="{ly+4}" font-size="11" font-weight="700" fill="{INK}">{fr}</text>')
        p.append(f'<text x="{xx+33}" y="{ly+17}" font-size="9" font-style="italic" fill="{MUTE}">{esp}</text>')
        p.append(f'<text x="{xx}" y="{ly+40}" font-size="9.3" fill="{SOFT}">{role}</text>')

    p.append(f'<text x="14" y="{ly+66}" font-size="10" fill="{MUTE}">'
             f'Le petit doigt (<tspan font-style="italic">meñique</tspan>, noté <tspan font-weight="700">e</tspan> ou '
             f'<tspan font-weight="700">c</tspan>) ne sert quasiment jamais&#160;: il reste détendu.</text>')
    p.append(f'<text x="14" y="{ly+82}" font-size="10" fill="{MUTE}">'
             f'Le pouce passe <tspan font-weight="700" fill="{RUSTD}">devant</tspan> les autres doigts&#160;: '
             f'vu de dessus, p et i forment une croix.</text>')
    p.append("</svg>")
    write("main-droite-pima.svg", "".join(p))


# =====================================================================
#  APOYANDO / TIRANDO
# =====================================================================
def build_strokes():
    W, H = 560, 210
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

    def panel(ox, title, sub, col, path_d, arrow_d, note):
        s = [f'<rect x="{ox}" y="14" width="250" height="182" rx="8" fill="#fff" stroke="{LINE}"/>']
        s.append(f'<text x="{ox+16}" y="36" font-size="11.5" font-weight="700" fill="{col}">{title}</text>')
        s.append(f'<text x="{ox+16}" y="50" font-size="9.3" fill="{MUTE}">{sub}</text>')
        for k in range(4):
            yy = 76 + k * 17
            s.append(f'<line x1="{ox+22}" y1="{yy}" x2="{ox+228}" y2="{yy}" stroke="{SOFT}" '
                     f'stroke-width="{1.9-k*0.25:.2f}"/>')
        s.append(f'<path d="{path_d}" stroke="{col}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".9"/>')
        s.append(f'<path d="{arrow_d}" stroke="{RUSTD}" stroke-width="1.8" fill="none" marker-end="url(#ah)"/>')
        s.append(f'<text x="{ox+16}" y="176" font-size="9.5" fill="{SOFT}">{note}</text>')
        return "".join(s)

    p.append(f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
             f'<path d="M0,0 L6,3 L0,6 Z" fill="{RUSTD}"/></marker></defs>')

    p.append(panel(14, "TIRANDO — le jeu « libre »", "le doigt passe au-dessus des autres cordes", TEAL,
                   "M 120 140 C 140 120, 150 100, 152 78",
                   "M 152 90 C 160 78, 168 62, 166 46",
                   "→ arpèges, accords. Doigt vers la paume."))
    p.append(panel(296, "APOYANDO — le jeu « butté »", "le doigt s'appuie sur la corde voisine", RUST,
                   "M 402 140 C 422 122, 432 104, 434 82",
                   "M 434 78 L 434 100",
                   "→ mélodies, basses. Son plus rond."))
    p.append("</svg>")
    write("apoyando-tirando.svg", "".join(p))


# =====================================================================
#  ACCORDAGE RELATIF (méthode de la 5e case)
# =====================================================================
def build_relative_tuning():
    W, H = 640, 300
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="12" font-weight="700" fill="{RUSTD}">ACCORDAGE RELATIF&#160;: LA MÉTHODE DE LA 5<tspan font-size="8" dy="-4">e</tspan><tspan dy="4"> CASE</tspan></text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">on part d\'une corde juste (la 6) et on accorde de proche en proche</text>')

    ml, mt = 92.0, 66.0
    sx, sy = 84.0, 30.0
    nf = 6
    p.append(f'<rect x="{ml}" y="{mt}" width="{sx*nf}" height="{sy*5}" fill="#F6F0E5"/>')
    p.append(f'<rect x="{ml-7}" y="{mt-5}" width="7" height="{sy*5+10}" rx="2" fill="{INK}"/>')
    for f in range(nf + 1):
        xx = ml + sx * f
        p.append(f'<line x1="{xx}" y1="{mt}" x2="{xx}" y2="{mt+sy*5}" stroke="{MUTE}" stroke-width="2"/>')
        if f:
            p.append(f'<text x="{ml+sx*(f-.5)}" y="{mt-10}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="10" font-weight="700" fill="{MUTE}">{f}</text>')
    labels = ["6 · Mi", "5 · La", "4 · Ré", "3 · Sol", "2 · Si", "1 · Mi"]
    for k in range(6):
        yy = mt + sy * k
        p.append(f'<line x1="{ml-7}" y1="{yy}" x2="{ml+sx*nf}" y2="{yy}" stroke="{SOFT}" stroke-width="{2.5-k*0.26:.2f}"/>')
        p.append(f'<text x="{ml-34}" y="{yy+4}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTE}">{labels[k]}</text>')

    # paires : (corde pressée idx, case, corde à vide idx)
    pairs = [(0, 5, 1), (1, 5, 2), (2, 5, 3), (3, 4, 4), (4, 5, 5)]
    for k, (si, fr, sj) in enumerate(pairs):
        cx = ml + sx * (fr - .5)
        y1 = mt + sy * si
        y2 = mt + sy * sj
        col = RUST if fr == 4 else TEAL
        p.append(f'<circle cx="{cx}" cy="{y1}" r="10.5" fill="{col}"/>')
        p.append(f'<text x="{cx}" y="{y1+3.8}" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">{fr}</text>')
        p.append(f'<circle cx="{ml-17}" cy="{y2}" r="6.5" fill="none" stroke="{col}" stroke-width="2"/>')
        p.append(f'<path d="M {cx+13} {y1} C {cx+46} {y1}, {cx+46} {y2}, {cx+13} {y2}" '
                 f'stroke="{col}" stroke-width="1.6" fill="none" stroke-dasharray="3 3"/>')
        p.append(f'<text x="{cx+52}" y="{(y1+y2)/2+3.5}" font-size="9.5" fill="{col}" font-weight="600">=</text>')

    yb = mt + sy * 5 + 34
    p.append(f'<rect x="14" y="{yb}" width="{W-28}" height="52" rx="7" fill="#FBEDE6" stroke="#E6C6B6"/>')
    p.append(f'<text x="28" y="{yb+20}" font-size="11" font-weight="700" fill="{RUSTD}">L\'EXCEPTION À RETENIR</text>')
    p.append(f'<text x="28" y="{yb+37}" font-size="10.5" fill="{SOFT}">'
             f'Pour accorder la corde 2 (si), on presse la corde 3 à la '
             f'<tspan font-weight="700" fill="{RUSTD}">4<tspan font-size="7" dy="-3">e</tspan><tspan dy="3"> case</tspan></tspan>, '
             f'et non la 5<tspan font-size="7" dy="-3">e</tspan><tspan dy="3">. Partout ailleurs&#160;: 5</tspan><tspan font-size="7" dy="-3">e</tspan><tspan dy="3"> case.</tspan></text>')
    p.append("</svg>")
    write("accordage-relatif.svg", "".join(p))


# =====================================================================
#  SENS DE ROTATION DES MÉCANIQUES
# =====================================================================
def build_tuner_direction():
    W, H = 600, 190
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="11.5" font-weight="700" fill="{RUSTD}">TENDRE OU DÉTENDRE&#160;?</text>')

    p.append(f'<defs><marker id="a2" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">'
             f'<path d="M0,0 L7,3.2 L0,6.4 Z" fill="{TEAL}"/></marker>'
             f'<marker id="a3" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">'
             f'<path d="M0,0 L7,3.2 L0,6.4 Z" fill="{RUST}"/></marker></defs>')

    # axe + corde enroulée
    p.append(f'<rect x="60" y="58" width="130" height="26" rx="8" fill="#5C3F27"/>')
    p.append(f'<circle cx="125" cy="71" r="18" fill="#D8D2C6" stroke="{SOFT}" stroke-width="1.5"/>')
    for k in range(5):
        p.append(f'<line x1="{112+k*6}" y1="53" x2="{112+k*6}" y2="89" stroke="#9A8C78" stroke-width="2.6"/>')
    p.append(f'<path d="M 125 40 A 30 30 0 1 1 96 78" stroke="{TEAL}" stroke-width="2.4" fill="none" marker-end="url(#a2)"/>')
    p.append(f'<text x="125" y="122" text-anchor="middle" font-size="11" font-weight="700" fill="{TEAL}">Le son MONTE</text>')
    p.append(f'<text x="125" y="137" text-anchor="middle" font-size="9.5" fill="{MUTE}">la corde s\'enroule, elle se tend</text>')

    p.append(f'<line x1="285" y1="40" x2="285" y2="150" stroke="{LINE}"/>')

    p.append(f'<rect x="370" y="58" width="130" height="26" rx="8" fill="#5C3F27"/>')
    p.append(f'<circle cx="435" cy="71" r="18" fill="#D8D2C6" stroke="{SOFT}" stroke-width="1.5"/>')
    for k in range(5):
        p.append(f'<line x1="{422+k*6}" y1="53" x2="{422+k*6}" y2="89" stroke="#9A8C78" stroke-width="2.6"/>')
    p.append(f'<path d="M 435 40 A 30 30 0 1 0 464 78" stroke="{RUST}" stroke-width="2.4" fill="none" marker-end="url(#a3)"/>')
    p.append(f'<text x="435" y="122" text-anchor="middle" font-size="11" font-weight="700" fill="{RUST}">Le son DESCEND</text>')
    p.append(f'<text x="435" y="137" text-anchor="middle" font-size="9.5" fill="{MUTE}">la corde se déroule, elle se détend</text>')

    p.append(f'<rect x="14" y="152" width="{W-28}" height="28" rx="6" fill="{SAND}" stroke="{LINE}"/>')
    p.append(f'<text x="26" y="170" font-size="9.8" fill="{SOFT}">'
             f'<tspan font-weight="700" fill="{RUSTD}">Règle d\'or&#160;:</tspan> arriver à la note '
             f'<tspan font-style="italic">par en dessous</tspan>. Trop haut&#160;? Redescends dessous, puis remonte.</text>')
    p.append("</svg>")
    write("mecaniques-sens.svg", "".join(p))


# =====================================================================
#  DOIGTS PIVOTS (Em → Am)
# =====================================================================
def build_pivot():
    W, H = 560, 250
    sx, sy = 24.0, 29.0
    p = [svg_open(W, H)]
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    p.append(f'<text x="14" y="22" font-size="11.5" font-weight="700" fill="{RUSTD}">LE PRINCIPE DU DOIGT PIVOT</text>')
    p.append(f'<text x="14" y="38" font-size="10" fill="{MUTE}">exemple Em → Am&#160;: la forme glisse d\'une corde, on ne reconstruit rien</text>')

    def mini(ox, title, frets, fings, highlight):
        ml, mt = ox, 84.0
        x = lambda i: ml + sx * i
        y = lambda f: mt + sy * f
        s = [f'<text x="{ml+sx*2.5}" y="{mt-30}" text-anchor="middle" font-family="{SERIF}" '
             f'font-size="19" font-weight="700" fill="{INK}">{title}</text>']
        for i, fr in enumerate(frets):
            oy = mt - 12
            if fr == -1:
                s.append(f'<g stroke="{MUTE}" stroke-width="1.7" stroke-linecap="round">'
                         f'<line x1="{x(i)-4}" y1="{oy-4}" x2="{x(i)+4}" y2="{oy+4}"/>'
                         f'<line x1="{x(i)-4}" y1="{oy+4}" x2="{x(i)+4}" y2="{oy-4}"/></g>')
            elif fr == 0:
                s.append(f'<circle cx="{x(i)}" cy="{oy}" r="4.3" fill="none" stroke="{TEAL}" stroke-width="1.7"/>')
        s.append(f'<rect x="{ml-1.5}" y="{mt-4.5}" width="{sx*5+3}" height="4.5" rx="1.4" fill="{INK}"/>')
        for f in range(4):
            s.append(f'<line x1="{ml}" y1="{y(f)}" x2="{ml+sx*5}" y2="{y(f)}" stroke="#B9AB93" stroke-width="1.3"/>')
        for i in range(6):
            s.append(f'<line x1="{x(i)}" y1="{mt}" x2="{x(i)}" y2="{y(3)}" stroke="{SOFT}" stroke-width="{1.9-i*.17:.2f}"/>')
        for i, fr in enumerate(frets):
            if fr > 0:
                cyy = y(fr) - sy / 2
                col = GREEN if i in highlight else RUST
                s.append(f'<circle cx="{x(i)}" cy="{cyy}" r="9" fill="{col}"/>')
                s.append(f'<text x="{x(i)}" y="{cyy+3.9}" text-anchor="middle" font-size="10.5" '
                         f'font-weight="700" fill="#fff">{fings[i]}</text>')
        return "".join(s)

    p.append(mini(60, "Em", [0, 2, 2, 0, 0, 0], [0, 2, 3, 0, 0, 0], [1, 2]))
    p.append(mini(320, "Am", [-1, 0, 2, 2, 1, 0], [0, 0, 2, 3, 1, 0], [2, 3]))

    p.append(f'<path d="M 222 140 L 288 140" stroke="{GREEN}" stroke-width="2.4" fill="none" marker-end="url(#a4)"/>')
    p.append(f'<defs><marker id="a4" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">'
             f'<path d="M0,0 L7,3.2 L0,6.4 Z" fill="{GREEN}"/></marker></defs>')
    p.append(f'<text x="255" y="132" text-anchor="middle" font-size="9.5" font-weight="700" fill="{GREEN}">glisse</text>')
    p.append(f'<text x="255" y="156" text-anchor="middle" font-size="9" fill="{MUTE}">d\'une corde</text>')

    p.append(f'<rect x="14" y="196" width="{W-28}" height="42" rx="7" fill="{"#EAF3ED"}" stroke="#C6DCCF"/>')
    p.append(f'<text x="28" y="214" font-size="10.3" fill="{SOFT}">'
             f'<tspan font-weight="700" fill="{GREEN}">Les doigts 2 et 3</tspan> gardent le même écart&#160;: '
             f'ils descendent d\'une corde, même case.</text>')
    p.append(f'<text x="28" y="230" font-size="10.3" fill="{SOFT}">'
             f'Seul <tspan font-weight="700" fill="{RUST}">l\'index</tspan> vient s\'ajouter en case 1. '
             f'Un seul doigt à penser au lieu de trois&#160;!</text>')
    p.append("</svg>")
    write("doigts-pivots.svg", "".join(p))


if __name__ == "__main__":
    print("Anatomie / posture / mains :")
    build_anatomy()
    build_posture()
    build_right_hand()
    build_strokes()
    build_relative_tuning()
    build_tuner_direction()
    build_pivot()
    print("OK")

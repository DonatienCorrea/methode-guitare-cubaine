#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playlist d'écoute du guide + génération des QR codes.

Choix technique : les liens pointent vers une *recherche* YouTube plutôt que
vers un identifiant de vidéo précis. Un PDF imprimé vit plusieurs années ;
une vidéo peut être retirée, bloquée dans un pays ou remplacée, alors qu'une
recherche « titre + artiste » reste valide indéfiniment et fonctionne partout.
Chaque entrée indique aussi l'album, pour retrouver le morceau sur Spotify,
Deezer ou Apple Music.
"""
import os
import urllib.parse

import qrcode
import qrcode.image.svg

OUT = os.path.join(os.path.dirname(__file__), "assets", "qr")
os.makedirs(OUT, exist_ok=True)

# slug : (titre, interprète, année, album / contexte, requête de recherche)
TRACKS = {
    "chan-chan": (
        "Chan Chan", "Compay Segundo", "1997",
        "Buena Vista Social Club",
        "Chan Chan Compay Segundo Buena Vista Social Club"),
    "dos-gardenias": (
        "Dos gardenias", "Ibrahim Ferrer", "1997",
        "Buena Vista Social Club — le boléro type",
        "Dos Gardenias Ibrahim Ferrer Buena Vista"),
    "el-carretero": (
        "El carretero", "Guillermo Portabales", "1950s",
        "la guajira de référence",
        "El Carretero Guillermo Portabales"),
    "guantanamera": (
        "Guantanamera", "Joseíto Fernández", "1929",
        "la guajira la plus célèbre du monde",
        "Guantanamera Joseito Fernandez original"),
    "lagrimas-negras": (
        "Lágrimas negras", "Trío Matamoros", "1929",
        "bolero-son, le croisement des deux genres",
        "Lagrimas Negras Trio Matamoros 1929"),
    "como-fue": (
        "Cómo fue", "Beny Moré", "1958",
        "le boléro cubain dans sa version orchestrale",
        "Como Fue Beny More"),
    "sabor-a-mi": (
        "Sabor a mí", "Los Panchos", "1959",
        "trio de guitares, arpèges en requinto",
        "Sabor a mi Los Panchos"),
    "un-dia-de-noviembre": (
        "Un día de noviembre", "Leo Brouwer", "1972",
        "guitare classique cubaine, arpège pur",
        "Un dia de noviembre Leo Brouwer guitar"),
    "la-comparsa": (
        "La comparsa", "Ernesto Lecuona", "1912",
        "la conga de carnaval au piano",
        "La Comparsa Lecuona piano"),
    "bruca-manigua": (
        "Bruca Maniguá", "Arsenio Rodríguez", "1937",
        "le son montuno et son tresillo",
        "Bruca Manigua Arsenio Rodriguez"),
    "silencio": (
        "Silencio", "Ibrahim Ferrer & Omara Portuondo", "1997",
        "boléro chanté en duo",
        "Silencio Ibrahim Ferrer Omara Portuondo"),
    "habanera-carmen": (
        "Habanera (Carmen)", "Georges Bizet", "1875",
        "le tresillo cubain infiltré dans l'opéra français",
        "Bizet Carmen Habanera"),
    "recuerdos": (
        "Recuerdos de la Alhambra", "Francisco Tárrega", "1899",
        "le trémolo, sommet de la guitare romantique",
        "Recuerdos de la Alhambra Tarrega guitar"),
    "asturias": (
        "Asturias (Leyenda)", "Isaac Albéniz", "1892",
        "écrit pour piano, devenu un hymne de la guitare",
        "Asturias Leyenda Albeniz classical guitar"),
    "clave-son": (
        "La clave 3-2 expliquée", "leçon de percussion", "—",
        "entendre la cellule seule, en boucle",
        "son clave 3-2 pattern explained"),
    "afinar": (
        "La 6e corde — mi grave (82,4 Hz)", "note de référence", "—",
        "pour accorder à l'oreille sans accordeur",
        "low E string 82.41 Hz tuning note guitar"),
    "el-cuarto-de-tula": (
        "El cuarto de Tula", "Buena Vista Social Club", "1997",
        "son cubain, montuno endiablé",
        "El cuarto de Tula Buena Vista Social Club"),
    "veinte-anos": (
        "Veinte años", "María Teresa Vera", "1935",
        "trova cubaine, deux voix et deux guitares",
        "Veinte anos Maria Teresa Vera"),
}

BASE = "https://www.youtube.com/results?search_query="


def url_for(slug):
    return BASE + urllib.parse.quote_plus(TRACKS[slug][4])


def build():
    factory = qrcode.image.svg.SvgPathImage
    for slug in TRACKS:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(url_for(slug))
        qr.make(fit=True)
        img = qr.make_image(image_factory=factory)
        path = os.path.join(OUT, f"{slug}.svg")
        img.save(path)
        # la lib écrit un <svg> avec width/height en mm : on normalise
        with open(path, encoding="utf-8") as f:
            svg = f.read()
        import re
        svg = re.sub(r'width="[^"]+" height="[^"]+"', 'width="100%" height="100%"', svg, count=1)
        svg = svg.replace('<svg ', '<svg preserveAspectRatio="xMidYMid meet" ', 1)
        svg = svg.replace('fill="#000000"', 'fill="#1F1B18"')
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("  ·", f"{slug}.svg")


if __name__ == "__main__":
    print("QR codes d'écoute :")
    build()
    print(f"OK — {len(TRACKS)} codes")

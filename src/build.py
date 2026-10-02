#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur unique : les mêmes fragments HTML produisent
  · le site web multi-pages  -> ../site/
  · le PDF A4 paginé         -> ../Methode-guitare-couleurs-cubaines.pdf

Une modification dans src/sections/*.html se répercute sur les deux formats.
"""
import html as html_mod
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "docs")   # dossier publié par GitHub Pages
SECT = os.path.join(HERE, "sections")

sys.path.insert(0, HERE)
from manifest import SECTIONS, TITRE, SOUS_TITRE  # noqa: E402
import ecoutes  # noqa: E402

PDF_NAME = "Methode-guitare-couleurs-cubaines.pdf"
SITE_URL = "https://donatiencorrea.github.io/methode-guitare-cubaine/"


# ------------------------------------------------------------ encarts d'écoute
QR_BLOCK = re.compile(
    r'<div class="qr">\s*<img src="assets/qr/([a-z0-9-]+)\.svg"[^>]*>\s*'
    r'(?:<span>([^<]*)</span>)?\s*</div>', re.DOTALL)


def qr_alt(slug, web):
    """Alternative textuelle dérivée du titre du morceau, jamais un « QR code » nu."""
    track = ecoutes.TRACKS.get(slug)
    if not track:
        return "QR code"
    titre, interprete, annee = track[0], track[1], track[2]
    qui = "" if annee == "—" else f", {interprete}"
    texte = (f"Écouter {titre}{qui} sur YouTube" if web
             else f"QR code vers {titre}{qui}")
    return html_mod.escape(texte, quote=True)


def listening(frag, web):
    """Sur le site, le QR devient un lien : on ne scanne pas l'écran qu'on lit.
    Dans le PDF il reste une image, puisque c'est là qu'il sert vraiment."""
    def repl(m):
        slug = m.group(1)
        label = m.group(2) or "Écouter"
        img = f'<img src="assets/qr/{slug}.svg" alt="{qr_alt(slug, web)}">'
        if not web:
            return f'<div class="qr">{img}<span>{label}</span></div>'
        return (f'<a class="qr" href="{ecoutes.url_for(slug)}" target="_blank" '
                f'rel="noopener">{img}<span>{label}</span></a>')
    return QR_BLOCK.sub(repl, frag)


# ---------------------------------------------------------------- fragments
WIDGET = re.compile(r'<div class="widget" data-widget="([a-z0-9-]+)"></div>')

def widgets(frag, web):
    """Même principe que listening() : un marqueur, deux rendus.
    Sur le web il devient un composant interactif ; dans le PDF, un renvoi."""
    def repl(m):
        name = m.group(1)
        path = os.path.join(HERE, "widgets", name + ".html")
        if not os.path.exists(path):
            return ""
        if not web:
            return ('<p class="widget-print"><b>Sur le site</b>, cette grille est '
                    'jouable&nbsp;: la clave, le tresillo et le cinquillo s\'y écoutent '
                    'au tempo de ton choix, avec la pulsation en dessous. '
                    '<span class="u">' + SITE_URL.replace("https://", "") +
                    'rythme.html</span></p>')
        with open(path, encoding="utf-8") as f:
            return f.read()
    return WIDGET.sub(repl, frag)


FIG_IMG = re.compile(r'(<figure[^>]*>\s*)(<img [^>]*>)')

def scrollable_figures(frag):
    """Web uniquement : rend les figures défilables horizontalement.

    Une figure est une image : son texte est hors de portée du CSS. Réduite
    à la largeur d'un téléphone, une figure dessinée dans 660 unités voit ses
    étiquettes tomber sous 5 px. On préfère la montrer à sa taille réelle et
    la faire balayer du doigt, exactement comme une tablature trop large."""
    return FIG_IMG.sub(r'\1<div class="fig-scroll">\2</div>', frag)


def fragment(sec):
    path = os.path.join(SECT, f"{sec['n']:02d}-{sec['slug']}.html")
    if not os.path.exists(path):
        return f"<p><em>(section « {sec['title']} » à rédiger)</em></p>"
    with open(path, encoding="utf-8") as f:
        return f.read()


def head_block(sec):
    return (
        '<header class="sec-head">'
        f'<span class="sec-kicker">{sec["kicker"]} &middot; Section {sec["n"]}</span>'
        f'<h1>{sec["title"]}</h1>'
        f'<p class="sec-sub">{sec["sub"]}</p>'
        '</header><div class="sec-rule"></div>'
    )


def section_html(sec):
    return (f'<section class="section" id="s{sec["n"]}">'
            + head_block(sec) + widgets(listening(fragment(sec), web=False), web=False)
                + "</section>")


# ------------------------------------------------------------------ le PDF
def cover():
    return f"""
<div class="cover">
  <div class="cover-inner">
    <div class="cover-kicker">Guitare classique &middot; Méthode progressive</div>
    <h1>Couleurs<em>cubaines</em></h1>
    <div class="cover-rule"></div>
    <p class="cover-sub">Du premier enchaînement d'accords au premier arpège de
    guajira. Huit semaines, vingt minutes par jour, et une guitare à cordes nylon.</p>
    <div class="cover-spacer"></div>
    <div class="cover-facts">
      <div><b>8</b><span>semaines</span></div>
      <div><b>20</b><span>minutes / jour</span></div>
      <div><b>13</b><span>sections</span></div>
      <div><b>56</b><span>séances</span></div>
    </div>
    <div class="cover-foot">Méthode personnelle &middot; édition {__import__('datetime').date.today().year}</div>
  </div>
</div>"""


def toc():
    items = []
    for s in SECTIONS:
        items.append(
            f'<li><span class="n">{s["n"]:02d}</span>'
            f'<a href="#s{s["n"]}">{s["title"]}</a>'
            f'<span class="d">{s["desc"]}</span>'
            f'<a class="pg" href="#s{s["n"]}"></a></li>')
    return ('<div class="toc"><h1>Sommaire</h1>'
            '<p class="sec-sub">Treize étapes, dans l\'ordre où elles se jouent.</p>'
            '<ol class="toc-list">' + "".join(items) + "</ol></div>")


def build_pdf():
    from weasyprint import HTML
    body = cover() + toc() + "".join(section_html(s) for s in SECTIONS)
    doc = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<title>{TITRE} — {SOUS_TITRE}</title>
<link rel="stylesheet" href="css/print.css">
</head><body>{body}</body></html>"""
    os.makedirs(SITE, exist_ok=True)
    out = os.path.join(SITE, PDF_NAME)
    HTML(string=doc, base_url=HERE + "/").write_pdf(out)
    return out


# ----------------------------------------------------------------- le site
def nav(active_slug):
    li = []
    for s in SECTIONS:
        cls = ' class="active"' if s["slug"] == active_slug else ""
        li.append(f'<li><a href="{s["slug"]}.html"{cls}>'
                  f'<span class="n">{s["n"]:02d}</span>'
                  f'<span>{s["title"]}</span></a></li>')
    return "<ol>" + "".join(li) + "</ol>"


def page(active_slug, title, inner, crumb="", desc="", path="index.html", scripts=""):
    accueil = (path == "index.html")
    brut = f"{TITRE} — méthode de guitare classique cubaine" if accueil else f"{title} — {TITRE}"
    t = html_mod.escape(brut, quote=True)
    d = html_mod.escape(desc or SOUS_TITRE, quote=True)
    url = SITE_URL + ("" if accueil else path)
    ogtype = "website" if accueil else "article"
    return f"""<!DOCTYPE html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="author" content="Donatien Correa">
<meta name="theme-color" content="#16343A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{TITRE}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="css/web.css">
</head><body>
<a class="skip" href="#contenu">Aller au contenu</a>
<button class="burger" id="burger" aria-expanded="false" aria-controls="sommaire">
  <span aria-hidden="true">&#9776;</span> {TITRE} — sommaire</button>
<div class="layout">
  <aside class="side" id="sommaire">
    <a class="brand" href="index.html">
      <span class="bk">Méthode de guitare</span>
      <span class="bt">Couleurs <em>cubaines</em></span>
    </a>
    <nav aria-label="Sommaire des sections">{nav(active_slug)}</nav>
    <div class="side-foot">
      <a class="dl-pdf" href="{PDF_NAME}">&#8595;&nbsp; Version PDF imprimable</a>
      <p>Guitare classique, cordes nylon.<br>8 semaines &middot; 20 min/jour.</p>
    </div>
  </aside>
  <main class="main" id="contenu" tabindex="-1">
    <div class="progress"><i></i></div>
    <div class="wrap">{crumb}{inner}</div>
  </main>
</div>
<a class="totop" href="#" title="Haut de page" aria-label="Revenir en haut de page">&#8593;</a>
<script>
(function(){{
  var bar    = document.querySelector('.progress i');
  var top    = document.querySelector('.totop');
  var burger = document.getElementById('burger');
  var side   = document.getElementById('sommaire');

  function up(){{
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var r = max > 0 ? (h.scrollTop / max) : 0;
    if (bar) bar.style.width = (r*100).toFixed(1) + '%';
    if (top) top.classList.toggle('on', h.scrollTop > 400);
  }}
  document.addEventListener('scroll', up, {{passive:true}});
  up();

  function setMenu(open){{
    side.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }}
  burger.addEventListener('click', function(){{
    setMenu(!side.classList.contains('open'));
  }});
  // refermer après un choix : sinon le sommaire reste déployé sur mobile
  side.addEventListener('click', function(e){{
    if (e.target.closest('a')) setMenu(false);
  }});
  document.addEventListener('keydown', function(e){{
    if (e.key === 'Escape' && side.classList.contains('open')) {{
      setMenu(false); burger.focus();
    }}
  }});
}})();
</script>
{scripts}
</body></html>"""


def pager(i):
    prev = SECTIONS[i - 1] if i > 0 else None
    nxt = SECTIONS[i + 1] if i < len(SECTIONS) - 1 else None
    a = (f'<a class="prev" href="{prev["slug"]}.html"><span class="lbl">&#8592; Précédent</span>'
         f'<span class="ttl">{prev["title"]}</span></a>') if prev else \
        ('<a class="prev" href="index.html"><span class="lbl">&#8592; Retour</span>'
         '<span class="ttl">Accueil</span></a>')
    b = (f'<a class="next" href="{nxt["slug"]}.html"><span class="lbl">Suivant &#8594;</span>'
         f'<span class="ttl">{nxt["title"]}</span></a>') if nxt else \
        ('<a class="next" href="index.html"><span class="lbl">Fin &#8594;</span>'
         '<span class="ttl">Revenir au sommaire</span></a>')
    return f'<div class="pager">{a}{b}</div>'


def home():
    cards = "".join(
        f'<a class="home-card" href="{s["slug"]}.html">'
        f'<span class="n">SECTION {s["n"]:02d}</span>'
        f'<h3>{s["title"]}</h3><p>{s["desc"]}</p></a>' for s in SECTIONS)
    inner = f"""
<div class="hero"><div class="hero-in">
  <span class="k">Guitare classique &middot; méthode progressive</span>
  <h1>Couleurs<em>cubaines</em></h1>
  <p>Du premier enchaînement d'accords au premier arpège de guajira.
     Huit semaines, vingt minutes par jour, une guitare à cordes nylon.</p>
  <div class="hero-facts">
    <div><b>8</b><span>semaines</span></div>
    <div><b>20</b><span>min / jour</span></div>
    <div><b>13</b><span>sections</span></div>
    <div><b>56</b><span>séances</span></div>
  </div>
</div></div>
<h2>Par où commencer</h2>
<p>Lis la section&nbsp;1 en entier&nbsp;: elle tient en cinq minutes et elle change tout
le reste. Accorde ta guitare (section&nbsp;2). Puis ouvre la section&nbsp;9 et commence
la semaine&nbsp;1 le jour même — les sections&nbsp;3 à 8 sont des <em>références</em>
que le programme t'enverra consulter au bon moment.</p>
<div class="home-grid">{cards}</div>
<h2>Le guide en version imprimable</h2>
<p>Le PDF contient exactement le même contenu, paginé pour l'impression A4,
avec le carnet de suivi à remplir au crayon.</p>
<p><a class="dl-pdf" href="{PDF_NAME}">&#8595;&nbsp; Télécharger le PDF</a></p>
"""
    return page("", "Accueil", inner,
                desc=("Méthode de guitare classique pour débutant, orientée répertoire cubain : "
                      "8 semaines, 20 minutes par jour, guitare à cordes nylon. "
                      "Site et PDF imprimable, gratuits."),
                path="index.html")


def write_branding():
    """favicon + image Open Graph : fichiers statiques, pas de dépendance de build."""
    static = os.path.join(HERE, "static")
    if os.path.isdir(static):
        for name in sorted(os.listdir(static)):
            if name.endswith(".svg") and name.startswith("og-"):
                continue  # la source vectorielle de la carte OG reste dans src/
            shutil.copy2(os.path.join(static, name), os.path.join(SITE, name))


def page_scripts(inner):
    """Un script n'est chargé que sur la page qui en a besoin."""
    return ('<script src="js/metronome.js" defer></script>'
            if 'id="metro"' in inner else "")


def build_site():
    os.makedirs(SITE, exist_ok=True)
    shutil.copytree(os.path.join(HERE, "css"), os.path.join(SITE, "css"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(SITE, "assets"), dirs_exist_ok=True)
    if os.path.isdir(os.path.join(HERE, "js")):
        shutil.copytree(os.path.join(HERE, "js"), os.path.join(SITE, "js"), dirs_exist_ok=True)
    write_branding()

    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(home())

    for i, s in enumerate(SECTIONS):
        crumb = (f'<div class="crumb">{s["kicker"]} &nbsp;&middot;&nbsp; '
                 f'Section <b>{s["n"]:02d}</b> / {len(SECTIONS)}</div>')
        inner = (head_block(s)
                 + scrollable_figures(widgets(listening(fragment(s), web=True), web=True))
                 + pager(i))
        with open(os.path.join(SITE, f"{s['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(page(s["slug"], s["title"], inner, crumb,
                         desc=s["sub"], path=f'{s["slug"]}.html',
                         scripts=page_scripts(inner)))
    return SITE


# -------------------------------------------------------------------- main
if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "site"):
        print("Site  ->", build_site())
    if what in ("all", "pdf"):
        print("PDF   ->", build_pdf())
    print("OK")

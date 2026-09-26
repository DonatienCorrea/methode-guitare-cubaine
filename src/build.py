#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur unique : les mêmes fragments HTML produisent
  · le site web multi-pages  -> ../site/
  · le PDF A4 paginé         -> ../Methode-guitare-couleurs-cubaines.pdf

Une modification dans src/sections/*.html se répercute sur les deux formats.
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
SECT = os.path.join(HERE, "sections")

sys.path.insert(0, HERE)
from manifest import SECTIONS, TITRE, SOUS_TITRE  # noqa: E402
import ecoutes  # noqa: E402

PDF_NAME = "Methode-guitare-couleurs-cubaines.pdf"


# ---------------------------------------------------------------- fragments
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
            + head_block(sec) + fragment(sec) + "</section>")


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
    out = os.path.join(ROOT, PDF_NAME)
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


def page(active_slug, title, inner, crumb=""):
    return f"""<!DOCTYPE html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {TITRE}</title>
<link rel="stylesheet" href="css/web.css">
</head><body>
<button class="burger" onclick="document.querySelector('.side').classList.toggle('open')">
  <span>&#9776;</span> {TITRE} — sommaire</button>
<div class="layout">
  <aside class="side">
    <a class="brand" href="index.html">
      <span class="bk">Méthode de guitare</span>
      <span class="bt">Couleurs <em>cubaines</em></span>
    </a>
    <nav>{nav(active_slug)}</nav>
    <div class="side-foot">
      <a class="dl-pdf" href="{PDF_NAME}">&#8595;&nbsp; Version PDF imprimable</a>
      <p>Guitare classique, cordes nylon.<br>8 semaines &middot; 20 min/jour.</p>
    </div>
  </aside>
  <main class="main">
    <div class="progress"><i></i></div>
    <div class="wrap">{crumb}{inner}</div>
  </main>
</div>
<a class="totop" href="#" title="Haut de page">&#8593;</a>
<script>
(function(){{
  var bar = document.querySelector('.progress i');
  var top = document.querySelector('.totop');
  function up(){{
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var r = max > 0 ? (h.scrollTop / max) : 0;
    if (bar) bar.style.width = (r*100).toFixed(1) + '%';
    if (top) top.classList.toggle('on', h.scrollTop > 400);
  }}
  document.addEventListener('scroll', up, {{passive:true}});
  up();
}})();
</script>
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
    return page("", "Accueil", inner)


def build_site():
    os.makedirs(SITE, exist_ok=True)
    shutil.copytree(os.path.join(HERE, "css"), os.path.join(SITE, "css"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(SITE, "assets"), dirs_exist_ok=True)
    pdf_src = os.path.join(ROOT, PDF_NAME)
    if os.path.exists(pdf_src):
        shutil.copy2(pdf_src, os.path.join(SITE, PDF_NAME))

    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(home())

    for i, s in enumerate(SECTIONS):
        crumb = (f'<div class="crumb">{s["kicker"]} &nbsp;&middot;&nbsp; '
                 f'Section <b>{s["n"]:02d}</b> / {len(SECTIONS)}</div>')
        inner = head_block(s) + fragment(s) + pager(i)
        with open(os.path.join(SITE, f"{s['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(page(s["slug"], s["title"], inner, crumb))
    return SITE


# -------------------------------------------------------------------- main
if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "site"):
        print("Site  ->", build_site())
    if what in ("all", "pdf"):
        print("PDF   ->", build_pdf())
    print("OK")

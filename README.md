# Couleurs cubaines — méthode de guitare

Deux formats, une seule source.

- `Methode-guitare-couleurs-cubaines.pdf` — 86 pages, A4, prêt à imprimer (recto simple ou recto-verso).
- `site/index.html` — la même méthode en 13 pages web, avec sommaire latéral et navigation précédent/suivant. À ouvrir directement dans un navigateur, aucun serveur nécessaire.

## Modifier le contenu

Tout le texte vit dans `src/sections/NN-slug.html`. Chaque fichier ne contient que le corps
de la section : le titre, le sur-titre et le filet sont générés automatiquement à partir de
`src/manifest.py`, qui est la source unique du sommaire (ordre, numéros, titres, descriptions).

Les styles sont séparés en trois feuilles dans `src/css/` :

- `base.css` — tous les composants partagés (encarts, tableaux, diagrammes, tablatures) ;
- `print.css` — la mise en page A4, les en-têtes courants, les numéros de page, le sommaire ;
- `web.css` — la mise en page du site.

Une modification dans `sections/` ou dans `base.css` se propage donc aux deux formats.

## Reconstruire

```
cd src
python3 build.py          # PDF + site
python3 build.py pdf      # PDF seul
python3 build.py site     # site seul
```

Dépendances : `weasyprint` pour le PDF, rien d'autre pour le site.
Les diagrammes SVG (`src/assets/img/`) et les QR codes (`src/assets/qr/`) sont déjà générés ;
les scripts `diagrams_*.py` et `ecoutes.py` permettent de les régénérer si besoin.

## Les QR codes

Ils pointent vers des recherches YouTube, pas vers des identifiants de vidéo précis :
sur un document imprimé qui durera des années, une recherche résiste aux suppressions de
chaînes et aux blocages géographiques, contrairement à un lien direct.

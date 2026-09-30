# Couleurs cubaines — méthode de guitare classique

Une méthode de guitare classique pour débutant, orientée répertoire cubain :
huit semaines, vingt minutes par jour, cordes nylon.

- **Site** → <https://donatiencorrea.github.io/methode-guitare-cubaine/>
- **PDF imprimable** → [`docs/Methode-guitare-couleurs-cubaines.pdf`](docs/Methode-guitare-couleurs-cubaines.pdf) (86 pages, A4)

Les deux formats sortent de la **même source** : une modification dans
`src/sections/` se répercute sur le site et sur le PDF.

## Structure

```
src/                 la source, seul endroit à modifier
  sections/NN-slug.html  le texte de chaque section
  manifest.py            sommaire : ordre, numéros, titres, descriptions
  css/base.css           composants partagés site + PDF
  css/print.css          mise en page A4, en-têtes courants, pagination
  css/web.css            mise en page du site
  js/                    scripts de page (boîte à rythme de la section 7)
  widgets/               composants web injectés par build.py
  static/                favicon et carte Open Graph
  diagrams_*.py          génération des diagrammes SVG
  ecoutes.py             catalogue des morceaux et génération des QR codes
  build.py               le générateur
docs/                 GÉNÉRÉ — ne pas éditer à la main
```

`docs/` est publié tel quel par GitHub Pages (branche `main`, dossier `/docs`).
Il est versionné pour que le site reste servi sans étape de déploiement, mais il
est **entièrement reconstructible** : ne modifiez jamais un fichier de `docs/`,
il serait écrasé au prochain build.

## Reconstruire

```
pip install -r requirements.txt
python3 src/build.py          # site + PDF
python3 src/build.py site     # site seul
python3 src/build.py pdf      # PDF seul
```

Le rendu du PDF dépend des polices installées sur la machine : *EB Garamond*,
*Inter* et *JetBrains Mono*. À défaut, WeasyPrint retombe silencieusement sur
des substituts et la mise en page bouge.

C'est pour cette raison que la reconstruction de référence tourne en intégration
continue : le workflow [`.github/workflows/build.yml`](.github/workflows/build.yml)
installe les bonnes polices, relance `build.py` à chaque modification de `src/`
et recommite `docs/`. `docs/` ne peut donc pas diverger durablement des sources.

## Composants interactifs

Un marqueur `<div class="widget" data-widget="nom"></div>` posé dans un fragment
de section est développé par `build.py` en composant HTML sur le site, et
remplacé par un renvoi d'une ligne dans le PDF. Même mécanisme que les encarts
d'écoute : une seule source, deux rendus.

La boîte à rythme de la section 7 (`src/js/metronome.js`) synthétise ses sons —
aucun fichier audio dans le dépôt — et ordonnance les frappes sur l'horloge de
la Web Audio API plutôt qu'avec `setInterval`, qui dérive. Cette partie est
couverte par un banc d'essai :

```
node tests/metronome.test.js
```

## Les QR codes

Ils pointent vers des **recherches** YouTube, pas vers des identifiants de vidéo
précis : sur un document imprimé qui durera des années, une recherche résiste aux
suppressions de chaînes et aux blocages géographiques, contrairement à un lien
direct. Sur le site, où l'on ne scanne pas l'écran qu'on est en train de lire,
le même encart devient un lien cliquable.

## Licence

[CC BY-NC-SA 4.0](LICENSE) — partage et adaptation libres, usage non commercial,
partage à l'identique. Les morceaux cités et les enregistrements pointés par les
QR codes restent la propriété de leurs ayants droit.

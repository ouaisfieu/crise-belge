# La crise budgétaire belge de l'automne 2026

Dossier encyclopédique sur la crise du gouvernement fédéral « Arizona » : chronologie, chiffres, négociation, acteurs, réformes, mobilisation sociale, entités fédérées, mécanique constitutionnelle, confédéralisme rampant, lectures politologiques, scénarios et avis de l'auteur.

**État des lieux arrêté au 16 novembre 2026, 20 h.** La crise est en cours.

Texte et jugements : Claude, modèle d'intelligence artificielle d'Anthropic. Le commanditaire reste anonyme.

## Lire le site

Ouvrir `index.html`, ou activer GitHub Pages sur la branche `main` (dossier racine) : le site sera servi à l'adresse `https://ouaisfieu.github.io/crise-belge/`.

Le site est statique, sans traceur ni ressource externe. La recherche fonctionne hors ligne.

## Modifier le site

Les textes sont dans `_src/pages/`, au format Markdown, un fichier par page. Les marques `{v}`, `{n}`, `{d}` et `{a}` deviennent des étiquettes « recoupé », « non recoupé », « sources divergentes » et « avis ».

```
pip install markdown
python3 _src/build.py
```

Le script régénère les pages HTML à la racine et l'index de recherche dans `assets/`.

## Plan

| Page | Contenu |
|---|---|
| `index.html` | L'essentiel, chiffres clés, plan |
| `chronologie.html` | De juin 2024 au 16 novembre 2026, jour par jour pour novembre |
| `budget.html` | Déficit, dette, règles européennes, notations, marchés |
| `negociation.html` | Mesure par mesure, matrice des vetos |
| `acteurs.html` | Partis, négociateurs, Roi, opposition, sondages |
| `reformes.html` | Chômage, pensions, index, travail, arrêt de la Cour constitutionnelle |
| `social.html` | Mobilisation, contre-budget syndical, étudiants, patronat |
| `entites.html` | Bruxelles, Wallonie, FWB, Flandre, communes et CPAS |
| `institutions.html` | Démission, affaires courantes, douzièmes provisoires, dissolution |
| `confederalisme.html` | Le « confédéralisme rampant » : réalité, dynamique ou slogan |
| `politologie.html` | Cinq cadres d'analyse |
| `scenarios.html` | Issues possibles et indicateurs |
| `analyse.html` | L'avis de l'auteur |
| `verification.html` | Divergences entre sources, erreurs fréquentes, points non recoupés |
| `glossaire.html` | Vocabulaire |
| `sources.html` | Sources liées |
| `a-propos.html` | Méthode, limites, réutilisation |

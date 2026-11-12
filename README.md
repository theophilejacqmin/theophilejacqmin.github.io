# Les Garçons Glaciers — nouveau site

Site statique (HTML/CSS/JS, sans dépendance), construit d'après l'audit du 11/11/2026
et les skills d'Emil Kowalski (installées dans `.claude/skills/`).

## Voir le site en local
    python3 -m http.server 4321
puis ouvrir http://localhost:4321

## Modifier
Textes, parfums, produits et horaires sont dans `build.py`. Après modification :
    python3 build.py

## Avant la mise en ligne
- Chercher « À compléter » : allergènes, ingrédients, tarifs de livraison, hébergeur, CGV, nom de l'avis client.
- Confirmer horaires, téléphone et e-mail (questions de l'audit).
- Formulaires : ils ouvrent la messagerie (mailto). Pour un envoi direct, ajouter un `action` (Formspree, Netlify Forms…).
- Photos produits : visuels générés avec du texte déformé, recadrés au centre. À remplacer par de vraies photos.
- `_redirects` (Netlify/Cloudflare) et `.htaccess` (Apache/o2switch) redirigent les anciennes adresses Wix.

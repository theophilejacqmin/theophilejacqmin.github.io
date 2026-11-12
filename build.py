#!/usr/bin/env python3
"""Génère le site statique des Garçons Glaciers.

Lancer :  python3 build.py
Toutes les pages HTML sont réécrites à partir des données ci-dessous.
Les mentions [À compléter] signalent les infos introuvables pendant l'audit.
"""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
SITE = "https://www.lesgarconsglaciers.fr"
import time
VERSION = str(int(time.time()))  # casse le cache des CSS/JS à chaque build

PHONE = "+33 7 87 81 11 59"
PHONE_HREF = "tel:+33787811159"
EMAIL = "contact@lesgarconsglaciers.com"
ADDRESS = "4 Square La Fayette, 49000 Angers"
ROUTE = "https://www.google.com/maps/dir/?api=1&destination=" + "Place+La+Fayette+49000+Angers"

SOCIAL = {
    "Instagram": "https://www.instagram.com/les_garcons_glaciers/",
    "Facebook": "https://www.facebook.com/lesgarconsglaciers/",
    "YouTube": "https://www.youtube.com/@lesgarconsglaciers1618",
}

# ---------------------------------------------------------------------------
# Parfums (textes réécrits à partir du site ; fautes corrigées)
# famille : "creme" ou "sorbet"
# ---------------------------------------------------------------------------
FLAVORS = [
    ("vanille-sarrasin", "Vanille sarrasin", "creme", "La douceur de la vanille, relevée par le goût toasté du sarrasin."),
    ("vanille-tonka", "Vanille Tonka", "creme", "Le parfum préféré du chef François : vanille et fève tonka."),
    ("stracciatella", "Stracciatella", "creme", "Une crème onctueuse parsemée de copeaux de chocolat."),
    ("praline-noisette", "Praliné noisette", "creme", "Un praliné généreux, pour les amoureux de noisette."),
    ("grue-cacao", "Grué de cacao", "creme", "Une crème parsemée d'éclats croquants de fèves de cacao."),
    ("chocolat-blanc", "Chocolat blanc", "creme", "Douce et ronde, tout en gourmandise."),
    ("chevre", "Chèvre", "creme", "Née de la demande d'un chef de la région, à servir en salé comme en sucré."),
    ("caramel-cacahuete", "Caramel, cacahuète, chocolat", "creme", "Le trio gourmand : caramel, cacahuète et chocolat."),
    ("caramel-beurre-sale", "Caramel beurre salé", "creme", "Un classique, avec le bon équilibre entre sucré et salé."),
    ("cafe-ethiopie", "Café d'Éthiopie", "creme", "Un café d'origine Éthiopie, aux notes fruitées."),
    ("coco-menthe", "Coco menthe", "creme", "La noix de coco, rafraîchie par la menthe."),
    ("sierra-leone", "Chocolat Sierra Leone", "sorbet", "Un chocolat d'origine Sierra Leone, intense et sans lait."),
    ("cacao-pleine-arome", "Cacao pleine arôme", "sorbet", "Un assemblage de 25 cacaos pour un chocolat profond."),
    ("thym", "Thym", "sorbet", "Herbacé et surprenant, idéal en fin de repas."),
    ("rhum-raisin", "Rhum raisin", "sorbet", "Des raisins macérés dans le rhum, un grand classique."),
    ("poire", "Poire", "sorbet", "Le fruit de l'automne, tout simplement."),
    ("pistache", "Pistache", "sorbet", "Le goût franc de la pistache."),
    ("pamplemousse", "Pamplemousse", "sorbet", "Vif et acidulé, de saison en janvier."),
    ("orange-sanguine", "Orange sanguine", "sorbet", "La star du premier trimestre, à la couleur intense."),
    ("orange-basilic", "Orange basilic", "sorbet", "L'orange, réveillée par la fraîcheur du basilic."),
    ("noix", "Noix", "sorbet", "Le goût boisé de la noix."),
    ("nectarine", "Nectarine", "sorbet", "Le fruit de juillet, juteux et parfumé."),
    ("melon-menthe", "Melon menthe", "sorbet", "Le melon d'été et une touche de menthe."),
    ("mangue-thai", "Mangue thaï", "sorbet", "Une mangue mûre et parfumée."),
    ("kiwi", "Kiwi", "sorbet", "Acidulé et de saison en janvier."),
    ("framboise-poivron", "Framboise poivron", "sorbet", "Une alliance étonnante, fruitée et légèrement poivrée."),
    ("fraise", "Fraise", "sorbet", "Notre meilleure vente de l'été."),
    ("duo-citron", "Duo de citrons", "sorbet", "Deux citrons pour un sorbet frais et acidulé."),
    ("clementine", "Clémentine", "sorbet", "Le sorbet de décembre, doux et parfumé."),
    ("chocolat-banane", "Chocolat banane", "sorbet", "Le chocolat et la banane, le duo réconfortant."),
    ("cassis-poivre", "Cassis poivre noir", "sorbet", "Le cassis, relevé d'une pointe de poivre noir."),
    ("ananas", "Ananas", "sorbet", "Juteux et ensoleillé."),
    ("abricot", "Abricot", "sorbet", "L'abricot bien mûr, pour l'été."),
]
FLAVOR_DATA = [
    {"id": i, "name": n, "family": f, "desc": d, "img": f"/img/{i}.jpg"} for i, n, f, d in FLAVORS
]

# ---------------------------------------------------------------------------
# Boutique
# ---------------------------------------------------------------------------
TODO = '<span class="todo">À compléter</span>'
PRODUCTS = [
    dict(name="Bûche Framboise Passion & Vanille Tonka", price="33,00 €", parts=["6"], img="event-2.jpg",
         desc="Une bûche glacée fruitée : framboise, passion et vanille tonka.", out=True),
    dict(name="Bûche nougat", price="33,00 €", parts=["6"], img="event-2.jpg",
         desc="Une bûche glacée au nougat pour les fêtes."),
    dict(name="Vacherin Vanille Fraise", price="dès 24,90 €", parts=["4", "12"], img="fraise.jpg",
         desc="Meringue, glace vanille et sorbet fraise."),
    dict(name="Vacherin Vanille Chocolat", price="dès 24,90 €", parts=["4", "12"], img="cacao-pleine-arome.jpg",
         desc="Meringue, glace vanille et chocolat."),
    dict(name="Omelette norvégienne Rhum raisin", price="29,00 €", parts=["6"], img="event-1.jpg",
         desc="Meringue dorée, cœur glacé rhum raisin."),
    dict(name="Omelette norvégienne Vanille", price="29,00 €", parts=["6"], img="event-1.jpg",
         desc="Meringue dorée, cœur glacé vanille."),
]

# ---------------------------------------------------------------------------
# Icônes (traits, 24px)
# ---------------------------------------------------------------------------
def icon(name):
    paths = {
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
        "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "close": '<path d="M18 6 6 18M6 6l12 12"/>',
        "chev": '<path d="m6 9 6 6 6-6"/>',
        "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
        "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        "hands": '<path d="M20.4 14.5 16 10 4 20"/><path d="m7 9 5-5 8.5 8.5-5 5"/>',
        "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
        "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.7a1 1 0 0 0-.2-.6l-3.5-4.4A1 1 0 0 0 17.5 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
        "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
        "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.4A4 4 0 1 1 12.6 8 4 4 0 0 1 16 11.4z"/><path d="M17.5 6.5h.01"/>',
        "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
        "youtube": '<path d="M2.5 17a24 24 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24 24 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


CUR = ' aria-current="page"'

NAV = [
    ("/", "Accueil"),
    ("/nos-glaces/", "Nos glaces"),
    ("/desserts-glaces/", "Desserts glacés"),
    ("/professionnels/", "Pros & événements"),
    ("/notre-histoire/", "Notre histoire"),
    ("/contact/", "Nous trouver"),
]

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": "IceCreamShop",
    "name": "Les Garçons Glaciers",
    "description": "Artisan glacier angevin : glaces et sorbets bio, de saison et sans additif, desserts glacés et glaces pour événements à Angers.",
    "url": SITE + "/",
    "telephone": PHONE.replace(" ", ""),
    "email": EMAIL,
    "image": SITE + "/img/share.png",
    "logo": SITE + "/img/favicon.png",
    "foundingDate": "2018",
    "address": {"@type": "PostalAddress", "streetAddress": "4 Square La Fayette", "postalCode": "49000",
                "addressLocality": "Angers", "addressRegion": "Maine-et-Loire", "addressCountry": "FR"},
    "areaServed": ["Angers", "Anjou", "Maine-et-Loire"],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "13:00"},
    ],
    "sameAs": list(SOCIAL.values()),
}


def layout(path, title, description, body, extra_head=""):
    canonical = SITE + path
    nav = "".join(
        f'<a href="{href}"{CUR if href == path else ""}>{label}</a>' for href, label in NAV
    )
    drawer_nav = "".join(
        f'<a href="{href}"{CUR if href == path else ""}>{label}{icon("arrow")}</a>' for href, label in NAV
    )
    social = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{icon(n.lower())}</a>' for n, u in SOCIAL.items())
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#fbf8f2">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Les Garçons Glaciers">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/img/share.png">
<link rel="icon" href="/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Rubik:wght@500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={VERSION}">
<script type="application/ld+json">{json.dumps(LOCAL_BUSINESS, ensure_ascii=False)}</script>
{extra_head}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>

<div class="topbar">
  <div class="wrap">
    <span><span class="dot" aria-hidden="true"></span><span data-open-status>Lun–ven 9h–17h30 · sam 9h–13h</span></span>
    <span class="topbar-right">
      <a class="hide-sm" href="/contact/">Marché place La Fayette · mer. &amp; sam. matin</a>
      <a href="{PHONE_HREF}">{PHONE.replace("+33 ", "0")}</a>
    </span>
  </div>
</div>

<header class="header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Les Garçons Glaciers, accueil">
      <img src="/img/icon.png" alt="" width="160" height="200">
      <span class="brand-text"><span class="brand-name">Les Garçons Glaciers</span><span class="brand-tag">Artisan glacier bio · Angers</span></span>
    </a>
    <nav class="nav" aria-label="Navigation principale">{nav}</nav>
    <a class="btn btn-navy btn-sm btn-call" href="{PHONE_HREF}">{icon("phone")}Appeler</a>
    <button class="menu-toggle" type="button" data-open-menu aria-controls="drawer" aria-expanded="false" aria-label="Ouvrir le menu">{icon("menu")}</button>
  </div>
</header>

<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-backdrop" data-close-menu></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer-head">
      <span class="brand-name">Menu</span>
      <button class="menu-toggle" style="display:inline-flex" type="button" data-close-menu aria-label="Fermer le menu">{icon("close")}</button>
    </div>
    <nav aria-label="Navigation mobile">{drawer_nav}</nav>
    <div class="drawer-cta">
      <a class="btn btn-primary" href="/desserts-glaces/">Commander un dessert glacé</a>
      <a class="btn btn-ghost" href="{PHONE_HREF}">{icon("phone")}{PHONE}</a>
    </div>
  </div>
</div>

<main id="contenu">
{body}
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <span class="brand-name">Les Garçons Glaciers</span>
        <p style="margin-top:12px;max-width:34ch">Artisan glacier bio à Angers depuis 2018. Glaces, sorbets plein fruit et desserts glacés, faits avec les fruits de producteurs de l'Anjou.</p>
        <div class="socials">{social}</div>
      </div>
      <div>
        <h3>Nous joindre</h3>
        <ul>
          <li><a href="{PHONE_HREF}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ADDRESS}</li>
          <li><a href="{ROUTE}" target="_blank" rel="noopener">Itinéraire →</a></li>
        </ul>
      </div>
      <div>
        <h3>Horaires</h3>
        <ul class="tabular">
          <li>Lun – ven : 9h – 17h30</li>
          <li>Marché place La Fayette : mer. &amp; sam. 9h – 13h</li>
          <li>Dimanche : fermé</li>
        </ul>
      </div>
      <div>
        <h3>Le site</h3>
        <ul>
          <li><a href="/nos-glaces/">Nos crèmes glacées et sorbets</a></li>
          <li><a href="/desserts-glaces/">Bûches, vacherins et omelettes</a></li>
          <li><a href="/professionnels/">Glaces pour mariage et séminaire</a></li>
          <li><a href="/contact/#devis">Demander un devis</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Les Garçons Glaciers · SAS · Angers</span>
      <span><a href="/mentions-legales/">Mentions légales</a> · <a href="/mentions-legales/#confidentialite">Confidentialité</a> · <a href="/mentions-legales/#cgv">CGV</a></span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  <a class="btn btn-ghost" href="{PHONE_HREF}">{icon("phone")}Appeler</a>
  <a class="btn btn-primary" href="/contact/#devis">Devis</a>
</div>

<script src="/assets/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


def flavor_card(id_, name, family, desc):
    kind = "Crème glacée" if family == "creme" else "Sorbet"
    alt = f"{kind} {name.lower()} artisanale des Garçons Glaciers, Angers"
    return f"""<article class="flavor" data-id="{id_}" data-family="{family}">
  <div class="flavor-img"><img src="/img/{id_}.jpg" alt="{escape(alt)}" loading="lazy" decoding="async" width="720" height="720"><span class="chip">{kind}</span></div>
  <div class="flavor-body"><h3>{escape(name)}</h3><p>{escape(desc)}</p></div>
</article>"""


def cta_band():
    return f"""<section class="section-tight"><div class="wrap">
  <div class="cta-band">
    <div>
      <h2>Une question, une commande, un événement ?</h2>
      <p>Appelez-nous ou écrivez-nous : on répond vite, et on adore parler glace.</p>
    </div>
    <div class="actions">
      <a class="btn btn-primary" href="/contact/#devis">Demander un devis</a>
      <a class="btn btn-light" href="{PHONE_HREF}">{icon("phone")}{PHONE}</a>
    </div>
  </div>
</div></section>"""


def mk(m):
    return f'<span class="market">{m}</span>' if m else ""


def hours_table():
    rows = [
        (1, "Lundi", "9h – 17h30", ""),
        (2, "Mardi", "9h – 17h30", ""),
        (3, "Mercredi", "9h – 17h30", "Marché place La Fayette 9h – 13h"),
        (4, "Jeudi", "9h – 17h30", ""),
        (5, "Vendredi", "9h – 17h30", ""),
        (6, "Samedi", "9h – 13h", "Marché place La Fayette"),
        (0, "Dimanche", "Fermé", ""),
    ]
    out = "".join(
        f'<tr data-day="{d}"><th scope="row">{n}</th><td>{h}{mk(m)}</td></tr>'
        for d, n, h, m in rows
    )
    return f'<table class="hours"><caption class="muted" style="caption-side:bottom;text-align:left;padding-top:10px;font-size:.85rem">Horaires à confirmer avec l\'équipe avant mise en ligne.</caption><tbody>{out}</tbody></table>'


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_home():
    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="intro">
      <span class="eyebrow">{icon("pin")}Artisan glacier · Angers (49)</span>
      <h1>Glaces et sorbets bio, faits à Angers <em>avec les fruits de l'Anjou</em></h1>
      <p class="hero-lead">Depuis 2018, deux amis d'enfance fabriquent des crèmes glacées, des sorbets plein fruit et des desserts glacés bio, sans additif, au rythme des saisons.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="/desserts-glaces/">Commander un dessert glacé</a>
        <a class="btn btn-ghost" href="/contact/#devis">Devis pour un événement</a>
      </div>
      <ul class="hero-points">
        <li>{icon("check")}Bio et sans additif</li>
        <li>{icon("check")}Circuits courts</li>
        <li>{icon("check")}Livraison partout en France</li>
      </ul>
    </div>
    <div class="hero-art">
      <img src="/img/truck.png" alt="Illustration du triporteur glacier des Garçons Glaciers" width="1200" height="816" fetchpriority="high">
      <div class="hero-badge">
        <span class="pin">{icon("pin")}</span>
        <span><strong>Marché place La Fayette</strong>Mercredi et samedi, 9h – 13h</span>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow">Ce que l'on fait</span>
        <h2>Pour vous, vos clients ou vos invités</h2>
      </div>
    </div>
    <div class="paths">
      <a class="path" href="/desserts-glaces/">
        <div class="path-img"><img src="/img/event-2.jpg" alt="Bûches et desserts glacés artisanaux sur un plateau" loading="lazy" width="1400" height="1000"></div>
        <div class="path-body"><span class="path-tag">Particuliers</span><h3>Desserts glacés à commander</h3><p>Bûches, vacherins et omelettes norvégiennes, à retirer à Angers ou livrés partout en France.</p><span class="link-arrow">Voir les desserts glacés {icon("arrow")}</span></div>
      </a>
      <a class="path" href="/professionnels/#restaurants">
        <div class="path-img"><img src="/img/restaurant.jpg" alt="Desserts glacés au chocolat servis sur un plateau" loading="lazy" width="1400" height="1000"></div>
        <div class="path-body"><span class="path-tag">Professionnels</span><h3>Restaurants et revendeurs</h3><p>Nos crèmes glacées à la carte de votre restaurant, ou en revente dans votre commerce.</p><span class="link-arrow">Devenir partenaire {icon("arrow")}</span></div>
      </a>
      <a class="path" href="/professionnels/#evenements">
        <div class="path-img"><img src="/img/event-1.jpg" alt="Omelettes norvégiennes meringuées pour un événement" loading="lazy" width="1400" height="1000"></div>
        <div class="path-body"><span class="path-tag">Événements</span><h3>Mariages et séminaires</h3><p>Un stand glacier de 50 à 5 000 personnes, avec nos parfums de saison.</p><span class="link-arrow">Organiser un événement {icon("arrow")}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section section-white">
  <div class="wrap season">
    <div>
      <span class="eyebrow">En ce moment · <span data-month>novembre</span></span>
      <h2>Les parfums de saison</h2>
      <p class="muted prose">Nos sorbets suivent le calendrier des fruits : poire à l'automne, clémentine en décembre, orange sanguine en début d'année, fraise et nectarine l'été.</p>
      <a class="link-arrow" href="/nos-glaces/">Voir les 33 parfums {icon("arrow")}</a>
    </div>
    <div class="season-list" data-season-list></div>
  </div>
  <script type="application/json" id="flavor-data">{json.dumps(FLAVOR_DATA, ensure_ascii=False)}</script>
</section>

<section class="section section-mint">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow">Nos engagements</span>
        <h2>Une glace artisanale locale, et quatre respects</h2>
      </div>
    </div>
    <div class="values">
      <div class="value"><span class="ico">{icon("sun")}</span><h3>L'environnement</h3><p>On suit le cycle des saisons : chaque fruit arrive quand il est bon.</p></div>
      <div class="value"><span class="ico">{icon("hands")}</span><h3>Les producteurs</h3><p>Des circuits courts, avec des producteurs de la région.</p></div>
      <div class="value"><span class="ico">{icon("leaf")}</span><h3>Les fruits</h3><p>Ni colorant, ni conservateur, ni arôme artificiel.</p></div>
      <div class="value"><span class="ico">{icon("heart")}</span><h3>Vous</h3><p>Des glaces saines, naturelles et gourmandes.</p></div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap labels">
    <span class="eyebrow">Labels et partenaires</span>
    <img src="/img/labels.png" alt="Labels : Produit en Anjou, Collège culinaire de France, Département de Maine-et-Loire, Artisans militants de la qualité, Ville d'Angers" loading="lazy" width="1110" height="165">
    <p>Produit en Anjou · Artisans militants de la qualité (Collège culinaire de France) · soutenus par le Département et la Ville d'Angers</p>
  </div>
</section>

<section class="section section-white" id="avis">
  <div class="wrap">
    <span class="eyebrow">Ils nous ont fait confiance</span>
    <figure class="quote">
      <blockquote>« Tout était parfait pour notre mariage, et surtout les glaces bio ! »</blockquote>
      <figcaption>Un couple de mariés · <span class="todo">Ajouter le prénom, la date et la note avec l'accord du client</span></figcaption>
    </figure>
    <p style="margin-top:20px"><a class="link-arrow" href="https://www.mariages.net/food-truck/les-garcons-glaciers--e278772" target="_blank" rel="noopener">Lire les avis sur Mariages.net {icon("arrow")}</a></p>
  </div>
</section>

<section class="section-tight">
  <div class="wrap info-grid">
    <div class="info-card">
      <h2 style="font-size:1.6rem">Nous trouver à Angers</h2>
      <ul class="info-list">
        <li><span class="ico">{icon("pin")}</span><span><strong>Marché place La Fayette</strong>Mercredi et samedi, 9h – 13h<br><a href="{ROUTE}" target="_blank" rel="noopener">Itinéraire</a></span></li>
        <li><span class="ico">{icon("phone")}</span><span><strong>Téléphone</strong><a href="{PHONE_HREF}">{PHONE}</a></span></li>
        <li><span class="ico">{icon("mail")}</span><span><strong>E-mail</strong><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
      </ul>
    </div>
    <div class="info-card">{hours_table()}</div>
  </div>
</section>

{cta_band()}
"""
    return layout("/", "Glacier artisanal bio à Angers | Les Garçons Glaciers",
                  "Artisan glacier angevin depuis 2018 : glaces bio, sorbets plein fruit et desserts glacés sans additif. Marché place La Fayette, livraison et événements.",
                  body)


def page_glaces():
    cremes = [f for f in FLAVORS if f[2] == "creme"]
    sorbets = [f for f in FLAVORS if f[2] == "sorbet"]
    cards = "".join(flavor_card(*f) for f in FLAVORS)
    tabs = [("tout", "Tous"), ("saison", "De saison"), ("creme", "Crèmes glacées"), ("sorbet", "Sorbets plein fruit")]
    btns = "".join(
        f'<li><button type="button" role="tab" data-value="{v}" aria-selected="{"true" if v == "tout" else "false"}">{l}<span class="count" data-count="{v}"></span></button></li>'
        for v, l in tabs)
    btns_copy = "".join(
        f'<li><button type="button" tabindex="-1">{l}<span class="count" data-count="{v}"></span></button></li>' for v, l in tabs)
    body = f"""
<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / Nos glaces</nav>
    <h1>Nos glaces bio à Angers : crèmes glacées et sorbets plein fruit</h1>
    <p>{len(cremes)} crèmes glacées onctueuses et {len(sorbets)} sorbets riches en fruits, fabriqués à Angers avec des ingrédients de qualité et des fruits de saison. Sans colorant, sans conservateur, sans arôme artificiel.</p>
  </div>
</section>

<section style="padding-bottom:80px">
  <div class="wrap">
    <div class="toolbar">
      <div class="tabs" data-flavor-tabs>
        <ul class="tabs-list" role="tablist" aria-label="Filtrer les parfums">{btns}</ul>
        <div class="tabs-active" aria-hidden="true" inert><ul class="tabs-list">{btns_copy}</ul></div>
      </div>
      <span class="results-note tabular" data-results aria-live="polite"></span>
    </div>
    <h2 class="visually-hidden" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Tous nos parfums</h2>
    <div class="flavors">{cards}</div>

    <div class="info-card" style="margin-top:48px">
      <h2 style="font-size:1.5rem">Où goûter nos glaces ?</h2>
      <p class="muted prose">Au marché place La Fayette à Angers, le mercredi et le samedi matin, chez nos restaurants partenaires, ou lors de vos événements. Ingrédients et allergènes : demandez-nous la fiche de chaque parfum. {TODO}</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-navy" href="/contact/">Nous trouver</a><a class="btn btn-ghost" href="/professionnels/">Glaces pour professionnels</a></div>
    </div>
  </div>
</section>
"""
    return layout("/nos-glaces/", "Glaces et sorbets bio à Angers | Les Garçons Glaciers",
                  "Découvrez nos 33 parfums : crèmes glacées et sorbets plein fruit bio, de saison et sans additif, fabriqués à Angers par Les Garçons Glaciers.",
                  body)


def page_boutique():
    tabs = [("tout", "Tous"), ("4", "4 parts"), ("6", "6 parts"), ("12", "12 parts")]
    btns = "".join(
        f'<li><button type="button" role="tab" data-value="{v}" aria-selected="{"true" if v == "tout" else "false"}">{l}</button></li>' for v, l in tabs)
    btns_copy = "".join(f'<li><button type="button" tabindex="-1">{l}</button></li>' for v, l in tabs)
    items = []
    for p in PRODUCTS:
        parts = " ou ".join(p["parts"]) + " parts"
        out = p.get("out")
        actions = (
            f'<button class="btn btn-navy btn-sm" type="button" data-notify="{escape(p["name"])}">{icon("bell")}Me prévenir du retour</button>'
            f'<a class="btn btn-ghost btn-sm" href="#produits">Voir les autres bûches</a>'
            if out else
            f'<a class="btn btn-primary btn-sm" href="https://www.pourdebon.com" target="_blank" rel="noopener">Commander</a>'
            f'<a class="btn btn-ghost btn-sm" href="{PHONE_HREF}">Réserver par téléphone</a>'
        )
        items.append(f"""<article class="product{' is-out' if out else ''}" data-parts="{','.join(p['parts'])}">
  <div class="product-img"><img{' class="crop"' if not p['img'].startswith('event') else ''} src="/img/{p['img']}" alt="{escape(p['name'])}, dessert glacé artisanal" loading="lazy" width="1400" height="1000"></div>
  <div class="product-body">
    <div class="product-top"><h3>{escape(p['name'])}</h3><span class="price">{p['price']}</span></div>
    <div class="product-meta"><span class="pill">{parts}</span><span class="pill">Bio</span>{'<span class="pill out">Victime de son succès</span>' if out else ''}</div>
    <p class="product-desc">{escape(p['desc'])}</p>
    <details class="more">
      <summary>Ingrédients, allergènes et livraison {icon("chev")}</summary>
      <dl>
        <dt>Ingrédients</dt><dd>{TODO}</dd>
        <dt>Allergènes</dt><dd>{TODO}</dd>
        <dt>Conservation</dt><dd>Au congélateur (−18 °C). {TODO}</dd>
        <dt>Retrait</dt><dd>Au marché place La Fayette, Angers</dd>
        <dt>Livraison</dt><dd>Partout en France via pourdebon.com · délai et tarif {TODO}</dd>
      </dl>
    </details>
    <div class="product-actions">{actions}</div>
  </div>
</article>""")
    body = f"""
<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / Desserts glacés</nav>
    <h1>Desserts glacés artisanaux : bûches, vacherins et omelettes norvégiennes</h1>
    <p>Des desserts glacés bio, faits à Angers. À retirer au marché ou livrés partout en France.</p>
  </div>
</section>

<section style="padding-bottom:80px" id="produits">
  <div class="wrap">
    <div class="notice">
      <span class="ico">{icon("truck")}</span>
      <p><strong>Livraison de glace partout en France.</strong> Nos desserts voyagent au froid grâce à notre partenaire pourdebon.com.</p>
      <a class="btn btn-ghost btn-sm" href="https://www.pourdebon.com" target="_blank" rel="noopener">Par ici</a>
    </div>
    <div class="toolbar">
      <div class="tabs" data-shop-tabs>
        <ul class="tabs-list" role="tablist" aria-label="Filtrer par nombre de parts">{btns}</ul>
        <div class="tabs-active" aria-hidden="true" inert><ul class="tabs-list">{btns_copy}</ul></div>
      </div>
    </div>
    <h2 style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Nos desserts glacés</h2>
    <div class="products">{''.join(items)}</div>
  </div>
</section>
{cta_band()}
"""
    return layout("/desserts-glaces/", "Bûche glacée et desserts glacés bio | Les Garçons Glaciers Angers",
                  "Bûches glacées, vacherins et omelettes norvégiennes bio, faits à Angers. Retrait au marché place La Fayette ou livraison de glace partout en France.",
                  body)


def page_pros():
    def offer(id_, img, alt, tag, title, text, bullets, cta):
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        return f"""<article class="offer" id="{id_}">
  <div class="offer-img"><img src="/img/{img}" alt="{alt}" loading="lazy" width="1400" height="1000"></div>
  <div class="offer-body"><span class="path-tag">{tag}</span><h3>{title}</h3><p>{text}</p><ul>{lis}</ul>{cta}</div>
</article>"""
    devis = '<a class="btn btn-primary btn-sm" href="/contact/#devis">Demander un devis</a>'
    body = f"""
<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / Professionnels et événements</nav>
    <h1>Glace pour mariage, séminaire et restaurant à Angers</h1>
    <p>Fournisseur de glaces artisanales en Anjou : événements de 50 à 5 000 personnes, crèmes glacées à la carte pour les restaurants et vente aux entreprises.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><a class="btn btn-primary" href="/contact/#devis">Demander un devis</a><a class="btn btn-ghost" href="{PHONE_HREF}">{icon("phone")}{PHONE}</a></div>
  </div>
</section>

<section style="padding-bottom:80px">
  <div class="wrap">
    <h2 style="font-size:1.8rem;margin-bottom:24px">Nos quatre offres</h2>
    <div class="offers">
      {offer("evenements", "event-1.jpg", "Omelettes norvégiennes meringuées servies lors d'un événement", "Événements", "Organiser un événement", "Mariages, séminaires, fêtes : on vient avec nos glaces et nos parfums de saison.", ["De 50 à 5 000 personnes", "Mariages, séminaires, anniversaires", "Parfums choisis avec vous"], devis)}
      {offer("restaurants", "restaurant.jpg", "Desserts glacés au chocolat préparés pour un restaurant", "Restaurants", "Fournisseur pour restaurant", "Proposez une crème glacée artisanale et bio à votre carte, fabriquée à Angers.", ["Parfums à la carte", "Créations sur demande (notre glace au chèvre est née ainsi)", "Approvisionnement local"], devis)}
      {offer("entreprises", "entreprises.jpg", "Texture d'une crème glacée artisanale au chocolat", "Revendeurs", "Vente aux entreprises", "Épiceries fines, cavistes, comités d'entreprise : nos glaces bio en revente.", ["Glaces et sorbets en pots", "Bâtonnets glacés et coffrets", "Tarifs professionnels sur demande"], devis)}
      {offer("marche", "event-2.jpg", "Desserts glacés présentés au marché", "Marché", "Marché place La Fayette", "Retrouvez-nous chaque semaine au cœur d'Angers pour goûter les parfums du moment.", ["Mercredi et samedi, 9h – 13h", "Place La Fayette, Angers", "Parfums de saison"], f'<a class="btn btn-navy btn-sm" href="{ROUTE}" target="_blank" rel="noopener">Itinéraire</a>')}
    </div>
  </div>
</section>

<section class="section section-navy">
  <div class="wrap">
    <span class="eyebrow" style="color:#f6b27a">Pourquoi nous choisir</span>
    <h2>Des glaces fabriquées à Angers, avec l'agriculture locale</h2>
    <p class="prose">Des produits bio, sans additif, de saison, et une équipe qui se déplace avec vous. Les tarifs dépendent du nombre de convives et des parfums : on vous répond avec un devis précis.</p>
    <div class="stats">
      <div class="stat"><strong>50 – 5 000</strong><span>convives par événement</span></div>
      <div class="stat"><strong>33</strong><span>parfums au fil de l'année</span></div>
      <div class="stat"><strong>2018</strong><span>artisan glacier angevin depuis</span></div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap info-card" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:center">
    <div><h2 style="font-size:1.5rem;margin-bottom:6px">Atelier « Fabriquer de la glace avec un pro »</h2><p class="muted" style="margin:0">Au laboratoire d'Angers, apprenez à faire votre glace et repartez avec deux pots de 500 g. Idéal pour une sortie d'équipe.</p></div>
    <a class="btn btn-navy" href="/contact/">Nous contacter</a>
  </div>
</section>
{cta_band()}
"""
    return layout("/professionnels/", "Glace pour mariage et séminaire à Angers | Les Garçons Glaciers",
                  "Glaces artisanales bio pour mariages, séminaires et restaurants en Anjou : événements de 50 à 5 000 personnes et vente aux entreprises. Devis gratuit.",
                  body)


def page_histoire():
    body = f"""
<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / Notre histoire</nav>
    <h1>Notre histoire : deux amis d'enfance, glaciers en Anjou</h1>
  </div>
</section>
<section style="padding-bottom:80px">
  <div class="wrap story">
    <div class="prose">
      <p style="font-size:1.15rem">Les Garçons Glaciers, ce sont deux amis d'enfance attachés à leur terroir, qui ont décidé en 2018 de fabriquer des glaces artisanales à Angers.</p>
      <p>Nos sorbets sont faits « plein fruit », avec des fruits de l'agriculture locale. Nos crèmes glacées sont préparées avec des ingrédients de qualité. Le résultat : des glaces saines, naturelles et gourmandes.</p>
      <h2 style="font-size:1.6rem;margin-top:1.4em">Glace artisanale locale</h2>
      <p>Nous nous approvisionnons auprès de producteurs de la région, sans additifs, et nous travaillons au rythme des saisons. C'est pour cela que notre carte change au fil de l'année.</p>
      <p class="muted" style="font-size:.95rem">{TODO} Photos de l'équipe, du laboratoire et des producteurs partenaires.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px"><a class="btn btn-primary" href="/nos-glaces/">Découvrir nos parfums</a><a class="btn btn-ghost" href="/contact/">Venir nous voir</a></div>
    </div>
    <img src="/img/truck.png" alt="Illustration du triporteur des Garçons Glaciers au bord de l'eau" loading="lazy" width="1200" height="816" style="box-shadow:none;mix-blend-mode:multiply">
  </div>
</section>
<section class="section section-mint">
  <div class="wrap">
    <h2>Nos quatre respects</h2>
    <div class="values">
      <div class="value"><span class="ico">{icon("sun")}</span><h3>L'environnement</h3><p>Le cycle des saisons guide notre carte.</p></div>
      <div class="value"><span class="ico">{icon("hands")}</span><h3>Les producteurs</h3><p>Circuits courts et fruits de la région.</p></div>
      <div class="value"><span class="ico">{icon("leaf")}</span><h3>Les fruits</h3><p>Ni colorant, ni conservateur, ni arôme artificiel.</p></div>
      <div class="value"><span class="ico">{icon("heart")}</span><h3>Les consommateurs</h3><p>Des glaces bio, saines et gourmandes.</p></div>
    </div>
  </div>
</section>
<section class="section-tight">
  <div class="wrap labels">
    <img src="/img/labels.png" alt="Labels : Produit en Anjou, Collège culinaire de France, Département de Maine-et-Loire, Artisans militants de la qualité, Ville d'Angers" loading="lazy" width="1110" height="165">
  </div>
</section>
"""
    return layout("/notre-histoire/", "Notre histoire, artisan glacier angevin | Les Garçons Glaciers",
                  "Deux amis d'enfance, artisans glaciers à Angers depuis 2018 : glaces bio, sorbets plein fruit, circuits courts et produits de saison en Anjou.",
                  body)


def page_contact():
    body = f"""
<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / Nous trouver</nav>
    <h1>Nous trouver et nous contacter à Angers</h1>
    <p>Au marché place La Fayette, par téléphone ou par e-mail. Pour un événement, demandez un devis en deux minutes.</p>
  </div>
</section>

<section style="padding-bottom:56px">
  <div class="wrap info-grid">
    <div style="display:grid;gap:20px">
      <div class="info-card">
        <ul class="info-list">
          <li><span class="ico">{icon("phone")}</span><span><strong>Téléphone</strong><a href="{PHONE_HREF}">{PHONE}</a></span></li>
          <li><span class="ico">{icon("mail")}</span><span><strong>E-mail</strong><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
          <li><span class="ico">{icon("pin")}</span><span><strong>Marché place La Fayette</strong>{ADDRESS}<br><a href="{ROUTE}" target="_blank" rel="noopener">Ouvrir l'itinéraire</a></span></li>
        </ul>
      </div>
      <div class="info-card"><h2 style="font-size:1.3rem">Horaires</h2>{hours_table()}</div>
    </div>
    <div class="map">
      <div class="map-placeholder">
        <div>
          <strong style="font-family:var(--font-display);color:var(--navy);font-size:1.2rem">Place La Fayette, Angers</strong>
          <p>La carte Google se charge seulement si vous cliquez, pour ne pas déposer de cookies sans votre accord.</p>
          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
            <button class="btn btn-navy btn-sm" type="button" data-load-map>Afficher la carte</button>
            <a class="btn btn-ghost btn-sm" href="{ROUTE}" target="_blank" rel="noopener">Itinéraire</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-white" id="devis">
  <div class="wrap" style="max-width:860px">
    <h2>Écrivez-nous</h2>
    <p class="muted">Une simple question, ou un devis pour votre mariage, séminaire ou restaurant.</p>
    <div class="form-card">
      <div class="switch" role="tablist" data-switch>
        <button type="button" role="tab" aria-selected="true" aria-controls="f-question" data-key="question">Une question</button>
        <button type="button" role="tab" aria-selected="false" aria-controls="f-devis" data-key="devis">Un devis événement</button>
      </div>

      <form id="f-question" class="form-panel" data-mail="Question depuis le site" novalidate>
        <div class="form-grid">
          <div class="field"><label for="q-nom">Nom et prénom</label><input id="q-nom" name="Nom" autocomplete="name" required></div>
          <div class="field"><label for="q-mail">E-mail</label><input id="q-mail" name="E-mail" type="email" autocomplete="email" autocapitalize="none" required></div>
          <div class="field full"><label for="q-msg">Votre message</label><textarea id="q-msg" name="Message" required></textarea></div>
        </div>
        <div class="form-foot"><small>Vos données servent uniquement à vous répondre. <a href="/mentions-legales/#confidentialite">Confidentialité</a></small><button class="btn btn-primary" type="submit" enterkeyhint="send">Envoyer</button></div>
      </form>

      <form id="f-devis" class="form-panel" data-mail="Demande de devis événement" hidden novalidate>
        <div class="form-grid">
          <div class="field"><label for="d-nom">Nom et prénom</label><input id="d-nom" name="Nom" autocomplete="name" required></div>
          <div class="field"><label for="d-mail">E-mail</label><input id="d-mail" name="E-mail" type="email" autocomplete="email" autocapitalize="none" required></div>
          <div class="field"><label for="d-tel">Téléphone</label><input id="d-tel" name="Téléphone" type="tel" autocomplete="tel" inputmode="tel" required></div>
          <div class="field"><label for="d-type">Type d'événement</label><select id="d-type" name="Type"><option>Mariage</option><option>Séminaire / entreprise</option><option>Restaurant / revente</option><option>Fête privée</option><option>Autre</option></select></div>
          <div class="field"><label for="d-lieu">Lieu</label><input id="d-lieu" name="Lieu" autocomplete="address-level2" required></div>
          <div class="field"><label for="d-date">Date</label><input id="d-date" name="Date" type="date" required></div>
          <div class="field"><label for="d-nb">Nombre de convives</label><input id="d-nb" name="Convives" type="number" inputmode="numeric" min="1" required></div>
          <div class="field"><label for="d-budget">Budget <span class="opt">(facultatif)</span></label><input id="d-budget" name="Budget" inputmode="decimal"></div>
          <div class="field full"><label for="d-msg">Précisions <span class="opt">(facultatif)</span></label><textarea id="d-msg" name="Précisions"></textarea></div>
        </div>
        <div class="form-foot"><small>Réponse sous 48 h ouvrées. {TODO}</small><button class="btn btn-primary" type="submit" enterkeyhint="send">Demander mon devis</button></div>
      </form>
    </div>
  </div>
</section>
"""
    return layout("/contact/", "Contact et horaires, glacier à Angers | Les Garçons Glaciers",
                  "Contactez Les Garçons Glaciers : téléphone, e-mail, horaires et marché place La Fayette à Angers. Demande de devis pour mariage, séminaire et restaurant.",
                  body)


def page_legal():
    body = f"""
<section class="page-head"><div class="wrap"><nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / Mentions légales</nav><h1>Mentions légales et confidentialité</h1></div></section>
<section style="padding-bottom:80px"><div class="wrap prose legal">
  <h2>Éditeur du site</h2>
  <dl>
    <dt>Raison sociale</dt><dd>Les Garçons Glaciers, SAS au capital de 12 000 €</dd>
    <dt>Siège social</dt><dd>{ADDRESS}</dd>
    <dt>SIRET</dt><dd class="tabular">840 379 069 00015</dd>
    <dt>RCS</dt><dd>Angers 840 379 069</dd>
    <dt>TVA intracommunautaire</dt><dd class="tabular">FR34840379069</dd>
    <dt>Directeur de la publication</dt><dd>François Blourde, Président</dd>
    <dt>Téléphone</dt><dd><a href="{PHONE_HREF}">{PHONE}</a></dd>
    <dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
  </dl>
  <h2>Hébergement</h2>
  <p>{TODO} Indiquer l'hébergeur réel du nouveau site (nom, adresse, téléphone).</p>
  <h2 id="confidentialite">Politique de confidentialité</h2>
  <p>Les informations envoyées via les formulaires (nom, e-mail, téléphone, détails de l'événement) servent uniquement à répondre à votre demande et à établir un devis. Elles ne sont ni vendues ni cédées.</p>
  <p>Elles sont conservées le temps nécessaire au traitement de la demande, puis au maximum 3 ans après le dernier contact. Vous pouvez demander leur consultation, rectification ou suppression à <a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez aussi adresser une réclamation à la CNIL.</p>
  <h2>Cookies</h2>
  <p>Ce site ne dépose pas de cookie de mesure d'audience ni de publicité. La carte Google Maps de la page « Nous trouver » n'est chargée que si vous cliquez sur « Afficher la carte » ; Google peut alors déposer ses propres cookies.</p>
  <h2 id="cgv">Conditions générales de vente</h2>
  <p>{TODO} Reprendre les CGV de l'ancien site (non relues pendant l'audit).</p>
</div></section>
"""
    return layout("/mentions-legales/", "Mentions légales | Les Garçons Glaciers, glacier à Angers",
                  "Mentions légales, politique de confidentialité et cookies du site des Garçons Glaciers, artisan glacier bio à Angers (SAS, RCS Angers 840 379 069).",
                  body, '<meta name="robots" content="noindex, follow">')


PAGES = {
    "index.html": page_home,
    "nos-glaces/index.html": page_glaces,
    "desserts-glaces/index.html": page_boutique,
    "professionnels/index.html": page_pros,
    "notre-histoire/index.html": page_histoire,
    "contact/index.html": page_contact,
    "mentions-legales/index.html": page_legal,
}

# Anciennes adresses Wix → nouvelles (audit : URLs trompeuses)
REDIRECTS = [
    ("/accueil", "/"),
    ("/a-propos-de-nous", "/notre-histoire/"),
    ("/about", "/notre-histoire/"),
    ("/copie-de-nos-sorbet-plein-fruit", "/nos-glaces/#creme"),
    ("/copie-de-nos-cr%C3%AAmes-glac%C3%A9es", "/nos-glaces/"),
    ("/services-9", "/nos-glaces/#sorbet"),
    ("/services-6", "/nos-glaces/"),
    ("/shop", "/desserts-glaces/"),
    ("/boutique", "/desserts-glaces/"),
    ("/boutique/", "/desserts-glaces/"),
    ("/evenementiel", "/professionnels/"),
    ("/avis", "/#avis"),
    ("/mentions-legales", "/mentions-legales/"),
]


def main():
    for rel, fn in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fn(), encoding="utf-8")
        print("écrit", rel)

    urls = "".join(f"<url><loc>{SITE}/{rel.replace('index.html', '')}</loc></url>" for rel in PAGES if "mentions" not in rel)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    # Netlify / Cloudflare Pages
    (ROOT / "_redirects").write_text("".join(f"{a}  {b}  301\n" for a, b in REDIRECTS), encoding="utf-8")
    # Apache (o2switch)
    ht = "RewriteEngine On\n" + "".join(f"Redirect 301 {a} {b}\n" for a, b in REDIRECTS if "%" not in a)
    ht += "ErrorDocument 404 /index.html\n"
    (ROOT / ".htaccess").write_text(ht, encoding="utf-8")
    print("écrit sitemap.xml, robots.txt, _redirects, .htaccess")


if __name__ == "__main__":
    main()

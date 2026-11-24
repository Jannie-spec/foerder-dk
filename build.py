"""Bygger foerder.dk som statiske filer i dist/.

Kør:  python3 build.py
Teksterne står i PAGES herunder. Billederne ligger allerede på webhotellet i /onewebmedia/
(fra den gamle Website Builder-side) og røres ikke.
Upload: se README.md.
"""
import json, shutil, sys
from datetime import date
from pathlib import Path
from html import escape as e

ROOT = Path(__file__).parent
BASE = sys.argv[1] if len(sys.argv) > 1 else ""   # fx "/_ny" til en testudgave
DIST = ROOT / ("dist" if not BASE else "dist" + BASE.replace("/", "-"))
DOMAIN = "https://foerder.dk"
M = "/onewebmedia/"
CF_TOKEN = "a81efc8b0a634bd7a1ac0a85a38879da"     # Cloudflare Web Analytics (cookiefri)
VER = "1"
FB, IG = "https://facebook.com/foerderbornholm", "https://instagram.com/foerder_bornholm"
EMAIL, PHONE, PHONE_TEL = "info@hotelklippen.dk", "+45 31 68 88 29", "+4531688829"
PLACES = [("Grevens Dal", "https://www.hotelklippen.com/grevens-dal-gudhjem"),
          ("Skt. Jørgens Gaard", "https://www.hotelklippen.com/skt-joergens-gaard-gudhjem"),
          ("Therns", "https://www.hotelklippen.com/therns-hotel-gudhjem"),
          ("Therns Hostel", "https://therns.dk/")]


# Julekalender-banner (1.–24. dec 2026). Slet filen julekalender-banner.html efter jul, så forsvinder banneret.
_JKB = Path(__file__).with_name("julekalender-banner.html")
JK_BANNER = _JKB.read_text(encoding="utf-8") if _JKB.exists() else ""

def link(path):
    return BASE + path


def places_inline():
    a = [f'<a href="{u}">{n}</a>' for n, u in PLACES]
    return f"Klippen Hotel – {a[0]}, {a[1]} og {a[2]} – og for {a[3]}"


NAV = [("", "Hjem"), ("butikken", "Butikken"), ("reception", "Reception")]


def page(slug, title, desc, body):
    canon = DOMAIN + "/" + slug
    nav = "".join(f'<a href="{link("/" + s)}"{" aria-current=\"page\"" if s == slug else ""}>{n}</a>' for s, n in NAV)
    ld = {"@context": "https://schema.org", "@type": "Store", "@id": DOMAIN + "/#store", "name": "Førder",
          "description": "Butik med bornholmske varer og fælles reception for Klippen Hotel og Therns Hostel i Gudhjem.",
          "url": DOMAIN + "/", "image": DOMAIN + M + "Udefra.jpg", "logo": DOMAIN + M + "forder_black_logo.png",
          "email": EMAIL, "telephone": PHONE,
          "address": {"@type": "PostalAddress", "streetAddress": "Brøddegade 28", "postalCode": "3760",
                      "addressLocality": "Gudhjem", "addressRegion": "Bornholm", "addressCountry": "DK"},
          "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
              "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
              "opens": "09:00", "closes": "17:00"}],
          "sameAs": [FB, IG], "parentOrganization": {"@type": "Hotel", "name": "Klippen Hotel", "url": "https://www.hotelklippen.com"}}
    robots = '<meta name="robots" content="noindex">' if BASE else ""
    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" href="{M}foerder-favicon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Førder">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}{M}Udefra.jpg"><meta property="og:locale" content="da_DK">
<link rel="preload" href="{link('/assets/fonts/source-serif.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{link('/assets/site.css')}?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{link('/')}"><img src="{M}forder_black_logo.png" alt="Førder – butik og reception i Gudhjem" width="160" height="28"></a>
<nav>{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><img class="flogo" src="{M}forder_black_logo.png" alt="Førder" width="140" height="24">
<p>Butik og fælles reception<br>Brøddegade 28 · 3760 Gudhjem</p>
<p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
<div><h4>Overnatning</h4><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in PLACES)}</ul></div>
<div><h4>Følg Førder</h4><ul><li><a href="{FB}" rel="noopener">Facebook</a></li><li><a href="{IG}" rel="noopener">Instagram</a></li></ul>
<p class="small">En del af <a href="https://www.hotelklippen.com">Klippen Hotel</a>, drevet af <a href="https://janniebuchthorborg.dk/">Jannie Buch Thorborg</a></p></div>
</div></footer>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CF_TOKEN}"}}'></script>
</body>
</html>
"""


def img(name, alt, cls=""):
    return f'<figure class="{cls}"><img src="{M}{name}" alt="{e(alt)}" loading="lazy"></figure>'


HOME = page("", "Førder – butik og fælles reception i Gudhjem, Bornholm",
 "Førder i Brøddegade 28, Gudhjem: butik med bornholmske delikatesser, tøj og smykker – og fælles reception for Klippen Hotel og Therns Hostel.",
 f"""<section class="hero"><div class="wrap split">
<div><h1>Førder i Gudhjem</h1>
<p class="lead">Førder er en butik med udvalgte bornholmske varer og fælles reception for Klippen Hotel og Therns Hostel i Gudhjem. Du finder os i Brøddegade 28.</p>
<div class="btns"><a class="btn" href="{link('/reception')}">Besøg os</a><a class="btn ghost" href="{link('/butikken')}">Se butikken</a></div></div>
<figure class="tall"><img src="{M}Udefra.jpg" alt="Førders butik og fælles reception i Brøddegade 28, Gudhjem"><figcaption>Førder i Brøddegade 28</figcaption></figure>
</div></section>{JK_BANNER}
<section><div class="wrap split">
<div><h2>Fælles reception</h2>
<p>Førder er fælles reception for {places_inline()}. Kig ind i Brøddegade 28, så hjælper vi dig godt i gang med opholdet i Gudhjem.</p>
<p class="hours">Åbent dagligt kl. 9–17 · I sommerferien kl. 9–21</p>
<div class="btns"><a class="btn" href="{link('/reception')}">Om receptionen</a></div></div>
<figure><img src="{M}foerder-logoer-4___serialized1.jpg" alt="Logoer for Grevens Dal, Skt. Jørgens Gaard, Therns og Therns Hostel" loading="lazy"></figure>
</div></section>
<section class="mint"><div class="wrap">
<h2>Butikken</h2>
<p class="intro">Bornholmske delikatesser og drikkevarer, tøj, smykker og gaver – i et gammelt bindingsværkshus midt i Gudhjem.</p>
<div class="gallery">
{img('foerder-butik-1.jpg', 'Skilt foran Førder med nogle af mærkerne i butikken')}
{img('foerder-2.jpg', 'Inde i Førder, med disken i receptionen')}
{img('Udefra%20jul%20aften.jpg', 'Førders butik i Brøddegade 28 pyntet med lys ved juletid')}
</div>
<div class="btns"><a class="btn" href="{link('/butikken')}">Se hvad vi har</a></div>
</div></section>""")

BUTIK = page("butikken", "Butikken – bornholmske varer i Gudhjem | Førder",
 "Førder i Gudhjem: bornholmske delikatesser og drikkevarer, tøj, smykker, gaver og hudpleje i et gammelt bindingsværkshus i Brøddegade 28.",
 f"""<section class="hero"><div class="wrap split">
<div><h1>Butikken Førder</h1>
<p class="lead">Førder er en lille butik i et gammelt bindingsværkshus midt i Gudhjem. Her finder du bornholmske delikatesser og drikkevarer, tøj, smykker og gaver – til dig selv eller som en hilsen fra Bornholm.</p></div>
<figure class="tall"><img src="{M}Udefra%20jul%20aften.jpg" alt="Førders butik i Brøddegade 28 pyntet med lys ved juletid"><figcaption>Førder ved juletid</figcaption></figure>
</div></section>
<section><div class="wrap">
<dl class="brands">
<div><dt>Drikkevarer</dt><dd>Wild Distillery, Poul Pava, Snaps Bornholm, Bornholms Mosteri, Svaneke Bryghus, FALK Bornholm, Beer Here (øl fra Tejn) og bornholmsk te.</dd></div>
<div><dt>Bornholmske specialiteter</dt><dd>Høstet, Pastariget, Smedens ketchup og sennep, Vingummi Bornholm, No Crap, olie fra Lehnsgaard, bornholmsk honning og is fra Krølle Bølle.</dd></div>
<div><dt>Tøj</dt><dd>mbyM, Basic Apparel, Cozy og ICHI.</dd></div>
<div><dt>Smykker</dt><dd>WiOGA og Pilgrim.</dd></div>
<div><dt>Bolig og gaver</dt><dd>Chic Antique og Bornameter.</dd></div>
<div><dt>Hudpleje</dt><dd>Meraki og Ecooking.</dd></div>
</dl>
<p class="lead" style="margin-top:36px">Kig ind, når du går en tur i byen. Snart kan du også købe bornholmske varer og gavekurve i vores webshop.</p>
<p class="hours">Brøddegade 28, Gudhjem · Åbent dagligt kl. 9–17 · I sommerferien kl. 9–21</p>
</div></section>""")

RECEP = page("reception", "Reception i Gudhjem – Klippen Hotel & Therns Hostel | Førder",
 "Førder i Brøddegade 28 er fælles reception for Klippen Hotel (Grevens Dal, Skt. Jørgens Gaard, Therns) og Therns Hostel i Gudhjem. Åbent dagligt kl. 9–17.",
 f"""<section class="hero"><div class="wrap split">
<div><h1>Reception i Gudhjem</h1>
<p class="lead">Førder i Brøddegade 28 er fælles reception for {places_inline()}. Her får du svar på spørgsmål og gode råd om Gudhjem og Bornholm.</p>
<p>Receptionen hjælper med cykeludlevering, betaling for honestybaren og bestilling af rengøring eller nye håndklæder (senest kl. 10).</p>
<p class="hours">Åbent dagligt kl. 9–17 · I sommerferien kl. 9–21</p>
<p>Kontakt: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
<div class="btns"><a class="btn" href="https://www.hotelklippen.com/book-overnatning">Book Klippen Hotel</a><a class="btn ghost" href="https://therns.dk/book-nu/">Book Therns Hostel</a></div></div>
<figure class="tall"><img src="{M}foerder-2.jpg" alt="Receptionen i Førder"><figcaption>Receptionen i Førder</figcaption></figure>
</div></section>
<section class="mint"><div class="wrap center">
<img src="{M}foerder-logoer-4___serialized1.jpg" alt="Logoer for Grevens Dal, Skt. Jørgens Gaard, Therns og Therns Hostel" loading="lazy" style="max-width:720px;margin:0 auto">
</div></section>""")

NOTFOUND = page("404", "Siden findes ikke | Førder", "Siden findes ikke.",
 f"""<section class="hero"><div class="wrap center"><h1>Siden findes ikke</h1>
<p class="lead">Linket virker ikke længere, eller adressen er skrevet forkert.</p>
<div class="btns" style="justify-content:center"><a class="btn" href="{link('/')}">Gå til forsiden</a></div></div></section>""").replace(
 '<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"', 1)


if __name__ == "__main__":
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "site", DIST)
    (DIST / "index.html").write_text(HOME, encoding="utf-8")
    (DIST / "butikken.html").write_text(BUTIK, encoding="utf-8")
    (DIST / "reception.html").write_text(RECEP, encoding="utf-8")
    (DIST / "404.html").write_text(NOTFOUND, encoding="utf-8")
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{DOMAIN}/{s}</loc><lastmod>{today}</lastmod></url>" for s, _ in NAV)
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      + urls + "</urlset>\n", encoding="utf-8")
    if BASE:
        (DIST / ".htaccess").unlink()
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_ny/\nDisallow: /_wsb-backup/\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    files = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file())
    if not BASE:
        (ROOT / "filer.txt").write_text("\n".join(files) + "\n", encoding="utf-8")
    print("bygget", len(files), "filer", "(BASE=" + BASE + ")" if BASE else "")

# Alma Ibérica Online Shop

> Die Seele der Iberischen Halbinsel – authentisch, hochwertig, mit Liebe ausgewählt.

Statischer Shop-Prototyp für portugiesische und spanische Feinkost (Bacalhau, Olivenöl, Wein, Käse, Wurst u. a.). Entstanden im Rahmen der DSP Academy (KI-Manager, Baustein 3: KI-gestützte Webentwicklung mit Claude Code).

> **Hinweis:** Alle Firmen-, Kontakt- und Produktdaten (Adresse in Essen, Telefon, E-Mail, Marken) sind **erfundene Demo-Daten**. Die Rechtstexte sind Platzhalter und keine Rechtsberatung. Bezahlung und Bestellung sind nur simuliert.

## Funktionen

- Startseite, Shop mit Filtern (Region, Preis, Allergene, Bio, Tradition), Produktseite mit Galerie und Schnellansicht
- Warenkorb mit Gratisversand-Fortschritt, Kühlversand-Aufschlag und Gast-Checkout (simuliert)
- Suche mit Autocomplete, Wunschliste, Geschenkkörbe, Kundenkonto-Seite
- Mega-Menü, Cookie-Hinweis, Sprachumschalter (DE/PT/EN/ES, nur vorbereitet)
- SEO: Meta-Tags, Open Graph, JSON-LD, `sitemap.xml`, `robots.txt`, `llms.txt`
- Barrierefreiheit nach WCAG 2.2 AA: Tastaturbedienung, Fokusring, ARIA-Live-Meldungen, Skip-Link, `prefers-reduced-motion`

## Technik

| Bereich | Umsetzung |
|---|---|
| Markup / Styling | HTML5, Bootstrap 5.3.3 und Bootstrap Icons (CDN), eigenes Theme `assets/css/alma.css` |
| Logik | Vanilla JavaScript (`assets/js/alma.js`), kein Framework |
| Seitengenerator | Python-Skript `build.py` (nur Standardbibliothek) |
| Daten | Produktliste in `build.py`, daraus erzeugt `assets/js/products.js` |
| Speicher | Browser-`localStorage` (Warenkorb, Wunschliste, Einwilligung) |

## Schnellstart

Voraussetzung: Python 3. Für die Platzhalterbilder zusätzlich Pillow (`pip install pillow`).

```bash
# Seiten neu erzeugen
python build.py

# Lokal ansehen: http://localhost:8123
python -m http.server 8123
```

Die erzeugten Seiten laufen auch per Doppelklick auf `index.html`. Für Bootstrap ist eine Internetverbindung nötig.

## Projektstruktur

```
build.py                 Generator: Marken-Konfiguration, Produkte, Seiten-Metadaten
src/
  partials/              head.html, header.html, footer.html
  pages/                 Inhalt der Seiten (index, shop, product, cart, checkout, ...)
assets/
  css/alma.css           Theme (Farben und Abstände als Variablen in :root)
  js/alma.js             Shop-Logik
  js/products.js         GENERIERT aus build.py
  img/  fonts/           Bilder (WebP), Flaggen, Schrift
tools/make_images.py     Platzhalterbilder erzeugen
docs/DOKUMENTATION.md    Design-Entscheidungen, Komponenten, Checklisten
*.html (Hauptordner)     GENERIERT – nicht von Hand bearbeiten
```

## Wichtig: erzeugte Dateien

Die `.html`-Dateien im Hauptordner und `assets/js/products.js` werden bei jedem `python build.py` überschrieben. Änderungen gehören in `src/` oder `build.py`, danach neu bauen.

## Anpassen

- **Produkte:** Liste `PRODUCTS` in `build.py` bearbeiten, Bilder `assets/img/<name>.webp` und `<name>-s.webp` (180×240) ablegen, neu bauen.
- **Marke und Kontaktdaten:** Block `BRAND` in `build.py`.
- **Farben und Schrift:** Variablen im Block `:root` in `assets/css/alma.css`.
- **Neue Seite:** `meta(...)`-Eintrag in `build.py` plus Datei in `src/pages/`.

Ausführlich: [docs/DOKUMENTATION.md](docs/DOKUMENTATION.md). Hinweise für Claude Code: [CLAUDE.md](CLAUDE.md).

## Bekannte Grenzen

- Kein Backend: Warenkorb und Wunschliste liegen nur im Browser, Zahlung ist simuliert.
- Mehrsprachigkeit ist nur vorbereitet, Inhalte sind ausschließlich Deutsch.
- Einige Produktbilder (z. B. Rioja, Portwein, Jamón) sind Platzhalter.
- Bootstrap kommt per CDN; produktiv selbst hosten (DSGVO).
- Rechtstexte müssen vor einem Echtbetrieb von Fachleuten erstellt werden.

## Nächste Schritte

Anbindung an ein Shopsystem (z. B. Shopware, Shopify, WooCommerce) über das Objekt `cart` in `alma.js`, echte Zahlungsanbieter, Kühlversand-Logistik, Mehrsprachigkeit und eine Barrierefreiheitsprüfung durch Dritte.

## Sicherheit

Keine API-Schlüssel, Passwörter oder Zugangsdaten in den Code oder auf GitHub. Solche Werte gehören in eine `.env`-Datei, die in `.gitignore` steht.

## Lizenz

Noch nicht festgelegt. Lehr- und Demoprojekt.

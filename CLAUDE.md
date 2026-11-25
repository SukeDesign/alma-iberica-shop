# CLAUDE.md – Alma Ibérica Online Shop

Statischer Prototyp eines Online-Shops für iberische Feinkost (Portugal/Spanien). Sprache der Inhalte: Deutsch (de-DE). Stack: HTML5, Bootstrap 5.3.3 (CDN), Vanilla JS, Python-Generator – **kein npm, kein Backend**. Alle Produktdaten sind erfundene Demo-Daten.

## Wichtigste Regel: HTML-Dateien im Stammordner sind ERZEUGT

`index.html`, `shop.html`, `product.html`, `cart.html`, `checkout.html`, `search.html`, `gifts.html`, `account.html`, `terms.html`, `privacy.html`, `imprint.html`, `withdrawal.html`, `shipping.html`, `faq.html`, `contact.html`, `accessibility.html` werden von `build.py` überschrieben. **Änderungen nie dort machen**, sondern in `src/` bzw. `build.py`, danach neu bauen.

Ebenso erzeugt: `assets/js/products.js` (nicht von Hand ändern).

## Befehle

```bash
python build.py                       # alle Seiten + products.js neu erzeugen (Windows: python, nicht python3)
python -m http.server 8123            # lokaler Server (auch in .claude/launch.json als "alma-shop" konfiguriert)
python tools/make_images.py           # Platzhalterbilder erzeugen (braucht Pillow)
```
Die Seiten laufen auch per Doppelklick auf `index.html` (Internet nötig für Bootstrap-CDN). Es gibt keine Tests und keinen Linter. Nach dem Bauen auf die Meldung `WARN ungelöste Platzhalter` achten.

## Struktur

```
build.py                 Generator: BRAND-Konfig, PRODUCTS, Kategorien, Seiten-Meta, Statik-Seiten, FAQ
src/partials/            head.html, header.html, footer.html (auf jeder Seite)
src/pages/               Inhalt je Seite: index, shop, product, cart, checkout, search, geschenke, account
assets/css/alma.css      eigenes Theme (Tokens in :root, ca. 370 Zeilen)
assets/js/alma.js        gesamte Logik in einer IIFE (ca. 490 Zeilen)
assets/js/products.js    GENERIERT: window.AI_PRODUCTS / AI_CATS
assets/img/              *.webp (Produkt: name.webp + name-s.webp 180×240), flags/*.svg, hero.mp4/.webm
assets/fonts/amatic/     lokal gehostete Schrift Amatic
tools/make_images.py     Platzhalterbilder (überschreibt nie echte Fotos)
docs/DOKUMENTATION.md    Design-Rationale, Komponenten, Checklisten, Handover
```

## Wie der Build funktioniert (`build.py`)

- Pro Seite: `head + header + body + footer` werden zusammengesetzt. Der Body kommt aus `src/pages/<name>.html`; die 8 Rechts-/Info-Seiten (`STATIC`) und FAQ/Kontakt/Versand werden direkt in `static_body()` erzeugt – dort Texte/Platzhalter ändern, nicht in einer Datei.
- Platzhalter `{{...}}`: Variablen aus `BRAND` plus `title`, `description`, `canonical`, `body_class`, `extra_head`, `page`, `ld_org`, `ld_page`.
- Produktplatzhalter in Seiten: `{{cards:bestseller}}`, `{{cards:all}}`, `{{cards:related}}`, `{{cards:id1,id2}}`, `{{colcards:...}}` (mit Bootstrap-Spalte) und `{{shopcards}}` (alle, ab `BATCH`=8 versteckt für „Mehr laden“).
- Neue Seite: `meta(...)` in `build.py` eintragen + `src/pages/<name>.html` anlegen (oder in `STATIC` aufnehmen).
- Neues Produkt: Eintrag in `PRODUCTS` (Felder: id, name, brand, cat, region, price, amount, unit, rating, count, stock, badges, cool, img, bio, trad, desc, allergens, origin); Kategorie/Region ggf. in `CATS`/`REGIONS`; Bilder `assets/img/<img>.webp` und `<img>-s.webp`. Grundpreis wird aus `price/amount*1000` berechnet.
- Strukturierte Daten (JSON-LD) in `ld_for()`; Product-Schema gilt nur für das erste Produkt (Bacalhau) auf `product.html`.
- Rebranding: `BRAND` in `build.py`, `:root` in `alma.css`, Logo in `header.html` + `favicon.svg`.

## Frontend-Logik (`assets/js/alma.js`)

- Seitenspezifisches Verhalten über `<body data-page="...">`; Versandwerte über `data-free-ship`, `data-ship-cost`, `data-cool-cost` (kommen aus `BRAND`).
- Objekt `cart` ist die vorgesehene Schnittstelle zu einem echten Shopsystem. Datenquelle für Suche/Quick-View/Warenkorb ist `window.AI_PRODUCTS`.
- Browser-Speicher (localStorage, immer in try/catch): `ai_cart`, `ai_wish`, `ai_recent`, `ai_consent`, `ai_mode`.
- Produktkarten tragen `data-*`-Attribute (cat, region, price, stock, cool, bio, trad, allergens, rating), nach denen der Shop filtert.
- Bezahlung ist nur simuliert; kein Server-Code.

## Konventionen

- **Barrierefreiheit (WCAG 2.2 AA / BFSG) ist Kernanforderung**: Tap-Ziele ≥ 44 px, Fokusring 3 px, Icons mit `aria-hidden` + sichtbarem Text, Lagerstatus nie nur über Farbe, `aria-live` für Warenkorb/Toasts, ein H1 pro Seite. Laranja `#FF4F37` nicht für Text verwenden (Kontrast); Badges nutzen `--c-laranja-badge`.
- Keine Fremd-Fonts-CDNs (DSGVO); Bootstrap kommt per CDN mit SRI – produktiv selbst hosten.
- Rechtstexte sind `[PLATZHALTER]`; keine echten Firmen-/Personendaten eintragen, nur erfundene Testdaten.
- Sprachumschalter (DE/PT/EN/ES) im Header ist nur vorbereitet, Inhalte sind nur Deutsch.
- Keine Geheimnisse (API-Schlüssel, Passwörter) im Code; bei späterer Backend-Anbindung `.env` + `.gitignore` nutzen.
- Das Projekt ist (noch) kein Git-Repository – Arbeitsstände regelmäßig sichern (`git init`, Commits).

## Bekannte Grenzen

Warenkorb/Wunschliste nur im Browser, Filter „Marke“ kennt 4 Beispielmarken, Geschenk-Konfigurator nur Teaser, Produktbilder für Rioja, Portwein, Jamón, Manchego, Sardinen, Kaffee, Ginja (nutzt `portwein`) sowie Hero/Teaser sind Platzhalter. Details: `docs/DOKUMENTATION.md`.

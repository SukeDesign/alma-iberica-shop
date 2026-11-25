# Alma Ibérica Online Shop – Theme-Dokumentation

Stand: Prototyp v1 · HTML5, Bootstrap 5.3.3, Vanilla JS · Sprache: de-DE

## 1. Design-Rationale

**Farben (Ihre Vorgabe, 1:1 als Tokens in `assets/css/alma.css`)**

| Token | Wert | Einsatz | Kontrast |
|---|---|---|---|
| `--c-vinho` | #7F1D23 | CTA, Preise, Logo, Links, Hero | 10,0:1 auf Weiß |
| `--c-ink` | #16181D | Überschriften | – |
| `--c-gray` | #5A6570 | Fließtext, Meta | 5,9:1 auf Weiß |
| `--c-azulejo` | #5EB1BF | Hover-Unterstreichung, „Neu“-Badge (Tinte-Text), Muster | Tinte darauf 7,2:1 |
| `--c-laranja` | #FF4F37 | nur dekorativ | Weiß darauf nur **3,3:1** |

**Abweichung, die Sie kennen sollten:** Weißer Text auf `#FF4F37` verfehlt WCAG AA (4,5:1), besonders bei 11 px. Das Theme nutzt für Promo-/Bestseller-Badges deshalb `--c-laranja-badge: #C4301B` (5,5:1). Das Original-Laranja bleibt als Token erhalten, wird aber nicht für Text verwendet. Ebenso: Azulejo (#5EB1BF) hat auf Weiß nur 2,5:1 – daher nie als Fokusring oder Textfarbe, nur als Akzent.

**Typografie:** System-Schriften (Fließtext) und eine Serifen-Systemschrift (Überschriften: Iowan Old Style / Palatino / Georgia). Grund: keine Font-Requests (schneller, kein CLS) und DSGVO-sicher – Google-Fonts-CDN ist in Deutschland rechtlich heikel. Wollen Sie Fraunces/Inter, die Dateien selbst hosten und `--ai-font-head` / `--ai-font-body` ändern. 16 px Basis, Zeilenhöhe 1,6, max. 65ch Zeilenlänge.

**UX-Entscheidungen (Zielgruppe 55+):** Tap-Ziele ≥ 44 px, sichtbarer 3-px-Fokusring in Vinho, immer sichtbare Labels, Icons stets mit Text, Lagerstatus mit Icon + Text (nie nur Farbe), Gast-Checkout, Express-Zahlung, Gratisversand-Fortschrittsbalken, Lieferschätzung, „Wir importieren es für Sie“ bei leerer Suche.

**Barrierefreiheit:** Landmarks, ein H1 pro Seite, Skip-Link, Mega-Menü per Tastatur (Pfeile, Esc), ARIA-Combobox für die Suche, `aria-live` für Warenkorb/Toasts, Fehlerübersicht im Checkout mit Sprunglinks und `aria-describedby`, `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`.

**Performance:** keine Webfonts, keine Bibliotheken außer Bootstrap, Bilder mit `width`/`height` + `aspect-ratio`, `loading="lazy"` unterhalb des Falzes, Hero mit Preload + `fetchpriority="high"`, CSS-Containment auf Produktkarten, Skeleton statt Spinner, Karussell rein per CSS (scroll-snap).

### Rebranding in 3 Schritten
1. `assets/css/alma.css` → Block `:root` (Farben, Radius, Schriften, Azulejo-Muster `--ai-pattern`).
2. `build.py` → Block `BRAND` (Name, Claim, Domain, Öffnungszeiten, Telefon, WhatsApp, Versandwerte).
3. Logo-SVG in `src/partials/header.html` und `assets/img/favicon.svg` ersetzen, dann `python3 build.py`.

## 2. Dateistruktur

```
index.html shop.html product.html cart.html checkout.html   ← Pflichtseiten
search.html gifts.html account.html           ← weitere Seiten
agb/datenschutz/widerruf/impressum/versand/faq/kontakt/accessibility.html (Platzhalter)
assets/css/alma.css · assets/js/alma.js · assets/js/products.js (generiert)
assets/img/*.webp (Platzhalter-Bilder)
src/partials/ (head, header, footer)  src/pages/ (Seiteninhalte)
build.py (Generator)   tools/make_images.py (Platzhalterbilder)
```
Die `.html`-Dateien im Hauptordner sind **erzeugt**. Änderungen immer in `src/` machen und `python3 build.py` ausführen. Zum Ansehen genügt Doppelklick auf `index.html` (Internet nötig für Bootstrap-CDN).

## 3. Komponenten-Bibliothek

| Komponente | Bootstrap-Klassen / eigene Klassen |
|---|---|
| Header / Top-Bar / Sticky | `.topbar`, `.site-header.is-stuck`, `.container`, `.d-flex` |
| Mega-Menü | `.main-nav`, `.mega-panel`, `.nav-link-ai`, `aria-expanded` |
| Suche + Autocomplete | `.search-form`, `.suggest`, `role="combobox/listbox"` |
| Mobile Navigation / Warenkorb / Filter | `.offcanvas`, `.offcanvas-lg` |
| Produktkarte | `.p-card`, `.p-media`, `.p-badges`, `.p-wish`, `.stars`, `.ai-clamp-2` |
| Badges | `.badge .badge-promo/.badge-bestseller/.badge-new/.badge-cool/.badge-import` |
| Buttons | `.btn .btn-primary/.btn-outline-primary/.btn-light-ai`, `.is-loading` |
| Filter-Akkordeon | `.accordion`, `.form-check-input`, `.form-range`, `.filter-pill` |
| Produktraster | `.row .row-cols-2 .row-cols-md-3 .row-cols-xl-4` |
| Karussell | `.ai-carousel` (scroll-snap) |
| Galerie + Zoom | `.gallery-main`, `.thumb` |
| Mengen-Stepper | `.qty` |
| Warenkorbzeile / Fortschritt | `.cart-line`, `.free-ship > progress` |
| Checkout-Stepper / Auswahlkarten | `.stepper`, `.choice-card`, `.error-summary`, `.field-error` |
| Quick-View / Cookie | `.modal`, `.cookie-bar` |
| Toast | `.toast` in `#toastRegion` (aria-live) |
| Skeleton | `.skeleton` |
| Tabelle → Karten (mobil) | `.table .table-stack` |
| Breadcrumb / Pagination | `.breadcrumb`, `.pagination` |

## 4. Checklisten

**Breakpoints**

| Breite | Verhalten |
|---|---|
| 360 px | 2-Spalten-Raster, Suche unter Logo, Filter + Warenkorb als Offcanvas, Sticky-Kaufleiste |
| 576 px | größere Abstände, Karussell 42 % |
| 768 px | 3 Spalten, Desktop-Suche im Header, Trust-Bar 4-spaltig |
| 992 px | Filter-Sidebar fest, Mega-Menü, Kaufleiste ausgeblendet |
| 1200 / 1400 px | 4 Spalten, breiterer Container |

**WCAG 2.2 AA** (✔ umgesetzt im Code · ◐ im Livebetrieb zu prüfen)
- ✔ Kontraste (siehe Tabelle), ✔ Fokus 3 px, ✔ Tastaturbedienung Menü/Suche/Galerie, ✔ Labels + Fehlertexte, ✔ Statusmeldungen live, ✔ Reduced-Motion/Contrast/Forced-Colors, ✔ Ziel-Größe ≥ 44 px
- ◐ Test mit NVDA/VoiceOver, ◐ Lighthouse-Messung im Zielhosting, ◐ Prüfung durch Dritte vor BFSG-Erklärung

**Performance-Budget**

| Metrik | Ziel |
|---|---|
| LCP | < 2,5 s |
| INP | < 200 ms |
| CLS | < 0,1 |
| Lighthouse Performance / Accessibility | ≥ 90 / ≥ 95 |
| JS eigen | < 15 KB gzip (alma.js ≈ 10 KB, gemessen) |
| Eigenes CSS | < 10 KB gzip (alma.css ≈ 6,5 KB, gemessen) |

Gemessen wurde im Prototyp noch nicht (kein Lighthouse-Lauf möglich). Die Werte sind Ziele.

## 5. Handover

**Bilder/Produkte ersetzen:** Produktbilder sind jetzt im Hochformat 3:4 (Foto `name.webp`, Mini `name-s.webp` 180×240). Echte Fotos vorhanden für: Bacalhau, Olivenöl, Pastéis de Nata, Alentejo-Rotwein, Vinho Verde, Queijo de Cabra, Queijo da Ilha, Chouriço, Farinheira, Mel. Noch Platzhalter: Rioja, Portwein, Jamón, Manchego, Sardinen, Kaffee, Ginja sowie Hero, Story-, Geschenk- und Café-Teaser. Die Fotos haben nur 307×409 px – für scharfe Darstellung auf Retina/Produktseite bitte Originale mit mind. 900×1200 px liefern. `tools/make_images.py` überschreibt nie die echten Fotos. Produkte stehen in `build.py` (Liste `PRODUCTS`); `products.js` wird daraus erzeugt.

**Rechtstexte:** `AGB`, `Datenschutz`, `Widerruf`, `Impressum`, `Versand`, `Barrierefreiheit` sind markierte `[PLATZHALTER]`. Von Anwalt/Rechtstexter-Dienst füllen lassen. Datenschutz muss das Bootstrap-CDN nennen – oder Bootstrap selbst hosten (empfohlen).

**Anbindung an Shopsysteme:** Das Objekt `cart` in `alma.js` durch API-Aufrufe ersetzen (Shopware Store-API, Shopify Cart-API, WooCommerce Store API). Partials (`head/header/footer`) werden zu Twig-/Fluid-/Liquid-Templates, `card()` in `build.py` zum Produktkarten-Template.

**Nächste Schritte:** 1) Backend & Warenwirtschaft, 2) Zahlungsanbieter (PayPal, Kreditkarte, Rechnung mit Bonitätsprüfung), 3) Versand: DHL-Kühlversand, Zonen/Preise, Click & Collect je Standort, 4) Mehrsprachigkeit EN/PT/ES (Texte in Sprachdateien auslagern, `lang`-Attribute sind vorbereitet), 5) echte Bilder/Nährwerte/Allergene (LMIV), 6) Cookie-Banner mit echtem Consent-Management verbinden, 7) Barrierefreiheitsprüfung.

**Bekannte Grenzen des Prototyps:** Warenkorb/Wunschliste im Browser-Speicher, Bezahlung ist simuliert, JSON-LD „Product“ gilt nur für die Standard-Produktseite, Filter „Marke“ kennt nur 4 Beispielmarken, Geschenk-Konfigurator ist nur ein Teaser.

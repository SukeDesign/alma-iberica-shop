#!/usr/bin/env python3
"""
ALMA IBÉRICA ONLINE SHOP – Mini-Generator
Setzt src/partials + src/pages zu fertigen HTML-Dateien zusammen (kein npm nötig).
Aufruf:  python3 build.py
Rebranding: BRAND-Block unten ändern + :root in assets/css/alma.css.
Die erzeugten HTML-Dateien liegen im Projektstamm und laufen ohne Server (Doppelklick).
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)

# ===================== KONFIGURATION (Global Theme) =====================
BRAND = {
    "brand": "Alma Ibérica",
    "promise": "Die Seele der Iberischen Halbinsel – authentisch, hochwertig, mit Liebe ausgewählt.",
    "base_url": "https://www.almaiberica.de",   # erfundene Demo-Domain (passend zur Demo-E-Mail)
    "hours": "Mo–Fr 10–18 Uhr, Sa 10–14 Uhr",
    # --- Erfundene Kundendaten (Demo) ---
    "street": "Schornstr. 1988",
    "zip": "45128",
    "city": "Essen",
    "region_name": "Nordrhein-Westfalen",
    "region_code": "DE-NW",
    "country": "Deutschland",
    "lat": "51.4556",       # ungefähre Koordinaten Essen (Demo) – im Echtbetrieb exakt eintragen
    "lon": "7.0116",
    "address": "Schornstr. 1988, 45128 Essen",
    "pickup": "Essen, Schornstr. 1988",
    "phone": "0176 12345678",
    "phone_raw": "+4917612345678",
    "email": "info@almaiberica.de",
    "whatsapp_url": "https://wa.me/4917612345678",
    "free_ship": "69",      # Gratis-Versand ab (EUR)
    "ship_cost": "5.90",    # Standardversand
    "cool_cost": "4.90",    # Kühlversand-Aufschlag
}
BATCH = 8  # Produkte pro "Mehr laden"

# ===================== PRODUKTDATEN (Demo, erfundene Marken) =====================
# unit: "kg" oder "l"; amount in g bzw. ml
PRODUCTS = [
 dict(id="bacalhau-graudo", name="Bacalhau Graúdo, Stockfisch getrocknet", brand="Casa do Mar", cat="bacalhau", region="minho", price=24.90, amount=1000, unit="kg", rating=4.8, count=212, stock=14, badges=["bestseller","import"], cool=False, img="bacalhau", bio=False, trad=True,
      desc="Handverlesener Gadus morhua, nach traditioneller Art gesalzen und luftgetrocknet. Vor der Zubereitung 36–48 Std. wässern.", allergens="Fisch (Dorsch)", origin="Portugal"),
 dict(id="azeite-alentejo", name="Azeite Virgem Extra, Alentejo 0,5 l", brand="Herdade Aurora", cat="oel", region="alentejo", price=11.90, amount=500, unit="l", rating=4.9, count=167, stock=40, badges=["bestseller"], cool=False, img="olivenoel", bio=True, trad=True,
      desc="Fruchtiges, leicht pfeffriges Olivenöl aus Cobrançosa- und Picual-Oliven, kalt extrahiert.", allergens="keine", origin="Portugal"),
 dict(id="pasteis-de-nata", name="Pastéis de Nata, tiefgekühlt, 6 Stück", brand="Doçaria Lusa", cat="brot", region="minho", price=6.90, amount=360, unit="kg", rating=4.9, count=341, stock=3, badges=["bestseller","cool"], cool=True, img="pasteis", bio=False, trad=True,
      desc="Blätterteig-Törtchen mit Vanillecreme – 12 Min. aufbacken, bis die Oberseite karamellisiert.", allergens="Weizen, Milch, Eier, Gluten", origin="Portugal"),
 dict(id="alentejo-tinto", name="Alentejo DOC Tinto 2021, 0,75 l", brand="Herdade Aurora", cat="wein", region="alentejo", price=12.90, amount=750, unit="l", rating=4.7, count=104, stock=26, badges=["new"], cool=False, img="wein-alentejo", bio=False, trad=False,
      desc="Samtiger Rotwein aus Aragonez und Trincadeira mit reifen roten Früchten und weichen Tanninen.", allergens="Sulfite", origin="Portugal"),
 dict(id="rioja-reserva", name="Rioja Reserva 2018, 0,75 l", brand="Bodega Vega Alta", cat="wein", region="rioja", price=16.50, amount=750, unit="l", rating=4.6, count=76, stock=18, badges=[], cool=False, img="wein-rioja", bio=False, trad=False,
      desc="Tempranillo-Cuvée, 24 Monate im Eichenfass gereift – Vanille, Leder und rote Frucht.", allergens="Sulfite", origin="Spanien"),
 dict(id="porto-tawny-10", name="Vinho do Porto Tawny 10 Anos, 0,75 l", brand="Quinta da Serra", cat="wein", region="douro", price=21.90, amount=750, unit="l", rating=4.8, count=121, stock=9, badges=["import"], cool=False, img="portwein", bio=False, trad=True,
      desc="Nussig-karamelliger Tawny im Fass gereift – ideal zu Käse und Schokolade.", allergens="Sulfite", origin="Portugal"),
 dict(id="jamon-iberico-bellota", name="Jamón Ibérico de Bellota, handgeschnitten, 100 g", brand="Dehesa Real", cat="schinken", region="andalusien", price=12.90, amount=100, unit="kg", rating=4.9, count=88, stock=22, badges=["new","cool"], cool=True, img="jamon", bio=False, trad=True,
      desc="Eichel-gemästeter Ibérico-Schinken, 36 Monate gereift, hauchdünn aufgeschnitten und vakuumiert.", allergens="keine", origin="Spanien"),
 dict(id="manchego-curado", name="Queso Manchego Curado D.O.P., 250 g", brand="Finca Llanura", cat="kaese", region="kastilien", price=8.90, amount=250, unit="kg", rating=4.7, count=134, stock=31, badges=["cool"], cool=True, img="manchego", bio=False, trad=True,
      desc="Schafskäse aus Rohmilch, 6 Monate gereift, kräftig-nussig im Geschmack.", allergens="Milch", origin="Spanien"),
 dict(id="chourico-carne", name="Chouriço de Carne, geräuchert, 250 g", brand="Casa do Monte", cat="schinken", region="alentejo", price=5.90, amount=250, unit="kg", rating=4.6, count=159, stock=45, badges=["bestseller"], cool=False, img="chourico", bio=False, trad=True,
      desc="Paprikawurst nach Hausrezept, über Eichenholz geräuchert – perfekt für Feijoada und Grill.", allergens="keine", origin="Portugal"),
 dict(id="sardinhas-azeite", name="Sardinhas em Azeite, 120 g", brand="Conservas Atlântico", cat="konserven", region="minho", price=3.90, amount=120, unit="kg", rating=4.8, count=203, stock=120, badges=["import"], cool=False, img="sardinen", bio=False, trad=True,
      desc="Sardinen von der Atlantikküste, von Hand verpackt und in Olivenöl eingelegt.", allergens="Fisch", origin="Portugal"),
 dict(id="cafe-torrado", name="Café Torrado em Grão, 500 g", brand="Torra Lusa", cat="kaffee", region="alentejo", price=9.90, amount=500, unit="kg", rating=4.5, count=64, stock=0, badges=[], cool=False, img="kaffee", bio=False, trad=True,
      desc="Mittelkräftige Röstung nach portugiesischer Art, mit Schokoladennote und wenig Säure.", allergens="keine", origin="Portugal"),
 dict(id="ginja-licor", name="Ginja Likör mit Sauerkirschen, 0,7 l", brand="Casa Óbidos", cat="spirituosen", region="alentejo", price=13.90, amount=700, unit="l", rating=4.7, count=57, stock=16, badges=["new"], cool=False, img="portwein", bio=False, trad=True,
      desc="Sauerkirschlikör nach klassischem Rezept – traditionell im Schokoladenbecher serviert.", allergens="keine", origin="Portugal"),
 dict(id="vinho-verde-doc", name="Vinho Verde DOC Branco, 0,75 l", brand="Quinta do Lima", cat="wein", region="minho", price=8.90, amount=750, unit="l", rating=4.6, count=91, stock=38, badges=[], cool=False, img="vinho-verde", bio=False, trad=False,
      desc="Leichter, spritziger Weißwein aus dem Minho mit Zitrus- und Apfelnoten – ideal zu Fisch und Meeresfrüchten.", allergens="Sulfite", origin="Portugal"),
 dict(id="queijo-de-cabra", name="Queijo de Cabra, Ziegenkäse, 250 g", brand="Serra Verde", cat="kaese", region="alentejo", price=7.50, amount=250, unit="kg", rating=4.7, count=63, stock=12, badges=["new","cool"], cool=True, img="queijo-cabra", bio=False, trad=True,
      desc="Cremig-milder Ziegenkäse mit feiner Säure, nach traditionellem Rezept gereift.", allergens="Milch", origin="Portugal"),
 dict(id="queijo-da-ilha", name="Queijo da Ilha, Schnittkäse, 300 g", brand="Ilha Azul", cat="kaese", region="azoren", price=9.90, amount=300, unit="kg", rating=4.8, count=72, stock=15, badges=["import","cool"], cool=True, img="queijo-ilha", bio=False, trad=True,
      desc="Würziger Kuhmilchkäse von den Azoren mit kräftigem Aroma und goldgelber Rinde.", allergens="Milch", origin="Portugal (Azoren)"),
 dict(id="farinheira", name="Farinheira, portugiesische Mehlwurst, 200 g", brand="Casa do Monte", cat="schinken", region="alentejo", price=4.90, amount=200, unit="kg", rating=4.5, count=48, stock=33, badges=[], cool=False, img="farinheira", bio=False, trad=True,
      desc="Geräucherte Wurst aus Weizenmehl und Schweinefett, gewürzt mit Paprika – klassisch gebraten oder im Eintopf.", allergens="Weizen, Gluten", origin="Portugal"),
 dict(id="mel-de-portugal", name="Mel de Portugal, Blütenhonig, 500 g", brand="Apiário Serra", cat="suess", region="alentejo", price=8.90, amount=500, unit="kg", rating=4.9, count=86, stock=52, badges=["new"], cool=False, img="mel", bio=False, trad=True,
      desc="Milder Blütenhonig aus portugiesischer Imkerei mit Lavendelnote.", allergens="keine", origin="Portugal"),
]
CATS = {"wein":"Wein","bacalhau":"Bacalhau","oel":"Olivenöl","brot":"Brot & Gebäck","schinken":"Schinken & Wurst","kaese":"Käse","konserven":"Konserven","kaffee":"Kaffee","spirituosen":"Spirituosen","suess":"Süßes & Gebäck"}
REGIONS = {"alentejo":"Alentejo","douro":"Douro","minho":"Minho","rioja":"Rioja","andalusien":"Andalusien","katalonien":"Katalonien","kastilien":"Kastilien-La Mancha","azoren":"Azoren"}
BADGE = {"bestseller":("badge-bestseller","Bestseller"),"new":("badge-new","Neu"),"cool":("badge-cool","Kühlpflichtig"),"import":("badge-import","Importiert")}

def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"
def base(p):
    per = p["price"] / p["amount"] * 1000
    return f"{eur(per)} / {p['unit']}"
def stock_html(p):
    if p["stock"] == 0: return '<span class="stock stock-out"><i class="bi bi-x-circle" aria-hidden="true"></i> Derzeit nicht verfügbar</span>'
    if p["stock"] <= 5: return f'<span class="stock stock-low"><i class="bi bi-exclamation-circle" aria-hidden="true"></i> Nur noch {p["stock"]}× verfügbar</span>'
    return '<span class="stock stock-ok"><i class="bi bi-check-circle" aria-hidden="true"></i> Auf Lager</span>'
def stars(r):
    full = int(r); half = 1 if r - full >= .5 else 0
    s = '<i class="bi bi-star-fill" aria-hidden="true"></i>' * full + ('<i class="bi bi-star-half" aria-hidden="true"></i>' if half else '') + '<i class="bi bi-star" aria-hidden="true"></i>' * (5 - full - half)
    return s

def card(p, hidden=False):
    badges = "".join(f'<span class="badge {BADGE[b][0]}">{BADGE[b][1]}</span>' for b in p["badges"])
    out = p["stock"] == 0
    add = ('<button type="button" class="btn p-add" disabled aria-label="Nicht verfügbar" title="Nicht verfügbar"><i class="bi bi-cart-x-fill" aria-hidden="true"></i></button>' if out else
           f'<button type="button" class="btn p-add" data-add="{p["id"]}" aria-label="In den Warenkorb: {p["name"]}" title="In den Warenkorb"><i class="bi bi-cart-fill" aria-hidden="true"></i></button>')
    return f'''<article class="p-card" data-id="{p["id"]}" data-cat="{p["cat"]}" data-region="{p["region"]}" data-price="{p["price"]}" data-stock="{p["stock"]}" data-cool="{int(p["cool"])}" data-bio="{int(p["bio"])}" data-trad="{int(p["trad"])}" data-allergens="{p["allergens"].lower()}" data-rating="{p["rating"]}" data-name="{p["name"]}" data-brand="{p["brand"]}"{" hidden" if hidden else ""}>
  <div class="p-media"><a class="p-media-link" href="product.html?id={p["id"]}" tabindex="-1" aria-hidden="true"><img src="assets/img/{p["img"]}.webp" alt="{p["name"]}" width="307" height="409" loading="lazy" decoding="async"></a><div class="p-badges">{badges}</div>
    <button type="button" class="p-wish" data-wish="{p["id"]}" aria-pressed="false" aria-label="{p["name"]} zur Wunschliste hinzufügen"><i class="bi bi-heart" aria-hidden="true"></i></button>
    <div class="p-add-wrap">{add}</div></div>
  <div class="p-body">
    <span class="p-brand">{p["brand"]}</span>
    <h3 class="p-title ai-clamp-2"><a href="product.html?id={p["id"]}">{p["name"]}</a></h3>
    <div><span class="stars" role="img" aria-label="Bewertung {str(p["rating"]).replace(".", ",")} von 5 Sternen">{stars(p["rating"])}</span> <span class="rating-count">({p["count"]})</span></div>
    <div class="p-price ai-price">{eur(p["price"])}</div>
    <div class="p-base">{base(p)} · inkl. MwSt.</div>
    <div>{stock_html(p)}</div>
  </div>
</article>'''

def colcard(p, hidden=False):
    return f'<div class="col"{" hidden" if hidden else ""}>' + card(p) + '</div>'

def cards(sel):
    if sel == "all": ps = PRODUCTS
    elif sel == "bestseller": ps = [p for p in PRODUCTS if "bestseller" in p["badges"]] + [p for p in PRODUCTS if "new" in p["badges"]][:3]
    elif sel == "related": ps = [PRODUCTS[i] for i in (1, 9, 3, 8)]
    elif sel == "cross": ps = [PRODUCTS[i] for i in (1, 9, 8)]
    else: ps = [p for p in PRODUCTS if p["id"] in sel.split(",")]
    return ps

PAGES = {}  # filename -> dict(title, description, body_class, extra_head, robots, ld)
NOINDEX = "noindex, follow"
INDEX = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
def meta(f, title, desc, body_class="", extra_head="", ld=None, robots=INDEX): PAGES[f] = dict(title=title, description=desc, body_class=body_class, extra_head=extra_head, ld=ld, robots=robots)
SUF = " | Alma Ibérica"
# SEO: Titel ca. ≤ 60 Zeichen, Beschreibung ca. ≤ 155 Zeichen, Hauptkeyword + Ort (Essen) vorn
meta("index.html", "Iberische Feinkost online kaufen – aus Essen" + SUF, "Portugiesische & spanische Feinkost, Wein, Bacalhau und Olivenöl online bestellen. Kühlversand deutschlandweit, Click & Collect in Essen.")
meta("shop.html", "Feinkost, Wein & Bacalhau aus Portugal & Spanien" + SUF, "Wein, Bacalhau, Olivenöl, Käse und Wurst aus Portugal & Spanien – filtern nach Region, Preis und Allergenen. Versand ab Essen, frei ab 69 €.")
meta("product.html", "Bacalhau Graúdo, Stockfisch getrocknet, 1 kg" + SUF, "Bacalhau Graúdo (Gadus morhua) aus Portugal, traditionell gesalzen und getrocknet. 24,90 € pro kg. Versand ab Essen oder Abholung.", "has-sticky-buy")
meta("cart.html", "Warenkorb" + SUF, "Ihr Warenkorb bei Alma Ibérica – Versandart wählen und sicher zur Kasse.", robots=NOINDEX)
meta("checkout.html", "Kasse – Kontakt, Zahlung, Übersicht" + SUF, "Sicher bestellen als Gast: Kontakt & Lieferart, Zahlung per PayPal, Kreditkarte, Vorkasse oder Rechnung.", robots=NOINDEX)
meta("search.html", "Suche" + SUF, "Suchergebnisse bei Alma Ibérica – nicht gefunden? Wir importieren es für Sie.", robots=NOINDEX)
meta("gifts.html", "Geschenkkörbe mit iberischen Spezialitäten" + SUF, "Geschenkkörbe und Gutscheine mit portugiesischen & spanischen Feinkost-Spezialitäten für Geburtstag, Weihnachten und Firmen – aus Essen.")
meta("account.html", "Mein Konto – Login, Registrierung, Wunschliste" + SUF, "Anmelden, registrieren oder Wunschliste ansehen.", robots=NOINDEX)
STATIC = {
 "terms.html": ("Allgemeine Geschäftsbedingungen (AGB)", "AGB"), "privacy.html": ("Datenschutzerklärung", "Datenschutz"),
 "withdrawal.html": ("Widerrufsbelehrung", "Widerruf"), "imprint.html": ("Impressum", "Impressum"),
 "shipping.html": ("Versand, Kühlversand & Click & Collect", "Versand"), "faq.html": ("Häufige Fragen (FAQ)", "FAQ"),
 "contact.html": ("Kontakt, Öffnungszeiten & Anfahrt", "Kontakt"), "accessibility.html": ("Erklärung zur Barrierefreiheit (BFSG)", "Barrierefreiheit"),
}
for f, (t, s_) in STATIC.items(): meta(f, t + SUF, f"{t} – Alma Ibérica, {BRAND['street']}, {BRAND['zip']} {BRAND['city']}.")
meta("faq.html", "FAQ: Lieferung, Kühlversand, Abholung in Essen" + SUF, "Antworten zu Lieferzeit, Kühlversand, Versandkosten, Zahlung und Abholung in Essen – Alma Ibérica, Ihr Shop für iberische Feinkost.")
meta("contact.html", "Kontakt & Anfahrt – Alma Ibérica in Essen" + SUF, f"Alma Ibérica, {BRAND['street']}, {BRAND['zip']} {BRAND['city']}. Tel. {BRAND['phone']}, {BRAND['email']}. Öffnungszeiten: {BRAND['hours']}.")
meta("shipping.html", "Versand, Kühlversand & Click & Collect in Essen" + SUF, "Versandkosten 5,90 € (frei ab 69 €), Lieferzeit 2–4 Werktage, Kühlversand für Käse & Schinken, Abholung in Essen.")

# ===================== SEO / GEO: strukturierte Daten (JSON-LD) =====================
def abs_(u): return f'{BRAND["base_url"]}/{u}'

def ld_business():
    """Organization + lokales Geschäft + WebSite (auf jeder Seite). NAP-Daten (Name, Adresse, Telefon) kommen nur aus BRAND."""
    b = BRAND["base_url"]
    addr = {"@type":"PostalAddress","streetAddress":BRAND["street"],"postalCode":BRAND["zip"],"addressLocality":BRAND["city"],"addressRegion":BRAND["region_name"],"addressCountry":"DE"}
    hours = [{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"10:00","closes":"18:00"},
             {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"10:00","closes":"14:00"}]
    maps = "https://www.google.com/maps/search/?api=1&query=" + (BRAND["street"] + ", " + BRAND["zip"] + " " + BRAND["city"]).replace(" ", "+")
    return {"@context":"https://schema.org","@graph":[
        {"@type":"Organization","@id":b+"/#organization","name":BRAND["brand"],"alternateName":BRAND["brand"]+" Online Shop","url":b,"logo":b+"/assets/img/favicon.svg","slogan":BRAND["promise"],
         "email":BRAND["email"],"telephone":BRAND["phone_raw"],"address":addr,
         "contactPoint":[{"@type":"ContactPoint","contactType":"customer service","telephone":BRAND["phone_raw"],"email":BRAND["email"],"areaServed":"DE","availableLanguage":["de"]}]},
        {"@type":["Store","LocalBusiness"],"@id":b+"/#store","name":BRAND["brand"],"description":"Online-Shop und Abholstation für portugiesische und spanische Feinkost, Wein, Bacalhau und Olivenöl in Essen.",
         "url":b,"image":b+"/assets/img/hero.webp","logo":b+"/assets/img/favicon.svg","telephone":BRAND["phone_raw"],"email":BRAND["email"],"address":addr,
         "geo":{"@type":"GeoCoordinates","latitude":BRAND["lat"],"longitude":BRAND["lon"]},"hasMap":maps,
         "openingHoursSpecification":hours,"priceRange":"€€","currenciesAccepted":"EUR","paymentAccepted":"PayPal, Kreditkarte, Vorkasse, Rechnung",
         "areaServed":[{"@type":"Country","name":"Deutschland"},{"@type":"City","name":BRAND["city"]}],
         "knowsAbout":["Portugiesische Feinkost","Spanische Feinkost","Bacalhau","Olivenöl","Portwein","Rioja","Jamón Ibérico"],
         "parentOrganization":{"@id":b+"/#organization"}},
        {"@type":"WebSite","@id":b+"/#website","url":b,"name":BRAND["brand"]+" Online Shop","inLanguage":"de-DE","publisher":{"@id":b+"/#organization"},
         "potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":b+"/search.html?q={search_term_string}"},"query-input":"required name=search_term_string"}}]}

def ld_for(f):
    pid = PRODUCTS[0]; b = BRAND["base_url"]; m = PAGES[f]
    crumbs = lambda items: {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":abs_(u)} for i,(n,u) in enumerate(items)]}
    page = lambda t: {"@context":"https://schema.org","@type":t,"@id":abs_(f)+"#webpage","url":abs_(f),"name":m["title"],"description":m["description"],"inLanguage":"de-DE","isPartOf":{"@id":b+"/#website"},"about":{"@id":b+"/#store"}}
    out = []
    if f == "index.html": out.append(page("WebPage"))
    if f == "shop.html":
        out.append(crumbs([("Start","index.html"),("Shop","shop.html")])); out.append(page("CollectionPage"))
        out.append({"@context":"https://schema.org","@type":"ItemList","name":"Produkte bei Alma Ibérica","itemListElement":[{"@type":"ListItem","position":i+1,"name":p["name"],"url":abs_("product.html") if i == 0 else abs_("shop.html")} for i,p in enumerate(PRODUCTS[:12])]})
    if f == "gifts.html": out.append(crumbs([("Start","index.html"),("Geschenkkörbe","gifts.html")]))
    if f == "contact.html": out.append(crumbs([("Start","index.html"),("Kontakt","contact.html")])); out.append(page("ContactPage"))
    if f == "shipping.html": out.append(crumbs([("Start","index.html"),("Versand","shipping.html")]))
    if f == "product.html":
        out.append(crumbs([("Start","index.html"),("Bacalhau","shop.html?kat=bacalhau"),(pid["name"],"product.html")]))
        ship = {"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":BRAND["ship_cost"],"currency":"EUR"},"shippingDestination":{"@type":"DefinedRegion","addressCountry":"DE"},
                "deliveryTime":{"@type":"ShippingDeliveryTime","handlingTime":{"@type":"QuantitativeValue","minValue":0,"maxValue":1,"unitCode":"DAY"},"transitTime":{"@type":"QuantitativeValue","minValue":2,"maxValue":4,"unitCode":"DAY"}}}
        ret = {"@type":"MerchantReturnPolicy","applicableCountry":"DE","returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow","merchantReturnDays":14,"returnMethod":"https://schema.org/ReturnByMail"}
        out.append({"@context":"https://schema.org","@type":"Product","@id":abs_("product.html")+"#product","name":pid["name"],"sku":pid["id"],"image":[f"{b}/assets/img/{pid['img']}.webp"],"description":pid["desc"],
            "brand":{"@type":"Brand","name":pid["brand"]},"category":"Bacalhau & Fisch","countryOfOrigin":{"@type":"Country","name":pid["origin"]},
            "aggregateRating":{"@type":"AggregateRating","ratingValue":str(pid["rating"]),"reviewCount":str(pid["count"])},
            "offers":{"@type":"Offer","priceCurrency":"EUR","price":f"{pid['price']:.2f}","availability":"https://schema.org/InStock" if pid["stock"] > 0 else "https://schema.org/OutOfStock",
                "itemCondition":"https://schema.org/NewCondition","url":abs_("product.html"),"seller":{"@id":b+"/#store"},"shippingDetails":ship,"hasMerchantReturnPolicy":ret}})
    if f == "faq.html":
        out.append(crumbs([("Start","index.html"),("FAQ","faq.html")]))
        out.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)

# FAQ: kurze, in sich verständliche Antworten (Rich Results + Zitate in KI-Antworten / GEO)
FAQ = [
 ("Wo sitzt Alma Ibérica und kann ich vor Ort abholen?", f"Alma Ibérica sitzt in {BRAND['street']}, {BRAND['zip']} {BRAND['city']}. Per Click & Collect holen Sie Ihre Online-Bestellung dort ab ({BRAND['hours']}). Telefon: {BRAND['phone']}, E-Mail: {BRAND['email']}."),
 ("Was verkauft Alma Ibérica?", "Alma Ibérica ist ein Online-Shop für portugiesische und spanische Feinkost: Bacalhau (Stockfisch), Olivenöl, Wein, Portwein, Käse, Wurst, Schinken, Konserven, Kaffee und Gebäck wie Pastéis de Nata."),
 ("Wie lange dauert die Lieferung?", f"Der Standardversand innerhalb Deutschlands dauert 2–4 Werktage. Kühlpflichtige Ware (z. B. Käse, Schinken, Pastéis de Nata) reist im Kühlversand in 1–2 Werktagen (Aufschlag {BRAND['cool_cost'].replace('.', ',')} €)."),
 ("Was kostet der Versand?", f"Der Standardversand kostet {BRAND['ship_cost'].replace('.', ',')} €. Ab einem Warenwert von {BRAND['free_ship']} € versenden wir innerhalb Deutschlands versandkostenfrei."),
 ("Liefern Sie auch nach Österreich oder in die Schweiz?", "Aktuell liefern wir innerhalb Deutschlands. Für andere EU-Länder fragen Sie uns bitte per E-Mail oder Telefon nach einer individuellen Lösung."),
 ("Kann ich meine Bestellung abholen?", f"Ja, per Click & Collect in {BRAND['pickup']}. Sie wählen beim Bestellen „Click & Collect“ und erhalten eine Benachrichtigung, sobald die Ware bereitliegt. Kühlware bleibt bis zur Abholung gekühlt."),
 ("Mein Produkt fehlt im Sortiment – was tun?", "Schreiben Sie uns per WhatsApp, E-Mail oder Kontaktformular. Wir importieren es für Sie, sofern verfügbar."),
 ("Welche Zahlungsarten gibt es?", "PayPal, Kreditkarte, Vorkasse und Kauf auf Rechnung."),
 ("Woher stammen die Produkte?", "Alle Produkte stammen von ausgewählten Erzeugern aus Portugal und Spanien, z. B. aus dem Alentejo, dem Minho, dem Douro-Tal und aus La Rioja. Herkunft und Allergene stehen bei jedem Artikel."),
]

def render(f, body):
    m = PAGES[f]
    vars_ = dict(BRAND)
    vars_.update(title=m["title"], description=m["description"], canonical=f'{BRAND["base_url"]}/{f}', body_class=m["body_class"], extra_head=m["extra_head"], page=f.replace(".html",""), robots=m["robots"])
    vars_["ld_org"] = json.dumps(ld_business(), ensure_ascii=False)
    vars_["ld_page"] = ld_for(f)
    part = lambda n: open(P("src","partials",n+".html"), encoding="utf-8").read()
    html = part("head") + part("header") + body + part("footer")
    html = re.sub(r"\{\{cards:([^}]+)\}\}", lambda mo: "\n".join(card(p, hidden=False) for p in cards(mo.group(1))), html)
    html = re.sub(r"\{\{colcards:([^}]+)\}\}", lambda mo: "\n".join(colcard(p) for p in cards(mo.group(1))), html)
    html = re.sub(r"\{\{shopcards\}\}", lambda mo: "\n".join(colcard(p, hidden=(i >= BATCH)) for i, p in enumerate(PRODUCTS)), html)
    for k, v in vars_.items(): html = html.replace("{{"+k+"}}", str(v))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left: print("WARN ungelöste Platzhalter in", f, set(left))
    open(P(f), "w", encoding="utf-8").write(html)

def static_body(f):
    title, short = STATIC[f]
    bc = f'<nav aria-label="Brotkrümelnavigation" class="mb-3"><ol class="breadcrumb mb-0"><li class="breadcrumb-item"><a href="index.html">Start</a></li><li class="breadcrumb-item active" aria-current="page">{short}</li></ol></nav>'
    notes = {
     "terms.html": "[PLATZHALTER – AGB hier einfügen: Vertragspartner, Vertragsschluss, Preise & Zahlung, Lieferung, Eigentumsvorbehalt, Gewährleistung, Streitbeilegung (OS/VSBG). Vom Anwalt oder Rechtstexter-Dienst erstellen lassen.]",
     "privacy.html": "[PLATZHALTER – Datenschutzerklärung (DSGVO/TDDDG): Verantwortlicher, Zwecke & Rechtsgrundlagen, Cookies, Zahlungsdienstleister, Hosting, CDN, Betroffenenrechte.]",
     "withdrawal.html": "[PLATZHALTER – Widerrufsbelehrung inkl. Muster-Widerrufsformular. Hinweis: Das Widerrufsrecht erlischt bei schnell verderblicher Ware (§ 312g Abs. 2 BGB).]",
     "imprint.html": "[PLATZHALTER – Impressum nach § 5 DDG: Firmenname, Rechtsform, Anschrift, Vertretungsberechtigte, Kontakt, Handelsregister, USt-IdNr., ggf. Lebensmittelkontrolle.]",
     "shipping.html": "[PLATZHALTER – Versandzonen & Preise: Deutschland / EU / Drittland. Kühlversand per [DHL Kühlversand / Paketdienst]. Click & Collect in Essen.]",
     "contact.html": "[PLATZHALTER – Anfahrt (Karte/ÖPNV/Parken) ergänzen.]",
     "accessibility.html": "[PLATZHALTER – Erklärung zur Barrierefreiheit nach BFSG: Stand der Vereinbarkeit (WCAG 2.2 AA), bekannte Einschränkungen, Feedback-Kontakt, Schlichtungsstelle.]",
    }
    if f == "faq.html":
        items = "".join(f'<div class="accordion-item"><h2 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq{i}" aria-expanded="false" aria-controls="faq{i}">{q}</button></h2><div id="faq{i}" class="accordion-collapse collapse"><div class="accordion-body">{a}</div></div></div>' for i,(q,a) in enumerate(FAQ))
        inner = f'<div class="accordion" id="faqAcc">{items}</div>'
    elif f == "contact.html":
        inner = f'''<div class="row g-4"><div class="col-lg-6"><h2 class="h4">Schreiben Sie uns</h2>
<form novalidate><div class="mb-3"><label class="form-label" for="contact-name">Name <span class="req" aria-hidden="true">*</span></label><input class="form-control" id="contact-name" name="name" autocomplete="name" required></div>
<div class="mb-3"><label class="form-label" for="contact-mail">E-Mail <span class="req" aria-hidden="true">*</span></label><input class="form-control" type="email" id="contact-mail" name="email" autocomplete="email" required></div>
<div class="mb-3"><label class="form-label" for="contact-msg">Nachricht <span class="req" aria-hidden="true">*</span></label><textarea class="form-control" id="contact-msg" rows="5" required></textarea></div>
<button class="btn btn-primary" type="submit">Nachricht senden</button></form></div>
<div class="col-lg-6" id="opening-hours"><h2 class="h4">Öffnungszeiten &amp; Anfahrt</h2><p>{BRAND["hours"]}</p><p>{BRAND["street"]}, {BRAND["zip"]} {BRAND["city"]}</p><p><a href="tel:{BRAND["phone_raw"]}">{BRAND["phone"]}</a> · <a href="mailto:{BRAND["email"]}">{BRAND["email"]}</a></p><p><a class="btn btn-outline-primary" href="{BRAND["whatsapp_url"]}"><i class="bi bi-whatsapp" aria-hidden="true"></i> WhatsApp-Chat</a></p></div></div>'''
    elif f == "shipping.html":
        inner = f'''<p class="alert alert-info"><i class="bi bi-info-circle" aria-hidden="true"></i> {notes[f]}</p>
<div class="table-responsive"><table class="table table-stack align-middle"><caption class="visually-hidden">Versandkosten nach Zone</caption><thead><tr><th scope="col">Zone</th><th scope="col">Lieferzeit</th><th scope="col">Kosten</th></tr></thead><tbody>
<tr><th scope="row">Deutschland</th><td data-label="Lieferzeit">2–4 Werktage</td><td data-label="Kosten">{BRAND["ship_cost"].replace(".", ",")} € · frei ab {BRAND["free_ship"]} €</td></tr>
<tr><th scope="row">Kühlversand (Aufschlag)</th><td data-label="Lieferzeit">1–2 Werktage</td><td data-label="Kosten">+{BRAND["cool_cost"].replace(".", ",")} €</td></tr>
<tr><th scope="row">[EU-Länder]</th><td data-label="Lieferzeit">[x–y Werktage]</td><td data-label="Kosten">[Preis]</td></tr></tbody></table></div>
<h2 class="h4 mt-4" id="pickup">Click &amp; Collect</h2><p>Bestellen Sie online und holen Sie Ihre Ware in {BRAND["pickup"]} ab. Kühlware bleibt bis zur Abholung gekühlt.</p>'''
    elif f == "imprint.html":
        inner = f'''<p class="alert alert-info"><i class="bi bi-info-circle" aria-hidden="true"></i> {notes[f]}</p>
<h2 class="h4 mt-4" id="ai-images">KI-generierte Bilder</h2>
<p>Ein Teil der Bilder auf dieser Website (Produkt-, Teaser- und Hintergrundbilder) wurde mit Hilfe von künstlicher Intelligenz (KI) erzeugt. Diese Bilder zeigen keine echten Aufnahmen und können vom tatsächlichen Produkt abweichen. Maßgeblich sind die Produktangaben im Text und die Angaben auf der Verpackung.</p>'''
    else:
        inner = f'<p class="alert alert-info"><i class="bi bi-info-circle" aria-hidden="true"></i> {notes.get(f, "[PLATZHALTER]")}</p>'
    return f'<main id="main"><div class="container ai-section">{bc}<h1 class="mb-4">{title}</h1><div class="ai-wide">{inner}</div></div></main>'

def write_seo_files():
    """robots.txt, sitemap.xml und llms.txt (für Suchmaschinen und KI-Assistenten)."""
    import datetime
    b = BRAND["base_url"]; today = datetime.date.today().isoformat()
    pages = [f for f in PAGES if PAGES[f]["robots"] != NOINDEX]
    prio = {"index.html": "1.0", "shop.html": "0.9", "product.html": "0.8", "gifts.html": "0.7", "faq.html": "0.6", "contact.html": "0.6", "shipping.html": "0.6"}
    urls = "".join(f"  <url><loc>{b}/{'' if f == 'index.html' else f}</loc><lastmod>{today}</lastmod><priority>{prio.get(f, '0.3')}</priority></url>\n" for f in pages)
    open(P("sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    ai_bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    robots = "# Automatisch erzeugt von build.py\nUser-agent: *\nAllow: /\nDisallow: /cart.html\nDisallow: /checkout.html\nDisallow: /account.html\nDisallow: /search.html\n\n"
    robots += "# KI-Crawler ausdrücklich erlaubt (GEO) – bei Bedarf auf 'Disallow: /' ändern\n" + "".join(f"User-agent: {a}\nAllow: /\n\n" for a in ai_bots)
    robots += f"Sitemap: {b}/sitemap.xml\n"
    open(P("robots.txt"), "w", encoding="utf-8").write(robots)
    c = lambda k: BRAND[k].replace(".", ",")
    llms = f"""# {BRAND['brand']}

> {BRAND['promise']} Online-Shop für portugiesische und spanische Feinkost mit Sitz in {BRAND['city']}, {BRAND['region_name']}.

## Fakten
- Sortiment: Bacalhau, Olivenöl, Wein, Portwein, Käse, Wurst, Schinken, Konserven, Kaffee, Gebäck, Geschenkkörbe
- Herkunft: Portugal und Spanien (Alentejo, Minho, Douro, La Rioja u. a.)
- Standort und Abholung (Click & Collect): {BRAND['street']}, {BRAND['zip']} {BRAND['city']}, {BRAND['country']}
- Öffnungszeiten: {BRAND['hours']}
- Telefon: {BRAND['phone']} · E-Mail: {BRAND['email']}
- Versand: innerhalb Deutschlands, 2–4 Werktage, {c('ship_cost')} € (frei ab {BRAND['free_ship']} €); Kühlversand +{c('cool_cost')} €
- Zahlung: PayPal, Kreditkarte, Vorkasse, Rechnung
- Sprache: Deutsch

## Wichtige Seiten
- [Startseite]({b}/): Überblick und Bestseller
- [Alle Produkte]({b}/shop.html): Sortiment mit Filtern
- [Geschenkkörbe]({b}/gifts.html)
- [Versand & Click & Collect]({b}/shipping.html)
- [Häufige Fragen]({b}/faq.html)
- [Kontakt & Anfahrt]({b}/contact.html)
"""
    open(P("llms.txt"), "w", encoding="utf-8").write(llms)

if __name__ == "__main__":
    # products.js (gemeinsame Datenquelle für Suche, Quick-View, Warenkorb)
    data = [dict(id=p["id"], name=p["name"], brand=p["brand"], cat=p["cat"], price=p["price"], base=base(p), img=p["img"], desc=p["desc"], cool=p["cool"], stock=p["stock"]) for p in PRODUCTS]
    cfg = dict(cats=CATS, regions=REGIONS)
    open(P("assets","js","products.js"), "w", encoding="utf-8").write("/* AUTOMATISCH ERZEUGT von build.py – nicht von Hand ändern. Im echten Shop: API/JSON des Shopsystems. */\nwindow.AI_PRODUCTS = " + json.dumps(data, ensure_ascii=False) + ";\nwindow.AI_CATS = " + json.dumps(CATS, ensure_ascii=False) + ";\n")
    n = 0
    for f in PAGES:
        src = P("src","pages",f)
        body = open(src, encoding="utf-8").read() if os.path.exists(src) else (static_body(f) if f in STATIC else None)
        if body is None: print("FEHLT:", src); continue
        render(f, body); n += 1
    print(n, "Seiten erzeugt")
    write_seo_files()

"""Erzeugt die Hero-Slider-Bilder (16:9) aus einem Quellordner.
Aufruf: python tools/make_slider.py [Quellordner]
Ausgabe: assets/img/slider/slide-N-{320,480,640,1280}.webp (640x360 = Basisformat).
Reihenfolge = Reihenfolge in SLIDES (PastÃ©is de Nata 'N' im Wechsel mit Landschaft/Deko).
Pro Eintrag: (Dateiname, vertikaler Bildausschnitt 0=oben .. 1=unten)."""
import sys, os
from PIL import Image, ImageOps
SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\suked\Downloads\slider"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img", "slider")
WIDTHS = (320, 480, 640, 1280)
SLIDES = [
    ("pexels-jacqueline-goncalves-2155137161-34334096.jpg", .5),  # N  Pasteis auf Holzbrett
    ("pexels-rainer-rohtla-2157494180-34753108.jpg", .6),         #    Tram 25
    ("pexels-kadernamuslu-39810418.jpg", .75),                    # N  Pastelaria-Vitrine
    ("IMG_20241020_151833.jpg", .5),                              #    Atlantik-Brandung
    ("pexels-receptcelik-7595397.jpg", .5),                       # N  Pasteis mit Zimt
    ("pexels-dominikagregus-34930563.jpg", .5),                   #    Azulejos + Jugendstil-Gitter
    ("pexels-kohankhaki-34079991.jpg", .5),                       #    Denkmal der Entdeckungen
    ("pexels-dario-fernandez-ruz-6836990.jpg", .5),               #    blaue Azulejo-Wand
    ("pexels-cruz-in-portugal-40540041.jpg", .5),                 #    Port/Ginja
    ("pexels-vedat-19842131.jpg", .5),                            #    Azulejo-Haustuer
]
os.makedirs(OUT, exist_ok=True)
for i, (name, cy) in enumerate(SLIDES, 1):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, name))).convert("RGB")
    for w in WIDTHS:
        out = ImageOps.fit(im, (w, round(w * 9 / 16)), Image.LANCZOS, centering=(0.5, cy))
        out.save(os.path.join(OUT, f"slide-{i}-{w}.webp"), "WEBP", quality=80, method=6)
    print(i, name)


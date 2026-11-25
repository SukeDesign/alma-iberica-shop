"""Platzhalter-Bilder (WebP) NUR für Produkte/Teaser ohne echtes Foto. Echte Fotos (3:4, 307x409+) unter gleichem Namen ablegen.
Achtung: Skript überschreibt nur die hier gelisteten Namen, nie die echten Fotos."""
from PIL import Image, ImageDraw, ImageFont
import math, os
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
FONT = None
for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"):
    try: FONT = ImageFont.truetype(f, 54); FONT_S = ImageFont.truetype(f, 30); break
    except Exception: pass
if FONT is None: FONT = FONT_S = ImageFont.load_default()
# name: (farbe1, farbe2, motiv, beschriftung)
ITEMS = {
 "hero": ((127,29,35),(94,177,191),"tile","Alma Ibérica"),
 "wein-rioja": ((110,23,28),(40,20,20),"bottle","Rioja Reserva"),
 "portwein": ((90,30,40),(22,24,29),"bottle","Portwein"),
 "jamon": ((170,60,50),(70,20,20),"circle","Jamón Ibérico"),
 "manchego": ((226,190,110),(150,110,40),"wedge","Manchego"),
 "sardinen": ((94,177,191),(30,70,90),"fish","Sardinen"),
 "kaffee": ((90,60,45),(22,24,29),"circle","Kaffee"),
 "geschenkkorb": ((127,29,35),(214,160,70),"tile","Geschenkkorb"),
 "cafe": ((214,160,70),(94,177,191),"circle","Café"),
 "import": ((94,177,191),(127,29,35),"tile","Import"),
}
BG = (90,101,112)  # #5A6570 – einheitlicher Platzhalter-Hintergrund (kein Verlauf)
def grad(w,h,c1,c2):
    return Image.new("RGB",(w,h),BG)
def make(name, spec, w, h, suffix=""):
    c1,c2,motif,label = spec
    im = grad(w,h,c1,c2); d = ImageDraw.Draw(im, "RGBA")
    cx,cy = w*0.5,h*0.45; s=h*0.28
    if motif=="tile":
        for i in range(-2,3):
            for j in range(-2,3):
                x,y=cx+i*s*1.3,cy+j*s*1.3
                d.polygon([(x,y-s*.6),(x+s*.6,y),(x,y+s*.6),(x-s*.6,y)],outline=(255,255,255,90),width=3)
                d.ellipse([x-s*.2,y-s*.2,x+s*.2,y+s*.2],outline=(255,255,255,90),width=3)
    elif motif=="circle":
        d.ellipse([cx-s,cy-s,cx+s,cy+s],fill=(255,255,255,60),outline=(255,255,255,170),width=5)
        d.ellipse([cx-s*.55,cy-s*.55,cx+s*.55,cy+s*.55],outline=(255,255,255,120),width=4)
    elif motif=="bottle":
        d.rounded_rectangle([cx-s*.38,cy-s*.2,cx+s*.38,cy+s*1.2],radius=26,fill=(255,255,255,70),outline=(255,255,255,180),width=5)
        d.rectangle([cx-s*.14,cy-s*.95,cx+s*.14,cy-s*.2],fill=(255,255,255,70),outline=(255,255,255,180),width=5)
    elif motif=="fish":
        d.ellipse([cx-s*1.2,cy-s*.5,cx+s*.7,cy+s*.5],fill=(255,255,255,70),outline=(255,255,255,180),width=5)
        d.polygon([(cx+s*.6,cy),(cx+s*1.3,cy-s*.5),(cx+s*1.3,cy+s*.5)],fill=(255,255,255,70),outline=(255,255,255,180))
    elif motif=="drop":
        d.ellipse([cx-s*.7,cy-s*.3,cx+s*.7,cy+s*1.1],fill=(255,255,255,70),outline=(255,255,255,180),width=5)
        d.polygon([(cx,cy-s*1.1),(cx-s*.62,cy+s*.2),(cx+s*.62,cy+s*.2)],fill=(255,255,255,70))
    elif motif=="wedge":
        d.polygon([(cx-s*1.1,cy+s*.7),(cx+s*1.1,cy+s*.7),(cx+s*.3,cy-s*.6)],fill=(255,255,255,80),outline=(255,255,255,190))
    f = FONT if h >= 600 else ImageFont.truetype(FONT.path, max(12, int(54*h/600))) if hasattr(FONT, "path") else FONT  # Thumbnails: Schrift mitskalieren
    tw = d.textlength(label,font=f)
    d.text(((w-tw)/2,h*0.82),label,font=f,fill=(255,255,255,235))
    im.save(os.path.join(OUT,f"{name}{suffix}.webp"),"WEBP",lossless=True)
PORTRAIT = {"wein-rioja","portwein","jamon","manchego","sardinen","kaffee"}
for n,spec in ITEMS.items():
    if n=="hero": make(n,spec,1200,900)
    elif n in PORTRAIT:
        make(n,spec,600,800); make(n,spec,180,240,"-s")
    else:
        make(n,spec,800,600); make(n,spec,320,240,"-s")
print(len(os.listdir(OUT)),"Dateien")

"""Mockup a escala de la navbar (desktop en las dos paletas + móvil).

No es una captura del navegador: reproduce las medidas del CSS con PIL.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1320, 580
FONT_DIR = r"C:\Windows\Fonts"

FUENTES = {
    "word": ["segoeuib.ttf", "arialbd.ttf"],
    "semibold": ["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"],
    "regular": ["segoeui.ttf", "arial.ttf"],
    "mono": ["consola.ttf", "cour.ttf"],
}


def f(clave, size):
    for cand in FUENTES[clave]:
        p = os.path.join(FONT_DIR, cand)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_WORD = f("word", 24)
F_BASIC = f("regular", 12)
F_WORD_M = f("word", 17)
F_NAV = f("semibold", 13)
F_BTN = f("word", 13)
F_MENU = f("semibold", 12)
F_LABEL = f("mono", 11)
F_NOTE = f("regular", 12)

PAL = {
    "A": {"sup": "#FFFFFF", "texto": "#1C1512", "suave": "#6E625B", "borde": "#EBDCD1",
          "vivo": "#E2703A", "accion": "#B8452C", "wa": "#17784B", "rojo": "#B0232B"},
    "B": {"sup": "#FFFFFF", "texto": "#111A2B", "suave": "#5C6678", "borde": "#DCE6F5",
          "vivo": "#3D7BF0", "accion": "#1E56D6", "wa": "#17784B", "rojo": "#B0232B"},
}

img = Image.new("RGB", (W, H), "#EDEDED")
d = ImageDraw.Draw(img)


def tracked(xy, texto, font, fill, track):
    x, y = xy
    for ch in texto:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x


def tl(texto, font, track):
    return sum(d.textlength(c, font=font) + track for c in texto) - track


def lockup(x, cy, p, chico=False):
    fw = F_WORD_M if chico else F_WORD
    # versión chica: sin "basic" (el CSS lo oculta bajo 400 px)
    tracked((x, cy - fw.size * 0.62), "AMERICAN JEANS", fw, p["texto"], 0.35)
    fin = x + tl("AMERICAN JEANS", fw, 0.35)
    if chico:
        return fin
    x2 = fin + 13
    d.rectangle([x2, cy - 16, x2 + 2, cy + 16], fill=p["rojo"])
    x3 = x2 + 13
    tracked((x3, cy - 6), "basic", F_BASIC, p["rojo"], 3.4)
    return x3 + tl("basic", F_BASIC, 3.4)


def navbar(x0, y0, ancho, p, movil=False):
    alto = 76
    d.rectangle([x0, y0, x0 + ancho, y0 + alto], fill=p["sup"], outline=p["borde"])
    cy = y0 + alto // 2
    pad = 20 if movil else 44

    fin = lockup(x0 + pad, cy, p, chico=movil)

    if movil:
        bx = x0 + ancho - pad - 96
        d.rounded_rectangle([bx, cy - 22, bx + 96, cy + 22], radius=6, outline=p["borde"], width=1)
        tracked((bx + 14, cy - 7), "MENÚ", F_MENU, p["texto"], 1.3)
        d.polygon([(bx + 72, cy - 2), (bx + 82, cy - 2), (bx + 77, cy + 4)], fill=p["vivo"])
    else:
        items = ["LOOKS", "AJ BASIC", "CÓMO COMPRAR", "TALLES", "PREGUNTAS"]
        nx = fin + 56
        for i, it in enumerate(items):
            tracked((nx, cy - 7), it, F_NAV, p["texto"] if i == 0 else p["suave"], 1.15)
            if i == 0:  # subrayado que se dibuja al pasar el mouse
                d.rectangle([nx, cy + 12, nx + tl(it, F_NAV, 1.15), cy + 14], fill=p["vivo"])
            nx += tl(it, F_NAV, 1.15) + 32
        bw = 118
        bx = x0 + ancho - pad - bw
        d.rounded_rectangle([bx, cy - 21, bx + bw, cy + 21], radius=6, fill=p["wa"])
        d.text((bx + 19, cy - 8), "WhatsApp", font=F_BTN, fill="#FFFFFF")


d.text((24, 18), "NAVBAR NUEVA · lockup tipográfico y menú con más presencia", font=f("word", 21), fill="#111111")
d.text((24, 44), "Reproducción a escala de las medidas del CSS (no es una captura del navegador)",
       font=F_NOTE, fill="#888888")

y1 = 96
d.text((24, y1 - 20), "DESKTOP 1280 · PALETA A", font=F_LABEL, fill="#777777")
navbar(24, y1, 1272, PAL["A"])

y2 = y1 + 76 + 54
d.text((24, y2 - 20), "DESKTOP 1280 · PALETA B", font=F_LABEL, fill="#777777")
navbar(24, y2, 1272, PAL["B"])

y3 = y2 + 76 + 58
d.text((24, y3 - 20), "MOBILE 390 · la marca se achica y aparece el menú", font=F_LABEL, fill="#777777")
d.rounded_rectangle([16, y3 - 10, 24 + 390 + 8, y3 + 76 + 10], radius=12, fill="#E4E4E4", outline="#CFCFCF")
navbar(24, y3, 390, PAL["A"], movil=True)

notas = [
    "Marca: AMERICAN JEANS en 24 px / 800 (antes 15 px) · divisoria roja de 2 px · basic en 12 px con tracking .3em",
    "Menú: mayúsculas de 13 px / 600 con tracking .09em y subrayado naranja que se dibuja en hover",
    "Móvil: nombre a 17 px, 'basic' oculto bajo 400 px y botón Menú desplegable sin JavaScript",
]
ny = H - 74
for n in notas:
    d.text((24, ny), "· " + n, font=F_NOTE, fill="#555555")
    ny += 21

out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paletas", "navbar.png"))
img.save(out, "PNG")
print("ok", out, img.size)

"""Mockup a escala del hero con el sello (escritorio y móvil). No es captura del navegador."""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1320, 1160
FONT_DIR = r"C:\Windows\Fonts"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing"))

FUENTES = {"bold": ["segoeuib.ttf", "arialbd.ttf"], "regular": ["segoeui.ttf", "arial.ttf"],
           "mono": ["consola.ttf", "cour.ttf"]}


def f(clave, size):
    for cand in FUENTES[clave]:
        p = os.path.join(FONT_DIR, cand)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


PAL = {"fondo": "#FDF6F1", "tinte2": "#E9F0F7", "texto": "#1C1512", "suave": "#6E625B",
       "accion": "#B8452C", "wa": "#17784B"}

sello = Image.open(os.path.join(BASE, "img", "logo-sello-480.png")).convert("RGBA")

img = Image.new("RGB", (W, H), "#EDEDED")
d = ImageDraw.Draw(img)

d.text((24, 18), "HERO CON SELLO · ubicación y tamaño a escala", font=f("bold", 21), fill="#111111")
d.text((24, 44), "Escritorio: sello de 240 px en la columna derecha. Móvil: 140 px arriba del titular.",
       font=f("regular", 12), fill="#888888")


def hero(x0, y0, ancho, alto, escritorio=True):
    # fondo del hero: degradado suave tinte → tinte2
    for i in range(alto):
        t = i / alto
        c = tuple(round(int(PAL["fondo"][j:j + 2], 16) * (1 - t) + int(PAL["tinte2"][j:j + 2], 16) * t)
                  for j in (1, 3, 5))
        d.line([(x0, y0 + i), (x0 + ancho, y0 + i)], fill=c)

    if escritorio:
        cw = 1120
        cx = x0 + (ancho - cw) // 2
        py = y0 + 80
        d.text((cx, py), "INDUMENTARIA MASCULINA · BUENOS AIRES", font=f("regular", 13), fill=PAL["accion"])
        fh1 = f("bold", 54)
        for i, linea in enumerate(["Camisas, jeans y básicos", "para el hombre que no", "tiene tiempo de pensarlo."]):
            d.text((cx, py + 34 + i * 58), linea, font=fh1, fill=PAL["texto"])
        fsub = f("regular", 19)
        d.text((cx, py + 220), "Cuatro locales que ya conocés, ahora también online.", font=fsub, fill=PAL["suave"])
        d.text((cx, py + 246), "Retiro en 2 horas y cambios gratis en las cuatro.", font=fsub, fill=PAL["suave"])
        d.rounded_rectangle([cx, py + 300, cx + 214, py + 348], radius=6, fill=PAL["accion"])
        d.text((cx + 22, py + 313), "Escribinos por WhatsApp", font=f("bold", 15), fill="#FFFFFF")
        d.rounded_rectangle([cx + 230, py + 300, cx + 366, py + 348], radius=6, outline=PAL["texto"], width=2)
        d.text((cx + 252, py + 313), "Cómo comprar", font=f("bold", 15), fill=PAL["texto"])
        d.text((cx, py + 372), "Lunes a sábado, de 9 a 19.", font=f("regular", 14), fill=PAL["suave"])

        # sello 240 px, alineado a la derecha del contenedor y centrado verticalmente
        s = sello.resize((240, round(240 * sello.height / sello.width)), Image.LANCZOS)
        sy = y0 + (alto - s.height) // 2
        img.paste(s, (cx + cw - 240, sy), s)
    else:
        px = x0 + 20
        py = y0 + 24
        # sello 140 px arriba del titular
        s = sello.resize((140, round(140 * sello.height / sello.width)), Image.LANCZOS)
        img.paste(s, (px, py), s)
        py += s.height + 22
        d.text((px, py), "INDUMENTARIA MASCULINA", font=f("regular", 10), fill=PAL["accion"])
        fh1 = f("bold", 30)
        for i, linea in enumerate(["Camisas, jeans y", "básicos para el hombre", "que no tiene tiempo."]):
            d.text((px, py + 22 + i * 34), linea, font=fh1, fill=PAL["texto"])
        py2 = py + 22 + 3 * 34 + 16
        d.text((px, py2), "Cuatro locales que ya conocés.", font=f("regular", 14), fill=PAL["suave"])
        d.text((px, py2 + 20), "Retiro en 2 horas.", font=f("regular", 14), fill=PAL["suave"])
        d.rounded_rectangle([px, py2 + 52, px + 210, py2 + 96], radius=6, fill=PAL["accion"])
        d.text((px + 20, py2 + 64), "Escribinos por WhatsApp", font=f("bold", 13), fill="#FFFFFF")


# escritorio 1280 de ancho
hero(24, 78, 1272, 490, True)
d.text((24, 78 + 490 + 14), "ESCRITORIO 1280 · contenedor 1120 · sello 240 px (relación 1.81)", font=f("mono", 11), fill="#777777")

# móvil 390 de ancho
y_m = 78 + 490 + 66
d.rounded_rectangle([24, y_m - 8, 24 + 390, y_m + 424], radius=14, fill="#FFFFFF", outline="#CFCFCF")
hero(24, y_m, 390, 424, False)
d.text((440, y_m + 8), "MÓVIL 390 · sello 140 px sobre el titular,", font=f("mono", 11), fill="#777777")
d.text((440, y_m + 24), "que es la posición 'entre navbar y encabezado'", font=f("mono", 11), fill="#777777")
d.text((440, y_m + 40), "El sello hace 140 px = 36% del ancho útil.", font=f("mono", 11), fill="#777777")

notas = [
    "Por qué el sello no va en la navbar: a 44 px, 'American Jeans' quedaría en 9 px e ilegible. Ahí manda el lockup tipográfico.",
    "El sello ocupa el aire que la captura mostraba a la derecha del titular, sin competir con el botón de WhatsApp.",
    "Mismo marcado para los dos tamaños: una sola imagen con srcset, sin duplicar HTML.",
]
ny = H - 70
for n in notas:
    d.text((24, ny), "· " + n, font=f("regular", 12), fill="#555555")
    ny += 20

out = os.path.join(BASE, "..", "paletas", "hero-sello.png")
img.save(os.path.normpath(out), "PNG")
print("ok", os.path.normpath(out), img.size)

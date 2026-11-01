"""Mockup a escala de la sección "Abrigo y talles especiales" (1120 px de contenedor)."""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONTS = r"C:\Windows\Fonts"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

PAL = {
    "fondo": "#E9F0F7", "sup": "#FFFFFF", "texto": "#1C1512", "suave": "#6E625B",
    "borde": "#EBDCD1", "accion": "#B8452C", "vivo": "#E2703A", "acento": "#F2B37A",
    "tinte": "#FBEFE6",
}


def f(nombre, size):
    p = os.path.join(FONTS, nombre)
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()


F_TIT = f("segoeuib.ttf", 34)
F_SUB = f("segoeui.ttf", 16)
F_H = f("segoeuib.ttf", 22)
F_HG = f("segoeuib.ttf", 27)
F_D = f("segoeui.ttf", 15)
F_L = f("segoeuib.ttf", 14)
F_B = f("segoeuib.ttf", 11)

W = 1200
CONT = 1120
X0 = (W - CONT) // 2
CARD_W = (CONT - 2 * 24) // 3
ALTO = 500

img = Image.new("RGB", (W, ALTO), PAL["fondo"])
d = ImageDraw.Draw(img)

d.text((X0, 40), "Abrigo y talles especiales", font=F_TIT, fill=PAL["texto"])
sub = "Lo que no entra en un look de tres prendas. Son pocas categorías, pero son las que resuelven el invierno y las que casi nadie tiene en stock."
y = 92
for linea in textwrap.wrap(sub, width=95):
    d.text((X0, y), linea, font=F_SUB, fill=PAL["suave"])
    y += 22

y0 = y + 26
tarjetas = [
    ("Camperas", "Jean, inflable y rompeviento. Abrigo real para el invierno de Buenos Aires.", "Ver camperas", False, None),
    ("Pulóveres", "Cuello redondo y chaleco tejido, en hilo sintético que no pica y no encoge.", "Ver pulóveres", False, None),
    ("Hasta el 12",
     "La curva depende de la prenda: hay artículos del 1 al 10 o 12 y otros que arrancan en el 6. Consultanos y te decimos qué hay hoy, sin pedido especial ni espera.",
     "Consultar mi talle", True, "TALLES ESPECIALES"),
]

for i, (titulo, desc, link, destacada, badge) in enumerate(tarjetas):
    x = X0 + i * (CARD_W + 24)
    fondo = PAL["tinte"] if destacada else PAL["sup"]
    borde = PAL["acento"] if destacada else PAL["borde"]
    d.rounded_rectangle([x, y0, x + CARD_W, y0 + 300], radius=12, fill=fondo, outline=borde, width=2)

    ty = y0 + 24
    if badge:
        tw = d.textlength(badge, font=F_B)
        d.rounded_rectangle([x + 24, ty, x + 24 + tw + 24, ty + 24], radius=12, fill=PAL["acento"])
        d.text((x + 36, ty + 6), badge, font=F_B, fill=PAL["texto"])
        ty += 38

    d.text((x + 24, ty), titulo, font=F_HG if destacada else F_H, fill=PAL["texto"])
    ty += 44 if destacada else 38

    for linea in textwrap.wrap(desc, width=38 if not destacada else 34):
        d.text((x + 24, ty), linea, font=F_D, fill=PAL["suave"])
        ty += 22

    d.text((x + 24, y0 + 264), link + "  →", font=F_L, fill=PAL["accion"])

salida = os.path.join(BASE, "paletas", "seccion-abrigo.png")
img.save(salida, "PNG")
print("ok", salida, img.size)

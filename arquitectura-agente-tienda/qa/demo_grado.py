"""Demostración del grado de color de la casa sobre dos tipos de imagen distintos."""

import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grado_casa import grado, recortar  # noqa: E402

AI = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\39\39e3ee7ddca3209ffbac0ce4365f437d3a70e86016da104cb6da9bbc04e111a0"
REAL = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\3b\3b726fd60d97ee313436dfc12de45b6812a716e73d282c125df4d21d5eae775b"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONTS = r"C:\Windows\Fonts"

W_CARD, H_CARD = 340, 425


def fuente(nombre, size):
    p = os.path.join(FONTS, nombre)
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()


F_TIT = fuente("segoeuib.ttf", 19)
F_LBL = fuente("segoeuib.ttf", 12)
F_MIN = fuente("segoeui.ttf", 11)
F_NOTA = fuente("segoeui.ttf", 12.5)

img = Image.new("RGB", (1560, 800), "#EDEDED")
d = ImageDraw.Draw(img)
d.text((24, 16), "MISMO GRADO DE COLOR · DOS USOS DISTINTOS", font=F_TIT, fill="#111")

ai = Image.open(AI).convert("RGB")
real = Image.open(REAL).convert("RGB")

# panel 1 y 2: la foto editada, antes y después del grado
ai_card = recortar(ai, 4 / 5).resize((W_CARD, H_CARD), Image.LANCZOS)
ai_grado = grado(ai_card.copy())

# panel 3: banda documental de la vidriera real, con el mismo grado
banda = recortar(real, 16 / 9)
banda = grado(banda)
banda = banda.resize((W_CARD, round(W_CARD * 9 / 16)), Image.LANCZOS)

paneles = [
    (24, ai_card, "1 · EDITADA, sin grado", "aspecto de banco de imágenes"),
    (404, ai_grado, "2 · EDITADA, con grado", "menos render, misma foto"),
]

for x, im, titulo, sub in paneles:
    d.text((x, 58), titulo, font=F_LBL, fill="#111")
    img.paste(im, (x, 84))
    d.rectangle([x, 84, x + W_CARD, 84 + H_CARD], outline="#C9C6C1")
    d.text((x, 84 + H_CARD + 10), sub, font=F_MIN, fill="#5A5A5A")

# panel 3: banda real, centrada en la misma caja
x3 = 784
d.text((x3, 58), "3 · REAL (tu vidriera), con grado", font=F_LBL, fill="#111")
alto_b = banda.height
img.paste(banda, (x3, 84 + (H_CARD - alto_b) // 2))
d.rectangle([x3, 84 + (H_CARD - alto_b) // 2, x3 + W_CARD, 84 + (H_CARD - alto_b) // 2 + alto_b], outline="#C9C6C1")
d.text((x3, 84 + H_CARD + 10), "sirve para 'En el local', no para ficha", font=F_MIN, fill="#5A5A5A")

# panel 4: explicación del límite
x4 = x3 + W_CARD + 40
d.text((x4, 58), "4 · QUÉ NO ARREGLA EL COLOR", font=F_LBL, fill="#111")
limites = [
    "Reflejos del vidrio sobre la prenda.",
    "Etiquetas de precio y carteles de Mercado Pago.",
    "Marcas de otras prendas en el mismo plano.",
    "Maniquí con luz plana y sin postura.",
]
y = 84
for item in limites:
    d.ellipse([x4, y + 5, x4 + 5, y + 10], fill="#B0232B")
    d.text((x4 + 14, y), item, font=F_NOTA, fill="#333")
    y += 24
d.text((x4, y + 12), "Eso se arregla al disparar, no en edición.", font=F_MIN, fill="#777")

notas = [
    "El grado —balance de blancos, curva suave, grano fino y viñeta— se aplica igual a cualquier foto. "
    "La consistencia es lo que hace que diez fotos distintas parezcan una sola producción.",
    "La vidriera real no es una foto de catálogo, pero es la prueba de que el local existe: un plano de tres "
    "maniquíes vestidos vale más que diez imágenes de banco para el cliente que duda.",
]
y = 600
for n in notas:
    for linea in textwrap.wrap(n, width=118):
        d.text((24, y), linea, font=F_NOTA, fill="#333")
        y += 18
    y += 10

salida = os.path.join(BASE, "paletas", "grado-comparacion.png")
img.save(salida, "PNG")
print("ok", salida, img.size)

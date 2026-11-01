"""Comparación de las dos tarjetas con foto, al tamaño real (340×425)."""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))
FONTS = r"C:\Windows\Fonts"


def fuente(nombre, size):
    p = os.path.join(FONTS, nombre)
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()


F_TIT = fuente("segoeuib.ttf", 18)
F_LBL = fuente("segoeuib.ttf", 12)
F_MIN = fuente("segoeui.ttf", 11)

W, H = 340, 425
img = Image.new("RGB", (2 * W + 120, H + 130), "#FDF6F1")
d = ImageDraw.Draw(img)

d.text((24, 16), "LAS DOS TARJETAS CON FOTO · dos escenas, dos usos", font=F_TIT, fill="#1C1512")

for i, (archivo, titulo, nota) in enumerate([
    ("look-trabajo-360.jpg", "Para trabajar", "oficina, luz fría, cuerpo completo"),
    ("look-noche-360.jpg", "Para la noche", "café, luz cálida, tres cuartos"),
]):
    x = 24 + i * (W + 60)
    im = Image.open(os.path.join(BASE, archivo)).convert("RGB").resize((W, H), Image.LANCZOS)
    img.paste(im, (x, 58))
    d.rectangle([x, 58, x + W, 58 + H], outline="#EBDCD1")
    d.text((x, 58 + H + 10), titulo, font=F_LBL, fill="#1C1512")
    d.text((x, 58 + H + 28), nota, font=F_MIN, fill="#6E625B")

salida = os.path.join(BASE, "..", "..", "paletas", "tarjetas-doble.png")
img.save(os.path.normpath(salida), "PNG")
print("ok", os.path.normpath(salida))

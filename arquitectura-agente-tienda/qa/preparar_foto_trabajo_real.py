"""Corrige el entorno de la selfie frente al espejo para usarla como foto de look.

Lo que hace: recorta las bandas negras, encuadra 4:5 sobre el modelo y apaga el fondo
con una caída de luz elíptica (oscurece, desatura y desenfoca fuera del sujeto), de modo
que el marco de madera, el TV y el colchón azul se pierden en la sombra en lugar de
competir con la ropa. Después aplica el grado de color de la casa.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grado_casa import balance_blancos, calidez, curva_suave, grano  # noqa: E402

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\0e\0e94b7536873fc3dac931b9b0ffdd8abd644bed1b72be8ca6394a007468aa964"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))

im = Image.open(SRC).convert("RGB")

# 1) fuera las bandas negras del mensaje
arr = np.asarray(im).astype(int)
filas = np.where(arr.max(axis=(1, 2)) > 25)[0]
im = im.crop((0, filas.min(), im.width, filas.max() + 1))
print("sin bandas:", im.size)

# 2) encuadre 4:5 sobre el modelo (dentro del espejo, sin el marco de madera)
CX0, CY0, CX1, CY1 = 92, 175, 517, 706      # 540 x 675
im = im.crop((CX0, CY0, CX1, CY1))
print("encuadre 4:5:", im.size)

ancho, alto = im.size

# 3) caída de luz: luz puntual sobre el sujeto, el fondo se apaga
yy, xx = np.mgrid[0:alto, 0:ancho]
cx, cy = ancho * 0.50, alto * 0.46
r = np.sqrt(((xx - cx) / (ancho * 0.46)) ** 2 + ((yy - cy) / (alto * 0.58)) ** 2)

# 1 en el centro del sujeto, 0 en el borde del cuadro
luz = np.clip(1.20 - (r ** 2) * 1.6, 0, 1)
luz = np.clip((luz - 0.08) / 0.92, 0, 1) ** 0.85
mascara = Image.fromarray((luz * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(ancho * 0.035))

# fondo: desenfocado, desaturado y a un quinto de luz
fondo = im.filter(ImageFilter.GaussianBlur(18))
gris = fondo.convert("L").convert("RGB")
fondo = Image.blend(fondo, gris, 0.7)
fondo = Image.eval(fondo, lambda v: int(v * 0.20))

resultado = Image.composite(im, fondo, mascara)

# 4) grado de color de la casa
resultado = balance_blancos(resultado)
resultado = curva_suave(resultado)
resultado = calidez(resultado, r=1.01, b=0.99)
resultado = grano(resultado, 2.4)

# viñeta suave extra para cerrar el cuadro
y, x = np.ogrid[:alto, :ancho]
d = np.sqrt(((x - ancho / 2) / (ancho / 2)) ** 2 + ((y - alto / 2) / (alto / 2)) ** 2) / np.sqrt(2)
vineta = 1 - 0.28 * np.clip(d, 0, 1) ** 2
resultado = Image.fromarray(
    np.clip(np.asarray(resultado).astype(np.float32) * vineta[..., None], 0, 255).astype(np.uint8)
)

# 5) derivados
for w in (720, 360):
    h = round(w * 5 / 4)
    ruta = os.path.join(BASE, f"look-trabajo-{w}.jpg")
    resultado.resize((w, h), Image.LANCZOS).save(
        ruta, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"look-trabajo-{w}.jpg  {os.path.getsize(ruta) / 1024:.1f} KB")

resultado.resize((340, 425), Image.LANCZOS).save(os.path.join(BASE, "_check-trabajo.jpg"), quality=88)
resultado.resize((720, 900), Image.LANCZOS).save(os.path.join(BASE, "_debug-trabajo.jpg"), quality=88)
print("control: landing/img/_check-trabajo.jpg")

"""Quita el logo de una marca ajena de la remera del padre (look de fin de semana).

Técnica: en lugar de clonar un bloque (que deja borde visible), se reconstruye la franja
interpolando verticalmente cada columna entre la tela de arriba y la de abajo. La tela
tiene nervaduras verticales, así que el resultado respeta la textura y el sombreado del
pecho sin costuras.
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\04\04a73f1671fcb86ba06b7ab4a720cc5e8800f14d713e37e9c5231b7e5e75f74a"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))

im = Image.open(SRC).convert("RGB")
arr = np.asarray(im).astype(np.float32)

# franja del logo, con margen
PX0, PY0, PX1, PY1 = 554, 392, 666, 431
ancho, alto = PX1 - PX0, PY1 - PY0

arriba = arr[PY0 - 3, PX0:PX1].copy()     # tela limpia arriba
abajo = arr[PY1 + 3, PX0:PX1].copy()      # tela limpia abajo

relleno = np.zeros((alto, ancho, 3), dtype=np.float32)
for i in range(alto):
    t = (i + 1) / (alto + 1)
    relleno[i] = arriba * (1 - t) + abajo * t

# grano para que la zona no quede más lisa que el resto
rng = np.random.default_rng(5)
relleno += rng.normal(0, 1.5, relleno.shape)

# se compone con máscara difuminada
parche = Image.fromarray(np.clip(relleno, 0, 255).astype(np.uint8))
mask = Image.new("L", (ancho, alto), 0)
ImageDraw.Draw(mask).rectangle((2, 1, ancho - 3, alto - 2), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(4))

resultado = im.copy()
resultado.paste(parche, (PX0, PY0), mask)

# micro-corrección de tono: comparar medias de la franja parcheada y su contexto
z = np.asarray(resultado.crop((PX0, PY0, PX1, PY1))).astype(np.float32)
ctx = np.concatenate([
    np.asarray(resultado.crop((PX0 - 30, PY0, PX0 - 10, PY1))).astype(np.float32).reshape(-1, 3),
    np.asarray(resultado.crop((PX1 + 10, PY0, PX1 + 30, PY1))).astype(np.float32).reshape(-1, 3),
]).mean(axis=0)
corr = np.clip(z + (ctx - z.reshape(-1, 3).mean(axis=0)), 0, 255)
resultado.paste(Image.fromarray(corr.astype(np.uint8)), (PX0, PY0), mask)

resultado.crop((480, 300, 720, 440)).resize((960, 560), Image.LANCZOS).save(
    os.path.join(BASE, "_debug-logo-despues.png"))

# derivados 4:5
alto_nuevo = int(im.width / (4 / 5))
recorte = resultado.crop((0, 0, im.width, alto_nuevo))
for ancho_salida in (720, 360):
    alto_salida = round(ancho_salida * 5 / 4)
    ruta = os.path.join(BASE, f"look-finde-{ancho_salida}.jpg")
    recorte.resize((ancho_salida, alto_salida), Image.LANCZOS).save(
        ruta, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"look-finde-{ancho_salida}.jpg  {os.path.getsize(ruta) / 1024:.1f} KB")

recorte.resize((340, 425), Image.LANCZOS).save(os.path.join(BASE, "_check-finde.jpg"), quality=86)
print("control:", os.path.join(BASE, "_debug-logo-despues.png"))

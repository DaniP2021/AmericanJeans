"""Prepara la foto de pantalones cargo: endereza, recorta al lienzo verde y deja la imagen
lista para que fotocatalogo la procese."""

import os
import sys

import numpy as np
from PIL import Image

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\f5\f544d9766561bf32603655ac0867a698e74d2d929606a53ec76b3dd13813d973"
SALIDA = r"CATALOGO\cargo\entrada"
os.makedirs(SALIDA, exist_ok=True)

im = Image.open(SRC).convert("RGB")
print("original:", im.size)

# 1) enderezar: la prenda va con la cintura arriba, así que se gira 90° antihorario
im = im.transpose(Image.ROTATE_90)
print("girada:", im.size)

# 2) recortar al lienzo verde: se detectan los píxeles verdes y se toma su caja
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
verde = (g > 110) & (g - r > 25) & (g - b > 35)

print("cobertura verde:", round(verde.mean()*100,1), "%")
filas = np.where(verde.sum(axis=1) > im.width * 0.15)[0]
cols = np.where(verde.sum(axis=0) > im.height * 0.15)[0]
if len(filas) and len(cols):
    caja = (cols.min(), filas.min(), cols.max(), filas.max())
    print("lienzo verde:", caja)
    im = im.crop(caja)

# 3) margen chico para no cortar prendas que tocan el borde del lienzo
m = int(min(im.size) * 0.02)
im = im.crop((m, m, im.width - m, im.height - m))
print("recortada:", im.size)

salida = os.path.join(SALIDA, "cargo-grupo.jpg")
im.save(salida, "JPEG", quality=92, optimize=True)
print("guardada:", salida)

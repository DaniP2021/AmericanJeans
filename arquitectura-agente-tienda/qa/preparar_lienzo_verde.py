"""Recorta una foto de prendas al lienzo verde y opcionalmente la gira.

Uso: python qa/preparar_lienzo_verde.py <foto> <nombre> [grados] [carpeta-salida]

grados: 0 (defecto) | 90 | 180 | 270, en sentido antihorario.
"""

import os
import sys

import numpy as np
from PIL import Image

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

origen = sys.argv[1]
nombre = sys.argv[2]
grados = int(sys.argv[3]) if len(sys.argv) > 3 else 0
salida = sys.argv[4] if len(sys.argv) > 4 else r"CATALOGO\otros\entrada"
os.makedirs(salida, exist_ok=True)

im = Image.open(origen).convert("RGB")
print("original:", im.size)

if grados:
    im = im.rotate(grados, expand=True)
    print(f"girada {grados}°:", im.size)

a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
verde = (g > 110) & (g - r > 25) & (g - b > 35)
print("cobertura verde:", round(float(verde.mean()) * 100, 1), "%")

filas = np.where(verde.sum(axis=1) > im.width * 0.15)[0]
cols = np.where(verde.sum(axis=0) > im.height * 0.15)[0]
if len(filas) and len(cols):
    caja = (int(cols.min()), int(filas.min()), int(cols.max()), int(filas.max()))
    print("lienzo:", caja)
    im = im.crop(caja)
else:
    print("no se detectó el lienzo: se usa la foto completa")

m = int(min(im.size) * 0.02)
im = im.crop((m, m, im.width - m, im.height - m))
print("resultado:", im.size)

destino = os.path.join(salida, f"{nombre}.jpg")
im.save(destino, "JPEG", quality=92, optimize=True)
print("guardada:", destino)

"""Recorta las hojas de eucalipto de la foto de referencia y las guarda con transparencia.

El fondo del ejemplo es un beige muy claro; las hojas son bastante más oscuras. Alcanza con
usar la luminancia como máscara, con una rampa suave para que el borde no quede duro.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\01\017e678b67c6508804c671e7933aff9a209b57ec11abde983b34e9a007b3cafb"
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "CATALOGO", "decor")

REGIONES = [
    ("hojas-arriba.png", (0, 0, 352, 198), (95, 175)),
    ("hojas-abajo.png", (742, 1390, 899, 1600), (95, 175)),
    ("piedra.png", (0, 1190, 150, 1380), (120, 190)),
]


def main():
    os.makedirs(os.path.abspath(SALIDA), exist_ok=True)
    im = Image.open(SRC).convert("RGB")
    for nombre, caja, (bajo, alto) in REGIONES:
        trozo = im.crop(caja)
        a = np.asarray(trozo).astype(np.float32)
        lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
        alfa = np.clip((alto - lum) / (alto - bajo), 0, 1)
        alfa = Image.fromarray((alfa * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
        rgba = np.dstack([a.astype(np.uint8), np.asarray(alfa)])
        destino = os.path.join(os.path.abspath(SALIDA), nombre)
        Image.fromarray(rgba, "RGBA").save(destino)
        print(f"{nombre}: {trozo.size} · {os.path.getsize(destino) / 1024:.0f} KB")


if __name__ == "__main__":
    main()

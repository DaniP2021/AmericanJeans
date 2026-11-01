"""Exporta las prendas del catálogo con transparencia (WebP).

Con la prenda recortada y sin fondo, el fondo de la página pasa a ser CSS: se cambia el
color y todas las fichas cambian con él, sin volver a procesar una sola foto.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, ".pylibs"))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas"))

import numpy as np  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

from fotocatalogo import recortar_sujeto  # noqa: E402

SEL = os.path.join(RAIZ, "CATALOGO", "seleccion")
SALIDA = os.path.join(RAIZ, "CATALOGO", "seleccion-transparente")


def recortar(ruta):
    prenda, _f, _b = recortar_sujeto(Image.open(ruta).convert("RGB"), piezas=0.08)
    if prenda is None:
        return None
    alfa = prenda.split()[3].filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.6))
    a = np.asarray(alfa).astype(np.uint8).copy()
    a[a < 26] = 0
    prenda.putalpha(Image.fromarray(a))
    return prenda


def main():
    os.makedirs(SALIDA, exist_ok=True)
    archivos = sorted(f for f in os.listdir(SEL) if f.endswith("-1200.jpg"))
    for archivo in archivos:
        base = archivo.replace("-1200.jpg", "")
        destino = os.path.join(SALIDA, base + "-1200.webp")
        if os.path.exists(destino) and os.path.getmtime(destino) > os.path.getmtime(os.path.join(SEL, archivo)):
            print("ya está:", base)
            continue
        prenda = recortar(os.path.join(SEL, archivo))
        if prenda is None:
            print("sin prenda:", base)
            continue
        prenda.save(destino, "WEBP", quality=88, method=6)
        prenda.resize((720, round(720 * prenda.height / prenda.width)), Image.LANCZOS).save(
            destino.replace("-1200", "-720"), "WEBP", quality=86, method=6)
        kb = os.path.getsize(destino) / 1024
        print(f"ok {base + '-1200.webp'}  {kb:.0f} KB  {prenda.size}")


if __name__ == "__main__":
    main()

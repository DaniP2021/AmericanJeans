"""Genera variantes de las fotos del catálogo sobre el fondo de la marca.

Toma las fotos ya procesadas (blanco), vuelve a recortar la prenda y la apoya sobre el
fondo lino de la paleta A. Sirve para comparar: blanco puro contra fondo cálido.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, ".pylibs"))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas"))

import numpy as np  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

from fondos import apoyo, sombra_de  # noqa: E402
from fotocatalogo import recortar_sujeto  # noqa: E402

SEL = os.path.join(RAIZ, "CATALOGO", "seleccion")
SALIDA = os.path.join(RAIZ, "CATALOGO", "variantes-lino")

ELEGIDAS = [
    "camisa-estampada-manga-larga-seis-colores-1200.jpg",
    "jean-clasico-tres-lavados-1200.jpg",
    "gabardina-corte-chino-beige-1200.jpg",
    "conjunto-deportivo-wafle-negro-1200.jpg",
    "pantalon-cargo-de-microfibra-cuatro-colores-1200.jpg",
    "chomba-rayada-cuatro-colores-1200.jpg",
    "bermuda-elastizada-corte-jean-negro-y-azul-1200.jpg",
]

MARGEN = 0.07


def main():
    os.makedirs(SALIDA, exist_ok=True)
    for archivo in ELEGIDAS:
        ruta = os.path.join(SEL, archivo)
        if not os.path.exists(ruta):
            print("falta:", archivo)
            continue

        im = Image.open(ruta).convert("RGB")
        prenda, _fraccion, _borde = recortar_sujeto(im, piezas=0.08)
        if prenda is None:
            print("sin prenda:", archivo)
            continue

        # comer 1,5 px de alfa: el JPG venía sobre blanco y deja un filo claro
        alfa = prenda.split()[3].filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.6))
        # el alfa que queda casi en cero se lleva a cero: si no, deja un recuadro tenue
        a = np.asarray(alfa).astype(np.uint8)
        a[a < 26] = 0
        prenda.putalpha(Image.fromarray(a))

        w, h = prenda.size
        util = 1 - 2 * MARGEN
        lienzo_w = max(int(w / util), int(h * 0.8 / util))
        lienzo_h = int(lienzo_w / 0.8)
        if lienzo_h * util < h:
            lienzo_h = int(h / util)
            lienzo_w = int(lienzo_h * 0.8)

        fondo = apoyo(lienzo_w, lienzo_h, semilla=hash(archivo) % 50)
        px = (lienzo_w - w) // 2
        py = int((lienzo_h - h) / 2 + lienzo_h * 0.01)

        sombra, mg = sombra_de(prenda)
        fondo.paste(sombra, (px - mg + int(w * 0.02), py - mg + int(h * 0.012)), sombra)
        fondo.paste(prenda, (px, py), prenda)

        nombre = archivo.replace("-1200.jpg", "-lino-1200.jpg")
        destino = os.path.join(SALIDA, nombre)
        final = fondo.resize((1200, 1500), Image.LANCZOS)
        final.save(destino, "JPEG", quality=88, optimize=True, progressive=True)
        final.resize((720, 900), Image.LANCZOS).save(destino.replace("-1200", "-720"),
                                                     "JPEG", quality=86, optimize=True)
        print(f"ok {nombre}  {os.path.getsize(destino) / 1024:.0f} KB")


if __name__ == "__main__":
    main()

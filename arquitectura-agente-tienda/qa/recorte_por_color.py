"""Recorta objetos sobre el lienzo verde por color, no por modelo.

Cuando lo que está sobre el lienzo es chico y del mismo tono que el fondo —corbatas verdes sobre
tela verde— el modelo de segmentación toma el lienzo como objeto. Acá se saca el fondo por color:
el verde del lienzo es muy saturado y muy claro; las prendas no.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, ".pylibs"))

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402


def sacar_lienzo(im: Image.Image) -> Image.Image:
    """Devuelve las prendas: son los huecos que quedan dentro del lienzo verde."""
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lienzo = ((g > 110) & (g - r > 8) & (g - b > 60)).astype(np.uint8)
    lienzo = cv2.morphologyEx(lienzo, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

    # lo que no es lienzo y además está rodeado de lienzo = la prenda
    fuera = (1 - lienzo).copy()
    h, w = fuera.shape
    relleno = fuera.copy()
    mascara = np.zeros((h + 2, w + 2), np.uint8)
    for semilla in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if relleno[semilla[1], semilla[0]]:
            cv2.floodFill(relleno, mascara, semilla, 0)
    huecos = relleno.astype(np.uint8)

    n, et, st, _ = cv2.connectedComponentsWithStats(huecos, connectivity=8)
    if n <= 1:
        return None
    areas = st[1:, cv2.CC_STAT_AREA]
    mayor = areas.max()
    permitidas = [i + 1 for i, ar in enumerate(areas) if ar >= max(mayor * 0.03, 500)]
    mask = np.isin(et, permitidas).astype(np.uint8)
    # abre y cierra: corta los puentes finos de tela entre una prenda y otra
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    if not mask.any():
        return None

    ys, xs = np.where(mask > 0)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    alfa = Image.fromarray((mask * 255).astype(np.uint8)).crop((x0, y0, x1 + 1, y1 + 1))
    alfa = alfa.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(0.8))
    prenda = im.convert("RGB").crop((x0, y0, x1 + 1, y1 + 1))
    prenda.putalpha(alfa)
    return prenda


def componer(prenda, ratio=0.8, margen=0.10):
    w, h = prenda.size
    util = 1 - 2 * margen
    lw = max(int(w / util), int(h * ratio / util))
    lh = int(lw / ratio)
    if lh * util < h:
        lh = int(h / util)
        lw = int(lh * ratio)
    lienzo = Image.new("RGB", (lw, lh), "#FFFFFF")
    x = (lw - w) // 2
    y = (lh - h) // 2

    sombra = Image.new("L", (lw, lh), 0)
    capa = Image.new("L", (w + 60, h + 60), 0)
    capa.paste(prenda.split()[3], (30, 30))
    capa = capa.filter(ImageFilter.GaussianBlur(14))
    sombra.paste(capa.point(lambda v: int(v * 0.16)), (x - 30 + 3, y - 30 + 6))
    lienzo.paste(Image.new("RGB", (lw, lh), "#B4ABA3"), (0, 0), sombra)
    lienzo.paste(prenda, (x, y), prenda)
    return lienzo


def main():
    origen, destino = sys.argv[1], sys.argv[2]
    im = Image.open(origen).convert("RGB")
    # recorte previo: saca el borde de la mesa y el fondo de la foto
    ancho, alto = im.size
    im = im.crop((int(ancho * 0.04), int(alto * 0.11), int(ancho * 0.97), int(alto * 0.97)))
    prenda = sacar_lienzo(im)
    if prenda is None:
        print("no se pudo separar")
        sys.exit(1)
    print("recorte:", prenda.size)
    final = componer(prenda).resize((1200, 1500), Image.LANCZOS)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    final.save(destino, "JPEG", quality=88, optimize=True, progressive=True)
    final.resize((720, 900), Image.LANCZOS).save(destino.replace("-1200", "-720"), "JPEG", quality=86)
    print("guardado:", destino)


if __name__ == "__main__":
    main()

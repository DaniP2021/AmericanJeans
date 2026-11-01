"""Prueba de segmentación en dos pasadas para prendas colgadas con fondo cargado.

Pasada 1: segmentar la foto completa y ubicar la prenda.
Pasada 2: recortar alrededor de esa prenda y volver a segmentar el recorte, donde la
prenda ocupa casi todo el cuadro. El modelo acierta mucho más en un encuadre cerrado.

Uso: python qa/probar_dos_pasadas.py <carpeta-entrada> <carpeta-salida>
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", ".pylibs")))
sys.path.insert(0, AQUI)

import cv2  # noqa: E402
import numpy as np  # noqa: E402
import onnxruntime as ort  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

MODELO = os.path.abspath(os.path.join(AQUI, "..", "..", ".models", "u2net.onnx"))
_s = None


def sesion():
    global _s
    if _s is None:
        _s = ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])
    return _s


def mascara_de(im):
    s = sesion()
    n = s.get_inputs()[0].name
    chica = im.convert("RGB").resize((320, 320), Image.LANCZOS)
    a = np.asarray(chica).astype(np.float32) / 255.0
    a = (a - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    a = a.transpose(2, 0, 1)[None, ...].astype(np.float32)
    bruto = s.run(None, {n: a})[0][0, 0]
    bruto = (bruto - bruto.min()) / (bruto.max() - bruto.min() + 1e-8)
    return np.asarray(
        Image.fromarray((bruto * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS))


def limpiar(m, umbral=120, rampa=70, min_frac=0.02):
    """Umbraliza y conserva todos los componentes grandes, no sólo el mayor.

    Un conjunto son dos piezas separadas: si se elige sólo la mayor, la otra se pierde.
    """
    a = np.clip((m.astype(np.float32) - umbral) / rampa, 0, 1) * 255
    a = np.asarray(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.MedianFilter(5)))
    n, et, st, _ = cv2.connectedComponentsWithStats((a > 100).astype(np.uint8), connectivity=8)
    if n > 1:
        areas = st[1:, cv2.CC_STAT_AREA]
        minimo = max(areas.max() * min_frac, 200)
        permitidas = [i + 1 for i, ar in enumerate(areas) if ar >= minimo]
        a = np.where(np.isin(et, permitidas), a, 0)
    return a.astype(np.uint8)


def bbox(a, margen=0.06):
    ys, xs = np.where(a > 40)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    dx, dy = int((x1 - x0) * margen), int((y1 - y0) * margen)
    return (max(0, x0 - dx), max(0, y0 - dy), min(a.shape[1], x1 + dx), min(a.shape[0], y1 + dy))


def dos_pasadas(ruta):
    im = Image.open(ruta).convert("RGB")
    m1 = limpiar(mascara_de(im), min_frac=0.05)
    caja1 = bbox(m1, 0.10)
    recorte = im.crop(caja1)

    m2 = limpiar(mascara_de(recorte), umbral=110, rampa=80, min_frac=0.05)
    caja2 = bbox(m2, 0.02)
    m2 = m2[caja2[1]:caja2[3], caja2[0]:caja2[2]]
    prenda = recorte.crop(caja2)

    rgba = np.dstack([np.asarray(prenda), m2])
    return Image.fromarray(rgba.astype(np.uint8), "RGBA")


def componer(sujeto, ratio=0.8, margen=0.08):
    w, h = sujeto.size
    util = 1 - 2 * margen
    lw = max(int(w / util), int(h * ratio / util))
    lh = int(lw / ratio)
    if lh * util < h:
        lh = int(h / util)
        lw = int(lh * ratio)
    lienzo = Image.new("RGB", (lw, lh), "#FFFFFF")
    lienzo.paste(sujeto, ((lw - w) // 2, (lh - h) // 2), sujeto)
    return lienzo


def main():
    entrada, salida = sys.argv[1], sys.argv[2]
    os.makedirs(salida, exist_ok=True)
    for f in sorted(os.listdir(entrada)):
        if not f.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        base = os.path.splitext(f)[0]
        sujeto = dos_pasadas(os.path.join(entrada, f))
        final = componer(sujeto)
        destino = os.path.join(salida, base + "-1200.jpg")
        final.resize((1200, 1500), Image.LANCZOS).save(destino, "JPEG", quality=86, optimize=True)
        print(f"{base}: {sujeto.size} -> {os.path.getsize(destino) / 1024:.0f} KB")


if __name__ == "__main__":
    main()

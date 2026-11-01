"""Recorta al modelo con U2Netp (ONNX, local) y lo compone sobre un fondo de estudio 4:5.

El lienzo se construye con la proporción final desde el principio y el sujeto se ubica
con márgenes fijos: así no hay que recortar después (recortar después fue lo que cortó
la cabeza en un intento anterior).
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
from grado_casa import balance_blancos, curva_suave, calidez, grano  # noqa: E402

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\0e\0e94b7536873fc3dac931b9b0ffdd8abd644bed1b72be8ca6394a007468aa964"
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
MODELO = os.path.join(RAIZ, ".models", "u2netp.onnx")
BASE = os.path.normpath(os.path.join(AQUI, "..", "landing", "img"))
SECRETS = os.path.join(RAIZ, ".secrets")

UMBRAL, RAMPA = 115, 80
MARGEN_LADOS = 0.10
MARGEN_ABAJO = 0.045
MARGEN_ARRIBA_MIN = 0.05


def segmentar(im):
    sesion = ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])
    nombre = sesion.get_inputs()[0].name
    chica = im.convert("RGB").resize((320, 320), Image.LANCZOS)
    a = np.asarray(chica).astype(np.float32) / 255.0
    a = (a - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    a = a.transpose(2, 0, 1)[None, ...].astype(np.float32)
    salida = sesion.run(None, {nombre: a})[0][0, 0]
    salida = (salida - salida.min()) / (salida.max() - salida.min() + 1e-8)
    return Image.fromarray((salida * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS)


im = Image.open(SRC).convert("RGB")
arr = np.asarray(im)
filas = np.where(arr.max(axis=(1, 2)) > 25)[0]
im = im.crop((0, filas.min(), im.width, filas.max() + 1))
print("sin bandas:", im.size)

mascara = segmentar(im)
mascara.save(os.path.join(SECRETS, "_mascara-u2net.png"))

m = np.asarray(mascara).astype(np.float32)
m = np.clip((m - UMBRAL) / RAMPA, 0, 1)
alfa = (m * 255).astype(np.uint8)
alfa = np.asarray(Image.fromarray(alfa).filter(ImageFilter.MedianFilter(5)))
# apertura: corta protuberancias finas (restos de muebles pegados al cuerpo)
alfa = cv2.morphologyEx(alfa, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
alfa = np.asarray(Image.fromarray(alfa).filter(ImageFilter.GaussianBlur(1.0)))

n, etiquetas, stats, _ = cv2.connectedComponentsWithStats((alfa > 100).astype(np.uint8), connectivity=8)
if n > 1:
    idx = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    alfa = np.where(etiquetas == idx, alfa, 0).astype(np.uint8)

ys, xs = np.where(alfa > 40)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
rgba = np.dstack([np.asarray(im), alfa]).astype(np.uint8)
sujeto = Image.fromarray(rgba, "RGBA").crop((x0, y0, x1 + 1, y1 + 1))
# el espejo estaba torcido: se endereza la figura antes de componer
GRADOS = 6.0
sujeto = sujeto.rotate(GRADOS, resample=Image.BICUBIC, expand=True)
print(f"sujeto recortado y enderezado {GRADOS}°: {sujeto.size}")

w_s, h_s = sujeto.size
lienzo_w = int(w_s / (1 - 2 * MARGEN_LADOS))
lienzo_h = int(lienzo_w / 0.8)
if lienzo_h < h_s / (1 - MARGEN_ABAJO - MARGEN_ARRIBA_MIN):
    lienzo_h = int(h_s / (1 - MARGEN_ABAJO - MARGEN_ARRIBA_MIN))
    lienzo_w = int(lienzo_h * 0.8)
print(f"lienzo: {lienzo_w}x{lienzo_h} (relación {lienzo_w / lienzo_h:.3f})")

fondo = Image.new("RGB", (lienzo_w, lienzo_h), "#EFE7DF")
pf = ImageDraw.Draw(fondo)
for i in range(lienzo_h):
    t = i / lienzo_h
    pf.line([(0, i), (lienzo_w, i)],
            fill=(int(241 - 46 * t), int(235 - 46 * t), int(228 - 45 * t)))

halo = Image.new("L", (lienzo_w, lienzo_h), 0)
ImageDraw.Draw(halo).ellipse(
    (lienzo_w * 0.16, lienzo_h * 0.06, lienzo_w * 0.86, lienzo_h * 0.80), fill=100)
halo = halo.filter(ImageFilter.GaussianBlur(lienzo_w * 0.11))
fondo = Image.composite(Image.new("RGB", fondo.size, "#FDF9F4"), fondo, halo)

px = (lienzo_w - w_s) // 2
py = lienzo_h - h_s - int(lienzo_h * MARGEN_ABAJO)

sombra = Image.new("L", (lienzo_w, lienzo_h), 0)
ps = ImageDraw.Draw(sombra)
ps.ellipse((px + w_s * 0.06, py + h_s * 0.965, px + w_s * 0.94, py + h_s * 1.045), fill=170)
sombra = sombra.filter(ImageFilter.GaussianBlur(lienzo_w * 0.045))
fondo = Image.composite(Image.new("RGB", fondo.size, "#6B635A"), fondo, sombra)

fondo.paste(sujeto, (px, py), sujeto)

b = sujeto.split()[3]
desp = Image.new("L", sujeto.size, 0)
desp.paste(b.filter(ImageFilter.GaussianBlur(3)), (5, 0))
luz = Image.fromarray(
    (np.asarray(desp).astype(np.int16) - np.asarray(b).astype(np.int16)).clip(0, 255).astype(np.uint8))
luz = luz.point(lambda v: int(v * 0.55))
fondo.paste(Image.new("RGB", sujeto.size, "#FFF3E2"), (px, py), luz)

compuesto = balance_blancos(fondo)
compuesto = curva_suave(compuesto)
compuesto = calidez(compuesto)
compuesto = grano(compuesto, 2.2)

for ancho_salida in (720, 360):
    alto_salida = round(ancho_salida * 5 / 4)
    ruta = os.path.join(BASE, f"look-trabajo-{ancho_salida}.jpg")
    compuesto.resize((ancho_salida, alto_salida), Image.LANCZOS).save(
        ruta, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"look-trabajo-{ancho_salida}.jpg  {os.path.getsize(ruta) / 1024:.1f} KB")

compuesto.resize((340, 425), Image.LANCZOS).save(os.path.join(SECRETS, "_check-trabajo.jpg"), quality=90)
compuesto.save(os.path.join(SECRETS, "_compuesto.jpg"), quality=90)
print("control: .secrets/_check-trabajo.jpg")

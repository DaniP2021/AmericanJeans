"""Recorta al modelo de la selfie frente al espejo y lo compone sobre un fondo de estudio.

Sin modelos de segmentación: GrabCut con semillas manuales. Las semillas son necesarias
porque la ropa es negra y hay una puerta oscura detrás; el color solo no alcanza.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# opencv se instaló sin pip, en .pylibs del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", ".pylibs")))
sys.path.insert(0, AQUI)

import numpy as np  # noqa: E402
import cv2  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402
from grado_casa import balance_blancos, curva_suave, calidez  # noqa: E402

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\0e\0e94b7536873fc3dac931b9b0ffdd8abd644bed1b72be8ca6394a007468aa964"
BASE = os.path.normpath(os.path.join(AQUI, "..", "landing", "img"))
TRABAJO = os.path.normpath(os.path.join(AQUI, "..", ".."))

im = Image.open(SRC).convert("RGB")
arr = np.asarray(im)
filas = np.where(arr.max(axis=(1, 2)) > 25)[0]
im = im.crop((0, filas.min(), im.width, filas.max() + 1))
print("sin bandas:", im.size)

rgb = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
alto, ancho = rgb.shape[:2]

# --- rectángulo que contiene al sujeto -------------------------------------
RX, RY, RW, RH = 150, 160, 420, 760
mascara = np.full((alto, ancho), cv2.GC_BGD, dtype=np.uint8)
mascara[RY:RY + RH, RX:RX + RW] = cv2.GC_PR_FGD

# --- semillas: persona segura ---------------------------------------------
def sembrar(x0, y0, x1, y1, valor):
    mascara[y0:y1, x0:x1] = valor

sembrar(430, 195, 470, 240, cv2.GC_FGD)     # piel de la frente/mejilla
sembrar(240, 300, 290, 330, cv2.GC_FGD)     # manga blanca izquierda
sembrar(205, 640, 250, 700, cv2.GC_FGD)     # mano en el bolsillo
sembrar(455, 470, 500, 520, cv2.GC_FGD)     # puño blanco derecho

# --- semillas: fondo seguro -----------------------------------------------
sembrar(160, 160, 200, 220, cv2.GC_BGD)     # pared arriba a la izquierda
sembrar(180, 760, 260, 860, cv2.GC_BGD)     # piso de madera
sembrar(560, 300, 620, 380, cv2.GC_BGD)     # TV
sembrar(600, 560, 660, 640, cv2.GC_BGD)     # colchón azul
sembrar(330, 200, 380, 260, cv2.GC_BGD)     # puerta oscura detrás de la cabeza

cv2.setRNGSeed(7)
cv2.grabCut(rgb, mascara, (RX, RY, RW, RH), np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64),
            6, cv2.GC_INIT_WITH_MASK)

alfa = np.where((mascara == cv2.GC_FGD) | (mascara == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

# limpieza: cerrar huecos y quedarse con la figura principal
nucleo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
alfa = cv2.morphologyEx(alfa, cv2.MORPH_CLOSE, nucleo, iterations=3)
alfa = cv2.morphologyEx(alfa, cv2.MORPH_OPEN, nucleo, iterations=1)

n, etiquetas, stats, _ = cv2.connectedComponentsWithStats(alfa, connectivity=8)
if n > 1:
    idx = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    alfa = np.where(etiquetas == idx, 255, 0).astype(np.uint8)
    print("componente elegido, área:", stats[idx, cv2.CC_STAT_AREA])

# suavizar el borde
alfa_f = cv2.GaussianBlur(alfa, (0, 0), 1.6)

cv2.imwrite(os.path.join(TRABAJO, ".secrets", "_mascara.png"), alfa)

# --- recorte y composición ------------------------------------------------
ys, xs = np.where(alfa > 0)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
print(f"sujeto: x {x0}-{x1} · y {y0}-{y1}")

sujeto = np.dstack([np.asarray(im)[:, :, 0], np.asarray(im)[:, :, 1], np.asarray(im)[:, :, 2]]).astype(np.uint8)
rgba = np.dstack([sujeto, alfa_f]).astype(np.uint8)
recorte = Image.fromarray(rgba, "RGBA").crop((x0, y0, x1 + 1, y1 + 1))
print("recorte:", recorte.size)

# --- fondo de estudio ------------------------------------------------------
MAR = 0.16
lienzo_w = int(recorte.width * (1 + MAR * 2))
lienzo_h = int(recorte.height * (1 + MAR * 2))
fondo = Image.new("RGB", (lienzo_w, lienzo_h), "#E8E2DB")
pf = ImageDraw.Draw(fondo)
for i in range(lienzo_h):
    t = i / lienzo_h
    c = (int(240 - 26 * t), int(236 - 26 * t), int(231 - 26 * t))
    pf.line([(0, i), (lienzo_w, i)], fill=c)

# halo de luz detrás del sujeto
halo = Image.new("L", (lienzo_w, lienzo_h), 0)
ImageDraw.Draw(halo).ellipse(
    (lienzo_w * 0.10, lienzo_h * 0.05, lienzo_w * 0.92, lienzo_h * 0.95), fill=90)
halo = halo.filter(ImageFilter.GaussianBlur(lienzo_w * 0.10))
fondo = Image.composite(Image.new("RGB", fondo.size, "#FBF6F1"), fondo, halo)

# sombra de piso
sombra = Image.new("L", (lienzo_w, lienzo_h), 0)
ps = ImageDraw.Draw(sombra)
ps.ellipse((lienzo_w * 0.16, lienzo_h * 0.90, lienzo_w * 0.86, lienzo_h * 1.02), fill=120)
sombra = sombra.filter(ImageFilter.GaussianBlur(lienzo_w * 0.05))
fondo = Image.composite(Image.new("RGB", fondo.size, "#8E857B"), fondo, sombra)

px = int((lienzo_w - recorte.width) / 2)
py = int(lienzo_h - recorte.height)
fondo.paste(recorte, (px, py), recorte)

# luz de borde del lado de la ventana
borde = recorte.split()[3].filter(ImageFilter.GaussianBlur(3))
desp = Image.new("L", recorte.size, 0)
desp.paste(borde, (4, 0))
luz = Image.fromarray((np.asarray(desp).astype(np.int16) - np.asarray(borde).astype(np.int16)).clip(0, 255).astype(np.uint8))
luz = luz.point(lambda v: int(v * 0.5))
fondo.paste(Image.new("RGB", recorte.size, "#FFF4E6"), (px, py), luz)

compuesto = balance_blancos(fondo)
compuesto = curva_suave(compuesto)
compuesto = calidez(compuesto)

# --- recorte final 4:5 y exportación --------------------------------------
w, h = compuesto.size
objetivo = 4 / 5
if w / h > objetivo:
    nuevo = (int(h * objetivo), h)
else:
    nuevo = (w, int(w / objetivo))
compuesto = compuesto.resize(nuevo, Image.LANCZOS)

for ancho_salida in (720, 360):
    alto_salida = round(ancho_salida * 5 / 4)
    ruta = os.path.join(BASE, f"look-trabajo-{ancho_salida}.jpg")
    compuesto.resize((ancho_salida, alto_salida), Image.LANCZOS).save(
        ruta, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"look-trabajo-{ancho_salida}.jpg  {os.path.getsize(ruta) / 1024:.1f} KB")

compuesto.resize((340, 425), Image.LANCZOS).save(os.path.join(TRABAJO, ".secrets", "_check-trabajo.jpg"), quality=88)
compuesto.save(os.path.join(TRABAJO, ".secrets", "_compuesto.jpg"), quality=88)
print("control: .secrets/_check-trabajo.jpg y .secrets/_compuesto.jpg")

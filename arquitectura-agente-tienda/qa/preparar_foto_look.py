"""Prepara la foto del look de trabajo para la tarjeta (4:5) y genera los tamaños de uso."""

import os

from PIL import Image

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\39\39e3ee7ddca3209ffbac0ce4365f437d3a70e86016da104cb6da9bbc04e111a0"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))

im = Image.open(SRC).convert("RGB")
w, h = im.size
print(f"original: {w}x{h} (relación {w / h:.2f})")

# 1) recorte a 4:5 centrado, con una pizca más de aire arriba (la cabeza no se corta)
objetivo = 4 / 5
if w / h > objetivo:          # sobra ancho
    nuevo_w = int(h * objetivo)
    x0 = (w - nuevo_w) // 2
    caja = (x0, 0, x0 + nuevo_w, h)
else:                          # sobra alto
    nuevo_h = int(w / objetivo)
    y0 = int((h - nuevo_h) * 0.72)   # 72% arriba, 28% abajo: recorta aire de arriba y deja los pies completos
    caja = (0, y0, w, y0 + nuevo_h)

recorte = im.crop(caja)
print(f"recorte: {recorte.width}x{recorte.height} desde {caja} (relación {recorte.width / recorte.height:.2f})")

# 2) tamaños de uso: la tarjeta muestra ~340 px de ancho en escritorio
for ancho, calidad in [(720, 82), (360, 80)]:
    alto = round(ancho * 5 / 4)
    salida = recorte.resize((ancho, alto), Image.LANCZOS)
    ruta = os.path.join(BASE, f"look-trabajo-{ancho}.jpg")
    salida.save(ruta, "JPEG", quality=calidad, optimize=True, progressive=True)
    print(f"look-trabajo-{ancho}.jpg  {ancho}x{alto}  {os.path.getsize(ruta) / 1024:.1f} KB")

# 3) control: la foto final a tamaño de tarjeta
prev = recorte.resize((340, 425), Image.LANCZOS)
prev.save(os.path.join(BASE, "_check-look.jpg"), "JPEG", quality=85)
print("control: landing/img/_check-look.jpg")

"""Prepara la foto del look de fin de semana (padre e hijo) para la tarjeta 4:5."""

import os

from PIL import Image

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\04\04a73f1671fcb86ba06b7ab4a720cc5e8800f14d713e37e9c5231b7e5e75f74a"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))

im = Image.open(SRC).convert("RGB")
ancho, alto = im.size
print(f"original: {ancho}x{alto} (relación {ancho / alto:.2f})")

# 4:5 → se recorta alto desde arriba: abajo están los pies y no se tocan
objetivo = 4 / 5
alto_nuevo = int(ancho / objetivo)      # 1120
y0 = 0
recorte = im.crop((0, y0, ancho, y0 + alto_nuevo))
print(f"recorte: {recorte.size} desde y={y0} (relación {recorte.width / recorte.height:.2f})")

for ancho_salida in (720, 360):
    alto_salida = round(ancho_salida * 5 / 4)
    ruta = os.path.join(BASE, f"look-finde-{ancho_salida}.jpg")
    recorte.resize((ancho_salida, alto_salida), Image.LANCZOS).save(
        ruta, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"look-finde-{ancho_salida}.jpg  {os.path.getsize(ruta) / 1024:.1f} KB")

recorte.resize((340, 425), Image.LANCZOS).save(os.path.join(BASE, "_check-finde.jpg"), quality=86)
print("control: landing/img/_check-finde.jpg")

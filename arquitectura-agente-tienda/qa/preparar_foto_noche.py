"""Prepara la foto del look de noche (café) para la tarjeta 4:5.

Fuente: hombre con camisa celeste de lunares, chaleco de hilo gris y pantalón azul,
en una cafetería con luz cálida. El encuadre original ya es de tres cuartos, así que
sólo hay que ajustar el alto al formato de la tarjeta sin cortar la cabeza.
"""

import os

from PIL import Image

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\2a\2ad05eb44f7672b3693065d6d7ec5f94f6a2719df885c0ac20ea3ae22dd75ec1"
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))

im = Image.open(SRC).convert("RGB")
ancho, alto = im.size
print(f"original: {ancho}x{alto} (relación {ancho / alto:.2f})")

# 4:5 → se recorta alto, desde abajo, para no tocar el aire sobre la cabeza
objetivo = 4 / 5
alto_nuevo = int(ancho / objetivo)      # 1120
y0 = max(0, alto - alto_nuevo)          # se quita de la parte baja (rodillas)
recorte = im.crop((0, y0, ancho, y0 + alto_nuevo))
print(f"recorte: {recorte.size} desde y={y0} (relación {recorte.width / recorte.height:.2f})")

for ancho_salida in (720, 360):
    alto_salida = round(ancho_salida * 5 / 4)
    ruta = os.path.join(BASE, f"look-noche-{ancho_salida}.jpg")
    recorte.resize((ancho_salida, alto_salida), Image.LANCZOS).save(
        ruta, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"look-noche-{ancho_salida}.jpg  {os.path.getsize(ruta) / 1024:.1f} KB")

# control al tamaño real de la tarjeta
recorte.resize((340, 425), Image.LANCZOS).save(os.path.join(BASE, "_check-noche.jpg"), quality=86)
print("control: landing/img/_check-noche.jpg")

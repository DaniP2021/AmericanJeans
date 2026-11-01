"""Genera el sello de la marca a partir del arte real: marco rojo + AJ | basic + American Jeans.

El círculo del avatar es un recorte de la plataforma, no parte del logo. Recortando el
contenido se eliminan de una vez el anillo del avatar y la burbuja del corazón.
Salida: sello rectangular con esquinas redondeadas y fondo negro, listo para la web.
"""

import os

from PIL import Image, ImageDraw

SRC = r"C:\Users\Daniel2026\.dsh\attachments\v1\objects\3c\3caaf60523923e0ebf2b7ba72f64837df3832b4e84c8934bb7fa43948b92127f"

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing", "img"))
os.makedirs(BASE, exist_ok=True)

im = Image.open(SRC).convert("RGB")
w, h = im.size
px = im.load()

# 1) círculo del avatar (para recortar el fondo)
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        if r < 45 and g < 45 and b < 45:
            minx, miny = min(minx, x), min(miny, y)
            maxx, maxy = max(maxx, x), max(maxy, y)

cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
radio = max(maxx - minx, maxy - miny) / 2

lienzo = Image.new("RGBA", (int(radio * 2), int(radio * 2)), (0, 0, 0, 0))
lienzo.paste(im.convert("RGBA"), (int(round(-(cx - radio))), int(round(-(cy - radio)))))

esc = 4
m = Image.new("L", (lienzo.width * esc, lienzo.height * esc), 0)
ImageDraw.Draw(m).ellipse((0, 0, lienzo.width * esc - 1, lienzo.height * esc - 1), fill=255)
lienzo.putalpha(m.resize(lienzo.size, Image.LANCZOS))

# 2) caja del contenido: marco rojo + texto blanco (sin el anillo ni la burbuja)
rojos = [(x, y) for y in range(0, lienzo.height, 2) for x in range(0, lienzo.width, 2)
         if (lambda c: c[3] > 200 and c[0] > 110 and c[1] < 80 and c[2] < 80)(lienzo.getpixel((x, y)))]

rx0 = min(p[0] for p in rojos)
rx1 = max(p[0] for p in rojos)
ry0 = min(p[1] for p in rojos)
ry1 = max(p[1] for p in rojos)

# filas con texto: muchas columnas blancas en la misma fila. El corazón tiene muy pocas.
filas_texto = []
for y in range(ry0, min(lienzo.height, ry0 + 220)):
    n = 0
    for x in range(rx0 - 40, rx1 + 40):
        c = lienzo.getpixel((x, y))
        if c[3] > 200 and min(c[:3]) > 185:
            n += 1
    if n >= 25:
        filas_texto.append(y)

if filas_texto:
    ty0, ty1 = min(filas_texto), max(filas_texto)
    tx0, tx1 = 10 ** 6, 0
    for y in range(ty0, ty1 + 1):
        for x in range(0, lienzo.width):
            c = lienzo.getpixel((x, y))
            if c[3] > 200 and min(c[:3]) > 185:
                tx0, tx1 = min(tx0, x), max(tx1, x)
else:
    ty0, ty1, tx0, tx1 = ry0, ry1, rx0, rx1

x0, y0 = min(rx0, tx0), min(ry0, ty0)
x1, y1 = max(rx1, tx1), max(ry1, ty1)
print(f"contenido: ({x0},{y0})-({x1},{y1}) → {x1 - x0}x{y1 - y0}")

# 3) sello: se recorta el arte exactamente por el contenido (sus esquinas quedan dentro del
#    círculo, sin anillo) y se le agrega margen negro del mismo tono.
pad_arte = 0
ax0, ay0 = max(0, x0 - pad_arte), max(0, y0 - pad_arte)
ax1, ay1 = min(lienzo.width, x1 + pad_arte), min(lienzo.height, y1 + pad_arte)
arte = lienzo.crop((ax0, ay0, ax1, ay1))
arte = arte.convert("RGB")  # dentro del círculo el arte es opaco

# tono del negro: mediana de los píxeles oscuros del propio arte (no del borde, que trae el marco)
oscuros = []
for y in range(0, arte.height, 2):
    for x in range(0, arte.width, 2):
        c = arte.getpixel((x, y))
        if sum(c) < 70:
            oscuros.append(c)
oscuros.sort(key=lambda c: sum(c))
negro = oscuros[len(oscuros) // 2] if oscuros else (14, 14, 14)
print("negro del arte:", negro)

margen = 26
sello = Image.new("RGBA", (arte.width + margen * 2, arte.height + margen * 2), negro + (255,))
sello.paste(arte, (margen, margen))

esquinas = Image.new("L", sello.size, 0)
ImageDraw.Draw(esquinas).rounded_rectangle((0, 0, sello.width - 1, sello.height - 1),
                                          radius=20, fill=255)
sello.putalpha(esquinas)

print(f"sello: {sello.width}x{sello.height} (relación {sello.width / sello.height:.2f})")

# 4) exportar a los anchos que se van a usar
for ancho in (480, 320, 160):
    alto = round(ancho * sello.height / sello.width)
    nombre = f"logo-sello-{ancho}.png"
    ruta = os.path.join(BASE, nombre)
    sello.resize((ancho, alto), Image.LANCZOS).save(ruta, "PNG", optimize=True)
    print(f"{nombre:22} {ancho}x{alto}  {os.path.getsize(ruta) / 1024:.1f} KB")

webp = os.path.join(BASE, "logo-sello-320.webp")
sello.resize((320, round(320 * sello.height / sello.width)), Image.LANCZOS).save(webp, "WEBP", quality=92)
print(f"{'logo-sello-320.webp':22} {os.path.getsize(webp) / 1024:.1f} KB")

# 5) control visual sobre los tres fondos
def muestra(fondo, ancho=260):
    alto = round(ancho * sello.height / sello.width)
    c = Image.new("RGB", (ancho + 48, alto + 48), fondo)
    s = sello.resize((ancho, alto), Image.LANCZOS)
    c.paste(s, (24, 24), s)
    return c

chk = Image.new("RGB", (3 * 330, 300), "#FFFFFF")
for i, fondo in enumerate(["#FDF6F1", "#F6F9FF", "#1F3A5F"]):
    chk.paste(muestra(fondo), (i * 330, 0))
chk.save(os.path.join(BASE, "_check-sello.png"))
print("check: landing/img/_check-sello.png")

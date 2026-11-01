"""Renderiza una comparación PNG de las dos paletas candidatas (sin navegador)."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1720, 1110
M = 40
COL = (W - M * 3) // 2

FONT_DIR = r"C:\Windows\Fonts"
def f(name, size, bold=False):
    for cand in ([name + "bd.ttf", name + ".ttf"] if bold else [name + ".ttf"]):
        p = os.path.join(FONT_DIR, cand)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TIT = f("segoeuib", 26, True)
F_SUB = f("segoeui", 13)
F_H1 = f("segoeuib", 27, True)
F_BODY = f("segoeui", 13)
F_SMALL = f("segoeui", 11)
F_BTN = f("segoeuib", 13, True)
F_HEX = f("consola", 11)

PALETAS = [
    {
        "nombre": "A · Terracota y denim",
        "claim": "Cálida y cercana. Azul del jean de ancla, terracota de acción.",
        "fondo": "#FDF6F1", "sup": "#FFFFFF", "texto": "#1C1512", "suave": "#6E625B",
        "borde": "#EBDCD1", "accion": "#B8452C", "hover": "#9C3822", "vivo": "#E2703A",
        "acento": "#F2B37A", "banda": "#1F3A5F", "tinte": "#FBEFE6", "tinte2": "#E9F0F7",
        "orden": ["fondo", "sup", "texto", "suave", "vivo", "accion", "acento", "banda"],
    },
    {
        "nombre": "B · Cielo y durazno",
        "claim": "Fresca y optimista. Azul vivo de acción, durazno de calidez.",
        "fondo": "#F6F9FF", "sup": "#FFFFFF", "texto": "#111A2B", "suave": "#5C6678",
        "borde": "#DCE6F5", "accion": "#1E56D6", "hover": "#1745B0", "vivo": "#3D7BF0",
        "acento": "#FF8A65", "banda": "#0F1B33", "tinte": "#E8F0FF", "tinte2": "#FFF2ED",
        "orden": ["fondo", "sup", "texto", "suave", "vivo", "accion", "acento", "banda"],
    },
]


def grad(img, box, c1, c2, steps=60):
    """Degradado diagonal aproximado, recortado al box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    small = Image.new("RGB", (steps, steps))
    px = small.load()
    a, b = Image.new("RGB", (1, 1), c1).getpixel((0, 0)), Image.new("RGB", (1, 1), c2).getpixel((0, 0))
    for y in range(steps):
        for x in range(steps):
            t = (x * 0.55 + y * 0.45) / (steps - 1)
            px[x, y] = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    img.paste(small.resize((w, h), Image.BILINEAR), (x0, y0))


def chip(d, x, y, w, h, color, label, small):
    d.rounded_rectangle([x, y, x + w, y + h - 22], radius=8, fill=color, outline="#00000022")
    txt = label.upper()
    d.text((x, y + h - 18), txt, font=small, fill="#555555")


img = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(img)

d.text((M, 22), "AMERICAN JEANS · DOS PALETAS PARA EL RESTO DE LA LANDING", font=F_TIT, fill="#0E0E0E")
d.text((M, 58), "El logo conserva negro y rojo. La tipografía sigue en negro. Cambian superficies, acciones y acentos.",
       font=F_SUB, fill="#666666")
d.text((M, 78), "Muestra de color y jerarquía; la vista real está en landing/preview-a.html y preview-b.html",
       font=F_SMALL, fill="#999999")

y0 = 112
for i, p in enumerate(PALETAS):
    x = M + i * (COL + M)
    # panel
    d.rounded_rectangle([x, y0, x + COL, H - 52], radius=16, fill=p["fondo"], outline=p["borde"], width=2)
    d.text((x + 24, y0 + 18), p["nombre"], font=F_TIT, fill=p["texto"])
    d.text((x + 24, y0 + 52), p["claim"], font=F_SMALL, fill=p["suave"])

    # muestras
    sw_y = y0 + 82
    cw = (COL - 48 - 7 * 8) // 8
    for j, key in enumerate(p["orden"]):
        cx = x + 24 + j * (cw + 8)
        chip(d, cx, sw_y, cw, 74, p[key], p[key], F_HEX)

    # header simulado
    hy = sw_y + 100
    d.rounded_rectangle([x + 24, hy, x + COL - 24, hy + 62], radius=10, fill=p["sup"], outline=p["borde"])
    d.text((x + 44, hy + 21), "AMERICAN JEANS", font=F_BTN, fill=p["texto"])
    wname = d.textlength("AMERICAN JEANS", font=F_BTN)
    d.rectangle([x + 44 + wname + 9, hy + 17, x + 44 + wname + 11, hy + 45], fill="#B0232B")
    d.text((x + 44 + wname + 19, hy + 25), "basic", font=F_SMALL, fill="#B0232B")
    nx = x + 44 + wname + 19 + d.textlength("basic", font=F_SMALL) + 38
    for k, item in enumerate(["Looks", "AJ basic", "Cómo comprar", "Talles"]):
        d.text((nx + k * 82, hy + 23), item, font=F_SMALL, fill=p["suave"])
    d.rounded_rectangle([x + COL - 150, hy + 14, x + COL - 40, hy + 48], radius=6, fill="#17784B")
    d.text((x + COL - 134, hy + 24), "WhatsApp", font=F_SMALL, fill="#FFFFFF")

    # hero simulado
    h_y = hy + 78
    h_h = 268
    grad(img, (x + 24, h_y, x + COL - 24, h_y + h_h), p["tinte"], p["tinte2"])
    d.rounded_rectangle([x + 24, h_y, x + COL - 24, h_y + h_h], radius=10, outline=p["borde"])
    d.text((x + 48, h_y + 26), "INDUMENTARIA MASCULINA · BUENOS AIRES", font=F_SMALL, fill=p["accion"])
    d.text((x + 48, h_y + 54), "Camisas, jeans y básicos", font=F_H1, fill=p["texto"])
    d.text((x + 48, h_y + 88), "para el hombre que no tiene", font=F_H1, fill=p["texto"])
    d.text((x + 48, h_y + 122), "tiempo de pensarlo.", font=F_H1, fill=p["texto"])
    d.text((x + 48, h_y + 166), "Cuatro locales que ya conocés, ahora también online.", font=F_BODY, fill=p["suave"])
    d.text((x + 48, h_y + 184), "Retiro en 2 horas y cambios gratis en las cuatro.", font=F_BODY, fill=p["suave"])
    bx = x + 48
    d.rounded_rectangle([bx, h_y + 210, bx + 210, h_y + 246], radius=6, fill=p["accion"])
    d.text((bx + 22, h_y + 222), "Escribinos por WhatsApp", font=F_SMALL, fill="#FFFFFF")
    d.rounded_rectangle([bx + 224, h_y + 210, bx + 356, h_y + 246], radius=6, outline=p["texto"], width=2)
    d.text((bx + 244, h_y + 222), "Cómo comprar", font=F_SMALL, fill=p["texto"])

    # promesas
    pr_y = h_y + h_h + 16
    d.rounded_rectangle([x + 24, pr_y, x + COL - 24, pr_y + 74], radius=10, fill=p["sup"], outline=p["borde"])
    for k, t in enumerate(["Retiro en 2 horas", "Cambios en 4 sucursales", "El talle que hay"]):
        px_ = x + 44 + k * 230
        d.rounded_rectangle([px_, pr_y + 26, px_ + 9, pr_y + 35], radius=2, fill=p["vivo"])
        d.text((px_ + 16, pr_y + 22), t, font=F_SMALL, fill=p["texto"])

    # tarjeta de producto
    c_y = pr_y + 92
    d.rounded_rectangle([x + 24, c_y, x + COL - 24, c_y + 214], radius=12, fill=p["sup"], outline=p["borde"])
    d.rounded_rectangle([x + 40, c_y + 16, x + 176, c_y + 198], radius=8, fill=p["tinte"], outline=p["acento"])
    d.text((x + 58, c_y + 100), "FOTO · LOOK", font=F_SMALL, fill=p["suave"])
    d.text((x + 196, c_y + 26), "Para trabajar", font=F_BTN, fill=p["texto"])
    d.text((x + 196, c_y + 50), "Camisa que se arruga poco y jean", font=F_SMALL, fill=p["suave"])
    d.text((x + 196, c_y + 66), "que no aprieta después de almorzar.", font=F_SMALL, fill=p["suave"])
    d.text((x + 196, c_y + 92), "Precio de referencia", font=F_SMALL, fill=p["suave"])
    d.rounded_rectangle([x + 196, c_y + 120, x + 320, c_y + 154], radius=6, outline=p["texto"], width=2)
    d.text((x + 214, c_y + 131), "Ver el look", font=F_SMALL, fill=p["texto"])
    d.rounded_rectangle([x + 336, c_y + 120, x + 470, c_y + 154], radius=6, fill=p["acento"])
    d.text((x + 352, c_y + 131), "AJ basic", font=F_SMALL, fill=p["texto"])

    # banda oscura
    b_y = c_y + 232
    d.rounded_rectangle([x + 24, b_y, x + COL - 24, b_y + 62], radius=10, fill=p["banda"])
    d.text((x + 44, b_y + 14), "AJ basic: la base del placard", font=F_BTN, fill="#FFFFFF")
    d.text((x + 44, b_y + 36), "Retiro en 2 h · Cambios gratis · 4 sucursales", font=F_SMALL, fill="#FFFFFFAA")
    for k, item in enumerate(["Sucursales", "Comprar", "Legales"]):
        d.text((x + COL - 260 + k * 78, b_y + 26), item, font=F_SMALL, fill=p["acento"])

# pie
d.text((M, H - 30), "Contraste verificado: A 5.35:1 y B 6.25:1 en botones · texto sobre fondo 16.8:1 y 16.5:1 · badge 9.9:1 y 7.5:1 · ambos cumplen AA",
       font=F_SMALL, fill="#777777")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paletas", "comparacion-paletas.png")
out = os.path.normpath(out)
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, "PNG")
print("ok", out, img.size)

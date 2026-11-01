"""QA técnico de la landing Fase 1: estructura, links, placeholders y contraste WCAG."""

import os
import re
import sys
from html.parser import HTMLParser

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing")
BASE = os.path.normpath(BASE)

PAGINAS = ["index.html", "talles.html",
           os.path.join("legal", "terminos.html"),
           os.path.join("legal", "cambios.html"),
           os.path.join("legal", "privacidad.html"),
           os.path.join("legal", "arrepentimiento.html")]

problemas = []
avisos = []


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.recursos = []
        self.ids = set()
        self.labels = set()
        self.inputs = []
        self.titulo = None
        self._en_titulo = False
        self.meta = {}
        self.lang = None
        self.h1 = 0
        self.img_sin_alt = 0
        self.imgs = []
        self.details = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = d.get("lang")
        elif tag == "title":
            self._en_titulo = True
            self.titulo = ""
        elif tag == "meta":
            if d.get("name"):
                self.meta[d["name"]] = d.get("content", "")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "a":
            if d.get("href"):
                self.links.append(d["href"])
        elif tag in ("link", "script"):
            if d.get("href"):
                self.recursos.append(d["href"])
            if d.get("src"):
                self.recursos.append(d["src"])
        elif tag == "img":
            if "alt" not in d:
                self.img_sin_alt += 1
            if d.get("src"):
                self.imgs.append(d["src"])
            if d.get("srcset"):
                for parte in d["srcset"].split(","):
                    ruta = parte.strip().split(" ")[0]
                    if ruta:
                        self.imgs.append(ruta)
        elif tag == "label":
            if d.get("for"):
                self.labels.add(d["for"])
        elif tag == "input":
            self.inputs.append(d)
        elif tag == "details":
            self.details += 1
        if d.get("id"):
            self.ids.add(d["id"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._en_titulo = False

    def handle_data(self, data):
        if self._en_titulo:
            self.titulo += data


def hex_a_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    def canal(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(fg, bg):
    l1, l2 = luminancia(hex_a_rgb(fg)), luminancia(hex_a_rgb(bg))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


print("=" * 66)
print("QA LANDING — American Jeans")
print("=" * 66)

for pagina in PAGINAS:
    ruta = os.path.join(BASE, pagina)
    print(f"\n--- {pagina} ---")
    if not os.path.exists(ruta):
        problemas.append(f"{pagina}: no existe")
        print("  FALTA EL ARCHIVO")
        continue

    with open(ruta, encoding="utf-8") as f:
        html = f.read()

    p = Parser()
    p.feed(html)

    if p.lang != "es-AR":
        problemas.append(f"{pagina}: lang={p.lang}")
    if p.h1 != 1:
        problemas.append(f"{pagina}: {p.h1} etiquetas h1 (debe haber 1)")
    if p.img_sin_alt:
        problemas.append(f"{pagina}: {p.img_sin_alt} img sin alt")

    len_titulo = len(p.titulo or "")
    desc = p.meta.get("description", "")
    print(f"  title: {len_titulo} car · description: {len(desc)} car · h1: {p.h1}")
    if len_titulo > 65:
        avisos.append(f"{pagina}: title de {len_titulo} caracteres")

    # links internos
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        destino = os.path.normpath(os.path.join(os.path.dirname(ruta), href.split("#")[0]))
        if not os.path.exists(destino):
            problemas.append(f"{pagina}: link roto -> {href}")

    # recursos
    for src in p.recursos:
        if src.startswith(("http", "data:")):
            continue
        destino = os.path.normpath(os.path.join(os.path.dirname(ruta), src))
        if not os.path.exists(destino):
            problemas.append(f"{pagina}: recurso faltante -> {src}")

    # imágenes (src y srcset)
    for src in p.imgs:
        if src.startswith(("http", "data:")):
            continue
        destino = os.path.normpath(os.path.join(os.path.dirname(ruta), src))
        if not os.path.exists(destino):
            problemas.append(f"{pagina}: imagen faltante -> {src}")
    if p.imgs:
        print(f"  imágenes: {len(set(p.imgs))} archivo(s) referenciado(s)")

    # formularios
    for inp in p.inputs:
        if inp.get("type") in ("hidden", "submit", "checkbox"):
            continue
        if inp.get("id") and inp["id"] not in p.labels:
            problemas.append(f"{pagina}: input #{inp['id']} sin label asociado")

    # placeholders a la vista
    marcadores = {
        "número provisorio": html.count("5491155550000"),
        "a confirmar": html.count("a confirmar"),
        "campos [..]": len(re.findall(r"\[[A-ZÁÉÍÓÚÑ][^\]]{2,20}\]", html)),
        "de ejemplo": html.count("de ejemplo"),
    }
    print("  placeholders: " + ", ".join(f"{k}={v}" for k, v in marcadores.items() if v))

print("\n" + "=" * 66)
print("CONTRASTE WCAG (AA texto normal = 4.5 · AA texto grande = 3.0)")
print("=" * 66)
PALETAS = {
    "A · Terracota y denim": {
        "fondo": "#FDF6F1", "texto": "#1C1512", "suave": "#6E625B",
        "accion": "#B8452C", "acento": "#F2B37A", "banda": "#1F3A5F",
        "tinte": "#FBEFE6", "tinte2": "#E9F0F7",
    },
    "B · Cielo y durazno": {
        "fondo": "#F6F9FF", "texto": "#111A2B", "suave": "#5C6678",
        "accion": "#1E56D6", "acento": "#FF8A65", "banda": "#0F1B33",
        "tinte": "#E8F0FF", "tinte2": "#FFF2ED",
    },
}

pares = [
    ("Marca · rojo del logo sobre blanco", "#B0232B", "#FFFFFF"),
    ("Marca · blanco sobre rojo", "#FFFFFF", "#B0232B"),
    ("WhatsApp · blanco sobre verde", "#FFFFFF", "#17784B"),
    ("Gris 5A5A5A sobre blanco", "#5A5A5A", "#FFFFFF"),
]
for nombre_pal, p in PALETAS.items():
    pares += [
        (f"{nombre_pal} · texto sobre fondo", p["texto"], p["fondo"]),
        (f"{nombre_pal} · texto suave sobre fondo", p["suave"], p["fondo"]),
        (f"{nombre_pal} · texto suave sobre tinte", p["suave"], p["tinte"]),
        (f"{nombre_pal} · blanco sobre acción (botón)", "#FFFFFF", p["accion"]),
        (f"{nombre_pal} · acción sobre tinte (eyebrow)", p["accion"], p["tinte"]),
        (f"{nombre_pal} · texto sobre acento (badge)", p["texto"], p["acento"]),
        (f"{nombre_pal} · acento sobre banda (footer)", p["acento"], p["banda"]),
        (f"{nombre_pal} · blanco sobre banda", "#FFFFFF", p["banda"]),
    ]

for nombre, fg, bg in pares:
    c = contraste(fg, bg)
    estado = "OK" if c >= 4.5 else "FALLA"
    if estado == "FALLA":
        problemas.append(f"contraste: {nombre} = {c:.2f} (< 4.5)")
    print(f"  {estado:5} {c:5.2f}  {nombre}")

print("\n" + "=" * 66)
if problemas:
    print(f"PROBLEMAS ({len(problemas)}):")
    for x in problemas:
        print("  ✗ " + x)
else:
    print("Sin problemas bloqueantes.")

if avisos:
    print(f"\nAVISOS ({len(avisos)}):")
    for x in avisos:
        print("  · " + x)

print("=" * 66)
sys.exit(1 if problemas else 0)

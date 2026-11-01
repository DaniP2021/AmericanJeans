"""Mockups de la web con el fondo de la marca, en dos variantes.

Variante 1: la prenda recortada se apoya directamente sobre el fondo de la página.
Variante 2: tarjetas blancas con la foto en blanco, sobre el mismo fondo.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, ".pylibs"))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas"))

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

from fondos import CREMA, TERRACOTA, lino, sombra_de  # noqa: E402
from fotocatalogo import recortar_sujeto  # noqa: E402

CAT = os.path.join(RAIZ, "CATALOGO")
SALIDA = os.path.join(CAT, "mockups")
os.makedirs(SALIDA, exist_ok=True)

NEGRITA = r"C:\Windows\Fonts\segoeuib.ttf"
REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
TINTA = (28, 21, 18)
SUAVE = (110, 98, 91)
BORDE = (214, 196, 178)

PRODUCTOS = [
    ("jean-clasico-tres-lavados", "Jean clásico", "Tres lavados"),
    ("camisa-estampada-manga-larga-seis-colores", "Camisa estampada", "Seis colores"),
    ("bermuda-elastizada-corte-jean-negro-y-azul", "Bermuda corte jean", "Negro y azul"),
]

ANCHO, ALTO = 1180, 820
MARGEN = 56
COL = 3
ALTO_IMG = 412


def txt(d, xy, t, fuente, color, tam=16):
    d.text(xy, t, font=ImageFont.truetype(fuente, tam), fill=color)


def encabezado(d, etiqueta):
    d.rectangle([0, 0, ANCHO, 96], fill=CREMA)
    txt(d, (MARGEN, 30), "AMERICAN JEANS", NEGRITA, TINTA, 26)
    d.line([(MARGEN + 232, 34), (MARGEN + 232, 58)], fill=BORDE, width=2)
    txt(d, (MARGEN + 244, 38), "basic", NEGRITA, TERRACOTA, 20)
    for i, item in enumerate(["LOOKS", "CATÁLOGO", "TALLES", "CONTACTO"]):
        txt(d, (ANCHO - MARGEN - 330 + i * 88, 40), item, NEGRITA, TINTA, 12)
    d.line([(0, 96), (ANCHO, 96)], fill=BORDE, width=1)

    txt(d, (MARGEN, 126), "Catálogo", NEGRITA, TINTA, 34)
    txt(d, (MARGEN, 174), "13 productos · jeans, camisas, bermudas, chombas y conjuntos",
        REGULAR, SUAVE, 15)
    txt(d, (ANCHO - MARGEN - 210, 128), etiqueta, NEGRITA, TERRACOTA, 13)


def pie_de_tarjeta(d, x, y, titulo, color):
    txt(d, (x, y), titulo.upper(), NEGRITA, TINTA, 15)
    txt(d, (x, y + 22), color, REGULAR, SUAVE, 14)
    by = y + 52
    d.rectangle([x, by, x + 200, by + 38], fill=TERRACOTA)
    fb = ImageFont.truetype(NEGRITA, 13)
    ancho_txt = d.textlength("CONSULTAR", font=fb)
    d.text((x + (200 - ancho_txt) / 2, by + 12), "CONSULTAR", font=fb, fill="#FFFFFF")


def variante_recortada(semilla):
    lienzo = lino(ANCHO, ALTO, semilla=semilla)
    d = ImageDraw.Draw(lienzo)
    encabezado(d, "VARIANTE 1 · PRENDA SOBRE EL FONDO")

    ancho_col = (ANCHO - 2 * MARGEN - (COL - 1) * 30) // COL
    for i, (slug, titulo, color) in enumerate(PRODUCTOS):
        ruta = os.path.join(CAT, "seleccion", slug + "-1200.jpg")
        if not os.path.exists(ruta):
            continue
        prenda, _f, _b = recortar_sujeto(Image.open(ruta).convert("RGB"), piezas=0.08)
        if prenda is None:
            continue
        # comer el filo blanco del JPG original
        alfa = prenda.split()[3].filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.6))
        # el alfa que queda casi en cero se lleva a cero: si no, deja un recuadro tenue
        a = np.asarray(alfa).astype(np.uint8)
        a[a < 26] = 0
        prenda.putalpha(Image.fromarray(a))

        escala = min(ancho_col / prenda.width, ALTO_IMG / prenda.height) * 0.94
        prenda = prenda.resize((int(prenda.width * escala), int(prenda.height * escala)), Image.LANCZOS)

        x = MARGEN + i * (ancho_col + 30)
        y = 232
        px = x + (ancho_col - prenda.width) // 2
        py = y + (ALTO_IMG - prenda.height) // 2

        sombra, mg = sombra_de(prenda, desenfoque=22, opacidad=0.20)
        lienzo.paste(sombra, (px - mg + 6, py - mg + 8), sombra)
        lienzo.paste(prenda, (px, py), prenda)

        pie_de_tarjeta(d, x, y + ALTO_IMG + 16, titulo, color)

    txt(d, (MARGEN, ALTO - 42), "Paleta A · terracota #B8452C · crema #FDF6F1 · arena #F5E9DE · denim #1F3A5F",
        REGULAR, SUAVE, 12)
    destino = os.path.join(SALIDA, f"web-variante-{semilla}.png")
    lienzo.save(destino)
    print("ok", destino)


def variante_tarjetas(semilla):
    lienzo = lino(ANCHO, ALTO, semilla=semilla)
    d = ImageDraw.Draw(lienzo)
    encabezado(d, "VARIANTE 2 · TARJETAS BLANCAS")

    ancho_col = (ANCHO - 2 * MARGEN - (COL - 1) * 30) // COL
    for i, (slug, titulo, color) in enumerate(PRODUCTOS):
        ruta = os.path.join(CAT, "seleccion", slug + "-1200.jpg")
        if not os.path.exists(ruta):
            continue
        x = MARGEN + i * (ancho_col + 30)
        y = 232
        alto_img = 396
        caja_alto = alto_img + 142
        d.rectangle([x, y, x + ancho_col, y + caja_alto], fill="#FFFFFF", outline=(230, 219, 208))
        im = Image.open(ruta).convert("RGB")
        escala = min((ancho_col - 16) / im.width, (alto_img - 16) / im.height)
        im = im.resize((int(im.width * escala), int(im.height * escala)), Image.LANCZOS)
        lienzo.paste(im, (x + (ancho_col - im.width) // 2, y + (alto_img - im.height) // 2))
        pie_de_tarjeta(d, x + 12, y + alto_img + 10, titulo, color)

    txt(d, (MARGEN, ALTO - 42), "Paleta A · terracota #B8452C · crema #FDF6F1 · arena #F5E9DE · denim #1F3A5F",
        REGULAR, SUAVE, 12)
    destino = os.path.join(SALIDA, "web-variante-2.png")
    lienzo.save(destino)
    print("ok", destino)


variante_recortada(1)
variante_tarjetas(2)

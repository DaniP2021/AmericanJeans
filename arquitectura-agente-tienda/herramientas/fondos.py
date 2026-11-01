"""Fondos generados con la paleta de la marca.

Un fondo no es un color: es color + textura + luz. Acá se arman los tres juntos, con los
valores de la paleta A (terracota y denim), para que catálogo y web compartan el mismo aire.

Uso desde otro script:

    from fondos import lino
    fondo = lino(1200, 1500)          # listo para pegar un recorte encima
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# paleta A — la aplicada en la web
CREMA = (253, 246, 241)      # #FDF6F1
ARENA = (245, 233, 222)      # #F5E9DE
TIERRA = (232, 216, 201)     # #E8D8C9
TERRACOTA = (184, 69, 44)    # #B8452C
VIVO = (226, 112, 58)        # #E2703A
ACENTO = (242, 179, 122)     # #F2B37A
DENIM = (31, 58, 95)         # #1F3A5F


def _gradiente(ancho, alto, arriba, abajo):
    """Degradé vertical entre dos colores."""
    col = Image.new("RGB", (1, alto))
    for y in range(alto):
        t = y / max(alto - 1, 1)
        col.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(arriba, abajo)))
    return col.resize((ancho, alto), Image.BILINEAR)


def _manchas(ancho, alto, semilla=7, radio=60, fuerza=4.5):
    """Manchas suaves de luz: lo que separa una foto de un fondo plano."""
    rng = np.random.default_rng(semilla)
    chico = rng.normal(0, 1, (max(alto // 40, 4), max(ancho // 40, 4)))
    img = Image.fromarray(((chico - chico.min()) / (np.ptp(chico) + 1e-9) * 255).astype(np.uint8))
    img = img.resize((ancho, alto), Image.BICUBIC).filter(ImageFilter.GaussianBlur(radio))
    a = np.asarray(img).astype(np.float32) / 255.0 - 0.5
    return a * fuerza


def _trama(ancho, alto, paso=4, fuerza=1.6):
    """Trama fina tipo lino: dos ondas cruzadas, apenas perceptibles."""
    x = np.arange(ancho)[None, :]
    y = np.arange(alto)[:, None]
    onda = (np.sin(x * np.pi / paso) * 0.5 + np.sin(y * np.pi / paso) * 0.5)
    return onda * fuerza


def _vineta(ancho, alto, fuerza=0.10):
    """Oscurece las esquinas: dirige la mirada al centro."""
    y, x = np.mgrid[0:alto, 0:ancho]
    cx, cy = ancho / 2, alto / 2
    d = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2) / 1.414
    return -(d ** 2) * 255 * fuerza


def _grano(ancho, alto, semilla=3, fuerza=2.2):
    rng = np.random.default_rng(semilla)
    return rng.normal(0, fuerza, (alto, ancho))


def lino(ancho, alto, semilla=7):
    """Fondo cálido tipo papel de algodón, con trama, manchas y viñeta."""
    base = np.asarray(_gradiente(ancho, alto, CREMA, TIERRA)).astype(np.float32)
    capa = np.zeros((alto, ancho), np.float32)
    capa += _manchas(ancho, alto, semilla)
    capa += _trama(ancho, alto)
    capa += _vineta(ancho, alto)
    capa += _grano(ancho, alto, semilla)
    out = np.clip(base + capa[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGB")


def sombra_de(im_rgba, desenfoque=18, opacidad=0.22, margen=None):
    """Sombra suave con la forma de la prenda.

    El lienzo se agranda antes de desenfocar: si no, el desenfoque se corta contra el
    borde y deja un recuadro visible sobre el fondo.
    Devuelve (imagen, margen) — hay que pegarla en (x - margen, y - margen).
    """
    margen = margen if margen is not None else int(desenfoque * 2.5)
    w, h = im_rgba.size
    alfa = Image.new("L", (w + 2 * margen, h + 2 * margen), 0)
    alfa.paste(im_rgba.split()[3], (margen, margen))
    alfa = alfa.filter(ImageFilter.GaussianBlur(desenfoque))
    a = np.asarray(alfa).astype(np.float32) * opacidad
    sombra = Image.new("RGBA", alfa.size, (90, 66, 50, 0))
    sombra.putalpha(Image.fromarray(a.astype(np.uint8)))
    return sombra, margen


def apoyo(ancho, alto, semilla=7):
    """Fondo lino con un halo de luz central."""
    base = lino(ancho, alto, semilla)
    halo = Image.new("L", (ancho, alto), 0)
    ImageDraw.Draw(halo).ellipse(
        (ancho * 0.14, alto * 0.06, ancho * 0.86, alto * 0.78), fill=70)
    halo = halo.filter(ImageFilter.GaussianBlur(min(ancho, alto) * 0.14))
    return Image.composite(Image.new("RGB", (ancho, alto), CREMA), base, halo)

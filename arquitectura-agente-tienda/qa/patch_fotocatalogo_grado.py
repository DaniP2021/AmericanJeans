"""Agrega a fotocatalogo: grado de producto (color fiel) y enderezado opcional."""

import os

RUTA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "herramientas", "fotocatalogo.py"))

with open(RUTA, encoding="utf-8") as f:
    s = f.read()

# 1) función de grado de producto
s = s.replace('''def grado(im: Image.Image, con_grano: bool = True) -> Image.Image:''',
'''def grado_producto(im: Image.Image) -> Image.Image:
    """Color fiel: sólo balance de blancos y un contraste mínimo. Sin calidez ni grano.

    Para catálogo manda la fidelidad: si el beige sale rosado, el cliente devuelve
    la prenda por "no es el color de la foto".
    """
    from PIL import ImageEnhance, ImageOps  # noqa: PLC0415

    sys.path.insert(0, os.path.join(AQUI, "..", "qa"))
    from grado_casa import balance_blancos  # noqa: PLC0415

    im = balance_blancos(im)
    im = ImageOps.autocontrast(im, cutoff=0.3)
    return ImageEnhance.Contrast(im).enhance(1.02)


def grado(im: Image.Image, con_grano: bool = True) -> Image.Image:''')

# 2) selector de grado en procesar()
s = s.replace('''        base = encuadrar_original(im, opciones.ratio)
        if opciones.grado:
            base = grado(base, opciones.grano)''',
'''        base = encuadrar_original(im, opciones.ratio)
        base = aplicar_grado(base, opciones)''')

s = s.replace('''        base = componer_con_fondo(sujeto, opciones.ratio, opciones.margen, opciones.fondo)
        if opciones.grado:
            base = grado(base, opciones.grano)''',
'''        base = componer_con_fondo(sujeto, opciones.ratio, opciones.margen, opciones.fondo)
        base = aplicar_grado(base, opciones)''')

# 3) helper de selección + rotación del sujeto
s = s.replace('''def procesar(ruta: str, opciones) -> list[tuple[str, int, int, float]]:''',
'''def aplicar_grado(im: Image.Image, opciones) -> Image.Image:
    modo = opciones.grado
    if modo == "ninguno":
        return im
    if modo == "producto":
        return grado_producto(im)
    return grado(im, opciones.grano)


def procesar(ruta: str, opciones) -> tuple[list[tuple[str, Image.Image]], str]:''')

s = s.replace('''        if fraccion > 0.95:''',
'''        if getattr(opciones, "rotar", 0):
            sujeto = sujeto.rotate(opciones.rotar, resample=Image.BICUBIC, expand=True)

        if fraccion > 0.95:''')

# 4) opciones de línea de comandos
s = s.replace('''    p.add_argument("--grano", dest="grano", action="store_true", default=True)
    p.add_argument("--sin-grano", dest="grano", action="store_false")
    p.add_argument("--grado", dest="grado", action="store_true", default=True)
    p.add_argument("--sin-grado", dest="grado", action="store_false")''',
'''    p.add_argument("--grano", dest="grano", action="store_true", default=True)
    p.add_argument("--sin-grano", dest="grano", action="store_false")
    p.add_argument("--grado", default="producto", choices=["producto", "editorial", "ninguno"],
                   help="producto = color fiel (defecto) · editorial = con calidez y grano · ninguno")
    p.add_argument("--sin-grado", dest="grado", action="store_const", const="ninguno")
    p.add_argument("--rotar", type=float, default=0.0,
                   help="grados a enderezar la prenda (positivo = antihorario)")''')

with open(RUTA, "w", encoding="utf-8") as f:
    f.write(s)

print("parcheado:", RUTA)

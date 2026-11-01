"""Grado de color de la casa: aplica el mismo tratamiento a cualquier foto.

La consistencia hace que un catálogo de fotos distintas parezca una sola producción.
Se usa igual sobre una foto de celular que sobre una imagen editada.

Uso: python qa/grado_casa.py <entrada> <salida> [--ratio 4:5] [--ancho 720]
"""

import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageOps


def balance_blancos(im: Image.Image) -> Image.Image:
    """Gray-world: corrige dominantes de color (la luz del local suele ser amarilla)."""
    arr = np.asarray(im).astype(np.float32)
    medias = arr.reshape(-1, 3).mean(axis=0)
    objetivo = medias.mean()
    factor = np.clip(objetivo / np.maximum(medias, 1), 0.85, 1.18)
    arr = np.clip(arr * factor, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def curva_suave(im: Image.Image) -> Image.Image:
    """Contraste tipo película: negros apenas levantados, luces sin quemar."""
    lut = []
    for i in range(256):
        x = i / 255
        y = x + 0.10 * np.sin((x - 0.5) * np.pi) * (1 - abs(x - 0.5) * 1.2)
        y = max(0.0, min(1.0, y))
        y = 0.03 + y * 0.94          # levanta el negro y baja el blanco puro
        lut.append(int(round(y * 255)))
    return im.point(lut * 3)


def calidez(im: Image.Image, r=1.02, b=0.985) -> Image.Image:
    arr = np.asarray(im).astype(np.float32)
    arr[..., 0] = np.clip(arr[..., 0] * r, 0, 255)
    arr[..., 2] = np.clip(arr[..., 2] * b, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def grano(im: Image.Image, intensidad=3.2) -> Image.Image:
    """Grano fino: quita el aspecto 'render' y empareja fotos de distinta fuente."""
    arr = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(7)
    ruido = rng.normal(0, intensidad, arr.shape[:2])[..., None]
    # el grano se nota menos en las luces altas
    lum = arr.mean(axis=2, keepdims=True) / 255
    peso = 1 - np.clip((lum - 0.75) / 0.25, 0, 1) * 0.7
    arr = np.clip(arr + ruido * peso, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def vineta(im: Image.Image, fuerza=0.12) -> Image.Image:
    ancho, alto = im.size
    y, x = np.ogrid[:alto, :ancho]
    cx, cy = ancho / 2, alto / 2
    d = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2) / np.sqrt(2)
    mascara = 1 - fuerza * np.clip(d, 0, 1) ** 2
    arr = np.asarray(im).astype(np.float32) * mascara[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def grado(im: Image.Image) -> Image.Image:
    im = balance_blancos(im)
    im = ImageOps.autocontrast(im, cutoff=0.4)
    im = curva_suave(im)
    im = calidez(im)
    im = ImageEnhance.Color(im).enhance(0.92)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = grano(im)
    im = vineta(im)
    return im


def recortar(im: Image.Image, ratio: float) -> Image.Image:
    """Recorte centrado al ratio pedido, sin deformar."""
    ancho, alto = im.size
    if ancho / alto > ratio:
        nuevo = (int(alto * ratio), alto)
    else:
        nuevo = (ancho, int(ancho / ratio))
    return ImageOps.fit(im, nuevo, Image.LANCZOS, centering=(0.5, 0.42))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    entrada, salida = sys.argv[1], sys.argv[2]
    ratio = 4 / 5
    ancho_salida = 720
    for i, arg in enumerate(sys.argv):
        if arg == "--ratio" and i + 1 < len(sys.argv):
            a, b = sys.argv[i + 1].split(":")
            ratio = float(a) / float(b)
        if arg == "--ancho" and i + 1 < len(sys.argv):
            ancho_salida = int(sys.argv[i + 1])

    im = Image.open(entrada).convert("RGB")
    im = recortar(im, ratio)
    im = grado(im)
    alto_salida = round(ancho_salida * ratio)
    im = im.resize((ancho_salida, alto_salida), Image.LANCZOS)
    im.save(salida, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"ok {salida} {im.size}")

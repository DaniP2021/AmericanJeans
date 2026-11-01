"""fotocatalogo — procesa fotos crudas de prendas y devuelve imágenes listas para el catálogo.

Qué resuelve: la consistencia. Todas las fotos salen con la misma proporción, el mismo
margen alrededor de la prenda, el mismo fondo y el mismo color. Sin eso, un catálogo
parece una colección de fotos sueltas, aunque cada una sea buena.

Uso típico:

    python herramientas/fotocatalogo.py --entrada fotos/crudas --salida fotos/catalogo

    # prendas colgadas o apoyadas, recortadas sobre blanco
    python herramientas/fotocatalogo.py -e fotos/crudas -s fotos/catalogo --fondo blanco --ratio 4:5

    # fotos con fondo propio (maniquí en el local), solo encuadre y color
    python herramientas/fotocatalogo.py -e fotos/local -s fotos/catalogo --fondo original --ratio 1:1

Opciones principales:
    --ratio      4:5 (defecto) · 1:1 · 3:4 · 16:9
    --fondo      blanco (defecto) · neutro · original · transparente
    --margen     fracción de aire alrededor de la prenda (defecto 0.08)
    --ancho      ancho de la versión maestra (defecto 1600)
    --webp       además del JPG, exportar WebP
    --sin-grano  no agregar grano
    --sin-grado  no tocar color ni contraste (solo geometría)
    --reporte    ruta del CSV (defecto: <salida>/reporte.csv)
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", ".pylibs")))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "qa")))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageOps  # noqa: E402

EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
RATIOS = {"4:5": 4 / 5, "1:1": 1.0, "3:4": 3 / 4, "16:9": 16 / 9, "2:3": 2 / 3}

MODELO = os.path.abspath(os.path.join(AQUI, "..", "..", ".models", "u2net.onnx"))
_sesion = None


def sesion():
    """Carga perezosa del modelo de segmentación (una sola vez por corrida)."""
    global _sesion
    if _sesion is None:
        import onnxruntime as ort
        _sesion = ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])
    return _sesion


def segmentar(im: Image.Image) -> Image.Image:
    """Máscara de la prenda/persona (0-255) al tamaño original."""
    s = sesion()
    nombre = s.get_inputs()[0].name
    chica = im.convert("RGB").resize((320, 320), Image.LANCZOS)
    a = np.asarray(chica).astype(np.float32) / 255.0
    a = (a - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    a = a.transpose(2, 0, 1)[None, ...].astype(np.float32)
    salida = s.run(None, {nombre: a})[0][0, 0]
    salida = (salida - salida.min()) / (salida.max() - salida.min() + 1e-8)
    return Image.fromarray((salida * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS)


def recortar_sujeto(im: Image.Image, umbral=115, rampa=80, piezas=0.35):
    """Devuelve (RGBA recortado, fracción de área del sujeto, toca_borde)."""
    m = np.asarray(segmentar(im)).astype(np.float32)
    m = np.clip((m - umbral) / rampa, 0, 1)
    alfa = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))

    import cv2  # noqa: PLC0415

    arr = np.asarray(alfa)
    if not (arr > 40).any():
        return None, 0.0, False

    # se queda con el objeto principal y mide cuánto descartó
    n, etiquetas, stats, _ = cv2.connectedComponentsWithStats((arr > 100).astype(np.uint8), connectivity=8)
    descartado = 0.0
    if n > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        mayor = float(areas.max())
        minimo = mayor * piezas
        permitidas = [i + 1 for i, ar in enumerate(areas) if ar >= minimo]
        conservado = float(sum(areas[i - 1] for i in permitidas))
        total = float(areas.sum())
        descartado = 1.0 - (conservado / total) if total else 0.0
        arr = np.where(np.isin(etiquetas, permitidas), arr, 0).astype(np.uint8)
        alfa = Image.fromarray(arr)

    ys, xs = np.where(arr > 40)
    if not len(xs):
        return None, 0.0, False

    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    fraccion = ((x1 - x0) * (y1 - y0)) / (im.width * im.height)

    # el borde inferior se ignora: muchas fotos de prendas se cortan a la rodilla y está bien
    toca = (x0 <= 2) or (y0 <= 2) or (x1 >= im.width - 3)

    # si se descartó mucho, había objetos sueltos en el cuadro
    if descartado > 0.30:
        toca = True

    rgba = np.dstack([np.asarray(im), np.asarray(alfa)]).astype(np.uint8)
    recorte = Image.fromarray(rgba, "RGBA").crop((x0, y0, x1 + 1, y1 + 1))
    return recorte, float(fraccion), bool(toca)


def fondo_de(tipo: str, alto: int, ancho: int) -> Image.Image:
    if tipo == "blanco":
        return Image.new("RGB", (ancho, alto), "#FFFFFF")
    if tipo == "neutro":
        base = Image.new("RGB", (ancho, alto), "#EFE9E3")
        d = ImageDraw.Draw(base)
        for i in range(alto):
            t = i / alto
            d.line([(0, i), (ancho, i)],
                   fill=(int(242 - 26 * t), int(236 - 26 * t), int(230 - 26 * t)))
        return base
    return Image.new("RGB", (ancho, alto), "#FFFFFF")


def componer_con_fondo(sujeto: Image.Image, ratio: float, margen: float, tipo_fondo: str) -> Image.Image:
    """Centra la prenda en un lienzo del ratio pedido, con margen parejo."""
    w_s, h_s = sujeto.size
    util = 1 - 2 * margen
    lienzo_w = max(int(w_s / util), int(h_s * ratio / util))
    lienzo_h = int(lienzo_w / ratio)
    if lienzo_h * util < h_s:            # la altura manda
        lienzo_h = int(h_s / util)
        lienzo_w = int(lienzo_h * ratio)

    canvas = fondo_de(tipo_fondo, lienzo_h, lienzo_w)
    px = (lienzo_w - w_s) // 2
    py = (lienzo_h - h_s) // 2

    if tipo_fondo != "original":
        sombra = Image.new("L", (lienzo_w, lienzo_h), 0)
        ImageDraw.Draw(sombra).ellipse(
            (px + w_s * 0.05, py + h_s * 0.94, px + w_s * 0.95, py + h_s * 1.03),
            fill=42)
        sombra = sombra.filter(ImageFilter.GaussianBlur(lienzo_w * 0.02))
        canvas = Image.composite(Image.new("RGB", canvas.size, "#CFC8C0"), canvas, sombra)

    canvas.paste(sujeto, (px, py), sujeto)
    return canvas


def encuadrar_original(im: Image.Image, ratio: float) -> Image.Image:
    """Recorte centrado sin segmentar (para fotos con fondo propio)."""
    ancho, alto = im.size
    if ancho / alto > ratio:
        nuevo = (int(alto * ratio), alto)
    else:
        nuevo = (ancho, int(ancho / ratio))
    return ImageOps.fit(im, nuevo, Image.LANCZOS, centering=(0.5, 0.4))


def grado_producto(im: Image.Image) -> Image.Image:
    """Color fiel: no se toca nada.

    Cualquier corrección automática (balance de blancos, autocontraste) se equivoca
    cuando el cuadro es casi todo fondo: el gris medio del lienzo arrastra el de la
    prenda y el beige termina marrón. Para catálogo manda la fidelidad, así que la
    foto sale tal como se disparó, sólo recortada y compuesta.
    """
    return im


def grado(im: Image.Image, con_grano: bool = True) -> Image.Image:
    sys.path.insert(0, os.path.join(AQUI, "..", "qa"))
    from grado_casa import balance_blancos, calidez, curva_suave, grano  # noqa: PLC0415

    im = balance_blancos(im)
    im = curva_suave(im)
    im = calidez(im, r=1.005, b=0.995)
    if con_grano:
        im = grano(im, 1.6)
    return im


def aplicar_grado(im: Image.Image, opciones) -> Image.Image:
    modo = opciones.grado
    if modo == "ninguno":
        return im
    if modo == "producto":
        return grado_producto(im)
    return grado(im, opciones.grano)


def procesar(ruta: str, opciones) -> tuple[list[tuple[str, Image.Image]], str]:
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    aviso = ""

    if opciones.fondo == "original":
        base = encuadrar_original(im, opciones.ratio)
        base = aplicar_grado(base, opciones)
        capas = [("", base)]
    else:
        sujeto, fraccion, toca_borde = recortar_sujeto(im, piezas=opciones.piezas)
        if sujeto is None:
            raise RuntimeError("no se detectó la prenda en la foto")
        if getattr(opciones, "rotar", 0):
            sujeto = sujeto.rotate(opciones.rotar, resample=Image.BICUBIC, expand=True)

        if fraccion > 0.95:
            aviso = "el recorte ocupa casi todo: probablemente no haya fondo que quitar"
        elif fraccion < 0.04:
            aviso = "objeto muy chico: acercate o recortá antes de procesar"
        elif toca_borde:
            aviso = "REVISAR: había otros objetos en el cuadro o la prenda se sale del encuadre"

        base = componer_con_fondo(sujeto, opciones.ratio, opciones.margen, opciones.fondo)
        base = aplicar_grado(base, opciones)

        if opciones.fondo == "transparente":
            lienzo = Image.new("RGBA", base.size, (255, 255, 255, 0))
            w_s, h_s = sujeto.size
            util = 1 - 2 * opciones.margen
            lienzo_w = max(int(w_s / util), int(h_s * opciones.ratio / util))
            lienzo_h = int(lienzo_w / opciones.ratio)
            lienzo = Image.new("RGBA", (lienzo_w, lienzo_h), (0, 0, 0, 0))
            lienzo.paste(sujeto, ((lienzo_w - w_s) // 2, (lienzo_h - h_s) // 2), sujeto)
            base = lienzo
            capas = [("-transparente", base)]
        else:
            capas = [("", base)]

    ancho_master = opciones.ancho
    alto_master = round(ancho_master / opciones.ratio)
    resultados = []
    for sufijo, capa in capas:
        master = capa.resize((ancho_master, alto_master), Image.LANCZOS)
        resultados.append((sufijo, master))
    return resultados, aviso


def nombre_salida(base: str, sufijo: str, ancho: int) -> str:
    return f"{base}{sufijo}-{ancho}"


def main():
    p = argparse.ArgumentParser(description="Prepara fotos de prendas para el catálogo.")
    p.add_argument("-e", "--entrada", required=True, help="carpeta con las fotos crudas (o un archivo)")
    p.add_argument("-s", "--salida", required=True, help="carpeta donde dejar el resultado")
    p.add_argument("--ratio", default="4:5", choices=list(RATIOS), help="proporción de salida")
    p.add_argument("--fondo", default="blanco", choices=["blanco", "neutro", "original", "transparente"])
    p.add_argument("--margen", type=float, default=0.08, help="aire alrededor de la prenda (0 a 0.3)")
    p.add_argument("--ancho", type=int, default=1600, help="ancho de la versión maestra")
    p.add_argument("--webp", action="store_true", help="exportar también WebP")
    p.add_argument("--grano", dest="grano", action="store_true", default=True)
    p.add_argument("--sin-grano", dest="grano", action="store_false")
    p.add_argument("--grado", default="producto", choices=["producto", "editorial", "ninguno"],
                   help="producto = color fiel (defecto) · editorial = con calidez y grano · ninguno")
    p.add_argument("--sin-grado", dest="grado", action="store_const", const="ninguno")
    p.add_argument("--piezas", type=float, default=0.35,
                   help="qué piezas conservar: 0.35 = sólo la principal · 0.08 = conjuntos de varias prendas")
    p.add_argument("--modelo", default="grande", choices=["grande", "chico"],
                   help="grande = mejor calidad y más lento (defecto) · chico = rápido")
    p.add_argument("--rotar", type=float, default=0.0,
                   help="grados a enderezar la prenda (positivo = antihorario)")
    p.add_argument("--reporte", default=None, help="ruta del CSV de control")
    opciones = p.parse_args()

    global MODELO
    if opciones.modelo == "chico":
        MODELO = os.path.abspath(os.path.join(AQUI, "..", "..", ".models", "u2netp.onnx"))

    opciones.ratio_valor = RATIOS[opciones.ratio]
    opciones.ratio = opciones.ratio_valor

    if not 0 <= opciones.margen <= 0.3:
        print("El margen debe estar entre 0 y 0.3")
        sys.exit(2)

    if os.path.isdir(opciones.entrada):
        archivos = sorted(
            os.path.join(opciones.entrada, f) for f in os.listdir(opciones.entrada)
            if os.path.splitext(f)[1].lower() in EXTENSIONES)
    else:
        archivos = [opciones.entrada]

    if not archivos:
        print("No hay imágenes en la entrada.")
        sys.exit(2)

    os.makedirs(opciones.salida, exist_ok=True)
    reporte = opciones.reporte or os.path.join(opciones.salida, "reporte.csv")
    filas = []
    ok = fallidos = 0

    print(f"{len(archivos)} foto(s) · ratio {opciones.ratio} · fondo {opciones.fondo} · margen {opciones.margen}")
    print()

    for ruta in archivos:
        base = os.path.splitext(os.path.basename(ruta))[0]
        try:
            capas, aviso = procesar(ruta, opciones)
        except Exception as e:
            fallidos += 1
            print(f"  ✗ {base}: {e}")
            filas.append([base, "", "", "", "", opciones.fondo, f"ERROR: {e}"])
            continue

        for sufijo, master in capas:
            for ancho in (opciones.ancho, 720, 360):
                alto = round(ancho / opciones.ratio)
                salida = master.resize((ancho, alto), Image.LANCZOS)
                destino = os.path.join(opciones.salida, nombre_salida(base, sufijo, ancho) + ".jpg")
                salida.convert("RGB").save(destino, "JPEG", quality=86, optimize=True, progressive=True)
                kb = os.path.getsize(destino) / 1024
                filas.append([base, os.path.basename(destino), ancho, alto, f"{kb:.0f}",
                              opciones.fondo, aviso])
                if ancho == opciones.ancho:
                    print(f"  ✓ {os.path.basename(destino):32} {ancho}x{alto}  {kb:5.0f} KB"
                          + (f"  ⚠ {aviso}" if aviso else ""))
                if opciones.webp:
                    destino_w = destino.replace(".jpg", ".webp")
                    salida.convert("RGB").save(destino_w, "WEBP", quality=88, method=4)
                    filas.append([base, os.path.basename(destino_w), ancho, alto,
                                  f"{os.path.getsize(destino_w) / 1024:.0f}", opciones.fondo, aviso])
        ok += 1

    with open(reporte, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["origen", "archivo", "ancho", "alto", "kb", "fondo", "aviso"])
        w.writerows(filas)

    print()
    print(f"Listo: {ok} procesadas, {fallidos} con error.")
    print(f"Reporte: {reporte}")
    print(f"Fecha: {datetime.now():%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()

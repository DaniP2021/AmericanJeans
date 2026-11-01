"""Kit para el catálogo de WhatsApp Business.

Genera, por producto:
  - imagen 1:1 de 1080 px (WhatsApp muestra las fichas cuadradas)
  - una línea de descripción corta para pegar
  - un CSV para cargar en Commerce Manager o para tener de control

El catálogo de WhatsApp Business no acepta un archivo con los productos: en la app se cargan
de a uno, y por Commerce Manager se sube un feed. Esto deja todo listo para cualquiera de los dos.
"""

import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas"))

from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

from fondos import apoyo  # noqa: E402

TRANSP = os.path.join(RAIZ, "CATALOGO", "seleccion-transparente")
SALIDA = os.path.join(RAIZ, "CATALOGO", "whatsapp")
LADO = 1080

# slug, nombre para la ficha, descripción corta
FICHAS = [
    ("gabardina-corte-chino-beige", "Gabardina corte chino - Beige",
     "Pantalón de gabardina corte chino. Color beige. Consultá talles disponibles."),
    ("gabardina-corte-chino-verde-oliva", "Gabardina corte chino - Verde oliva",
     "Pantalón de gabardina corte chino. Color verde oliva. Consultá talles disponibles."),
    ("gabardina-corte-chino-tres-colores", "Gabardina corte chino - Tres colores",
     "Pantalón de gabardina corte chino. Beige, blanco y verde oliva. Consultá talles."),
    ("gabardina-corte-jean-slim-fit-azul-y-negro", "Gabardina corte jean slim fit",
     "Pantalón de gabardina corte jean, calce slim fit. Azul y negro. Consultá talles."),
    ("gabardina-recto-expansible-corte-chino-cuatro-colores", "Gabardina recto expansible corte chino",
     "Pantalón de gabardina recto con cintura expansible. Cuatro colores. Consultá talles."),
    ("pantalon-cargo-de-microfibra-cuatro-colores", "Pantalón cargo de microfibra",
     "Pantalón cargo de microfibra con bolsillos de carga. Cuatro colores."),
    ("jean-clasico-tres-lavados", "Jean clásico - Tres lavados",
     "Jean clásico. Tres lavados: azul oscuro, celeste y negro. Consultá talles."),
    ("bermuda-elastizada-corte-jean-negro-y-azul", "Bermuda elastizada corte jean",
     "Bermuda elastizada corte jean. Negro y azul. Consultá talles."),
    ("pantalon-de-vestir-cuatro-colores", "Pantalón de vestir",
     "Pantalón de vestir, cuatro colores: gris, azul, blanco y negro. Consultá talles."),
    ("camisa-lisa-seis-colores", "Camisa de vestir",
     "Camisa lisa de manga larga, seis colores. Consultá talles."),
    ("corbata-lisa-varios-colores", "Corbata lisa",
     "Corbata lisa. Negro, azul, rojo y verde. Consultá disponibilidad."),
    ("chaleco-de-vestir-negro", "Chaleco de vestir",
     "Chaleco de vestir negro, tres botones y bolsillos de filete. Consultá talles."),
    ("look-camisas-y-pantalon-de-vestir", "Camisas lisas con pantalón de vestir",
     "Combinación armada: camisa lisa y pantalón de vestir. Consultá colores y talles."),
    ("look-camisa-de-vestir-con-corbata", "Camisa de vestir con corbata",
     "Combinación armada: camisa de vestir con corbata a juego. Consultá colores y talles."),
    ("sweter-cuello-v-azul-marino", "Sweter cuello V",
     "Sweter de cuello V, tejido. Azul marino. Consultá talles."),
    ("sweter-medio-cierre", "Sweter medio cierre",
     "Sweter con medio cierre y cuello alto. Azul y negro. Consultá talles."),
    ("camisa-estampada-manga-larga-seis-colores", "Camisa estampada manga larga",
     "Camisa de manga larga con estampado de puntos. Seis colores. Consultá talles."),
    ("chomba-rayada-cuatro-colores", "Chomba rayada",
     "Chomba rayada con cuello tejido. Cuatro colores. Consultá talles."),
    ("conjunto-deportivo-wafle-negro", "Conjunto deportivo - Negro",
     "Conjunto deportivo: camiseta y short. Color negro. Consultá talles."),
    ("conjunto-deportivo-wafle-blanco", "Conjunto deportivo - Blanco",
     "Conjunto deportivo: camiseta y short. Color blanco. Consultá talles."),
    ("conjunto-deportivo-wafle-bordo", "Conjunto deportivo - Bordó",
     "Conjunto deportivo: camiseta y short. Color bordó. Consultá talles."),
    ("conjunto-deportivo-oliva-negro", "Conjunto deportivo de microfibra",
     "Conjunto deportivo de microfibra, oliva y negro, con etiqueta American Jeans."),
    ("pantalon-con-tres-chombas-bordo-blanco-marino", "Pantalón con tres chombas - Bordó",
     "Combinación: pantalón con tres chombas (bordó, blanco y azul marino)."),
    ("pantalon-con-tres-chombas-rojo-blanco-marino", "Pantalón con tres chombas - Rojo",
     "Combinación: pantalón con tres chombas (rojo, blanco y azul marino)."),
]

# Muestras de prueba: quedan fuera hasta que lleguen las fotos de producción.
EXCLUIR = {
    "gabardina-corte-chino-beige",
    "gabardina-corte-chino-verde-oliva",
    "gabardina-corte-chino-tres-colores",
    "conjunto-deportivo-wafle-negro",
    "conjunto-deportivo-wafle-blanco",
    "conjunto-deportivo-wafle-bordo",
}
FICHAS = [f for f in FICHAS if f[0] not in EXCLUIR]


def cuadrada(slug, ruta):
    prenda = Image.open(ruta).convert("RGBA")
    margen = 0.10
    util = LADO * (1 - 2 * margen)
    escala = min(util / prenda.width, util / prenda.height)
    prenda = prenda.resize((int(prenda.width * escala), int(prenda.height * escala)), Image.LANCZOS)

    fondo = Image.new("RGB", (LADO, LADO), "#FFFFFF")
    x = (LADO - prenda.width) // 2
    y = (LADO - prenda.height) // 2

    sombra = Image.new("L", (LADO, LADO), 0)
    capa = Image.new("L", (prenda.width + 80, prenda.height + 80), 0)
    capa.paste(prenda.split()[3], (40, 40))
    capa = capa.filter(ImageFilter.GaussianBlur(18))
    sombra.paste(capa.point(lambda v: int(v * 0.18)), (x - 40 + 4, y - 40 + 8))
    fondo.paste(Image.new("RGB", (LADO, LADO), "#B9B0A8"), (0, 0), sombra)
    fondo.paste(prenda, (x, y), prenda)
    return fondo


def main():
    os.makedirs(SALIDA, exist_ok=True)
    filas = []
    for slug, nombre, descripcion in FICHAS:
        ruta = os.path.join(TRANSP, slug + "-1200.webp")
        if not os.path.exists(ruta):
            print("falta:", slug)
            continue
        img = cuadrada(slug, ruta)
        destino = os.path.join(SALIDA, slug + "-1080.jpg")
        img.save(destino, "JPEG", quality=86, optimize=True, progressive=True)
        kb = os.path.getsize(destino) / 1024
        filas.append([nombre, descripcion, "", "ARS", slug, slug + "-1080.jpg"])
        print(f"ok {slug}-1080.jpg  {kb:.0f} KB")

    with open(os.path.join(SALIDA, "catalogo-whatsapp.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["nombre", "descripcion", "precio", "moneda", "sku", "imagen"])
        w.writerows(filas)

    with open(os.path.join(SALIDA, "fichas-para-copiar.md"), "w", encoding="utf-8") as f:
        f.write("# Fichas para cargar en WhatsApp Business\n\n")
        f.write("Nombre y descripción listos para pegar. El precio queda vacío hasta que se defina.\n\n")
        for nombre, descripcion, _p, _m, sku, imagen in filas:
            f.write(f"## {nombre}\n\n**Precio:** a definir\n\n**Descripción:**\n{descripcion}\n\n")
            f.write(f"**Imagen:** `{imagen}`\n\n**SKU:** `{sku}`\n\n---\n\n")
    print(f"\n{len(filas)} fichas · CSV y textos generados en {SALIDA}")


if __name__ == "__main__":
    main()

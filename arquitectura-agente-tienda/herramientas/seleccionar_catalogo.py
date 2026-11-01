"""Arma la selección del catálogo: copia las elegidas, aparta el resto y genera la grilla.

Criterio de selección:
- una imagen por familia con varias prendas (gama de colores) o por prenda individual
- se descartan las que tienen recortes fallidos, prendas cortadas o superposiciones que
  impiden leer la prenda principal
"""

import os
import shutil

RAIZ = r"CATALOGO"
SEL = os.path.join(RAIZ, "seleccion")
DES = os.path.join(RAIZ, "descartadas")

# (carpeta-origen, archivo-1200, categoría, nombre visible, color)
ELEGIDAS = [
    (r"", "gabardina-beige-1200.jpg", "Pantalones", "Gabardina corte chino", "Beige"),
    (r"", "gabardina-verde-1200.jpg", "Pantalones", "Gabardina corte chino", "Verde oliva"),
    (r"", "gabardina-beige-abierta-1200.jpg", "Pantalones", "Gabardina corte chino", "Tres colores"),
    (r"conjuntos\procesadas", "conjunto-negro-1200.jpg", "Deportivo", "Conjunto deportivo wafle", "Negro"),
    (r"conjuntos\procesadas", "conjunto-blanco-1200.jpg", "Deportivo", "Conjunto deportivo wafle", "Blanco"),
    (r"conjuntos\procesadas", "conjunto-bordo-1200.jpg", "Deportivo", "Conjunto deportivo wafle", "Bordó"),
    (r"cargo\procesadas", "cargo-grupo-1200.jpg", "Pantalones", "Pantalón cargo de microfibra", "Cuatro colores"),
    (r"chombas\procesadas", "chombas-grupo-3-1200.jpg", "Chombas", "Chomba rayada", "Cuatro colores"),
    (r"camisas\procesadas", "camisas-estampadas-2-1200.jpg", "Camisas", "Camisa estampada manga larga", "Seis colores"),
    (r"jeans\procesadas", "jeans-3-1200.jpg", "Jeans", "Jean clásico", "Tres lavados"),
    (r"bermudas\procesadas", "bermudas-grupo-3-1200.jpg", "Bermudas", "Bermuda elastizada corte jean", "Negro y azul"),
    (r"jean-chombas\procesadas", "jean-chombas-1200.jpg", "Combinaciones", "Pantalón con tres chombas", "Bordó, blanco, marino"),
    (r"jean-chombas\procesadas", "pantalon-chombas-2-1200.jpg", "Combinaciones", "Pantalón con tres chombas", "Rojo, blanco, marino"),
]

# lo que queda afuera, con motivo
DESCARTADAS = [
    (r"conjuntos\procesadas", "conjunto-verde-1200.jpg", "el verde no se separa del fondo verde"),
    (r"cargo\procesadas", "cargo-grupo-2-1200.jpg", "misma información que la versión elegida"),
    (r"chombas\procesadas", "chombas-grupo-1200.jpg", "manga cortada en el origen"),
    (r"chombas\procesadas", "chombas-grupo-2-1200.jpg", "falta la chomba negra abierta"),
    (r"bermudas\procesadas", "bermudas-grupo-1200.jpg", "prendas superpuestas"),
    (r"bermudas\procesadas", "bermudas-grupo-2-1200.jpg", "reemplazada por la version elegida"),
    (r"jeans\procesadas", "jeans-1200.jpg", "reemplazada por la version de los tres lavados enfrentados"),
    (r"jeans\procesadas", "jeans-2-1200.jpg", "misma toma que la anterior, menos clara"),
    (r"camisas\procesadas", "camisas-estampadas-1200.jpg", "reemplazada por la de seis colores"),
]


def slug(texto):
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", " ": "-"}
    t = texto.lower()
    for a, b in reemplazos.items():
        t = t.replace(a, b)
    return "".join(c for c in t if c.isalnum() or c == "-")


def main():
    for carpeta in (SEL, DES):
        os.makedirs(carpeta, exist_ok=True)

    filas = []
    for origen, archivo, categoria, titulo, color in ELEGIDAS:
        ruta = os.path.join(RAIZ, origen, archivo) if origen else os.path.join(RAIZ, "procesadas", archivo)
        if not os.path.exists(ruta):
            print("FALTA:", ruta)
            continue
        destino_nombre = f"{slug(titulo)}-{slug(color)}"
        shutil.copy2(ruta, os.path.join(SEL, destino_nombre + "-1200.jpg"))
        ruta720 = ruta.replace("-1200.jpg", "-720.jpg")
        if os.path.exists(ruta720):
            shutil.copy2(ruta720, os.path.join(SEL, destino_nombre + "-720.jpg"))
        filas.append((destino_nombre, categoria, titulo, color))
        print("elegida:", destino_nombre)

    for origen, archivo, motivo in DESCARTADAS:
        ruta = os.path.join(RAIZ, origen, archivo)
        if not os.path.exists(ruta):
            continue
        shutil.move(ruta, os.path.join(DES, archivo))
        for sufijo in ("-720", "-360"):
            otra = ruta.replace("-1200.jpg", sufijo + ".jpg")
            if os.path.exists(otra):
                shutil.move(otra, os.path.join(DES, os.path.basename(otra)))
        print(f"descartada: {archivo} · {motivo}")

    # grilla del catálogo
    por_categoria = {}
    for nombre, categoria, titulo, color in filas:
        por_categoria.setdefault(categoria, []).append((nombre, titulo, color))

    tarjetas = []
    for categoria, items in por_categoria.items():
        for nombre, titulo, color in items:
            tarjetas.append(f"""
      <article class="producto">
        <a href="seleccion/{nombre}-1200.jpg" target="_blank">
          <img src="seleccion/{nombre}-720.jpg" alt="{titulo} {color}" loading="lazy">
        </a>
        <p class="chip">{categoria}</p>
        <h2>{titulo}</h2>
        <p class="color">{color}</p>
        <p class="precio">Precio de referencia</p>
        <a class="boton" href="#">Consultar</a>
      </article>""")

    html = f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo American Jeans — selección</title>
<style>
  :root {{ --tinta:#1C1512; --suave:#6E625B; --borde:#EBDCD1; --rojo:#B0232B; --fondo:#FDF6F1; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--fondo); color:var(--tinta);
         font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
  header {{ padding:32px 24px 20px; border-bottom:1px solid var(--borde); }}
  header h1 {{ margin:0 0 6px; font-size:1.6rem; }}
  header p {{ margin:0; color:var(--suave); font-size:.9rem; }}
  .aviso {{ margin:16px 24px; padding:12px 14px; background:#fff; border-left:3px solid var(--rojo);
            font-size:.85rem; color:var(--suave); }}
  .sello {{ margin:16px 24px; padding:16px 18px; background:var(--tinta); color:#fff; border-radius:10px;
            display:flex; gap:18px; align-items:center; flex-wrap:wrap; }}
  .sello strong {{ font-size:.95rem; }}
  .sello p {{ margin:0; font-size:.84rem; color:rgba(255,255,255,.78); line-height:1.5; max-width:640px; }}
  .sello .marca {{ font-weight:800; letter-spacing:.16em; font-size:.72rem; text-transform:uppercase;
                   color:#F2B37A; white-space:nowrap; }}
  main {{ padding:24px; display:grid; gap:22px;
          grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); }}
  .producto {{ background:#fff; border:1px solid var(--borde); border-radius:12px; padding:12px;
               display:flex; flex-direction:column; }}
  .producto img {{ width:100%; height:auto; border-radius:8px; display:block; background:#fff; }}
  .chip {{ margin:10px 0 4px; font-size:.68rem; letter-spacing:.12em; text-transform:uppercase;
           color:var(--rojo); font-weight:700; }}
  .producto h2 {{ margin:0; font-size:.98rem; line-height:1.25; }}
  .color {{ margin:2px 0 8px; font-size:.82rem; color:var(--suave); }}
  .precio {{ margin:auto 0 10px; font-size:.75rem; color:var(--suave); }}
  .boton {{ display:block; text-align:center; text-decoration:none; padding:10px;
            border:2px solid var(--tinta); border-radius:6px; font-weight:700; font-size:.85rem;
            color:var(--tinta); }}
  .boton:hover {{ background:var(--tinta); color:#fff; }}
  footer {{ padding:20px 24px 40px; color:var(--suave); font-size:.8rem; }}
</style>
</head>
<body>
  <header>
    <h1>Catálogo American Jeans</h1>
    <p>{len(filas)} imágenes seleccionadas · {len(por_categoria)} categorías · para aprobación</p>
  </header>
  <div class="aviso">
    Etapa de selección. Los precios son de referencia y todavía no se publican.
    Las imágenes descartadas están en <b>descartadas/</b>, con el motivo en la planilla del proyecto.
  </div>
  <div class=sello>
    <span class=marca>Etiqueta verificada</span>
    <p><strong>Etiqueta de marca a la vista.</strong>
    Camisas: etiqueta American Jeans cosida en el cuello. Jeans: parche de cuero American en la cintura.
    En las demás prendas la foto no alcanza a mostrar la etiqueta.</p>
  </div>
  <main>{''.join(tarjetas)}</main>
  <footer>
    Todas las imágenes son 4:5 y salieron del mismo proceso: recorte, fondo blanco, margen parejo.
    Los archivos están en <b>seleccion/</b> en 1200 y 720 px.
  </footer>
</body>
</html>"""

    with open(os.path.join(RAIZ, "catalogo.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\ncatalogo.html generado con {len(filas)} imágenes")


if __name__ == "__main__":
    main()

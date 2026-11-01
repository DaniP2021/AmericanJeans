"""Genera una galería HTML que compara fotos originales con las procesadas.

Un solo archivo para abrir y ver todo: qué entró, qué salió, cuánto pesa y con qué nombre.

Uso:
    python herramientas/galeria.py --originales fotos/crudas --procesadas fotos/catalogo --salida index.html
"""

import argparse
import base64
import io
import os

from PIL import Image


def miniatura(ruta, ancho=320):
    """Devuelve un data URI con la miniatura, para que el HTML sea un solo archivo."""
    im = Image.open(ruta).convert("RGB")
    alto = round(ancho * im.height / im.width)
    im = im.resize((ancho, alto), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def kb(ruta):
    return os.path.getsize(ruta) / 1024


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--originales", required=True)
    p.add_argument("--procesadas", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--titulo", default="Catálogo — comparación")
    a = p.parse_args()

    origs = sorted(f for f in os.listdir(a.originales)
                   if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png", ".webp"})

    filas = []
    for archivo in origs:
        base = os.path.splitext(archivo)[0]
        ruta_o = os.path.join(a.originales, archivo)
        candidatos = sorted(f for f in os.listdir(a.procesadas)
                            if f.startswith(base) and "1200" in f)
        ruta_p = os.path.join(a.procesadas, candidatos[0]) if candidatos else None
        filas.append((archivo, ruta_o, ruta_p))

    tarjetas = []
    for archivo, ruta_o, ruta_p in filas:
        im_o = Image.open(ruta_o)
        bloque_p = f"""
        <figure>
          <img src="{miniatura(ruta_p)}" alt="procesada">
          <figcaption><b>{os.path.basename(ruta_p)}</b><br>{kb(ruta_p):.0f} KB · 1200×1500</figcaption>
        </figure>""" if ruta_p else """
        <figure class="vacio"><div>sin procesar</div></figure>"""

        tarjetas.append(f"""
      <article class="par">
        <header>
          <h2>{archivo}</h2>
          <p>{im_o.width}×{im_o.height} · {kb(ruta_o):.0f} KB</p>
        </header>
        <div class="comparacion">
          <figure>
            <img src="{miniatura(ruta_o)}" alt="original">
            <figcaption><b>{archivo}</b><br>original</figcaption>
          </figure>
          <span class="flecha">→</span>
          {bloque_p}
        </div>
      </article>""")

    html = f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{a.titulo}</title>
<style>
  :root {{ --tinta:#1C1512; --suave:#6E625B; --borde:#E3DCD4; --rojo:#B0232B; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
         color:var(--tinta); background:#FBF7F3; }}
  header.top {{ padding:28px 24px 18px; border-bottom:1px solid var(--borde); }}
  header.top h1 {{ margin:0 0 6px; font-size:1.5rem; }}
  header.top p {{ margin:0; color:var(--suave); font-size:.9rem; }}
  .aviso {{ margin:16px 24px 0; padding:12px 14px; border-left:3px solid var(--rojo);
            background:#fff; font-size:.85rem; color:var(--suave); }}
  main {{ padding:24px; display:grid; gap:24px; }}
  .par {{ background:#fff; border:1px solid var(--borde); border-radius:12px; overflow:hidden; }}
  .par header {{ padding:14px 16px; border-bottom:1px solid var(--borde); }}
  .par h2 {{ margin:0; font-size:1rem; }}
  .par header p {{ margin:2px 0 0; font-size:.78rem; color:var(--suave); }}
  .comparacion {{ display:flex; align-items:center; gap:16px; padding:16px; flex-wrap:wrap; }}
  figure {{ margin:0; flex:1 1 240px; max-width:340px; }}
  figure img {{ width:100%; height:auto; display:block; border:1px solid var(--borde);
                border-radius:8px; background:#fff; }}
  figcaption {{ margin-top:6px; font-size:.72rem; color:var(--suave); line-height:1.4; }}
  .flecha {{ font-size:1.4rem; color:var(--rojo); }}
  .vacio div {{ display:grid; place-items:center; height:200px; border:1px dashed var(--borde);
                border-radius:8px; color:var(--suave); font-size:.85rem; }}
  @media (max-width:700px) {{ .flecha {{ transform:rotate(90deg); }} }}
</style>
</head>
<body>
  <header class="top">
    <h1>{a.titulo}</h1>
    <p>{len(filas)} foto(s) · original a la izquierda, resultado a la derecha</p>
  </header>
  <div class="aviso">
    Las miniaturas están embebidas: este archivo funciona solo, sin la carpeta al lado.
    Los archivos reales están en <b>{os.path.basename(os.path.normpath(a.procesadas))}/</b>.
  </div>
  <main>
{''.join(tarjetas)}
  </main>
</body>
</html>"""

    with open(a.salida, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"galería: {a.salida} ({os.path.getsize(a.salida) / 1024:.0f} KB, {len(filas)} pares)")


if __name__ == "__main__":
    main()

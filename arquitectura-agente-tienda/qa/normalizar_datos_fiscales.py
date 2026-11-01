"""Normaliza la línea de datos fiscales del pie y del bloque legal, en tipografía mínima.

El CUIT y la razón social son un dato, no un argumento: van chicos, en gris y sin negrita,
para cumplir sin ensuciar el diseño.
"""

import json
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing"))

with open(os.path.join(BASE, "datos-negocio.json"), encoding="utf-8") as f:
    cfg = json.load(f)

razon = cfg["razon_social"]
cuit = cfg["cuit"]
dir_completa = f"{cfg['sucursal']['direccion']}, CABA"
email = cfg["email"]

PIE = f'<p class="datos-fiscales">{razon} · CUIT {cuit} · {dir_completa}</p>'

# index: el pie tiene el email en la misma línea y un comentario de "completar"
VIEJO_INDEX = """    <p>
      <!-- COMPLETAR con los datos reales del vendedor -->
      American Jeans · CUIT 30-71486507-9 · Buenos Aires, Argentina ·
      <a href="mailto:hola@americanjeans.com.ar">hola@americanjeans.com.ar</a>
    </p>"""

NUEVO_INDEX = f"""    {PIE}
    <p class="datos-fiscales">
      <a href="mailto:{email}">{email}</a>
    </p>"""

VIEJO_PIE = f"<p>{razon} · CUIT {cuit} · Buenos Aires, Argentina</p>"

for archivo, viejo, nuevo in [
    ("index.html", VIEJO_INDEX, NUEVO_INDEX),
    ("talles.html", f"<p>American Jeans · CUIT {cuit} · Buenos Aires, Argentina</p>", PIE),
    (os.path.join("legal", "terminos.html"), VIEJO_PIE, PIE),
    (os.path.join("legal", "cambios.html"), VIEJO_PIE, PIE),
    (os.path.join("legal", "privacidad.html"), VIEJO_PIE, PIE),
    (os.path.join("legal", "arrepentimiento.html"), VIEJO_PIE, PIE),
]:
    ruta = os.path.join(BASE, archivo)
    with open(ruta, encoding="utf-8") as f:
        html = f.read()

    if viejo in html:
        html = html.replace(viejo, nuevo)
        estado = "ok"
    else:
        estado = "NO ENCONTRADO"

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{archivo:40} {estado}")

# domicilio: en el cuerpo legal conviene la calle sola, porque la frase ya dice
# "Ciudad Autónoma de Buenos Aires, Argentina"
for archivo in [os.path.join("legal", "terminos.html"), os.path.join("legal", "privacidad.html")]:
    ruta = os.path.join(BASE, archivo)
    with open(ruta, encoding="utf-8") as f:
        html = f.read()
    antes = html
    html = html.replace(f"con domicilio en {cfg['sucursal']['direccion']}, CABA",
                        f"con domicilio comercial en {cfg['sucursal']['direccion']}")
    if html != antes:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{archivo:40} domicilio simplificado")

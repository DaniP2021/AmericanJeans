"""Aplica los datos del negocio (`landing/datos-negocio.json`) a todas las páginas.

Cambiar el teléfono, el CUIT o la dirección tiene que ser una edición de JSON y un comando,
no trece ediciones a mano con el riesgo de dejar una vieja.
"""

import json
import os
import re

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing"))
CONFIG = os.path.join(BASE, "datos-negocio.json")

PAGINAS = ["index.html", "talles.html",
           os.path.join("legal", "terminos.html"),
           os.path.join("legal", "cambios.html"),
           os.path.join("legal", "privacidad.html"),
           os.path.join("legal", "arrepentimiento.html")]

with open(CONFIG, encoding="utf-8") as f:
    cfg = json.load(f)

numero = cfg["whatsapp_e164"]
razon = cfg["razon_social"]
cuit = cfg["cuit"]
domicilio = cfg["domicilio_comercial"]

print(f"WhatsApp: +{numero}")
print(f"Vendedor: {razon} · CUIT {cuit} · {domicilio}")
print()

PATRON_WA = re.compile(r"wa\.me/\d{8,15}")

# orden importa: primero las formas con <strong>, después las sueltas
REEMPLAZOS = [
    ("<strong>[RAZÓN SOCIAL]</strong>", razon),
    ("<strong>[CUIT]</strong>", cuit),
    ("<strong>[DOMICILIO]</strong>", domicilio),
    ("[RAZÓN SOCIAL]", razon),
    ("[CUIT]", cuit),
    ("[DOMICILIO]", domicilio),
    ("CUIT a confirmar", f"CUIT {cuit}"),
    ("American Jeans · El 73 S.R.L. ·", "El 73 S.R.L. ·"),
]

total_wa = total_datos = 0
for pagina in PAGINAS:
    ruta = os.path.join(BASE, pagina)
    with open(ruta, encoding="utf-8") as f:
        html = f.read()

    nuevo, n_wa = PATRON_WA.subn(f"wa.me/{numero}", html)
    nuevo = nuevo.replace("+24 11", "+54 11").replace("+24 9 11", "+54 9 11")

    n_datos = 0
    for viejo, valor in REEMPLAZOS:
        if viejo in nuevo:
            n_datos += nuevo.count(viejo)
            nuevo = nuevo.replace(viejo, valor)

    if nuevo != html:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(nuevo)
    print(f"{pagina:40} WhatsApp: {n_wa:2d}  datos fiscales: {n_datos}")
    total_wa += n_wa
    total_datos += n_datos

print(f"\nEnlaces actualizados: {total_wa} · Datos fiscales completados: {total_datos}")

# control 1: un solo número en todo el sitio
distintos = set()
for pagina in PAGINAS:
    with open(os.path.join(BASE, pagina), encoding="utf-8") as f:
        for m in PATRON_WA.finditer(f.read()):
            if m.group(0) != f"wa.me/{numero}":
                distintos.add(m.group(0))
print("control WhatsApp:", "OK" if not distintos else f"números distintos: {distintos}")

# control 2: no quedan marcadores fiscales
pendientes = 0
for pagina in PAGINAS:
    with open(os.path.join(BASE, pagina), encoding="utf-8") as f:
        txt = f.read()
    pendientes += txt.count("[RAZÓN SOCIAL]") + txt.count("[CUIT]") + txt.count("[DOMICILIO]")
print("control datos fiscales:", "OK" if not pendientes else f"quedan {pendientes} marcadores")

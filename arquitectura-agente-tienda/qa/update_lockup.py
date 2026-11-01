"""Reemplaza el lockup en caja (marca__caja) por el lockup tipográfico en todas las páginas."""

import os
import re

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing"))

PAGINAS = [
    "index.html", "talles.html",
    os.path.join("legal", "terminos.html"),
    os.path.join("legal", "cambios.html"),
    os.path.join("legal", "privacidad.html"),
    os.path.join("legal", "arrepentimiento.html"),
]

PATRON = re.compile(
    r'(\s*)<span class="marca__caja">.*?</span></span>\s*\n\s*<span class="marca__nombre">American Jeans</span>',
    re.DOTALL,
)

NUEVO = (
    '{ind}<span class="marca__nombre">American Jeans</span>\n'
    '{ind}<span class="marca__div" aria-hidden="true"></span>\n'
    '{ind}<span class="marca__linea">basic</span>'
)

total = 0
for pagina in PAGINAS:
    ruta = os.path.join(BASE, pagina)
    with open(ruta, encoding="utf-8") as f:
        html = f.read()

    def repl(m):
        return NUEVO.format(ind=m.group(1))

    nuevo, n = PATRON.subn(repl, html)
    if n:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(nuevo)
    print(f"{pagina:40} {n} reemplazo(s)")
    total += n

print(f"\ntotal: {total}")
restantes = 0
for pagina in PAGINAS:
    with open(os.path.join(BASE, pagina), encoding="utf-8") as f:
        restantes += f.read().count("marca__caja")
print("marca__caja restantes:", restantes)

"""Genera una página de prueba con nueve tarjetas para ver el riel en funcionamiento.

No se publica: sirve para revisar el comportamiento con más estilos de los que entran
en pantalla antes de cargar contenido real.
"""

import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing"))

with open(os.path.join(BASE, "index.html"), encoding="utf-8") as f:
    html = f.read()

# 1) control de estructura: etiquetas balanceadas
abre, cierra = html.count("<article"), html.count("</article>")
div_a, div_c = html.count("<div"), html.count("</div>")
print(f"<article> {abre}/{cierra} · <div> {div_a}/{div_c}")
assert abre == cierra and div_a == div_c, "HTML desbalanceado"

# 2) duplicar el bloque de tarjetas dos veces más, dentro del riel
inicio = html.index('<div class="looks__rail"')
fin = html.index("</div>\n\n        <div class=\"looks__nav\"")
bloque = html[inicio:fin]
solo_tarjetas = bloque[bloque.index(">") + 1:]           # sin la etiqueta de apertura del riel
nuevo = html[:fin] + solo_tarjetas * 2 + html[fin:]
nuevo = nuevo.replace("<title>American Jeans · básicos masculinos en Buenos Aires</title>",
                      "<title>PRUEBA · riel de looks con 9 tarjetas</title>")
nuevo = nuevo.replace('<h2 class="seccion__t">Un look para cada ocasión</h2>',
                      '<h2 class="seccion__t">PRUEBA · riel con 9 tarjetas</h2>')

salida = os.path.join(BASE, "_test-looks.html")
with open(salida, "w", encoding="utf-8") as f:
    f.write(nuevo)
print("ok", salida)
print("tarjetas en la prueba:", nuevo.count('<article class="look">'))

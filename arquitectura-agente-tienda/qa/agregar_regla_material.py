"""Agrega al esquema de producto la regla de cómo se nombra el material."""

import os

RUTA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                     "catalogo", "esquema-producto.md"))

BLOQUE = """
---

## 9. Cómo se nombra el material

Decidido con el caso del chaleco (hilo sintético, no lana ni lino):

1. **Se declara la fibra, siempre.** "Hilo sintético" en la tarjeta y el feed; el porcentaje exacto en la ficha cuando el proveedor lo informe (por ejemplo "100% poliéster" o "65% poliéster / 35% viscosa").
2. **No se dice lana ni lino si no lo es.** El cliente del rubro lo detecta al tacto en cinco segundos, y la devolución por "no es lo que decía" cuesta flete, tiempo y la confianza que es el diferencial de la marca.
3. **El sintético se vende por beneficio, no con vergüenza.** No encoge, no se arruga, seca rápido y mantiene la forma: para un chaleco de uso diario eso es una ventaja concreta frente a la lana, que hay que cuidar.
4. **Cuidado que corresponde a la fibra:** agua fría, plancha tibia, sin secadora. El calor es lo que deforma el sintético y lo que arruga el elastano de la gabardina expansible.
5. **En el título no va el material** (se come el espacio de la palabra clave); va en la descripción, en el primer párrafo, junto al calce.
"""

with open(RUTA, encoding="utf-8") as f:
    texto = f.read()

if "Cómo se nombra el material" in texto:
    print("ya estaba")
else:
    with open(RUTA, "w", encoding="utf-8") as f:
        f.write(texto.rstrip() + "\n" + BLOQUE)
    print("agregado")

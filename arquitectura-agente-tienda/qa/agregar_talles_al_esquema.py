"""Agrega la equivalencia oficial de talles al esquema de producto."""

import os

RUTA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                     "catalogo", "esquema-producto.md"))

BLOQUE = """
---

## 8. Talles: equivalencia oficial

| Letra | N.º | Equivale a (pantalón) |
|---|---|---|
| S | 1 | 38 |
| M | 2 | 40 |
| L | 3 | 42 |
| XL | 4 | 44 |
| XXL | 5 | 46 |
| XXXL | 6 | 48 |

Reglas de carga:

- En el CSV y en la tienda, `Variante 1 = Talle` con el **valor en letra** (`S`, `M`, `L`, `XL`, `XXL`, `XXXL`). El número (1 a 6) va en el título o en la descripción, nunca como variante: si se carga como variante, cada prenda se duplica en seis SKUs con el mismo stock.
- En la ficha y en el local la equivalencia aparece siempre junto a la letra: el cliente argentino piensa en número ("uso 42"), no en letra.
- `4XL` no existe en esta curva: termina en `XXXL = 6 = 48`. Escribirlo mal rompe la guía y la importación.
- Las medidas en centímetros se agregan cuando esté la moldería; la planilla `Guia-Talles-American-Jeans.xlsx` ya tiene las columnas preparadas.
"""

with open(RUTA, encoding="utf-8") as f:
    texto = f.read()

if "equivalencia oficial" in texto:
    print("ya estaba")
else:
    with open(RUTA, "w", encoding="utf-8") as f:
        f.write(texto.rstrip() + "\n" + BLOQUE)
    print("agregado a", os.path.basename(RUTA))

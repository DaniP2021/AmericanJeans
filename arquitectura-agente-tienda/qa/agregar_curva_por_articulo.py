"""Agrega la regla de curva por artículo al esquema de producto."""

import os

RUTA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                     "catalogo", "esquema-producto.md"))

BLOQUE = """
---

## 10. La curva de talles es por artículo, no por marca

Dato del local: no todas las prendas llegan al mismo talle.

- Pantalón de vestir, chaleco, camisa y jean: del **1 al 10 o 12** según el modelo.
- Otras prendas: arrancan en el **6**.
- Los talles **7 a 12 son especiales y no llevan letra** (la letra llega hasta XXXL = 6 = 48).

Consecuencias para el catálogo:

1. **Nunca publicar un rango global** ("talles del 1 al 12") ni en la home ni en el feed: es falso para la mitad del surtido y genera consultas que terminan en "no tengo".
2. **Cada ficha declara su curva**: los talles disponibles de esa prenda, ni uno más.
3. **La tabla de equivalencia es una escala, no una promesa**: explica cómo se lee un talle, no qué hay en stock.
4. **En el área mayorista, la curva es la unidad de venta**: cada artículo se pide por su curva completa, y esa curva también es propia del artículo.
5. **Si un talle no está, se dice con la verdad y con fecha**: "hoy no, entra con la reposición de la semana que viene" — nunca "consultá disponibilidad".
"""

with open(RUTA, encoding="utf-8") as f:
    texto = f.read()

if "curva de talles es por artículo" in texto:
    print("ya estaba")
else:
    with open(RUTA, "w", encoding="utf-8") as f:
        f.write(texto.rstrip() + "\n" + BLOQUE)
    print("agregado")

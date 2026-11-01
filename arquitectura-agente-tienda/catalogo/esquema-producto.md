# Esquema de producto — American Jeans

Un solo esquema para la landing, la tienda, el feed de Meta y la planilla. Si cambia acá, cambia en todos lados.

**Base:** los 8 campos de la ficha del plan de 90 días (sección 07) + el formato de importación de Tiendanube que ya usa `automatizacion-tienda/ejemplos/productos-tiendanube.csv`.

---

## 1. Los 8 campos obligatorios

| # | Campo | Regla | Por qué |
|---|---|---|---|
| 1 | **Título** | Marca + categoría + atributo + talle/color. Máx. 60 caracteres | SEO y búsqueda interna |
| 2 | **Fotos** | 6 a 8, en orden fijo (ver §4) | Reduce dudas y devoluciones |
| 3 | **Descripción** | 4 bloques: para qué sirve · calce · material · cuidado | Vende el beneficio, no la prenda |
| 4 | **Guía de talles** | Medidas en cm + cómo medir. Nunca sólo imagen | Primera causa de devolución |
| 5 | **Stock** | Por talle y color, actualizado a diario | Evita vender lo que no hay |
| 6 | **Precio y cuotas** | Precio final con impuestos + medios de pago | Transparencia |
| 7 | **Envío y cambios** | Plazo, costo y política, con el horario de atención | Reduce abandono |
| 8 | **Reseñas** | Foto y talle del comprador, sólo reales | Prueba social |

Un campo vacío no es un campo opcional: es una devolución futura.

---

## 2. Convención de título

```
[Marca/ Línea] + [Prenda] + [Atributo diferencial] + [Color] + [Talle]
```

El talle va en la variante, no en el título (si no, se duplica el producto 7 veces). El atributo es lo que la gente busca, no lo que a la marca le gusta decir.

| Mal | Bien | Por qué |
|---|---|---|
| Jean Wide Leg | Jean Wide Leg tiro alto azul oscuro | "tiro alto" es lo que se busca |
| Camisa Entallada | Camisa entallada manga larga oxford celeste | El calce y la tela deciden la compra |
| Remera Basic | Remera algodón peinado cuello redondo negra | "algodón peinado" filtra al que sabe |

**Regla anti-canibalización:** nunca usar "American Jeans" como única palabra clave. Es genérica: la pelea la gana el marketplace, no una tienda nueva. La pelea se da en long tail ("jean masculino tiro alto talle 44").

---

## 3. Descripción: fórmula de 4 bloques

1. **Para qué sirve** (una frase, en segunda persona): "Para el día que salís del trabajo y vas directo a cenar."
2. **Calce**: entallado / regular / amplio, y qué talle usa el modelo de la foto ("El modelo mide 1,80 m y usa L").
3. **Material y construcción**: composición, gramaje si aplica, si destiñe, si se arruga.
4. **Cuidado**: lavado, secado, plancha. Sin esto, la prenda vuelve.

**Ejemplo completo**

> **Camisa entallada manga larga oxford celeste**
> Para el día que arranca en la oficina y termina en una mesa.
> Calce entallado, sin apretar el torso: si estás entre dos talles, elegí el mayor. El modelo mide 1,80 m y usa L.
> Oxford de algodón peinado, cuello italiano que funciona con corbata o abierto. Se arruga poco y no destiñe.
> Lavar a máquina en frío, secar colgada, planchar a temperatura media.

**Prohibido:** "calidad premium", "elegancia atemporal", "la prenda que estabas esperando". No dicen nada y ocupan el lugar donde debería estar el dato que decide la compra.

---

## 4. Fotos: orden fijo y especificación

| # | Toma | Para qué |
|---|---|---|
| 1 | Producto solo, fondo blanco | Feed de Meta y Google Shopping |
| 2 | Producto puesto, cuerpo completo | Calce real |
| 3 | Detalle de tela (macro) | Justifica el precio |
| 4 | Detalle de costura o terminación | Confianza |
| 5 | Foto de medida (centímetro visible) | Elimina la duda de talle |
| 6 | Contexto de uso (oficina, calle, bar) | Vende la ocasión |
| 7-8 | Otros colores del mismo modelo | Reduce consultas |

**Técnica:** mismo fondo, misma luz, mismo encuadre en todo el catálogo. 1:1 para la primera foto (requisito de feed), 4:5 para las demás. Mínimo 1000 px de lado. La consistencia importa más que la calidad: un catálogo desparejo se ve barato aunque las fotos sean buenas.

---

## 5. Campos privados (mayorista, no públicos)

Estos campos **nunca** salen al HTML público ni al feed:

| Campo | Uso |
|---|---|
| `costo` | Cálculo de margen |
| `precio_mayorista` | Sólo con sesión de cuenta comercial aprobada |
| `cantidad_minima` | Curva o unidades |
| `escala_2` / `escala_3` | Precio por volumen (a partir de X unidades) |
| `proveedor` | Reposición |
| `curva_talles` | Qué talles incluye la curva |

Si el HTML público contiene el precio mayorista, el minorista lo ve y la sucursal queda cara. Es el error más caro y el más fácil de cometer.

---

## 6. Mapeo al CSV de Tiendanube

El archivo que ya existe usa este encabezado exacto:

```
Nombre,Descripcion,Categoria,SKU,Precio,Precio promocional,Stock,Peso (kg),
Variante 1,Valor 1,Variante 2,Valor 2,Imagen,SEO titulo,SEO descripcion,Estado
```

Reglas de importación:

- `Nombre` = título de §2, sin el talle.
- `Categoria` = ruta con `>`: `American Jeans > AJ basic > Remeras`.
- `Variante 1` = `Talle`, `Variante 2` = `Color`. Nunca al revés: rompe las colecciones.
- `Precio` = precio minorista final. El mayorista **no se importa**: se gestiona en la lista privada.
- `Stock` = unidades reales del talle/color de esa fila, no del producto.
- `SEO titulo` ≤ 60 caracteres · `SEO descripcion` ≤ 155.
- `Estado` = `Activo` sólo cuando la ficha tiene los 8 campos. Si falta la guía de talles, queda `Borrador`.

---

## 7. Checklist por ficha (no se publica sin esto)

- [ ] Título con atributo y color, ≤ 60 caracteres
- [ ] 6+ fotos en el orden de §4, misma luz y fondo
- [ ] Descripción con los 4 bloques, sin adjetivos vacíos
- [ ] Guía de talles en texto (no sólo imagen) y talle del modelo
- [ ] Stock real por talle y color
- [ ] Precio final + medios de pago
- [ ] Envío, retiro (2 h con cita, L-S 9 a 19) y cambios
- [ ] Al menos una reseña real, o el bloque de reseñas oculto

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

---

## 9. Cómo se nombra el material

Decidido con el caso del chaleco (hilo sintético, no lana ni lino):

1. **Se declara la fibra, siempre.** "Hilo sintético" en la tarjeta y el feed; el porcentaje exacto en la ficha cuando el proveedor lo informe (por ejemplo "100% poliéster" o "65% poliéster / 35% viscosa").
2. **No se dice lana ni lino si no lo es.** El cliente del rubro lo detecta al tacto en cinco segundos, y la devolución por "no es lo que decía" cuesta flete, tiempo y la confianza que es el diferencial de la marca.
3. **El sintético se vende por beneficio, no con vergüenza.** No encoge, no se arruga, seca rápido y mantiene la forma: para un chaleco de uso diario eso es una ventaja concreta frente a la lana, que hay que cuidar.
4. **Cuidado que corresponde a la fibra:** agua fría, plancha tibia, sin secadora. El calor es lo que deforma el sintético y lo que arruga el elastano de la gabardina expansible.
5. **En el título no va el material** (se come el espacio de la palabra clave); va en la descripción, en el primer párrafo, junto al calce.

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

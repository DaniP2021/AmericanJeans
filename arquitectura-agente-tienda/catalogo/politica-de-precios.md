# Política de precios — American Jeans

Reglas para que el precio sea el mismo en la web, en las 4 sucursales, en el feed de Meta y en la lista mayorista. Sin esto, el primer descuento paralelo rompe la confianza y la sucursal queda caras.

**Estado:** los precios definitivos no existen todavía. Este documento fija el método; los números salen de la planilla maestra + `precios-referencia.csv`.

---

## 1. Las tres reglas que no se negocian

1. **Precio online = precio de local.** Misma prenda, mismo precio. Si online es más barato, canibalizás las 4 sucursales y entrenás al cliente a esperar.
2. **El mayorista nunca es público.** Detrás de cuenta aprobada, `noindex`, fuera del HTML y del `schema.org`.
3. **Una sola fuente de verdad.** Un archivo (`precios.csv`) alimenta web, feed, anuncios y lista mayorista. Si el precio vive en dos lados, en un mes hay dos precios.

---

## 2. Cómo se calcula el precio minorista

El plan fija un margen bruto del **52%** sobre el precio de venta. De ahí sale la fórmula:

```
precio_minorista = costo / (1 − 0,52) ≈ costo × 2,08
```

Verificación con el mercado: el polo de Avellaneda muestra ratios minorista/mayorista de 1,12 (jean), 1,21 (camisa) y 1,75 (remera). Son ratios **entre dos precios de venta**, no márgenes: el "minorista" del polo es la venta de una unidad a un particular, y el mayorista es la venta a un revendedor. Sirven para ubicarse, no para calcular el margen propio.

**Lo que falta para cerrar los números:** el costo real de cada SKU. Está en la planilla maestra; hasta que no se cargue, cualquier precio es una hipótesis.

---

## 3. Escala mayorista

Propuesta de tres escalones, simple y explicable en una línea:

| Escalón | Condición | Precio |
|---|---|---|
| 1 | Mínimo de compra (bajo) | `precio_mayorista` |
| 2 | Desde 12 unidades de la misma curva | −5% |
| 3 | Desde 24 unidades | −8% |

Regla: **mínimo bajo, escalón claro**. El benchmark muestra mínimos que van de 2 unidades a $100.000 + IVA, y ningún criterio común. Un mínimo alto espanta al cliente nuevo; un mínimo bajo con escalón premia al que compra en serio.

El mínimo se expresa **en unidades y en monto**, los dos juntos, porque cada cliente entiende uno distinto:

> "Mínimo mayorista: 6 unidades o $60.000. Desde 12 unidades, 5% menos."

---

## 4. Envío gratis: se define por umbral, no por generosidad

```
umbral_envio_gratis ≈ 1,7 × ticket_promedio
```

Con el ticket del plan (USD 55), el umbral ronda 1,7 × 55 ≈ **USD 93**. Se recalcula con el precio final en pesos y se revisa cada temporada.

Por qué 1,7 y no 1,0: si el umbral es igual al ticket promedio, la mitad de los pedidos lo alcanza y regalás el flete en todos. Con 1,7 empujás a sumar una segunda prenda, que es exactamente el objetivo.

Alternativa más simple y más vendible en esta categoría: **"envío gratis desde 2 prendas"**. Se entiende sin calcular, y sube el ticket igual.

Referencia de mercado: Macowens lo tiene en $110.000 (minorista) y Madu en $200.000 + IVA (mayorista, CABA).

---

## 5. Cuotas

- **Minorista:** 2 o 3 cuotas sin interés **sólo en las categorías donde el margen lo soporta** (jean y camisa sí; remera de básico no). La cuota se paga con margen, no con el precio.
- **Promociones bancarias:** preferibles a financiar cuotas propias, porque parte del costo lo pone el banco. Es lo que hace Macowens con su sección de promociones.
- **Mayorista:** no se financian cuotas con margen propio en un pedido de $100.000. Transferencia o link de pago.

Mientras el precio esté en referencia: **no se anuncia ninguna cuota**. Anunciar "3 sin interés" sobre un precio provisorio es una promesa que no se puede sostener.

---

## 6. Promociones: con fecha, no permanentes

| Tipo | Cuándo | Regla |
|---|---|---|
| Combo (camisa + jean) | Siempre | Precio cerrado, beneficio percibido, margen calculado |
| Segunda prenda | Lanzamiento | 10-15%, sólo con código y fecha de fin |
| Retiro en sucursal | Permanente | Beneficio chico (regalo o 5%), para mover tráfico al local |
| Liquidación de temporada | 2 por año | Precio tachado real, no inflado antes |

Un "descuento permanente" no es una promoción: es el precio real con un cartel que dice otra cosa.

---

## 7. El hito que ordena todo: congelamiento de precios

Antes de la Fase 2 (tienda) hace falta un cierre formal:

- [ ] Costos cargados de los 120 SKUs prioritarios
- [ ] Precio minorista calculado y aprobado por el dueño
- [ ] Precio mayorista y escalones definidos
- [ ] Umbral de envío gratis y política de cuotas decididos
- [ ] Versión del archivo (`precios_v1.csv`) con fecha
- [ ] Publicación simultánea en web, feed y lista mayorista

Desde ese momento el precio es público, exacto, con impuestos incluidos. Antes de ese momento, la web dice "precio de referencia" y no se carga nada en Meta ni en Google Merchant Center: un feed con precios provisorios se rechaza o se desaprueba, y el anuncio queda muerto sin que nadie entienda por qué.

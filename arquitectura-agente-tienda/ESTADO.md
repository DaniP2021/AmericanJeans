# Estado del proyecto — American Jeans

**Actualizado:** 27/10/2026 · **Etapa:** 0 cerrada · **Etapa 1** construida · **Fase actual: maqueta para aprobación** (no se vende todavía).

> **Criterio de la etapa:** el objetivo ahora es que la idea se entienda y se apruebe, no publicar. Las fotos son provisorias y no bloquean nada; cuando la idea esté aprobada se reemplazan por tomas del local (recetas de costo cero en `qa/grado_casa.py` y en el README de la landing).

---

## 1. Qué está hecho

### Documentos de dirección

| Entregable | Archivo | Estado |
|---|---|---|
| Análisis del prompt original (19 hallazgos) | `01-Analisis-Prompt-v1.md` | ✅ |
| Prompt v2 del arquitecto de agentes | `02-Prompt-Arquitecto-v2.md` | ✅ |
| Brief de insumos y runbook de subagentes | `03-Brief-Inputs-y-Runbook.md` | ✅ |
| Identidad de marca (logo, paleta, tono, reglas) | `04-Identidad-American-Jeans.md` | ✅ |
| Tokens de diseño | `tokens.css` | ✅ |

### Investigación

| Entregable | Archivo | Estado |
|---|---|---|
| Benchmark de 9 competidores con fuentes verificadas | `benchmark-competencia.md` | ✅ auditado (3 URLs re-verificadas) |

### Landing Fase 1

| Entregable | Archivo | Estado |
|---|---|---|
| Página principal con copy real | `landing/index.html` | ✅ QA técnico sin bloqueantes |
| Estilos con tokens de marca | `landing/styles.css` | ✅ color semántico + contraste AA verificado |
| Paleta candidata A ("Terracota y denim") | `landing/theme-a.css` · `landing/preview-a.html` | ⏳ aplicada como default, pendiente de aprobación |
| Paleta candidata B ("Cielo y durazno") | `landing/theme-b.css` · `landing/preview-b.html` | ⏳ pendiente de decisión |
| Comparación visual de ambas paletas | `paletas/comparacion-paletas.png` · `06-Paletas.md` | ✅ |
| Sello de marca recortado y sin fondo | `landing/img/logo-sello-{160,320,480}.png` | ✅ extraído del avatar |
| Ubicación del sello en el hero (240 px / 140 px) | `paletas/hero-sello.png` | ✅ implementado |
| Sección "Abrigo y talles especiales" (3 tarjetas tipográficas) | `landing/index.html#abrigo` | ✅ sin fotos, con CTA a WhatsApp |
| Medición de clics y FAQ | `landing/app.js` | ✅ |
| Guía de talles pública | `landing/talles.html` | ⚠️ tabla de ejemplo |
| Términos y condiciones | `landing/legal/terminos.html` | ⚠️ borrador |
| Cambios y devoluciones | `landing/legal/cambios.html` | ⚠️ borrador |
| Privacidad (Ley 25.326) | `landing/legal/privacidad.html` | ⚠️ borrador |
| Botón de arrepentimiento (Res. 424/2020) | `landing/legal/arrepentimiento.html` | ⚠️ formulario sin endpoint |
| Plan de medición | `landing/medicion.md` | ✅ |
| Instrucciones de publicación y reemplazos | `landing/README.md` | ✅ |
| QA automatizado de la landing | `qa/verify_landing.py` | ✅ corre limpio |

### Catálogo y operación

| Entregable | Archivo | Estado |
|---|---|---|
| Esquema de producto (8 campos + mapeo Tiendanube) | `catalogo/esquema-producto.md` | ✅ |
| Política de precios y congelamiento | `catalogo/politica-de-precios.md` | ✅ |
| Precios de referencia del mercado | `catalogo/precios-referencia.csv` | ✅ 3 anclas con fuente |
| Priorización de 30 SKUs | `catalogo/priorizacion-30-skus.md` | ⚠️ slots sin SKU real |
| Macros de WhatsApp (12 situaciones) | `operacion/whatsapp-macros.md` | ✅ |
| Runbook de retiro en 2 h | `operacion/retiro-2h.md` | ✅ |
| Grilla de contenidos de lanzamiento | `05-Grilla-Contenidos-Lanzamiento.md` | ✅ |
| Planilla de guía de talles | `Guia-Talles-American-Jeans.xlsx` | ⚠️ vacía para completar |
| Dos notas de blog con SEO long tail | `contenido/blog/` | ✅ |
| Checklist de lanzamiento (41 ítems) | `qa/checklist-lanzamiento.md` | ✅ |

### QA ejecutado

```
qa/verify_landing.py → EXIT 0
6 páginas · 1 h1 cada una · 0 links rotos · 0 recursos faltantes
contraste AA: 8 pares OK (rojo 6.73 · blanco/negro 19.30 · gris 5.33)
```

Correcciones aplicadas durante el QA: el gris de los tokens no pasaba AA (3.45 → 5.33), el título del index excedía 60 caracteres, faltaba la meta descripción en términos.

---

## 2. Qué falta y solo lo puede hacer el dueño

En orden de impacto. Los tres primeros bloquean el lanzamiento.

| # | Tarea | Tiempo estimado | Bloquea a |
|---|---|---|---|
| 0 | **Elegir paleta A o B** (`06-Paletas.md`) | 5 min | El aspecto final de toda la landing |
| 1 | **Medidas en cm** (pecho, cintura, largo por talle, 3 prendas por talle) — *en proceso; la equivalencia ya está publicada* | 2 h en el local | Completar la tabla de talles |
| 2 | **Precios de referencia aprobados** (remera, camisa, jean) — *en proceso* | 30 min | "Desde $", umbral de envío gratis, meta de ROAS |
| 3 | **Fotos de los looks** — *en proceso; 2 de 3 con foto (trabajo y noche usan la misma; falta finde)* | jornada de producción | Landing visual completa |
| 4 | **Logo vectorial** (hoy: sello PNG + lockup tipográfico) | pedido al diseñador | Header y favicon |
| 5 | **Revisión profesional de los 4 textos legales** | 1 h del contador/abogado | Publicar legales |
| 6 | **Endpoint del formulario de arrepentimiento** (email o CRM) | 20 min | Ejercicio del derecho online |
| 7 | **ID de GA4** | 10 min | Medición |
| 8 | **Responsable por turno** que mire la bandeja de pedidos | decisión interna | La promesa de 2 horas |
| 9 | **Búsqueda de antecedentes en INPI** (clases 25 y 35) | trámite | Protección de la marca |

### Datos de contacto cargados (26/10)

| Dato | Valor |
|---|---|
| Razón social | El 73 S.R.L. |
| CUIT | 30-71486507-9 |
| WhatsApp | +54 9 11 5646-9722 (13 enlaces; fuente única en `landing/datos-negocio.json`) |
| Sucursal | Av. Rivadavia 2713, CABA — también depósito |
| Horario | lunes a sábado, 9 a 19, con cita para retiro y cambios |
| Structured data | `Store` con dirección, teléfono y horarios en el `<head>` |

Los datos fiscales van al pie en 11 px, sin negrita y en gris (`.datos-fiscales`, contraste 4,7:1 sobre la banda de la paleta A y 6,4:1 sobre la de B: ambos cumplen AA). Son un dato obligatorio, no un argumento de venta: no compiten con nada.

**Pendientes que el dueño dejó en proceso:** medidas en cm, precios de referencia y fotos. La **equivalencia de talles ya está publicada** (S/1/38 · M/2/40 · L/3/42 · XL/4/44 · XXL/5/46 · XXXL/6/48); las columnas en centímetros de la planilla quedan listas para completar. Los precios siguen como referencia.

**Decisión del dueño:** se publica solo Sucursal 1. Consecuencia asumida: el diferencial "cambios en cualquiera de las 4 sucursales" queda en pausa y el sitio dice "cambios gratis en el local". Cuando se publiquen las otras direcciones, se revierte cambiando el bloque de promesas y el footer (una edición de 10 minutos).

Ninguna de las tareas de la tabla requiere decidir nada nuevo: son datos que ya existen en el negocio.

---

## 3. Cuando lleguen los datos, qué se hace

1. Reemplazo de placeholders (30 min) y re-corrida del QA.
2. Publicación: hosting estático + dominio + SSL.
3. Carga de los 30 SKUs priorizados con las fotos reales.
4. Arranque de la grilla de contenidos de la semana 1.
5. A los 14 días: lectura del tablero y decisión de pasar a Fase 2 (tienda).

---

## 4. Reglas que quedaron fijadas

- Precio online = precio de local. Sin excepciones.
- Mayorista nunca público: cuenta aprobada, `noindex`, fuera del schema.
- "Retiro en 2 horas" siempre con "con cita, lunes a sábado de 9 a 19".
- Ningún precio exacto ni cuota hasta el congelamiento de precios.
- Ninguna reseña que no exista. El bloque de testimonios está comentado en el HTML.
- Ningún dato de competidor sin URL y fecha.

---

## 5. Cómo retomar

Leer este archivo y después `landing/README.md` (reemplazos obligatorios) y `qa/checklist-lanzamiento.md` (puerta de salida). Todo lo demás es referencia.

Para verificar que nada se rompió después de editar:

```
python qa/verify_landing.py
```

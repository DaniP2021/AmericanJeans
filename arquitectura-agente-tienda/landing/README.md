# Landing Fase 1 — American Jeans

Landing de una columna, mobile-first, sin frameworks ni fuentes externas. Objetivo: validar demanda con 30-50 pedidos antes de construir la tienda (Fase 1 del plan de 90 días).

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | Página principal (hero, promesas, looks, AJ basic, cómo comprar, talles, FAQ, footer) |
| `styles.css` | Estilos + tokens de marca sincronizados con `../tokens.css` |
| `app.js` | Año del footer, medición de clics a WhatsApp y de FAQ (~1 KB) |
| `medicion.md` | Plan de GA4, eventos, UTM y tablero semanal |
| `talles.html` | Página de guía de talles y cómo medir |
| `legal/` | Términos, cambios, privacidad y botón de arrepentimiento |
| `img/logo-sello-*.png` | Sello de marca (marco rojo + AJ basic + American Jeans) recortado del avatar, sin fondo. Tres anchos: 160, 320 y 480 |

## Marca: dos piezas, dos usos

| Pieza | Dónde | Por qué |
|---|---|---|
| **Lockup tipográfico** (`.marca`) | Navbar y footer | Legible a cualquier tamaño; el sello a 44 px dejaría el nombre en 9 px |
| **Sello** (`img/logo-sello-*.png`) | Hero: 240 px a la derecha en escritorio, 140 px arriba del titular en móvil | Aporta el peso visual de la marca sin competir con el botón de WhatsApp |

El sello se recorta del avatar original por dentro del círculo: el anillo y el corazón de Instagram son de la plataforma, no del logo.

## Antes de publicar: reemplazos obligatorios (P0)

| # | Qué | Dónde | Estado |
|---|---|---|---|
| 1 | **Número de WhatsApp** — `+54 9 11 5646-9722` (13 enlaces) | `datos-negocio.json` + `qa/aplicar_datos.py` | ✅ 26/10 |
| 2 | **Dirección** — Av. Rivadavia 2713, CABA (sucursal y depósito) | `index.html` hero, promesas, FAQ y footer | ✅ 26/10 |
| 3 | **Datos fiscales** — El 73 S.R.L. · CUIT 30-71486507-9 · Av. Rivadavia 2713, CABA (20 reemplazos en 6 páginas) | `datos-negocio.json` + `qa/aplicar_datos.py` | ✅ 26/10 |
| 4 | ID de GA4 (`G-XXXXXXX`) | `<head>` de cada página | ⬜ |
| 5 | Logo vectorial oficial (hoy: sello PNG derivado del avatar + lockup tipográfico en la navbar) | `img/` y `.marca` en `styles.css` | ⬜ |
| 6 | Fotos de los looks (**provisorias de maqueta**: trabajo y noche con la misma foto; falta finde). Variante de recorte cerrado en `img/look-noche-*` | `img/look-*.jpg` y `.look__media` | ⏳ maqueta |
| 7 | **Medidas en cm** de la tabla de talles (la equivalencia S/1/38 a XXXL/6/48 ya está publicada) | `talles.html` + `Guia-Talles-American-Jeans.xlsx` | ⏳ en proceso |
| 8 | Precio de referencia de los 3 looks | `.look__precio` | ⬜ |
| 9 | Revisión profesional de los textos legales | `legal/` | ⬜ |
| 10 | Dominio y certificado SSL | hosting | ⬜ |

**Datos de contacto en un solo lugar.** El teléfono, la dirección y el horario viven en `datos-negocio.json`. Para cambiarlos: editar el JSON y correr `python qa/aplicar_datos.py`, que reescribe los 13 enlaces y avisa si quedó algún número distinto. El número original decía `+24`, que no es un código de país: se interpretó como `+54` (Argentina) y está anotado en el JSON.

Ningún placeholder está disimulado: todos dicen "a confirmar" o "de ejemplo" a la vista. Un placeholder honesto no rompe la confianza; un precio inventado sí.

## Cómo verla

Abrir `index.html` en el navegador alcanza para revisar contenido. Para probar con rutas relativas y medir velocidad de verdad, servir la carpeta:

```
python -m http.server 8000
```

Luego `http://localhost:8000`.

## Presupuesto de rendimiento

| Recurso | Peso actual | Límite |
|---|---|---|
| HTML | ~15 KB | 40 KB |
| CSS | ~12 KB | 20 KB |
| JS | ~1,8 KB | 10 KB |
| Fuentes externas | 0 | 0 |
| Imágenes | 1 (sello, 36 KB en móvil / 64 KB en escritorio) | ≤ 1,5 MB en total |

Al entrar las fotos reales: formato AVIF o WebP, `width`/`height` declarados, `loading="lazy"` salvo la primera, y máximo 3 imágenes sobre el pliegue. El presupuesto se rompe con fotos de 3 MB, no con el CSS.

## Decisiones de diseño que no son estéticas

- **Sin precios exactos:** están en referencia. Mostrar un número que después cambia es la forma más rápida de perder confianza y de complicar la posición frente al consumidor.
- **Sin cuotas anunciadas:** no hay precio firme ni acuerdo de financiación. Se consultan caso por caso.
- **"Retiro en 2 horas" siempre con la condición:** "con cita, lunes a sábado de 9 a 19". La promesa sin el horario es la que se rompe el sábado a las 20.
- **Preguntas en `<details>`:** acordeón nativo, sin JS, funciona con teclado y con lector de pantalla.
- **Barra fija de WhatsApp sólo en móvil:** el 80% del tráfico de esta categoría es móvil y el pulgar no hace scroll hasta el footer.

## Qué falta para que esto sea una tienda (Fase 2)

Carrito, checkout, stock por variante, envíos por código postal, cuenta mayorista y páginas de producto. Esta landing es deliberadamente una sola página: su trabajo es validar la oferta, no reemplazar la tienda.

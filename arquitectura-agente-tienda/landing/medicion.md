# Plan de medición — landing Fase 1

Sin esto, la Fase 3 (performance) arranca a ciegas. Se instala el día 1, no después.

---

## 1. Qué se mide y para qué

| Evento | Cuándo | Para qué se usa |
|---|---|---|
| `page_view` | automático (GA4) | Volumen y origen del tráfico |
| `whatsapp_click` | clic en cualquier botón de WhatsApp | **El número que anticipa pedidos en Fase 1** |
| `faq_open` | apertura de una pregunta | Qué duda frena la compra |
| `talles_open` | clic en "Ver la guía de talles" | Confirma si el talle es el freno real |
| `scroll_75` | 75% de la página | Si el mensaje se lee o se abandona |
| `purchase` | cuando exista checkout (Fase 2) | ROAS y CAC reales |

**El evento propio de la Fase 1 es `whatsapp_click` con el parámetro `seccion`.** Permite saber si convierte el hero, el look de trabajo, la barra fija o el cierre. Sin ese parámetro, todos los botones se ven iguales y no se puede optimizar nada.

---

## 2. Implementación

**GA4.** Pegar el snippet en el `<head>` de `index.html` y de las páginas legales, antes de `app.js`. El archivo `app.js` ya envía los eventos; no hay que tocar código.

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
</script>
```

**Píxel de Meta.** Se instala recién cuando haya catálogo con precios (Fase 2). Un píxel sin catálogo sólo acumula datos sucios.

**WhatsApp.** Sin API, el clic se mide en la web. Cuando se adopte WhatsApp Business API o un CRM, se agrega el evento de "mensaje respondido" para medir tiempo real de respuesta.

---

## 3. Convención de UTM (fija, no improvisada)

```
utm_source   = instagram | tiktok | whatsapp | email | google | meta
utm_medium   = social | bio | story | email | cpc | referral
utm_campaign = lanzamiento | basic | talles | looks | siempre
utm_content  = nombre_de_la_pieza  (ej: reel-presentacion, story-encuesta-talle)
```

Reglas:
- Siempre en minúsculas, sin acentos, con guiones.
- `utm_content` es obligatorio: sin él no se sabe qué pieza trajo el clic.
- El link de la bio de Instagram lleva `utm_source=instagram&utm_medium=bio&utm_campaign=lanzamiento`.

---

## 4. Tablero semanal (una sola pantalla)

| Métrica | Fórmula | Meta Fase 1 |
|---|---|---|
| Visitas | sesiones | 800/semana |
| Clics a WhatsApp | `whatsapp_click` | ≥ 30 |
| Tasa de contacto | clics / visitas | ≥ 4% |
| Mensajes iniciados | conteo manual en WhatsApp Business | ≥ 15 |
| Pedidos | conteo manual | 30-50 en 2 semanas |
| Ticket promedio | facturación / pedidos | USD 55 |
| Consultas por talle | conteo manual | si > 30% de los mensajes, la guía es urgente |

El tablero se completa **a mano** en la Fase 1. Una planilla de tres columnas alcanza: fecha, métrica, valor. Automatizarlo antes de tener volumen es perder tiempo.

---

## 5. Control de calidad de la medición (antes de publicar)

- [ ] Abrir la landing con el modo incógnito y confirmar que GA4 recibe `page_view`.
- [ ] Hacer clic en los 5 botones de WhatsApp y verificar que llegan los 5 `whatsapp_click` con `seccion` distinta.
- [ ] Abrir una pregunta de FAQ y ver `faq_open` con el texto correcto.
- [ ] Confirmar que el link de WhatsApp abre con el mensaje precargado correcto en móvil (Android e iOS).
- [ ] Verificar que no hay eventos duplicados (un clic = un evento).
- [ ] Anotar la fecha de instalación y el ID de la propiedad en el tablero.

---

## 6. Lo que no se mide todavía (y por qué)

- **ROAS / CAC:** no hay inversión publicitaria en Fase 1.
- **Tasa de conversión real:** no hay checkout; el embudo termina en WhatsApp.
- **Recuperación de carrito:** no hay carrito.

Prometer estas métricas en la Fase 1 sería medir algo que no existe. Se activan en Fase 2, cuando el checkout esté operativo.

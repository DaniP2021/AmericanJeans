# Checklist de lanzamiento (QA) — Fase 1

Puerta de salida antes de publicar la landing. Cada ítem tiene un responsable. **Un ítem bloqueante sin marcar detiene el lanzamiento**: no se negocia con la fecha, se mueve la fecha.

Leyenda: 🔴 bloqueante · 🟡 importante · ⚪ deseable

---

## 1. Contenido y promesas

| # | Ítem | Tipo | Responsable |
|---|---|---|---|
| 1 | No queda ningún placeholder visible ("a confirmar", "de ejemplo", "[fecha]", "[CUIT]") | 🔴 | Dueño |
| 2 | Número de WhatsApp real en los 7 botones y en las páginas legales | 🔴 | Dueño |
| 3 | Dirección publicada: Av. Rivadavia 2713, CABA, y número de WhatsApp real | ✅ | Dueño |
| 4 | Ningún precio exacto publicado (están en referencia) | 🔴 | Dueño |
| 5 | Ninguna cuota anunciada | 🔴 | Dueño |
| 6 | "Retiro en 2 horas" aparece siempre con "con cita, lunes a sábado de 9 a 19" | 🔴 | A4 |
| 7 | La tabla de talles tiene medidas reales, no de ejemplo | 🔴 | Local |
| 8 | No hay reseñas ni testimonios inventados | 🔴 | A4 |
| 9 | Ortografía y voseo consistentes (no "tú") | 🟡 | A4 |

## 2. Legal

| # | Ítem | Tipo | Responsable |
|---|---|---|---|
| 10 | Botón de arrepentimiento visible en la página principal (Res. 424/2020) | 🔴 | A1 |
| 11 | Formulario de arrepentimiento conectado a un destino real (email o CRM) | 🔴 | A1 |
| 12 | Términos, cambios, privacidad y arrepentimiento publicados y enlazados en el footer | 🔴 | A1 |
| 13 | Razón social, CUIT y domicilio cargados en las 4 páginas legales | 🔴 | Dueño + contador |
| 14 | Link al formulario de Defensa del Consumidor presente | 🔴 | A1 |
| 15 | Textos legales revisados por un profesional | 🔴 | Contador/abogado |
| 16 | Consentimiento explícito para la lista de difusión de WhatsApp | 🟡 | A1 |
| 17 | Cesión de derechos de imagen para modelos y UGC | 🟡 | Dueño |

## 3. Técnico

| # | Ítem | Tipo | Responsable |
|---|---|---|---|
| 18 | HTTPS activo y redirección de http a https | 🔴 | A1 |
| 19 | Dominio apuntando al hosting correcto | 🔴 | A1 |
| 20 | PageSpeed mobile ≥ 85 | 🟡 | A1 |
| 21 | LCP ≤ 2,5 s en 4G, CLS ≤ 0,1 | 🟡 | A1 |
| 22 | La landing se ve bien en 360×640 (el ancho más común) | 🔴 | A1 |
| 23 | Los 7 links de WhatsApp abren con el mensaje precargado, en Android e iOS | 🔴 | A1 |
| 24 | Todos los links internos funcionan (looks, talles, legales) | 🔴 | A1 |
| 25 | Formularios con `label` asociado y foco visible | 🟡 | A1 |
| 26 | Contraste AA en textos sobre negro y sobre rojo | 🟡 | A1 |
| 27 | Favicon y `theme-color` cargados | ⚪ | A1 |
| 28 | 404 personalizada con link al inicio | ⚪ | A1 |

## 4. Medición

| # | Ítem | Tipo | Responsable |
|---|---|---|---|
| 29 | GA4 instalado y recibiendo `page_view` | 🔴 | A1 |
| 30 | Los 5 botones emiten `whatsapp_click` con `seccion` distinta | 🔴 | A1 |
| 31 | UTM en el link de la bio de Instagram y de TikTok | 🔴 | A4 |
| 32 | Tablero semanal creado (aunque sea una planilla de 3 columnas) | 🟡 | Dueño |

## 5. Operación

| # | Ítem | Tipo | Responsable |
|---|---|---|---|
| 33 | Un responsable por turno con acceso a la bandeja de pedidos | 🔴 | Dueño |
| 34 | Respuesta automática de WhatsApp fuera de horario configurada | 🔴 | Dueño |
| 35 | Macros cargadas en WhatsApp Business | 🟡 | Dueño |
| 36 | Lugar físico para pedidos listos, separado del mostrador | 🔴 | Dueño |
| 37 | Proceso de cambios explicado al personal del local | 🟡 | Dueño |
| 38 | Registro diario de retiros (la planilla de `retiro-2h.md`) | 🟡 | Dueño |

## 6. Prueba real antes de abrir

| # | Ítem | Tipo |
|---|---|---|
| 39 | Compra de prueba completa: consulta → link de pago → pago → retiro, con reloj | 🔴 |
| 40 | Devolución de prueba: pedir el arrepentimiento como si fuera un cliente | 🔴 |
| 41 | Consulta de prueba desde un teléfono que no sea del negocio, sin sesión iniciada | 🟡 |

---

## Cómo se usa

1. Se completa en una reunión de 30 minutos con la landing abierta en el teléfono.
2. Cada 🔴 sin marcar se convierte en una tarea con nombre y fecha.
3. Se vuelve a pasar el checklist completo antes de cada campaña, no sólo en el lanzamiento.

**Regla final:** si hay que elegir entre lanzar el jueves con un 🔴 pendiente o lanzar el lunes con todo cerrado, se lanza el lunes. Un lanzamiento roto se recuerda más que un lanzamiento tardío.

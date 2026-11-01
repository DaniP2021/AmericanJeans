# Brief de insumos y runbook de ejecución

Complemento del prompt v2: qué falta para arrancar, qué preguntar en el kickoff y en qué orden llamar a los subagentes.

---

## 1. Insumos que faltan (bloquean la Etapa 0)

| Insumo | Estado | Por qué bloquea | Quién lo aporta |
|---|---|---|---|
| **Nombre de marca** y 1 frase de posicionamiento | ✅ Resuelto 25/10 | American Jeans · línea `AJ basic`. Ver `04-Identidad-American-Jeans.md` | Dueño |
| **Lista de precios minorista y mayorista** (con costo y mínimo mayorista) | ⏳ Referencia hasta el *freeze* | Se publica "desde $X" sin cuotas; el precio exacto y el catálogo de Meta/Google esperan el congelamiento | Dueño + contador |
| **Horario de atención y reglas de retiro** | ✅ Resuelto 25/10 | WhatsApp L-S 9-19; envíos y cambios con cita previa. Cambia la promesa de "retiro en 2 h" (ver §6 del archivo de identidad) | Dueño |
| **Curva de talles real por SKU** | Falta | La guía de talles es la primera causa de devolución; sin medidas en cm no se publica | Dueño + locales |
| **Cuenta de Mercado Pago / pasarela y decisión de cuotas** | Falta | Define el checkout y el costo financiero del precio | Dueño |
| **Fotos de producto** (frente, espalda, detalle, puesto, medida) | Falta | Sin fotos no hay ficha, ni feed de Meta, ni Shop | Producción externa |
| **Brief de identidad** (paleta, tipografía, 5 adjetivos, 3 mensajes) | Falta | Sin esto A4 y A1 inventan un tono distinto cada uno | Dueño |
| **Cuentas de redes y accesos** (IG, TikTok, WhatsApp Business, Meta Business) | Falta | No se puede programar contenido ni medir | Dueño |
| **Datos fiscales** (razón social, CUIT, condición) | Falta | Bloquea páginas legales y facturación A/B | Contador |
| **Política de envíos y cambios actual** | ⏳ Parcial | La promesa "cambios gratis en 4 sucursales" necesita condiciones escritas y horario (ya definido: L-S 9-19 con cita) | Dueño |

> Nota: el plan de 90 días ya trae el esquema completo del catálogo (8 campos por ficha) y la tabla de frecuencias por canal. No hay que redefinirlos: hay que completarlos.

---

## 2. Preguntas de kickoff (las que cambian el diseño)

1. ¿El mayorista compra por WhatsApp/telefono hoy o ya tiene cuenta? ¿Cuántos clientes mayoristas activos hay y cuánto pesan en la facturación?
2. ¿La marca ya tiene nombre y logo, o hay que proponerlos?
3. ¿Cuál es el SKU más vendido de los 4 locales y cuál el que más se devuelve? (define el orden de carga y el riesgo)
4. ¿Hay stock real disponible para vender online o hay que reservar unidades?
5. ¿Quién atiende WhatsApp y en qué horario? (el retiro en 2 h es una promesa operativa, no de marketing)
6. ¿Se factura A a mayoristas hoy? ¿Quién emite?
7. ¿Cuál es el presupuesto mensual de publicidad de los primeros 3 meses?
8. ¿Hay fotos publicables de temporadas anteriores reutilizables?
9. ¿Existe base de clientes con email/teléfono y consentimiento?
10. ¿Quién aprueba precios y descuentos? (nombre, no rol)

---

## 3. Cómo ejecutarlo en DSH (orden de llamadas)

El error más común es lanzar los tres subagentes en paralelo el día 1. Así se duplica el trabajo y se contradicen. Secuencia recomendada:

**Paso 1 — A3 (Competitive Intelligence), solo y primero.**
Prompt: analizar 8-10 casos de Once, Avellaneda y e-commerce puro de indumentaria masculina; devolver `benchmark-competencia.md` con tabla (precio, surtido, talle, envío, atención, diferenciador, URL, fecha) y 5 conclusiones accionables. Validar a mano 3 URLs al azar antes de aceptar (control de alucinación).

**Paso 2 — A2 (Catálogo), con el benchmark en mano.**
Prompt: construir `esquema-producto.md` + `precios.csv` + priorización de 120 SKUs + guía de talles. Entregable en planilla, no en prosa.

**Paso 3 — A4 (Contenido), en paralelo con A2 si hay brief de marca.**
Prompt: grilla semanal Lun-Dom × Feed/Historia/Reel/TikTok derivada de la tabla de frecuencias del plan; 12 piezas iniciales; brief de la jornada de fotos (40-60 SKUs, un modelo, un día).

**Paso 4 — A1 (Tech), recién acá.**
Con esquema, precios y pilares aprobados: landing de una columna, WhatsApp, links de pago, medición. Entregar con PageSpeed adjunto.

**Paso 5 — A5 (QA), puerta de salida.**
Checklist completo: legales, accesibilidad, precios coherentes, compra de prueba, tracking verificado.

**Regla de paralelización:** A3 nunca en paralelo con A1. A2 y A4 sí pueden ir juntos. A5 siempre al final de cada etapa.

---

## 4. Qué cambió respecto de v1 (resumen para el dueño)

| v1 | v2 |
|---|---|
| "landing page / tienda online" | Etapa 1 landing, Etapa 2 tienda, con gate entre ellas |
| "alta conversión" | LCP, CLS, INP, PageSpeed, peso, checkout ≤ 3 pasos |
| "aplicar los pilares del plan adjunto" | Tabla de 7 pilares traducidos a web/feed/historia/métrica |
| 3 subagentes | 5 (se suman Contenido y QA/Compliance) |
| Precios mayorista y minorista juntos | Mayorista gated, una sola fuente de precios |
| "seguir la planificación semanal" | La grilla semanal pasa a ser un entregable a construir y aprobar |
| Autonomía total implícita | Límite explícito + tareas humanas con responsable y fecha |
| Sin legales ni medición | Mínimo legal argentino + GA4/píxel/UTM desde el día 1 |

---

## 5. Próximo paso sugerido

1. Responder las 10 preguntas de kickoff (o las que puedas).
2. Aprobar el prompt v2 y el reparto de agentes.
3. Lanzar **solo A3** para producir el benchmark.

Con el benchmark aprobado, la Etapa 0 queda cerrada en una semana y la landing puede salir en la semana 3, como prevé el plan.

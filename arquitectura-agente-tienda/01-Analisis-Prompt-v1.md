# Análisis crítico del prompt v1

**Documento analizado:** prompt "Arquitecto de Agentes de IA y Director de Proyecto" (3 subagentes: Tech & Social, Catalog & ERP, Competitive Intelligence).
**Base de contraste:** `sucursal-virtual/Plan-Sucursal-Virtual-Indumentaria-2026.docx` (16 secciones, 5 fases, 12 semanas) y `automatizacion-tienda/` (planilla maestra, 120 SKUs, prompts de fichas y anuncios).

---

## Veredicto

El prompt es **bueno como encuadre y débil como instrucción ejecutable**. Define bien el espíritu (vender identidad, no ropa) y reparte responsabilidades con lógica. Pero tiene tres problemas de fondo:

1. **Pide un resultado ambiguo** ("landing / tienda online") que contradice la recomendación central del plan propio.
2. **No define artefactos ni criterios de aceptación**, así que el sistema produce prosa convincente en lugar de entregables verificables.
3. **Da por existentes insumos que no están** (la planificación semanal de Feed e Historias, los pilares de marca, el nombre de marca, la lista de precios).

Un sistema multiagente sin contrato de entrega no coordina: superpone. Cada subagente va a escribir su propia versión de la propuesta de valor, del precio y del tono, y el resultado se contradice entre sí.

**Puntaje:** idea 8/10 · ejecutabilidad 4/10 · riesgo de retrabajo alto.

---

## Lo que ya funciona (conservar)

| Acierto | Por qué está bien |
|---|---|
| Separación en tres dominios (tech, catálogo, mercado) | Son tres velocidades distintas: código semanal, catálogo diario, investigación puntual. |
| Exigir enfoque emocional/aspiracional | Evita la trampa del catálogo commodity, que es exactamente donde compite Avellaneda. |
| Investigar Once y Avellaneda | Es el benchmark correcto para precio, talle y atención en indumentaria masculina mayorista. |
| Pedir estructura por etapas y por agente | La forma de respuesta ya está bien pensada; falta el contenido del contrato. |
| Incluir mayorista + minorista + sucursales | Reconoce la omnicanalidad, que es el diferencial real (retiro 2 h, cambios en local). |

---

## Hallazgos priorizados

### P0 — Bloqueantes (sin esto, la ejecución falla)

**1. Contradicción con el plan: pide tienda cuando el plan pide landing primero**
El plan (sección 04) recomienda explícitamente: Fase 1 = landing + WhatsApp + links de pago para validar 30-50 pedidos; Fase 2 (semana 5+) = tienda con Tiendanube. El prompt pide "landing page / tienda online" como si fuera una sola cosa. Un subagente obediente construye la tienda completa en la semana 1, que es justo el error que el plan advierte ("lanzar la tienda sin demanda validada es la forma más cara de aprender").
→ **Corrección:** el prompt debe declarar el plan como autoridad superior y atar cada entregable a una fase con gate.

**2. "Alta conversión" no es un criterio, es un deseo**
No hay una sola métrica verificable. Sin números, el subagente devuelve un HTML que "parece" rápido y el dueño no tiene cómo rechazarlo.
→ **Corrección:** criterios duros: LCP ≤ 2,5 s en 4G móvil, CLS ≤ 0,1, INP ≤ 200 ms, PageSpeed mobile ≥ 85, home ≤ 1,5 MB, WhatsApp visible sin scroll en 360×640, checkout ≤ 3 pasos con compra como invitado.

**3. La "planificación semanal de Feed e Historias" no existe en el plan**
Verifiqué el documento: la sección 07 trae una tabla de **frecuencia por canal** (Instagram 4-5/semana en reels, TikTok 3/semana, email 1/semana, WhatsApp 2/mes, blog 2/mes). No hay grilla día por día ni columna de Historias. El prompt manda "seguir" un documento que no dice lo que el prompt supone.
→ **Corrección:** convertirlo en entregable explícito del agente de contenido ("construir la grilla semanal Lun-Dom × Feed/Historia/Reel/TikTok derivada de la tabla de frecuencias, marcada como propuesta a aprobar").

**4. Los pilares de marca se invocan pero no se definen**
Medición sobre el plan: "identidad" 0 menciones, "aspiracional" 0, "confianza" 4, "humor" 1, "UGC" 1, "modelos" 4 (una jornada de fotos). El prompt dice "aplicando rigurosamente los pilares especificados en la planificación adjunta", pero esos pilares no están operacionalizados en ningún lado. Cada subagente va a inventar su propia interpretación del tono.
→ **Corrección:** tabla de pilares con traducción obligatoria a web, feed, historia y métrica (incluida en el prompt v2).

**5. Precio mayorista público = canibalización del minorista**
El prompt pide "precios diferenciados (escala mayorista y minorista)" sin decir cómo conviven. Si la lista mayorista queda visible, el minorista la ve y el plan (sección 03: "el precio online debe ser el mismo que en el local") se rompe en una semana.
→ **Corrección:** lista mayorista detrás de aprobación de cuenta, `noindex`, fuera del HTML público y del schema.org, mínimo de compra por curva, y una única fuente de verdad de precios (`precios.csv`).

**6. No hay contrato de entrega entre agentes**
Falta qué recibe y qué devuelve cada uno, en qué formato, con qué supuestos declarados. Sin eso, Catalog define un esquema de producto y Tech construye otro; los precios se duplican y las fichas no matchean con la tienda.
→ **Corrección:** esquema de producto único (los 8 campos de la tabla 19 del plan: título, fotos, descripción, guía de talles, stock, precio y cuotas, envío y cambios, reseñas) y formato de handoff fijo.

### P1 — Degradan la calidad del resultado

**7. La investigación de mercado puede terminar inventada**
"Indagar y analizar a fondo" sin regla de fuentes invita a benchmarks fabricados (tráfico, facturación, "el competidor X vende 3.000 prendas/mes"). Es el riesgo más caro del sistema: decisiones de precio tomadas sobre datos falsos.
→ Regla: toda afirmación con URL + fecha de consulta + qué se observó; prohibido estimar cifras de terceros sin declarar método.

**8. No hay agente de contenido, y el prompt es 60% contenido**
UGC, sesiones con modelos, videos creativos, humor, Feed e Historias... y ningún rol los produce. Quedan diluidos entre "tech" y "catálogo".
→ Agregar **Content & Community** y un **QA & Compliance** como gate (precios, legales, accesibilidad, consentimientos).

**9. Se promete autonomía que no existe**
Un LLM no abre una cuenta de Mercado Pago, no firma la cesión de imagen de un modelo y no produce las fotos. Si el prompt no lo dice, el plan de trabajo queda con huecos que nadie ve hasta la semana 3.
→ Declarar el límite: todo lo que requiere cuenta, dinero o firma se entrega como tarea humana con pasos, responsable y fecha.

**10. Falta lo legal, que en Argentina es bloqueante para cobrar**
Botón de arrepentimiento (Res. 424/2020), T&C, política de cambios, privacidad (Ley 25.326), datos del vendedor y CUIT, factura A/B (el mayorista casi siempre la necesita). Sin esto la tienda no puede salir a la calle.

**11. Las cuotas no aparecen, y en Argentina son el principal palanca de conversión**
El plan las menciona (3 cuotas sin interés en categorías selectas, no en todo el catálogo, porque el costo financiero se paga con margen). El prompt habla de "pasarelas de pago" en abstracto.

**12. No hay medición ni ritmo de gestión**
El plan exige GA4, píxel de Meta y UTM desde el día 1 (sección 10). El prompt no pide instrumentación ni tablero semanal, así que la Fase 3 (performance) arranca a ciegas.

**13. Sin formato de salida del orquestador**
No se especifica cómo responde el director: tabla de etapa/agente/entregable/estado, decisiones, bloqueos, próximo paso único. Sin eso, cada turno es un ensayo distinto.

### P2 — Detalles que suman

- **14.** Definir tono: voseo rioplatense, sin "tú", sin spanglish, emojis solo en WhatsApp/Historias, nunca prometer resultados.
- **15.** Nombre de marca ausente: el prompt habla de "la marca" sin nombrarla. Todo el copy queda con placeholders.
- **16.** "Conexiones directas con redes sociales" es ambiguo: ¿login social, catálogo de Meta, posts comprables, automatización de DMs? Verificar además qué está disponible en Argentina (TikTok Shop) antes de prometer checkout nativo.
- **17.** Falta presupuesto por etapa y tolerancia de gasto de los subagentes (el plan ya trae cifras: USD 500-700 fundaciones, 700-900 landing, 1.000-1.400 tienda, 1.200-1.800 performance).
- **18.** Falta vocabulario de stock compartido: reserva al acreditar el pago, stock de seguridad 1-2 por SKU/talle, regla de origen (retiro si hay stock en el local del cliente).
- **19.** Falta criterio de priorización del catálogo inicial (el plan ya lo resolvió: lo que más rota en locales y menos variantes de talle).

---

## Riesgos del diseño multiagente (y su mitigación)

| Riesgo | Síntoma | Mitigación en v2 |
|---|---|---|
| Handoff sin contrato | Tres propuestas de valor distintas | Formato de entrega fijo + un solo dueño por artefacto |
| Investigación inventada | Precios y benchmarks sin fuente | Regla de citas obligatoria + marca "estimación propia" |
| Autonomía sobrestimada | Cuentas y fotos "hechas" que no existen | Lista de tareas humanas con responsable y fecha |
| Deriva de fase | Tienda antes de validar demanda | Gates con métrica de salida del plan |
| Deriva de tono | Copy aspiracional en un canal y promo en otro | Tabla de pilares + glosario de prohibiciones |

---

## Qué debería producir el sistema (mapa de artefactos)

| Etapa | Artefacto | Dueño | Criterio de aceptación |
|---|---|---|---|
| 0 | `brief-marca.md`, `precios.csv`, `esquema-producto.md`, `benchmark-competencia.md` | A3 + A2 | 120 SKUs, precios validados, 8 competidores con fuente |
| 1 | `landing/` (HTML/CSS/JS), `whatsapp-flows.md`, `links-pago.md` | A1 | PageSpeed ≥ 85, 30-50 pedidos en 2 semanas |
| 2 | `tienda/` config + `fichas/` (120) + `guia-talles.md` | A1 + A2 | Compra de prueba end-to-end, 60 pedidos/mes |
| 3 | `campanas/` + `calendario-contenido.md` + `tablero-kpi` | A4 + A1 | ROAS > 3, GA4 con eventos verificados |
| 4 | `revision-90-dias.md` | Orquestador | EBITDA positivo, decisión de escala |

---

## Conclusión

No hace falta reescribir el prompt desde cero: hace falta **convertirlo en un contrato de proyecto**. Los cinco cambios que más mueven la aguja son:

1. Declarar el plan de 90 días como autoridad y atar todo a sus gates.
2. Reemplazar "alta conversión" por umbrales medibles.
3. Operacionalizar los pilares en una tabla web/feed/historia/métrica.
4. Separar precio mayorista (gated) de minorista (público) con una única fuente de precios.
5. Agregar Content & Community + QA/Compliance y declarar el límite de autonomía.

La versión corregida, lista para pegar, está en `02-Prompt-Arquitecto-v2.md`.

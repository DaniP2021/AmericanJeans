# Identidad American Jeans — lectura del logo y reglas de marca

**Insumo:** `me.jpg` (avatar 521×521, JPEG) + definiciones del dueño (25/10/2026).
**Uso:** este archivo es el anexo de marca del prompt v2 (sección 3, pilares) y la referencia obligatoria para A1 (web) y A4 (contenido).

---

## 1. Lectura del logo

**Composición observada:** círculo negro; dentro, un marco rectangular rojo de trazo fino que contiene `AJ` en rojo, una barra vertical y `basic` en rojo con tracking amplio y caja baja; debajo del marco, `American Jeans` en blanco.

**Qué comunica bien (conservar):**
- El marco como "etiqueta" o "parche": lee como denim, etiqueta de jean, sello de calidad. Es el activo gráfico más fuerte del logo.
- `AJ | basic` en dos niveles: sigla de marca + nombre de línea. Ya resuelve la arquitectura de surtido sin inventar nada.
- Negro + rojo: alto contraste, buena legibilidad en pantalla, tono directo y masculino sin caer en el cliché azul-marino.

**Tres problemas de reproducción (corregir antes del lanzamiento):**

| Problema | Dónde se rompe | Solución |
|---|---|---|
| `American Jeans` queda fuera del marco y pegado al borde del círculo | Avatar de Instagram (40 px), favicon (32 px), notificación: el nombre desaparece | Isotipo circular con solo `AJ\|basic` para avatar y favicon |
| El lockup es horizontal pero está forzado dentro de un círculo | Pierde área útil, el marco casi toca el borde | Lockup horizontal (marco + nombre al lado, no debajo) para el header de la web |
| Depende del negro de fondo | Sobre papel, factura o fondo claro el marco rojo compite con el texto | Versión monocroma (negro sobre blanco y blanco sobre negro) |

**Activos a pedir al diseñador:** SVG/AI del lockup, versión reducida `AJ|basic` cuadrada, versión negativa, versión a una tinta, y el rojo en CMYK/Pantone.

---

## 2. Paleta (muestreada del archivo, a confirmar con el original)

| Rol | Valor | Nota |
|---|---|---|
| Negro base | `#0E0E0E` | Fondo dominante del logo (14,14,14). Usar `#0E0E0E`, no `#000000` puro |
| Rojo marca | rango `#A03235` – `#B62A30` | Muestreo sobre JPEG comprimido. **Canónico propuesto: `#B0232B`** — debe confirmarse con el archivo vectorial o la carta del proveedor |
| Blanco | `#FFFFFF` | Texto sobre negro |
| Gris apoyo | `#6B6B6B` | Texto secundario (5,33:1 sobre blanco, cumple AA). `#8A8A8A` solo para íconos y bordes, nunca para texto |
| Fondo claro | `#F5F4F2` | Secciones alternas; nunca blanco puro con rojo al lado |

**Proporción de uso:** 80% neutros · 15% gris · 5% color. El rojo es **color de marca**: vive en el logo y en el isotipo, no en botones ni fondos de la web. La paleta de interfaz (superficies, acciones y acentos) se define aparte, en `06-Paletas.md`, con roles semánticos (`--u-accion`, `--u-banda`, `--u-tinte`).

Lectura estratégica: si el rojo se usa en todos los botones, deja de señalar la marca y compite con ella. El negro se reserva para el texto y el logo; el resto de la página se pinta con la paleta de interfaz.

**Tipografía:** el logo usa una sans geométrica de caja alta para `AJ` y caja baja espaciada para `basic`. Verificar la licencia de la original. Alternativas libres con tono equivalente: **Inter** (texto y UI), **Poppins** o **Montserrat** (títulos). Regla: una sola familia en la web, dos pesos (400 y 700), sin itálicas decorativas.

---

## 3. "basic" no es un adjetivo, es una línea

El logo ya declara una sub-línea. Conviene usarla como **arquitectura de surtido**, no solo como estética:

| Nivel | Nombre en la web | Función | Surtido |
|---|---|---|---|
| Entrada | **AJ basic** | Precio de entrada, rotación alta, compra por reposición | Remera, chomba, jean recto, buzo liso |
| Principal | **American Jeans** | El núcleo del margen | Camisa, jean de trabajo, conjunto, campera |
| Ocasión | **AJ selección** (a definir) | Ticket alto, regalo, evento | Blazer informal, pantalón de vestir, calzado si existe |

Beneficio concreto: permite dos escalas de precio sin que el cliente sienta que la marca "se abarató", y le da a A4 un eje de contenido (`basic` = resolvé la semana; `selección` = la ocasión).

---

## 4. Nombre: dos consecuencias que hay que asumir

1. **Marca débil como registro.** "American Jeans" es descriptivo del producto (nacionalidad + categoría). Eso dificulta la protección y aumenta el riesgo de antecedentes. Tarea humana: búsqueda en INPI (clases 25 indumentaria y 35 comercialización) antes de invertir en señalética, packaging o dominio principal. No es un trámite para después del lanzamiento.
2. **SEO: no se pelea la cabeza del mercado.** "american jeans" es una búsqueda genérica que usan marketplaces y competidores; no se gana con una tienda nueva. La estrategia tiene que ser **long tail por producto, talle y ocasión**: "jean masculino tiro alto talle 44", "camisa masculina manga corta para trabajo", "conjunto informal hombre 40 años". Eso se escribe en los títulos de ficha (el plan ya lo exige: marca + categoría + atributo + talle/color) y en el blog de 2 notas por mes.

---

## 5. Voz y tono

**Es:** directo, adulto, con oficio. Habla de resolver el día, no de "expresar tu estilo". Voseo. Frases cortas. Cero signos de admiración en cadena.

| Sí | No |
|---|---|
| "El jean que no te aprieta después de almorzar." | "¡La prenda que estabas esperando!" |
| "Camisa de trabajo. Se arruga poco, se plancha menos." | "Elegancia atemporal para el hombre moderno." |
| "Si no sabés el talle, escribinos: te lo medimos." | "Consultá disponibilidad." |
| "Retiro en 2 horas, con cita, de 9 a 19." | "Envíos a todo el país." |

**Humor:** de situación y de complicidad, nunca del cliente. El registro que funciona en este rubro es "el talle que pedís vs el que llega", "la camisa que sobrevive al asado del domingo". Los emojis se usan en WhatsApp e Historias; en la ficha de producto, ninguno.

---

## 6. El horario cambia la promesa (importante)

Definiste WhatsApp **lunes a sábado, 9 a 19 h**, y que envíos y cambios se coordinan con cita o confirmación previa. Eso convierte el "retiro en 2 horas" del plan en una promesa **condicionada**. Si la web no lo dice, el primer cliente que compre un sábado a las 20 va a sentir que la marca le mintió.

**Copy obligatorio (web, FAQ y WhatsApp):**

- Hero: **"Retiro en 2 horas en tu sucursal. Lunes a sábado, de 9 a 19, con cita confirmada."**
- Fuera de horario: **"Los pedidos que entran después de las 19 se preparan al abrir el siguiente día hábil."**
- Cambios: **"Cambio gratis en Av. Rivadavia 2713, con cita previa, de lunes a sábado de 9 a 19."**
  *(Hasta que se publiquen las otras direcciones, no se menciona la red: prometer cuatro locales y mostrar uno abre una pregunta que nadie responde.)*
- Respuesta prometida: **"Respondemos en menos de 15 minutos en horario de atención."** (Si no se puede sostener, no se promete: es la promesa que más se rompe.)
- Mensaje automático fuera de horario: horario + link de autogestión + "te respondemos mañana a las 9".

**Consecuencia operativa:** el retiro en 2 h exige que alguien en el local esté mirando la bandeja de pedidos. Definir un responsable por turno y un aviso sonoro/alerta. Sin eso, la promesa es marketing.

---

## 7. Precios de referencia: cómo publicar sin mentir

Dijiste que los precios serán al final y que por ahora son de referencia. Eso tiene tres efectos que hay que resolver ahora, no en la Fase 2:

1. **En la landing (Fase 1) no se publica precio exacto.** Se usa rango: **"desde $X"** o *"precio de referencia, sujeto a confirmación al confirmar el pedido"*. Nunca un número exacto que después cambie: el cliente lo recuerda y lo reclama.
2. **Nada de cuotas todavía.** Anunciar "3 cuotas sin interés" sobre un precio provisorio es una promesa que no se puede sostener y complica la posición frente al consumidor.
3. **No cargar catálogo en Meta ni en Google Merchant Center hasta el congelamiento de precios.** Los feeds exigen precio exacto y consistente entre web, feed y checkout; con precios provisorios se rechazan o se desaprueban los anuncios.

**Antes de la Fase 2 hace falta un hito formal: `freeze de precios`** (fecha, responsable, versión del archivo `precios.csv`). Desde ese momento el precio es público, exacto, con impuestos y con la política de cuotas definida.

---

## 8. Checklist de activos de marca pendientes

- [ ] Logo vectorial (SVG/AI) + versión reducida + negativa + una tinta
- [ ] Rojo canónico confirmado (HEX + CMYK) y tipografía con licencia
- [ ] Fotografía de la línea `basic` con fondo y luz consistentes (mismo encuadre en todo el catálogo)
- [ ] Manual de 2 páginas: paleta, tipografía, proporción de rojo, usos incorrectos
- [ ] Búsqueda de antecedentes en INPI (clases 25 y 35)
- [ ] Bio y nombre de usuario unificados en Instagram, TikTok y WhatsApp Business

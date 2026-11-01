# Runbook: retiro en 2 horas

La promesa más fuerte de la marca y la más fácil de romper. Un pedido que sale tarde cuesta más que la publicidad que lo trajo.

**Alcance:** pedidos con pago acreditado y retiro en sucursal.
**Horario:** lunes a sábado, 9 a 19, con cita o confirmación previa.

---

## 1. Las cinco reglas

1. **El reloj arranca cuando impacta el pago**, no cuando entra el mensaje. Un pedido sin pago acreditado no está en plazo.
2. **Siempre hay un responsable por turno** mirando la bandeja de pedidos. Si nadie mira, no hay promesa.
3. **Confirmación antes de preparar.** Si el cliente no confirmó sucursal y horario, no se prepara: se le pregunta.
4. **Fuera de horario no se promete 2 horas.** Se promete "al abrir el siguiente día hábil", y se dice con la hora exacta.
5. **Si el talle no está en esa sucursal, se avisa antes de preparar** y se ofrece la sucursal que lo tiene o el envío.

---

## 2. Flujo paso a paso

| Paso | Quién | Qué hace | Tiempo máximo |
|---|---|---|---|
| 1 | Local asignado | Ve el pedido en la bandeja con pago acreditado | 15 min |
| 2 | Local | Verifica stock físico del talle y color en la góndola | 10 min |
| 3 | Local | Prepara: prenda, control de etiqueta, bolsa, número de pedido | 20 min |
| 4 | Local | Avisa al cliente por WhatsApp: "está listo, te esperamos hoy de 9 a 19" | 15 min |
| 5 | Local | Espera la cita y entrega contra número de pedido o DNI | — |
| 6 | Local | Marca el pedido como entregado en el sistema | inmediato |

**Holgura total:** 60 minutos de trabajo real dentro de una ventana de 120. El resto es espera del cliente. Si el paso 1 tarda una hora, no hay forma de cumplir.

---

## 3. Qué hace el responsable al abrir y al cerrar

**Al abrir (9:00)**
- [ ] Revisar pedidos del día anterior que entraron después de las 19.
- [ ] Confirmar que los pagos acreditados tienen pedido preparado.
- [ ] Avisar a cada cliente pendiente con su horario.

**Al cerrar (18:30, antes de las 19)**
- [ ] Cerrar los pedidos que quedan listos para hoy.
- [ ] Avisar a los que no llegaron a retirar: "te lo guardamos hasta [fecha]".
- [ ] Anotar en el registro: pedidos recibidos, preparados, entregados y pendientes.

---

## 4. Excepciones y cómo se resuelven

| Situación | Qué se hace | Qué NO se hace |
|---|---|---|
| El pago no se acredita | Se avisa: "estamos esperando la acreditación, en cuanto impacte lo preparo" | No se prepara "por las dudas" |
| El talle no está en esa sucursal | Se ofrece la sucursal que lo tiene (traslado en el día) o envío sin cargo | No se cambia el talle por iniciativa propia |
| El cliente llega después de las 19 | Se guarda el pedido y se coordina el día siguiente | No se deja la bolsa en la puerta |
| El cliente no confirma | Se envía un recordatorio a las 2 horas y otro al día siguiente; después se libera el stock a las 72 h | No se reserva stock indefinidamente |
| Se rompe la promesa | Se avisa antes de que el cliente pregunte, se ofrece una compensación concreta (envío gratis o descuento en la próxima) y se registra el caso | No se explica con "el sistema no anduvo" |

---

## 5. Registro diario (una línea por pedido)

```
fecha | hora_pago | hora_listo | hora_entrega | sucursal | demora_min | cumplió_2h (S/N) | motivo_si_no
```

**Métrica de la promesa:** % de pedidos con `cumplió_2h = S`. Meta: 90% en el primer mes, 95% al tercero. Si baja del 85%, la promesa se retira de la web el mismo día: una promesa que no se cumple es peor que no prometerla.

---

## 6. Qué necesita el local para poder cumplir

- [ ] Una persona designada por turno con acceso a la bandeja de pedidos.
- [ ] Alerta sonora o notificación en el teléfono del local.
- [ ] Un lugar físico identificado para pedidos listos (no en el mostrador).
- [ ] Bolsas, etiquetas y cinta para preparar sin buscar nada.
- [ ] El número de WhatsApp del local separado del personal.
- [ ] Acceso al stock de las otras 3 sucursales para ofrecer alternativa.

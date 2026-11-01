# Higgsfield API — notas de integración

Estado: **funcionando**. Credencial y circuito completo verificados el 28/10/2026.

## Credencial

- Archivo: `.secrets/higgsfield.txt` (nunca se imprime completa ni se pega en el chat).
- Formato: `KEY=<uuid>:<secret>` — la consola muestra la cadena ya unida, con dos puntos.
- Cabecera correcta: `Authorization: Key <uuid>:<secret>`.
- La documentación habla de `key-id` + `key-secret`; la consola los entrega juntos y la API los acepta así.

## Diagnóstico rápido

```
node qa/higgsfield.mjs probe
```

Consulta un pedido inexistente. `404` = credencial aceptada; `401` = rechazada.

## Cuenta y costos

- La API es **otra cuenta**: saldo prepago en dólares, mínimo USD 5. No consume los créditos del plan.
- Modelo usado: `higgsfield-ai/soul/v2/standard` (SOUL 2, texto a imagen) a **USD 0.0032 por imagen**.
- Con USD 5 alcanzan ~1.500 imágenes: el costo no es la restricción, la calidad sí.

## Endpoint probado

```
POST https://api.higgsfield.ai/higgsfield-ai/soul/v2/standard
```

Body mínimo válido:

```json
{ "prompt": "texto en el idioma que sea", "aspect_ratio": "3:4" }
```

Valores aceptados de `aspect_ratio`: `9:16`, `16:9`, `4:3`, `3:4`, `1:1`, `2:3`, `3:2`.
**No existe `4:5`** (el formato de nuestras tarjetas): se genera en `3:4` y se recorta.

## Ciclo

1. `POST /<endpoint-id>` → `200` con `request_id` y estado `queued`.
2. `GET /requests/<id>/status` → `in_progress` hasta `completed` (18 s en la prueba).
3. `completed` trae `images[].url` (CloudFront, válido 7 días). Descargar y guardar.

Estados terminales: `completed`, `failed`, `nsfw`, `canceled`.

## Cliente propio

```
node qa/higgsfield.mjs probe
node qa/higgsfield.mjs submit --endpoint <id> --body <json> [--confirmar-costos]
node qa/higgsfield.mjs status <request_id>
node qa/higgsfield.mjs wait <request_id> [--cada 5] [--max 300]
node qa/higgsfield.mjs download <request_id> --out <carpeta>
```

Sin `--confirmar-costos` el envío es una simulación: muestra el body y no gasta.

## Lo que aprendimos sobre la calidad (prueba del 28/10)

Una remera blanca en flat lay salió con la estructura del cuello mal resuelta y una manga
asimétrica. Sirve para fondos, props y bocetos; **no** para representar una prenda que el
cliente va a recibir. Para el catálogo sigue mandando la foto real del local.

## Pendiente

- Buscar en el catálogo el endpoint de **edición / quita de fondo** (para la foto del espejo).
  SOUL 2 sólo genera desde texto.
- Definir tope de gasto por trabajo y anotarlo acá.

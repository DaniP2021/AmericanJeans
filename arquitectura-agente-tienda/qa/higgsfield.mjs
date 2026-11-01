/**
 * Cliente mínimo de la API de Higgsfield.
 *
 * Comandos:
 *   node qa/higgsfield.mjs probe
 *       Verifica credenciales contra un pedido inexistente (no gasta).
 *   node qa/higgsfield.mjs submit --endpoint <id> --body <archivo.json>
 *       Envía una generación. Sin --confirmar-costos no envía nada: muestra qué haría.
 *   node qa/higgsfield.mjs status <request_id>
 *   node qa/higgsfield.mjs wait <request_id> [--cada 5] [--max 300]
 *   node qa/higgsfield.mjs download <request_id> --out <carpeta>
 *
 * La credencial se lee de .secrets/higgsfield.txt y nunca se imprime completa.
 */

import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, '..', '..');
const CRED = join(RAIZ, '.secrets', 'higgsfield.txt');
const BASE = 'https://api.higgsfield.ai';
const TIMEOUT_MS = 20000;

function credencial() {
  if (!existsSync(CRED)) {
    throw new Error(`No existe ${CRED}. Pegá ahí: KEY=<uuid>:<secret>`);
  }
  const txt = readFileSync(CRED, 'utf8').replace(/^\uFEFF/, '');
  let clave = null;
  for (const cruda of txt.split(/\r?\n/)) {
    const linea = cruda.replace(/^\uFEFF/, '').trim();
    if (!linea || linea.startsWith('#')) continue;
    const i = linea.indexOf('=');
    if (i > 0 && linea.slice(0, i).trim().toUpperCase() === 'KEY') {
      clave = linea.slice(i + 1).trim().replace(/^["']|["']$/g, '');
      break;
    }
  }
  if (!clave) throw new Error('El archivo no tiene una línea que empiece con KEY=');
  if (!clave.includes(':')) {
    throw new Error('La clave debe ser <uuid>:<secret> (dos partes separadas por dos puntos)');
  }
  return clave;
}

function cabeceras(extra = {}) {
  return { Authorization: `Key ${credencial()}`, ...extra };
}

async function pedir(ruta, opciones = {}) {
  const control = new AbortController();
  const t = setTimeout(() => control.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(BASE + ruta, { ...opciones, signal: control.signal });
    const texto = await r.text();
    let json = null;
    try { json = texto ? JSON.parse(texto) : null; } catch { /* respuesta no JSON */ }
    return { status: r.status, json, texto };
  } finally {
    clearTimeout(t);
  }
}

const args = process.argv.slice(2);
const cmd = args[0];
const opcion = (nombre, def = null) => {
  const i = args.indexOf(`--${nombre}`);
  return i >= 0 && args[i + 1] ? args[i + 1] : def;
};
const bandera = (nombre) => args.includes(`--${nombre}`);

function salir(msg, codigo = 1) {
  console.log(msg);
  process.exit(codigo);
}

async function probe() {
  const r = await pedir('/requests/00000000-0000-0000-0000-000000000000/status', { headers: cabeceras() });
  if (r.status === 404) salir('Credencial aceptada (404 = pedido inexistente).', 0);
  if (r.status === 401) salir('Credencial rechazada (401).');
  salir(`Respuesta inesperada: HTTP ${r.status} ${r.texto.slice(0, 200)}`);
}

async function submit() {
  const endpoint = opcion('endpoint');
  const bodyPath = opcion('body');
  if (!endpoint || !bodyPath) salir('Uso: submit --endpoint <id> --body <archivo.json> [--confirmar-costos]');

  const cuerpo = readFileSync(resolve(bodyPath), 'utf8').replace(/^\uFEFF/, '');
  let payload;
  try { payload = JSON.parse(cuerpo); } catch (e) { salir(`El body no es JSON válido: ${e.message}`); }

  console.log(`Endpoint: POST ${BASE}/${endpoint}`);
  console.log(`Body: ${JSON.stringify(payload).slice(0, 400)}`);

  if (!bandera('confirmar-costos')) {
    console.log('\n[simulación] No se envió nada. Para enviar de verdad, agregá --confirmar-costos');
    console.log('después de ver el costo estimado y aprobarlo.');
    return;
  }

  const r = await pedir(`/${endpoint}`, {
    method: 'POST',
    headers: cabeceras({
      'Content-Type': 'application/json',
      'Idempotency-Key': opcion('idempotencia', crypto.randomUUID()),
    }),
    body: cuerpo,
  });

  console.log(`\nHTTP ${r.status}`);
  if (r.json) console.log(JSON.stringify(r.json, null, 2).slice(0, 1200));
  else console.log(r.texto.slice(0, 800));

  if (r.status >= 400) {
    if (r.status === 402 || r.status === 403) {
      console.log('\nSin saldo o cuenta sin habilitar: cargá saldo en la consola de la API.');
    }
    process.exit(1);
  }
}

async function status(id) {
  if (!id) salir('Uso: status <request_id>');
  const r = await pedir(`/requests/${id}/status`, { headers: cabeceras() });
  console.log(`HTTP ${r.status}`);
  console.log(r.json ? JSON.stringify(r.json, null, 2) : r.texto.slice(0, 800));
  return r.json;
}

async function wait(id) {
  if (!id) salir('Uso: wait <request_id> [--cada 5] [--max 300]');
  const cada = Number(opcion('cada', 5)) * 1000;
  const max = Number(opcion('max', 300)) * 1000;
  const inicio = Date.now();
  while (Date.now() - inicio < max) {
    const r = await pedir(`/requests/${id}/status`, { headers: cabeceras() });
    const estado = r.json?.status ?? (r.status === 200 ? 'desconocido' : `HTTP ${r.status}`);
    console.log(`${new Date().toLocaleTimeString()} · ${estado}`);
    if (['completed', 'failed', 'nsfw', 'canceled'].includes(estado)) {
      console.log(JSON.stringify(r.json, null, 2));
      return;
    }
    await new Promise((ok) => setTimeout(ok, cada));
  }
  salir('Se agotó el tiempo de espera; el pedido sigue en curso.');
}

async function download(id) {
  const salida = opcion('out', join(RAIZ, 'arquitectura-agente-tienda', 'landing', 'img'));
  if (!id) salir('Uso: download <request_id> --out <carpeta>');
  const r = await pedir(`/requests/${id}/status`, { headers: cabeceras() });
  if (r.status !== 200) salir(`No pude leer el pedido: HTTP ${r.status}`);
  const urls = [];
  const recorrer = (v) => {
    if (typeof v === 'string' && /^https?:\/\//.test(v) && /\.(png|jpe?g|webp|mp4|mov|webm)(\?|$)/i.test(v)) urls.push(v);
    else if (Array.isArray(v)) v.forEach(recorrer);
    else if (v && typeof v === 'object') Object.values(v).forEach(recorrer);
  };
  recorrer(r.json);
  if (!urls.length) salir('El pedido no tiene archivos descargables todavía.');

  mkdirSync(salida, { recursive: true });
  for (const [i, u] of urls.entries()) {
    const ext = u.match(/\.(png|jpe?g|webp|mp4|mov|webm)/i)[1].toLowerCase();
    const destino = join(salida, `hf-${id.slice(0, 8)}-${i + 1}.${ext}`);
    const resp = await fetch(u);
    if (!resp.ok) { console.log(`Fallo la descarga ${u}: HTTP ${resp.status}`); continue; }
    writeFileSync(destino, Buffer.from(await resp.arrayBuffer()));
    console.log('guardado:', destino);
  }
}

switch (cmd) {
  case 'probe': await probe(); break;
  case 'submit': await submit(); break;
  case 'status': await status(args[1]); break;
  case 'wait': await wait(args[1]); break;
  case 'download': await download(args[1]); break;
  default:
    console.log('Comandos: probe | submit | status | wait | download');
    console.log('Ver el encabezado del archivo para el uso de cada uno.');
    process.exit(2);
}

/**
 * Sonda de autenticación de la API de Higgsfield (Node).
 *
 * La consola entrega una sola cadena; la documentación pide `Key KEY_ID:KEY_SECRET`.
 * Se prueban las variantes contra un pedido inexistente: 401 = credencial rechazada,
 * 404 = credencial aceptada. No genera nada ni consume saldo.
 *
 * Uso: node qa/higgsfield_probe.mjs [ruta-de-credenciales]
 */

import { readFileSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = dirname(fileURLToPath(import.meta.url));
const RUTA_POR_DEFECTO = resolve(AQUI, '..', '..', '.secrets', 'higgsfield.txt');
const BASE = 'https://api.higgsfield.ai';
const RECURSO = '/requests/00000000-0000-0000-0000-000000000000/status';
const TIMEOUT_MS = 8000;

function enmascarar(v) {
  if (!v) return '(vacío)';
  if (v.length <= 8) return '*'.repeat(v.length);
  return `${v.slice(0, 4)}…${v.slice(-3)} (len ${v.length})`;
}

function leer(ruta) {
  if (!existsSync(ruta)) {
    console.log(`No existe el archivo: ${ruta}`);
    console.log('Pegá la clave adentro, en una línea:  KEY=tu-clave');
    process.exit(2);
  }
  const texto = readFileSync(ruta, 'utf8').replace(/^\uFEFF/, '');
  const valores = {};
  const sueltas = [];
  for (const cruda of texto.split(/\r?\n/)) {
    const linea = cruda.replace(/^\uFEFF/, '').trim();
    if (!linea || linea.startsWith('#')) continue;
    const i = linea.indexOf('=');
    if (i > 0) valores[linea.slice(0, i).trim().toUpperCase()] = linea.slice(i + 1).trim().replace(/^["']|["']$/g, '');
    else sueltas.push(linea);
  }
  return { valores, sueltas };
}

function variantes(clave) {
  const salida = [];
  if (clave.includes(':')) {
    const [id, sec] = [clave.slice(0, clave.indexOf(':')), clave.slice(clave.indexOf(':') + 1)];
    salida.push(
      { headers: { Authorization: `Key ${clave}` }, etiqueta: 'Key <id:secret>' },
      { headers: { Authorization: `Basic ${Buffer.from(clave).toString('base64')}` }, etiqueta: 'Basic <id:secret>' },
      { headers: { Authorization: `Key ${id}`, 'X-API-Key-Secret': sec }, etiqueta: 'Key <id> + X-API-Key-Secret' },
      { headers: { Authorization: `Key ${id}`, 'X-API-Secret': sec }, etiqueta: 'Key <id> + X-API-Secret' },
    );
  }
  salida.push(
    { headers: { Authorization: `Key ${clave}` }, etiqueta: 'Key <clave>' },
    { headers: { Authorization: `Bearer ${clave}` }, etiqueta: 'Bearer <clave>' },
    { headers: { 'X-API-Key': clave }, etiqueta: 'X-API-Key: <clave>' },
  );
  return salida;
}

async function probar({ headers, etiqueta }) {
  const control = new AbortController();
  const t = setTimeout(() => control.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(BASE + RECURSO, { headers, signal: control.signal });
    const cuerpo = (await r.text()).slice(0, 180).replace(/\s+/g, ' ');
    return { etiqueta, codigo: r.status, cuerpo };
  } catch (e) {
    return { etiqueta, codigo: null, cuerpo: `${e.name}: ${e.cause?.code ?? e.message}` };
  } finally {
    clearTimeout(t);
  }
}

const ruta = process.argv[2] ? resolve(process.argv[2]) : RUTA_POR_DEFECTO;
const { valores, sueltas } = leer(ruta);

let clave = valores.KEY ?? valores.API_KEY ?? valores.HF_API_KEY;
if (!clave && valores.KEY_ID && valores.SECRET) clave = `${valores.KEY_ID}:${valores.SECRET}`;
if (!clave && sueltas.length) clave = sueltas[0];

if (!clave) {
  console.log('El archivo existe pero no tiene ninguna clave. Debe decir:  KEY=...');
  process.exit(2);
}

console.log(`Clave detectada: ${enmascarar(clave)}`);
const lista = variantes(clave);
console.log(`\nProbando ${lista.length} variantes contra ${BASE}${RECURSO}\n`);

const resultados = [];
for (const v of lista) {
  const r = await probar(v);
  let estado;
  if (r.codigo === null) estado = 'SIN RESPUESTA';
  else if (r.codigo === 401) estado = 'rechazada';
  else if (r.codigo === 403) estado = 'prohibida';
  else if (r.codigo === 404) estado = 'ACEPTADA (recurso inexistente)';
  else if (r.codigo === 400 || r.codigo === 422) estado = 'ACEPTADA (pedido inválido)';
  else if (r.codigo >= 200 && r.codigo < 300) estado = 'ACEPTADA';
  else estado = `respuesta ${r.codigo}`;
  resultados.push({ ...r, estado });
  console.log(`  ${estado.padEnd(32)} ${r.etiqueta.padEnd(30)} HTTP ${r.codigo}`);
  if (r.cuerpo) console.log(`      → ${r.cuerpo}`);
}

const ok = resultados.find((r) => [200, 204, 400, 404, 422].includes(r.codigo));
console.log();
if (ok) {
  console.log(`Forma correcta: ${ok.etiqueta}`);
  console.log('Con eso escribo el cliente definitivo.');
} else if (resultados.every((r) => r.codigo === null)) {
  console.log('No hubo respuesta de la API: revisar conexión.');
} else {
  console.log('Ninguna variante autenticó: la credencial no sirve para esta API.');
  console.log('Siguiente paso: soporte de Higgsfield, o usar el plan en la web.');
}

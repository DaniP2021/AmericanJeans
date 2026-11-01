"""Sonda de autenticación de la API de Higgsfield.

La consola entrega una sola cadena y la documentación pide `Key KEY_ID:KEY_SECRET`.
En lugar de suponer, se prueban las variantes contra un pedido inexistente:
un 401 significa credencial rechazada; un 404 (o 400) significa que la credencial
fue aceptada y sólo falta el recurso.

No genera nada y no consume saldo.

Uso: python qa/higgsfield_probe.py [ruta-del-archivo-de-credenciales]
"""

import json
import os
import ssl
import sys
import urllib.error
import urllib.request

BASE = "https://api.higgsfield.ai"
RECURSO = "/requests/00000000-0000-0000-0000-000000000000/status"
TIMEOUT = 15

RUTA_POR_DEFECTO = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".secrets", "higgsfield.txt"))


def leer_credenciales(ruta):
    """Acepta KEY=..., KEY_ID=.../SECRET=..., o una línea suelta con la clave."""
    if not os.path.exists(ruta):
        print(f"No existe el archivo: {ruta}")
        print("Creá el archivo con la clave adentro, en una línea, así:")
        print("  KEY=la-clave-que-te-dio-la-consola")
        sys.exit(2)

    valores = {}
    sueltas = []
    # utf-8-sig: tolera el BOM que agregan Notepad y PowerShell al guardar
    with open(ruta, encoding="utf-8-sig", errors="replace") as f:
        for linea in f:
            linea = linea.replace("\ufeff", "").strip()
            if not linea or linea.startswith("#"):
                continue
            if "=" in linea:
                k, v = linea.split("=", 1)
                valores[k.strip().upper()] = v.strip().strip('"').strip("'")
            else:
                sueltas.append(linea)
    return valores, sueltas


def enmascarar(valor):
    if len(valor) <= 8:
        return "*" * len(valor)
    return f"{valor[:4]}…{valor[-3:]} (len {len(valor)})"


def probar(cabeceras, etiqueta):
    req = urllib.request.Request(BASE + RECURSO, headers=cabeceras, method="GET")
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            return etiqueta, r.status, (r.read(200) or b"").decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        cuerpo = e.read(300).decode("utf-8", "replace")
        return etiqueta, e.code, cuerpo
    except Exception as e:  # red, TLS, timeout
        return etiqueta, None, f"error de conexión: {type(e).__name__}: {e}"


def variantes(clave, etiqueta):
    """Formas plausibles de mandar una credencial de una sola cadena."""
    import base64

    salida = []
    if ":" in clave:
        kid, sec = clave.split(":", 1)
        salida += [
            ({"Authorization": f"Key {clave}"}, f"Key <{etiqueta} con dos partes>"),
            ({"Authorization": f"Basic {base64.b64encode(clave.encode()).decode()}"},
             f"Basic <{etiqueta} en base64>"),
            ({"Authorization": f"Key {kid}", "X-API-Key-Secret": sec},
             "Key <id> + X-API-Key-Secret"),
            ({"Authorization": f"Key {kid}", "X-API-Secret": sec},
             "Key <id> + X-API-Secret"),
        ]
    salida += [
        ({"Authorization": f"Key {clave}"}, f"Key <{etiqueta}>"),
        ({"Authorization": f"Bearer {clave}"}, f"Bearer <{etiqueta}>"),
        ({"X-API-Key": clave}, f"X-API-Key: <{etiqueta}>"),
        ({"Authorization": clave}, f"Authorization: <{etiqueta}>"),
    ]
    return salida


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    valores, sueltas = leer_credenciales(ruta)

    candidatos = []

    if "KEY" in valores:
        clave = valores["KEY"]
        print(f"clave detectada: {enmascarar(clave)}")
        candidatos += variantes(clave, "clave")
    elif "KEY_ID" in valores and "SECRET" in valores:
        kid, sec = valores["KEY_ID"], valores["SECRET"]
        print(f"par detectado: id {enmascarar(kid)} · secret {enmascarar(sec)}")
        candidatos += [
            ({"Authorization": f"Key {kid}:{sec}"}, "Key ID:SECRET (según docs)"),
            ({"Authorization": f"Key {sec}"}, "Key <secret>"),
            ({"Authorization": f"Bearer {sec}"}, "Bearer <secret>"),
        ]
    elif sueltas:
        clave = sueltas[0]
        print(f"línea suelta detectada: {enmascarar(clave)}")
        candidatos += variantes(clave, "línea")
    else:
        print("No encontré ninguna credencial en el archivo.")
        sys.exit(2)

    print(f"\nProbando {len(candidatos)} variantes contra {BASE}{RECURSO}\n")
    resultados = []
    for cabeceras, etiqueta in candidatos:
        etiqueta, codigo, cuerpo = probar(cabeceras, etiqueta)
        if codigo is None:
            estado = "SIN RED"
        elif codigo == 401:
            estado = "rechazada"
        elif codigo == 403:
            estado = "prohibida (sin saldo o sin permiso)"
        elif codigo == 404:
            estado = "ACEPTADA (recurso inexistente)"
        elif 200 <= codigo < 300:
            estado = "ACEPTADA"
        else:
            estado = f"respuesta {codigo}"
        resultados.append((etiqueta, codigo, estado, cuerpo))
        print(f"  {estado:34} {etiqueta:34} HTTP {codigo}")
        if cuerpo:
            print(f"      → {cuerpo[:160].replace(chr(10), ' ')}")

    validas = [r for r in resultados if r[1] in (200, 204, 400, 404, 422)]
    print()
    if validas:
        print("Forma correcta:", validas[0][0])
        print("Con eso alcanza para escribir el cliente.")
    else:
        print("Ninguna variante autenticó. Revisá que la clave esté completa")
        print("y que la cuenta tenga saldo; si sigue igual, la consola está")
        print("emitiendo otro tipo de credencial y hay que pedir soporte.")


if __name__ == "__main__":
    main()

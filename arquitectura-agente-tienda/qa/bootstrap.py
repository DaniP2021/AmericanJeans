"""Deja una PC lista para trabajar con el catálogo, sin pasos manuales.

Instala las dependencias de Python dentro del proyecto (`.pylibs/`, sin tocar el sistema) y baja
los modelos de segmentación a `.models/`. Se puede correr las veces que haga falta: lo que ya está
lo saltea.

    python qa/bootstrap.py              # dependencias + modelo chico (4,5 MB)
    python qa/bootstrap.py --completo   # además el modelo grande (167 MB), mejor calidad

Por qué no van en el repositorio: el modelo grande supera el límite de 100 MB por archivo de
GitHub, y las dependencias son 154 MB de binarios que se reinstalan solos en un minuto.
"""

import argparse
import io
import json
import os
import platform
import sys
import urllib.request
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
PYLIBS = os.path.join(RAIZ, ".pylibs")
MODELOS = os.path.join(RAIZ, ".models")

PAQUETES = ["onnxruntime", "opencv-python-headless"]

MODELOS_URL = {
    "u2netp.onnx": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx",
    "u2net.onnx": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
}


def log(msg):
    print(f"  {msg}", flush=True)


def rueda_para(paquete):
    """Elige la rueda que corresponde a este Python y a Windows de 64 bits."""
    version = f"{sys.version_info.major}{sys.version_info.minor}"
    with urllib.request.urlopen(f"https://pypi.org/pypi/{paquete}/json", timeout=60) as r:
        info = json.load(r)["info"]["version"]
    with urllib.request.urlopen(f"https://pypi.org/pypi/{paquete}/{info}/json", timeout=60) as r:
        archivos = json.load(r)["urls"]

    nombres = [a for a in archivos if a["filename"].endswith(".whl")]
    candidatas = [
        a for a in nombres
        if f"cp{version}" in a["filename"] and "win_amd64" in a["filename"]
    ]
    if not candidatas:
        candidatas = [a for a in nombres if "win_amd64" in a["filename"]]
    if not candidatas:
        raise RuntimeError(f"no hay rueda para Windows de {paquete} en Python {sys.version.split()[0]}")
    prefijo = paquete.replace("-", "_").split("_")[0]
    candidatas.sort(key=lambda a: (prefijo not in a["filename"].lower(), "abi3" not in a["filename"]))
    return candidatas[0], info


def instalar(paquete):
    destino_marca = os.path.join(PYLIBS, f".{paquete}.ok")
    if os.path.exists(destino_marca):
        log(f"{paquete}: ya instalado")
        return
    rueda, version = rueda_para(paquete)
    log(f"{paquete} {version}: bajando {rueda['filename']} ({rueda['size'] // 1024 // 1024} MB)")
    datos = urllib.request.urlopen(rueda["url"], timeout=600).read()
    os.makedirs(PYLIBS, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(datos)) as z:
        z.extractall(PYLIBS)
    open(destino_marca, "w").close()
    log(f"{paquete}: listo")


def bajar_modelo(nombre):
    destino = os.path.join(MODELOS, nombre)
    if os.path.exists(destino) and os.path.getsize(destino) > 1024 * 1024:
        log(f"{nombre}: ya está ({os.path.getsize(destino) // 1024 // 1024} MB)")
        return
    os.makedirs(MODELOS, exist_ok=True)
    log(f"{nombre}: bajando…")
    pedido = urllib.request.Request(MODELOS_URL[nombre], headers={"User-Agent": "american-jeans"})
    datos = urllib.request.urlopen(pedido, timeout=900).read()
    with open(destino, "wb") as f:
        f.write(datos)
    log(f"{nombre}: listo ({len(datos) // 1024 // 1024} MB)")


def verificar():
    sys.path.insert(0, PYLIBS)
    fallos = []
    for modulo, nombre in [("PIL", "Pillow"), ("numpy", "numpy"),
                           ("cv2", "opencv"), ("onnxruntime", "onnxruntime")]:
        try:
            __import__(modulo)
            log(f"{nombre}: ok")
        except Exception as e:
            fallos.append(f"{nombre}: {e}")
            log(f"{nombre}: FALLA — {e}")
    return fallos


def main():
    p = argparse.ArgumentParser(description="Prepara la PC para trabajar con el catálogo.")
    p.add_argument("--completo", action="store_true", help="baja también el modelo grande (167 MB)")
    args = p.parse_args()

    print()
    print(f"Python {sys.version.split()[0]} · {platform.system()} {platform.machine()}")
    print()

    if sys.version_info < (3, 10):
        print("Hace falta Python 3.10 o más nuevo.")
        sys.exit(1)

    print("Dependencias")
    for paquete in PAQUETES:
        try:
            instalar(paquete)
        except Exception as e:
            print(f"\nNo se pudo instalar {paquete}: {e}")
            print("Alternativa: pip install --target .pylibs " + " ".join(PAQUETES))
            sys.exit(1)

    print("\nModelos de segmentación")
    bajar_modelo("u2netp.onnx")
    if args.completo:
        bajar_modelo("u2net.onnx")
    else:
        log("u2net.onnx: salteado (usá --completo si querés el modelo de mejor calidad)")

    print("\nVerificación")
    fallos = verificar()
    print()
    if fallos:
        print("Terminó con problemas:")
        for f in fallos:
            print("  ·", f)
        sys.exit(1)
    print("Todo listo. Ya podés correr la herramienta de fotos:")
    print("  python arquitectura-agente-tienda/herramientas/fotocatalogo.py -e <carpeta> -s <salida>")


if __name__ == "__main__":
    main()

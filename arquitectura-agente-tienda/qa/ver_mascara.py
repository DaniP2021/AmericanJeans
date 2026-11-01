"""Depuración: guarda la máscara U2Net de una foto para ver qué detecta."""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", ".pylibs")))

import numpy as np  # noqa: E402
import onnxruntime as ort  # noqa: E402
from PIL import Image  # noqa: E402

MODELO = os.path.abspath(os.path.join(AQUI, "..", "..", ".models", "u2net.onnx"))
entrada = sys.argv[1]
salida = sys.argv[2]

im = Image.open(entrada).convert("RGB")
s = ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])
n = s.get_inputs()[0].name
chica = im.resize((320, 320), Image.LANCZOS)
a = np.asarray(chica).astype(np.float32) / 255.0
a = (a - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
a = a.transpose(2, 0, 1)[None, ...].astype(np.float32)

bruto = s.run(None, {n: a})[0][0, 0]
bruto = (bruto - bruto.min()) / (bruto.max() - bruto.min() + 1e-8)
m = Image.fromarray((bruto * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS)
m.save(salida)

arr = np.asarray(m)
print(f"{entrada}: {im.size} · píxeles >100: {(arr > 100).mean() * 100:.1f}%")

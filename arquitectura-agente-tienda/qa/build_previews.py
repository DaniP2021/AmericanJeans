"""Genera preview-a.html y preview-b.html a partir de index.html (sólo agrega el theme)."""

import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing")
BASE = os.path.normpath(BASE)

LINK = '<link rel="stylesheet" href="styles.css">'

with open(os.path.join(BASE, "index.html"), encoding="utf-8") as f:
    src = f.read()

if LINK not in src:
    raise SystemExit("no se encontró el link a styles.css en index.html")

for key in ("a", "b"):
    out = src.replace(LINK, LINK + '\n<link rel="stylesheet" href="theme-%s.css">' % key)
    destino = os.path.join(BASE, "preview-%s.html" % key)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(out)
    print("ok", os.path.basename(destino))

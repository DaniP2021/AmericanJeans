"""Genera catalogo.html: prendas transparentes, fondo conmutable, filtro por ocasión y galería.

La categoría es la ocasión de uso —formal, semi formal, casual, casual sport, sport— y el tipo
de prenda queda como etiqueta en la ficha. El cliente busca por ocasión; la ficha dice qué es.
"""

import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
CAT = os.path.join(RAIZ, "CATALOGO")
TRANSP = os.path.join(CAT, "seleccion-transparente")

OCASIONES = ["Vestir", "Oficina", "Informal", "Fin de semana", "Looks"]

# slug, ocasión, tipo, título, color, fotos adicionales
PRODUCTOS = [
    ("gabardina-recto-expansible-corte-chino-cuatro-colores", "Oficina", "Pantalón",
     "Gabardina recto expansible corte chino", "Cuatro colores", []),
    ("pantalon-de-vestir-cuatro-colores", "Vestir", "Pantalón",
     "Pantalón de vestir", "Cuatro colores", ["-alt1"]),
    ("camisa-lisa-seis-colores", "Vestir", "Camisa",
     "Camisa de vestir", "Seis colores", ["-alt1"]),
    ("corbata-lisa-varios-colores", "Vestir", "Corbata",
     "Corbata lisa", "Negro, azul, rojo y verde", ["-alt1", "-alt2"]),
    ("chaleco-de-vestir-negro", "Vestir", "Chaleco",
     "Chaleco de vestir", "Negro", ["-alt1"]),
    ("camisa-estampada-manga-larga-seis-colores", "Oficina", "Camisa",
     "Camisa estampada manga larga", "Seis colores", ["-alt1"]),
    ("sweter-cuello-v-azul-marino", "Oficina", "Sweter",
     "Sweter cuello V", "Azul marino", []),
    ("sweter-medio-cierre", "Oficina", "Sweter",
     "Sweter medio cierre", "Azul y negro", ["-alt1"]),
    ("look-camisas-y-pantalon-de-vestir", "Looks", "Combinación",
     "Camisas lisas con pantalón de vestir", "Look armado", []),
    ("look-camisa-de-vestir-con-corbata", "Looks", "Combinación",
     "Camisa de vestir con corbata", "Tres combinaciones", []),
    ("jean-clasico-tres-lavados", "Informal", "Jean",
     "Jean clásico", "Tres lavados", ["-alt1", "-alt2"]),
    ("gabardina-corte-jean-slim-fit-azul-y-negro", "Informal", "Pantalón",
     "Gabardina corte jean slim fit", "Azul y negro", []),
    ("chomba-rayada-cuatro-colores", "Informal", "Chomba",
     "Chomba rayada", "Cuatro colores", ["-alt1", "-alt2"]),
    ("bermuda-elastizada-corte-jean-negro-y-azul", "Informal", "Bermuda",
     "Bermuda corte jean", "Negro y azul", ["-alt1", "-alt2"]),
    ("pantalon-con-tres-chombas-bordo-blanco-marino", "Looks", "Combinación",
     "Pantalón con tres chombas", "Bordó, blanco, marino", []),
    ("pantalon-con-tres-chombas-rojo-blanco-marino", "Looks", "Combinación",
     "Pantalón con tres chombas", "Rojo, blanco, marino", []),
    ("pantalon-cargo-de-microfibra-cuatro-colores", "Fin de semana", "Pantalón",
     "Pantalón cargo de microfibra", "Cuatro colores", ["-alt1"]),
    ("conjunto-deportivo-oliva-negro", "Fin de semana", "Conjunto",
     "Conjunto deportivo microfibra", "Oliva y negro", ["-alt1"]),
]

# Muestras de prueba: quedan fuera hasta que lleguen las fotos de producción.
EXCLUIR = {
    "gabardina-corte-chino-beige",
    "gabardina-corte-chino-verde-oliva",
    "gabardina-corte-chino-tres-colores",
    "conjunto-deportivo-wafle-negro",
    "conjunto-deportivo-wafle-blanco",
    "conjunto-deportivo-wafle-bordo",
}
PRODUCTOS = [p for p in PRODUCTOS if p[0] not in EXCLUIR]

HTML = """<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo American Jeans</title>
<style>
  :root {{
    --tinta:#1C1512; --suave:#6E625B; --borde:#E4D6C8; --terracota:#B8452C;
    --crema:#FDF6F1; --arena:#F5E9DE; --tierra:#E8D8C9;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; color:var(--tinta); transition:background .35s ease;
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  }}
  body.lino {{
    background:
      radial-gradient(1200px 700px at 50% 12%, #FFFBF7 0%, rgba(255,251,247,0) 62%),
      linear-gradient(180deg, var(--crema) 0%, var(--arena) 46%, var(--tierra) 100%);
    background-attachment:fixed;
  }}
  body.blanco {{ background:#FFFFFF; }}

  header.top {{ padding:26px 26px 16px; border-bottom:1px solid var(--borde); }}
  header.top h1 {{ margin:0 0 6px; font-size:1.45rem; }}
  header.top p {{ margin:0; color:var(--suave); font-size:.88rem; }}

  .controles {{ padding:14px 26px 4px; display:flex; gap:22px; flex-wrap:wrap; align-items:center; }}
  .grupo {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }}
  .grupo > span {{ font-size:.74rem; color:var(--suave); letter-spacing:.04em; }}
  .pill {{
    font:inherit; font-size:.78rem; font-weight:700; cursor:pointer;
    padding:8px 15px; border-radius:999px; border:1px solid var(--borde);
    background:transparent; color:var(--tinta);
  }}
  .pill[aria-pressed="true"] {{ background:var(--tinta); color:#fff; border-color:var(--tinta); }}

  .sello {{ margin:12px 26px 0; padding:14px 16px; background:#fff; border-left:3px solid var(--terracota);
            border-radius:6px; font-size:.83rem; color:var(--suave); max-width:900px; line-height:1.55; }}
  .sello b {{ color:var(--tinta); }}

  main {{ padding:20px 26px 40px; display:grid; gap:28px;
          grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); }}

  .producto {{ display:flex; flex-direction:column; }}
  .producto[hidden] {{ display:none; }}
  .marco {{ position:relative; height:320px; padding:0; border:0; background:transparent;
            cursor:zoom-in; display:block; width:100%; }}
  .marco img {{
    position:absolute; inset:0; margin:auto; max-width:100%; max-height:100%;
    width:auto; height:auto; filter:drop-shadow(0 12px 18px rgba(120,86,62,.16));
    transition:opacity .3s ease, transform .3s ease;
  }}
  .marco .seg {{ opacity:0; }}
  .marco:hover .seg, .marco:focus-visible .seg {{ opacity:1; }}
  .marco:hover img {{ transform:translateY(-2px); }}
  body.blanco .marco img {{ filter:drop-shadow(0 10px 16px rgba(90,80,72,.10)); }}

  .cuantas {{ position:absolute; right:6px; bottom:6px; font-size:.66rem; font-weight:700;
              background:rgba(28,21,18,.72); color:#fff; padding:3px 8px; border-radius:999px; }}

  .chip {{ margin:12px 0 2px; font-size:.66rem; letter-spacing:.13em; text-transform:uppercase;
           color:var(--terracota); font-weight:800; }}
  .chip .tipo {{ color:var(--suave); font-weight:600; letter-spacing:.08em; }}
  h2 {{ margin:2px 0 0; font-size:.98rem; line-height:1.25; }}
  .color {{ margin:2px 0 12px; font-size:.82rem; color:var(--suave); }}
  .boton {{ margin-top:auto; display:block; text-align:center; text-decoration:none; padding:11px;
            background:var(--terracota); color:#fff; font-weight:700; font-size:.82rem;
            border-radius:6px; letter-spacing:.04em; }}
  .boton:hover {{ background:#9E3823; }}

  .vacio {{ padding:0 26px 40px; color:var(--suave); font-size:.9rem; display:none; }}
  .vacio.visible {{ display:block; }}

  .lupa {{ position:fixed; inset:0; background:rgba(20,15,12,.88); display:none;
           align-items:center; justify-content:center; z-index:50; padding:24px; }}
  .lupa.abierta {{ display:flex; }}
  .lupa img {{ max-width:92vw; max-height:86vh; border-radius:8px; }}
  .lupa .cerrar {{ position:absolute; top:18px; right:22px; font-size:2rem; line-height:1;
                   background:none; border:0; color:#fff; cursor:pointer; }}
  .lupa .mover {{ position:absolute; top:50%; transform:translateY(-50%); font-size:2.6rem;
                  background:none; border:0; color:#fff; cursor:pointer; padding:0 18px; }}
  .lupa .prev {{ left:0; }} .lupa .next {{ right:0; }}

  footer {{ padding:18px 26px 46px; color:var(--suave); font-size:.78rem; }}
  @media (max-width:720px) {{ .marco {{ height:260px; }} main {{ gap:20px; }} }}
{css_extra}
</style>
</head>
<body class="{bodyclass}">
{decor}
  <header class="top">
    <h1>Catálogo American Jeans</h1>
    <p>{n} productos · {fotos} fotos · ordenado por ocasión de uso</p>
  </header>

  <div class="controles">
    <div class="grupo">
      <span>OCASIÓN</span>
      <button class="pill" data-ocasion="todo" aria-pressed="true">Todo</button>
      {botones_ocasion}
    </div>
    <div class="grupo">
      <span>FONDO</span>
      <button class="pill" id="btn-lino" aria-pressed="true">Lino</button>
      <button class="pill" id="btn-blanco" aria-pressed="false">Blanco</button>
    </div>
  </div>

  <div class="sello">
    <b>Etiqueta de marca a la vista.</b> Camisas: etiqueta American Jeans cosida en el cuello.
    Jeans: parche de cuero American en la cintura. Conjuntos: etiqueta colgante American Jeans.
    En las demás prendas la foto no alcanza a mostrar la etiqueta.
  </div>

  <main id="grilla">{tarjetas}</main>
  <p class="vacio" id="vacio">No hay productos en esta ocasión todavía.</p>

  <footer>
    Las prendas van recortadas con transparencia: el fondo es de la página, no de la foto.
    Las categorías son de ocasión, no de tipo de prenda: el tipo figura en cada ficha.
  </footer>

<div class="lupa" id="lupa">
  <button class="cerrar" aria-label="Cerrar">&times;</button>
  <button class="mover prev" aria-label="Anterior">&#8249;</button>
  <img id="lupa-img" alt="">
  <button class="mover next" aria-label="Siguiente">&#8250;</button>
</div>

<script>
  const cuerpo = document.body;
  const bLino = document.getElementById('btn-lino');
  const bBlanco = document.getElementById('btn-blanco');
  function ponerFondo(fondo) {{
    cuerpo.classList.toggle('lino', fondo === 'lino');
    cuerpo.classList.toggle('blanco', fondo === 'blanco');
    bLino.setAttribute('aria-pressed', String(fondo === 'lino'));
    bBlanco.setAttribute('aria-pressed', String(fondo === 'blanco'));
    try {{ localStorage.setItem('aj-fondo', fondo); }} catch (e) {{}}
  }}
  bLino.addEventListener('click', () => ponerFondo('lino'));
  bBlanco.addEventListener('click', () => ponerFondo('blanco'));
  let guardado = null;
  try {{ guardado = localStorage.getItem('aj-fondo'); }} catch (e) {{}}
  ponerFondo(guardado === 'blanco' ? 'blanco' : 'lino');

  const fichas = [...document.querySelectorAll('.producto')];
  const pills = [...document.querySelectorAll('[data-ocasion]')];
  const vacio = document.getElementById('vacio');
  function filtrar(cual) {{
    let visibles = 0;
    for (const f of fichas) {{
      const ok = cual === 'todo' || f.dataset.ocasion === cual;
      f.hidden = !ok;
      if (ok) visibles++;
    }}
    for (const p of pills) p.setAttribute('aria-pressed', String(p.dataset.ocasion === cual));
    vacio.classList.toggle('visible', visibles === 0);
  }}
  for (const p of pills) p.addEventListener('click', () => filtrar(p.dataset.ocasion));

  const lupa = document.getElementById('lupa');
  const lupaImg = document.getElementById('lupa-img');
  let fotos = [], indice = 0;
  const mostrar = () => {{ lupaImg.src = fotos[indice]; }};
  document.querySelectorAll('.marco').forEach(m => {{
    m.addEventListener('click', () => {{
      fotos = (m.dataset.fotos || '').split('|').filter(Boolean);
      indice = 0; mostrar(); lupa.classList.add('abierta');
    }});
  }});
  const cerrar = () => lupa.classList.remove('abierta');
  lupa.querySelector('.cerrar').addEventListener('click', cerrar);
  lupa.querySelector('.prev').addEventListener('click', e => {{
    e.stopPropagation(); indice = (indice - 1 + fotos.length) % fotos.length; mostrar();
  }});
  lupa.querySelector('.next').addEventListener('click', e => {{
    e.stopPropagation(); indice = (indice + 1) % fotos.length; mostrar();
  }});
  lupa.addEventListener('click', e => {{ if (e.target === lupa) cerrar(); }});
  document.addEventListener('keydown', e => {{
    if (!lupa.classList.contains('abierta')) return;
    if (e.key === 'Escape') cerrar();
    if (e.key === 'ArrowLeft') {{ indice = (indice - 1 + fotos.length) % fotos.length; mostrar(); }}
    if (e.key === 'ArrowRight') {{ indice = (indice + 1) % fotos.length; mostrar(); }}
  }});
</script>
</body>
</html>"""


VARIANTES = {
    "catalogo.html": {
        "bodyclass": "lino",
        "css": "",
        "decor": "",
    },
    "catalogo-tarjetas.html": {
        "bodyclass": "lino tarjetas",
        "css": """
  body.tarjetas .producto { background:#fff; border:1px solid var(--borde); border-radius:12px;
                            padding:14px 14px 16px;
                            box-shadow:0 8px 18px rgba(120,86,62,.07); }
  body.tarjetas .marco { height:300px; }
  body.tarjetas .chip { margin-top:14px; }
""",
        "decor": "",
    },
}


def main():
    tarjetas = []
    total_fotos = 0
    faltantes = []
    for slug, ocasion, tipo, titulo, color, alts in PRODUCTOS:
        fotos = [slug + suf for suf in [""] + alts]
        fotos = [f for f in fotos if os.path.exists(os.path.join(TRANSP, f + "-720.webp"))]
        if not fotos:
            faltantes.append(slug)
            continue
        total_fotos += len(fotos)

        primaria, segunda = fotos[0], (fotos[1] if len(fotos) > 1 else None)
        urls1200 = "|".join(f"seleccion-transparente/{f}-1200.webp" for f in fotos)
        img_seg = (f'\n        <img class="seg" src="seleccion-transparente/{segunda}-720.webp" '
                   f'alt="{titulo}, otra vista" loading="lazy">' if segunda else "")
        contador = (f'\n        <span class="cuantas">{len(fotos)} fotos</span>' if len(fotos) > 1 else "")

        tarjetas.append(f"""
      <article class="producto" data-ocasion="{ocasion}">
        <button class="marco" data-fotos="{urls1200}" aria-label="Ver fotos de {titulo} {color}">
        <img src="seleccion-transparente/{primaria}-720.webp" alt="{titulo} {color}" loading="lazy">{img_seg}{contador}
        </button>
        <p class="chip">{ocasion} <span class="tipo">· {tipo}</span></p>
        <h2>{titulo}</h2>
        <p class="color">{color}</p>
        <a class="boton" href="#">Consultar</a>
      </article>""")

    presentes = {p[1] for p in PRODUCTOS}
    botones = "\n      ".join(
        f'<button class="pill" data-ocasion="{o}" aria-pressed="false">{o}</button>'
        for o in OCASIONES if o in presentes)

    if faltantes:
        print("sin fotos transparentes:", ", ".join(faltantes))

    for archivo, v in VARIANTES.items():
        destino = os.path.join(CAT, archivo)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(HTML.format(n=len(tarjetas), fotos=total_fotos, tarjetas="".join(tarjetas),
                                botones_ocasion=botones, bodyclass=v["bodyclass"],
                                css_extra=v["css"], decor=v["decor"]))
        print(f"{archivo} · {len(tarjetas)} productos · {total_fotos} fotos")


if __name__ == "__main__":
    main()

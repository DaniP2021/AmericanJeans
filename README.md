# American Jeans — catálogo y producción de fotos

Repositorio del catálogo de **American Jeans (línea `basic`)**: la herramienta que convierte fotos
crudas de prendas en imágenes de catálogo consistentes, el catálogo en sí, y los documentos de
identidad, precios y operación de la marca.

Todo está en español y pensado para trabajarse desde Windows con PowerShell.

---

## Qué hay acá

| Carpeta | Qué contiene |
|---|---|
| [`CATALOGO/`](CATALOGO) | El catálogo: fotos procesadas, prendas con transparencia, versiones web, kit de WhatsApp |
| [`arquitectura-agente-tienda/`](arquitectura-agente-tienda) | Herramientas, landing, documentos de marca, catálogo y operación |
| [`INDICE.md`](INDICE.md) | Mapa con enlaces a cada archivo del proyecto |
| [`PENDIENTES.md`](PENDIENTES.md) | Estado actual y qué sigue |

### El catálogo

18 productos, 33 fotos, ordenado por **ocasión de uso** y no por tipo de prenda:

| Categoría | Productos |
|---|---|
| Oficina | Sweter cuello V · Sweter medio cierre · Gabardina recto expansible · Camisa estampada |
| Vestir | Pantalón de vestir · Camisa de vestir · Corbata · Chaleco de vestir |
| Informal | Jean clásico · Gabardina corte jean slim · Chomba rayada · Bermuda corte jean |
| Fin de semana | Cargo de microfibra · Conjunto deportivo microfibra |
| Looks | Cuatro combinaciones armadas |

Dos presentaciones, con los mismos productos:

- [`CATALOGO/catalogo.html`](CATALOGO/catalogo.html) — la prenda se apoya sobre el fondo lino
- [`CATALOGO/catalogo-tarjetas.html`](CATALOGO/catalogo-tarjetas.html) — tarjetas blancas sobre lino

Índice para comparar: [`CATALOGO/versiones.html`](CATALOGO/versiones.html)

---

## La herramienta de fotos

Convierte una carpeta de fotos crudas en imágenes listas para el catálogo: recorta la prenda del
fondo, la centra en 4:5 con margen parejo, la apoya sobre blanco y exporta tres tamaños.

```
python arquitectura-agente-tienda/herramientas/fotocatalogo.py ^
  -e fotos\crudas -s fotos\catalogo --ratio 4:5 --fondo blanco --ancho 1200 --modelo grande
```

Después, para el catálogo web:

```
python arquitectura-agente-tienda/qa/exportar_transparentes.py
python arquitectura-agente-tienda/herramientas/generar_catalogo.py
python arquitectura-agente-tienda/qa/kit_whatsapp.py
```

El instructivo completo, con las reglas para disparar las fotos y los límites conocidos, está en
[`herramientas/LEEME.md`](arquitectura-agente-tienda/herramientas/LEEME.md).

### Requisitos

Python 3.12 con Pillow y numpy. Además, dos cosas que **no** están en el repositorio porque pesan
más de 300 MB en total:

- `.pylibs/` — OpenCV y ONNX Runtime
- `.models/` — modelos de segmentación U2Net (4,5 MB el chico, 167 MB el grande)

Se instalan una vez y quedan ignorados por git. El procedimiento está en el LEEME.

---

## Cómo se arma el catálogo

Los productos se declaran en dos listas de Python:

- `arquitectura-agente-tienda/herramientas/generar_catalogo.py` → lista `PRODUCTOS`
- `arquitectura-agente-tienda/qa/kit_whatsapp.py` → lista `FICHAS`

Cada entrada lleva el nombre del archivo, la ocasión, el tipo de prenda, el título, el color y las
fotos adicionales. Al correr los scripts, las dos versiones del catálogo y el kit de WhatsApp se
regeneran juntos.

Las categorías por ocasión y el criterio para asignarlas están en
[`categorias-por-ocasion.md`](arquitectura-agente-tienda/catalogo/categorias-por-ocasion.md).

---

## Estado

**Etapa de maqueta.** No hay precios publicados ni productos cargados en tiendas.

Lo que sigue, en orden, está en [`PENDIENTES.md`](PENDIENTES.md):

1. Congelar precios
2. Abrir WhatsApp Business y cargar el kit
3. Facebook e Instagram
4. Reels y vivos de TikTok

---

## Notas

- Las fotos son de prendas reales del local, tomadas sobre un lienzo verde y recortadas
  automáticamente. No hay imágenes generadas en el catálogo.
- La carpeta `.secrets/` está ignorada: guarda credenciales de la API de generación de imágenes.
- Los modelos y dependencias pesadas también están ignorados; el repositorio pesa unos 34 MB y es
  casi todo imágenes.

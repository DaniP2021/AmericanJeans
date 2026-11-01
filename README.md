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

## Trabajar desde otra PC

El repositorio trae el catálogo, las herramientas, la documentación y el modelo de segmentación
chico (4,5 MB). Lo único que falta se instala solo con un comando.

**1.** Clonar e entrar:

```powershell
git clone https://github.com/USUARIO/american-jeans.git
cd american-jeans
```

**2.** Preparar la máquina:

```powershell
.\setup.ps1
```

Instala OpenCV y ONNX Runtime dentro del proyecto (`.pylibs/`, sin tocar el sistema) y verifica que
todo importe. Si Windows bloquea la ejecución de scripts:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

**3.** Para el modelo de mejor calidad (167 MB), que no puede ir en el repositorio porque supera el
límite de 100 MB por archivo de GitHub:

```powershell
.\setup.ps1 -Completo
```

Sin ese paso la herramienta funciona igual, con el modelo chico: tarda menos y recorta bien las
prendas sobre fondo parejo. El grande conviene cuando el fondo es cargado.

### Qué trae y qué se baja

| | En el repo | Se baja con `setup.ps1` |
|---|---|---|
| Catálogo y fotos | ✓ 33 MB | |
| Herramientas y documentos | ✓ | |
| Modelo chico (`u2netp.onnx`) | ✓ 4,5 MB | |
| Modelo grande (`u2net.onnx`) | | 167 MB, con `-Completo` |
| OpenCV y ONNX Runtime | | 55 MB, siempre |

Las dependencias pesadas no van en git porque se reinstalan solas en un minuto y cambian según la
versión de Python de cada máquina. Así el repositorio queda liviano y el arranque es igual en
cualquier PC.

Alternativa con entorno virtual, si preferís pip:

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

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
- El modelo chico viaja en el repositorio; el grande y las dependencias se bajan con setup.ps1.
  El repositorio pesa unos 38 MB, casi todo imágenes.

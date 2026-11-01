# fotocatalogo — cómo se usa

Herramienta para convertir fotos crudas de prendas en imágenes de catálogo consistentes:
misma proporción, mismo margen, mismo fondo, color sin retocar.

## Comando base

```
python arquitectura-agente-tienda/herramientas/fotocatalogo.py -e <carpeta-crudas> -s <carpeta-salida>
```

Ejemplo real, con las fotos de gabardina:

```
python arquitectura-agente-tienda/herramientas/fotocatalogo.py ^
  -e fotos\crudas -s fotos\catalogo --ratio 4:5 --fondo blanco --ancho 1200 --webp
```

## Las tres configuraciones que vas a usar

| Para qué | Comando |
|---|---|
| Prenda sola, catálogo | `--fondo blanco --ratio 4:5 --grado producto` |
| Primera foto del feed (Meta/Google) | `--fondo blanco --ratio 1:1 --grado producto` |
| Foto con fondo propio (maniquí, local) | `--fondo original --ratio 3:4 --grado editorial` |
| Recorte para diseñador | `--fondo transparente` (exporta PNG con alfa) |

`--grado producto` **no toca el color**: sólo recorta y compone. Es lo correcto para
catálogo, porque el cliente devuelve la prenda si el color no coincide.
`--grado editorial` agrega calidez y grano: sirve para redes, no para fichas.

## Opciones útiles

| Opción | Para qué |
|---|---|
| `--margen 0.05` | menos aire alrededor de la prenda (defecto 0.08) |
| `--rotar 3` | endereza la prenda 3° (positivo = antihorario) |
| `--ancho 1600` | tamaño de la versión maestra (defecto 1600) |
| `--webp` | exporta además WebP, más liviano para la web |
| `--reporte ruta.csv` | dónde dejar el control de lo procesado |

## Cómo disparar para que la herramienta funcione

La herramienta recorta lo que el modelo reconoce como "objeto principal". Eso funciona
muy bien con una prenda sobre fondo parejo y falla con escenas cargadas. Reglas:

1. **Fondo liso y distinto de la prenda.** El azul de tus fotos funciona perfecto.
2. **La prenda entera dentro del cuadro**, sin cortar mangas, ruedos ni cintura.
3. **Cámara perpendicular**, a un metro y medio: evita el efecto de perspectiva.
4. **Luz de costado**, no del techo. Si hay sombra sobre el fondo, el recorte la arrastra.
5. **Una prenda por foto.** Las fotos de conjunto (como la del beige con las plegadas)
   salen bien, pero no sirven como foto principal del SKU.
6. **Sin objetos que toquen la prenda**: perchas, etiquetas, una mano.

## Qué mirar en el reporte

El CSV trae una columna `aviso`. Si dice `REVISAR`, la foto entró con fondo o la prenda
se sale del encuadre: se reprocesa `--fondo original` o se vuelve a disparar.

Las advertencias aparecen también en pantalla, al lado de cada archivo.

## Límites conocidos

- **Selfies frente al espejo**: el modelo toma el marco y la puerta como parte del objeto. No es el uso.
- **Prenda oscura sobre fondo oscuro**: el recorte se come los bordes.
- **Fotos con el piso o una mesa en el cuadro**: si la mesa toca la prenda, entra. Mejor recortar antes.

## Qué produce

Por cada foto, tres tamaños del mismo encuadre: maestra (1600 por defecto), 720 y 360.
Nombres: `<nombre>-<ancho>.jpg`, más `.webp` si se pidió.

Con 40-60 SKUs × 3 fotos, la corrida completa tarda menos de dos minutos.

## Requisitos

Ya están instalados dentro del proyecto, sin tocar el sistema:

- `.pylibs` — OpenCV y ONNX Runtime
- `.models/u2netp.onnx` — modelo de segmentación (4,5 MB)

Si se borran esas carpetas, la herramienta deja de recortar fondo; se reinstalan con el
mismo procedimiento (descargar el wheel y el modelo, descomprimir).

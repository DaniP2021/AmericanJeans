# Paleta a aplicar — instrucciones para el arnés

Documento de aplicación. Si la landing se ve **azulada** en vez de cálida, este archivo explica
qué pasó y qué hay que cambiar. No hace falta interpretar nada: los valores están todos acá y son
los mismos que están funcionando en la máquina de referencia.

---

## 1. El diagnóstico

La landing tiene **dos paletas candidatas**, y la azul existe solo como comparación:

| Archivo | Paleta | Estado |
|---|---|---|
| `landing/styles.css` (bloque `:root`) | **A — Terracota y denim** | **La que va** |
| `landing/theme-a.css` | A, repetida para previsualizar | Inofensiva |
| `landing/theme-b.css` | **B — Cielo y durazno** (`#1E56D6`) | **No debe usarse** |

Si la landing se ve azul, es por una de estas tres:

1. Se enlazó `theme-b.css` en algún HTML.
2. Se sobrescribieron los `--u-*` con los valores de B en otro lugar.
3. Se cacheó el CSS azul en el navegador.

La paleta B usa `--u-accion: #1E56D6`, un azul saturado. La A usa `#B8452C`, terracota. Es la
diferencia que se ve a simple vista.

---

## 2. El bloque exacto que tiene que estar

Estos son los valores de la paleta A. Van en el `:root` de `landing/styles.css` y **no se tocan**.
Si el `:root` de la otra máquina difiere en un solo valor, reemplazá el bloque entero por este.

```css
:root {
  --u-fondo: #FDF6F1;         /* lienzo de la página */
  --u-superficie: #FFFFFF;    /* tarjetas y header */
  --u-texto: #1C1512;         /* negro cálido, no puro */
  --u-texto-suave: #6E625B;
  --u-borde: #EBDCD1;

  --u-accion: #B8452C;        /* botón principal (AA con blanco: 5.36) */
  --u-accion-hover: #9C3822;
  --u-accion-texto: #FFFFFF;

  --u-vivo: #E2703A;          /* acento vivo: subrayados, badges, iconos */
  --u-acento: #F2B37A;

  --u-banda: #1F3A5F;         /* banda oscura: AJ basic y footer */
  --u-banda-texto: #FFFFFF;

  --u-tinte: #FBEFE6;         /* fondo del hero */
  --u-tinte-2: #E9F0F7;       /* fondo de la sección de talles */

  --u-wa: #17784B;            /* WhatsApp: funcional, igual en toda paleta */
  --u-wa-hover: #12603C;

  /* Marca: no se toca */
  --aj-rojo-logo: #B0232B;
  --aj-negro-logo: #0E0E0E;
}
```

---

## 3. Qué rol cumple cada color

Aplicar por rol, no por gusto. Si una parte de la página necesita color y no está en la tabla,
**no se inventa**: se usa el más cercano por función.

| Rol | Token | Valor | Dónde se usa |
|---|---|---|---|
| Lienzo | `--u-fondo` | `#FDF6F1` | Fondo general de la página |
| Superficie | `--u-superficie` | `#FFFFFF` | Header, tarjetas, fichas |
| Texto | `--u-texto` | `#1C1512` | Títulos y cuerpo |
| Texto suave | `--u-texto-suave` | `#6E625B` | Bajadas, notas, legal |
| Líneas | `--u-borde` | `#EBDCD1` | Bordes, separadores |
| **Acción** | `--u-accion` | `#B8452C` | Botones principales, links importantes |
| Acción hover | `--u-accion-hover` | `#9C3822` | Estado hover del botón |
| Acento vivo | `--u-vivo` | `#E2703A` | Subrayados, iconos, badges |
| Acento suave | `--u-acento` | `#F2B37A` | Fondos de badge, detalles |
| Banda | `--u-banda` | `#1F3A5F` | Franja de "AJ basic" y pie |
| Tinte hero | `--u-tinte` | `#FBEFE6` | Fondo del hero |
| Tinte talles | `--u-tinte-2` | `#E9F0F7` | Fondo de la sección de talles |
| WhatsApp | `--u-wa` | `#17784B` | Solo el botón de WhatsApp |

### Los dos únicos azules permitidos

- `--u-banda: #1F3A5F` — franja oscura. Nunca como color de acción ni de texto sobre claro.
- `--u-tinte-2: #E9F0F7` — fondo de una sección. Muy claro, casi imperceptible.

Cualquier otro azul en la página es un error.

---

## 4. Lo que no se hace

1. **No se usa `#B0232B`** como color de acción. Ese es el rojo del logo: es más frío y más
   oscuro, y sobre el lienzo cálido pelea. La acción es `#B8452C`.
2. **No se aclaran colores para "que se vea más suave".** Los valores ya están verificados para
   contraste; aclarar rompe la accesibilidad.
3. **No se agregan colores nuevos.** Si falta un rol, se consulta antes de inventarlo.
4. **No se mezclan paletas.** A y B no se combinan: la página es A entera.
5. **No se usa el azul de sistema** para links (`#0000EE` o el que ponga el navegador). Todo link
   lleva `--u-accion` o `--u-texto` con subrayado.

---

## 5. Contraste: los valores ya están medidos

No hay que "mejorar" estos números, están calculados contra WCAG AA (mínimo 4.5:1 en texto normal).

| Combinación | Ratio | Estado |
|---|---|---|
| `--u-texto` sobre `--u-fondo` | 15.8 | ✓ |
| `--u-texto-suave` sobre `--u-fondo` | 5.9 | ✓ |
| Blanco sobre `--u-accion` | 5.36 | ✓ |
| Blanco sobre `--u-banda` | 11.4 | ✓ |
| Blanco sobre `--u-wa` | 5.52 | ✓ |
| `--u-texto` sobre `--u-acento` | 8.9 | ✓ |

Si algún par queda por debajo de 4.5, el error está en qué token se usó, no en el valor del token.

---

## 6. Procedimiento para el otro arnés

Cinco pasos, en orden. No saltear el 4.

**1.** Traer la última versión del repositorio:

```
git pull
```

**2.** Verificar que ningún HTML enlace la paleta azul:

```
grep -rn "theme-b" arquitectura-agente-tienda/landing/
```

Tiene que devolver **solo** `preview-b.html`, que es la maqueta de comparación. Si aparece
`index.html` o `talles.html`, se quita esa línea del `<head>`.

**3.** Comparar el `:root` de `landing/styles.css` con el bloque de la sección 2 de este documento.
Si difiere, reemplazarlo completo. No editar valores sueltos.

**4.** Buscar colores escritos a mano fuera del `:root`, que es donde se cuelan las variantes:

```
grep -n "#[0-9A-Fa-f]\{6\}" arquitectura-agente-tienda/landing/styles.css
```

Deberían aparecer solo los del bloque `:root` y un `#FFFFFF`. Cualquier otro hex fuera de ahí es
una corrección que se hizo a mano y hay que devolver a un token.

**5.** Correr el verificador:

```
python arquitectura-agente-tienda/qa/verify_landing.py
```

Tiene que terminar con **"Sin problemas bloqueantes"**. Ese script revisa estructura, metadatos y
contraste. Si falla, el mensaje dice qué par de colores está mal.

---

## 7. Si después de esto sigue azul

En orden de probabilidad:

1. **Caché del navegador.** `Ctrl + F5` en la landing. Es lo más común: el CSS viejo queda guardado.
2. **Otro archivo CSS.** Buscar todos los `.css` que carga la página y confirmar que sean
   `styles.css` (y `tokens.css` si la página lo usa).
3. **Estilos en línea.** Revisar si el HTML trae `style="..."` con colores; hay que pasarlos a tokens.
4. **Otra copia del proyecto.** Confirmar que se está abriendo el archivo correcto y no una versión
   anterior en otra carpeta.

---

## 8. Referencia rápida

| Archivo | Para qué |
|---|---|
| `landing/styles.css` | La paleta A aplicada. **Fuente de verdad.** |
| `landing/theme-a.css` | La misma paleta, para previsualizar |
| `landing/theme-b.css` | Paleta B — azul. Solo comparación. No enlazar |
| `landing/preview-a.html` | Maqueta de A |
| `landing/preview-b.html` | Maqueta de B (la que NO va) |
| `qa/verify_landing.py` | Verificador de contraste y estructura |
| `06-Paletas.md` | Las dos paletas explicadas y por qué se eligió A |

---

## 9. Coherencia con el catálogo

El catálogo de fotos usa los mismos valores, así que la página y las fichas no se pelean:

- Fondo lino: `#FDF6F1` → `#F5E9DE` → `#E8D8C9`
- Terracota de acción: `#B8452C`
- Crema: `#FDF6F1`

Esos colores están en `herramientas/fondos.py`. Si se cambia la paleta de la landing, ese archivo
también hay que tocarlo, o el catálogo queda desalineado.

# Pendientes y estado — American Jeans

Última actualización: 30/10/2026

---

## Catálogo: dónde quedó

**18 productos · 33 fotos · 5 categorías por ocasión.**

| Categoría | Productos |
|---|---|
| Oficina | Sweter cuello V · Sweter medio cierre · Gabardina recto expansible · Camisa estampada |
| Vestir | Pantalón de vestir · Camisa de vestir · Corbata · Chaleco de vestir |
| Informal | Jean clásico · Gabardina corte jean slim · Chomba rayada · Bermuda corte jean |
| Fin de semana | Cargo de microfibra · Conjunto deportivo microfibra |
| Looks | Camisas con pantalón · Camisa con corbata · Pantalón + chombas (×2) |

**Abrir:** [CATALOGO/catalogo.html](CATALOGO/catalogo.html) — tiene filtro por ocasión y por fondo
(lino / blanco).

**Categorías vacías:** Formal y Sport. No se muestran hasta que tengan productos.

---

## Cómo se retoma

El flujo completo, en orden:

```
python arquitectura-agente-tienda/herramientas/fotocatalogo.py -e <crudas> -s <salida> --fondo blanco --ancho 1200 --modelo grande --piezas 0.08
python arquitectura-agente-tienda/qa/exportar_transparentes.py
python arquitectura-agente-tienda/herramientas/generar_catalogo.py
python arquitectura-agente-tienda/qa/kit_whatsapp.py
```

1. Procesar las fotos nuevas.
2. Exportar las prendas con transparencia (WebP).
3. Regenerar el catálogo (lee la tabla de productos del script).
4. Regenerar el kit de WhatsApp.

Los productos se agregan a mano en `generar_catalogo.py` (lista `PRODUCTOS`) y en
`qa/kit_whatsapp.py` (lista `FICHAS`). Cada entrada lleva: nombre de archivo, ocasión, tipo,
título, color y fotos adicionales.

---

## Mañana: precios y redes

### Precios

- [ ] **Congelar precios.** Es el bloqueante de todo lo demás: sin precio no hay ficha publicada,
      ni catálogo de WhatsApp, ni campaña.
- [ ] Definir si se publican cuotas o solo precio de lista.
- [ ] Cargar la tabla de precios: hoy está [precios-referencia.csv](arquitectura-agente-tienda/catalogo/precios-referencia.csv),
      sin valores definitivos.
- [ ] Revisar la política de precios: [politica-de-precios.md](arquitectura-agente-tienda/catalogo/politica-de-precios.md).

### WhatsApp

- [ ] Abrir WhatsApp Business y decidir el camino: app (carga manual) o Commerce Manager (feed).
- [ ] Cargar las 18 fichas desde [CATALOGO/whatsapp/](CATALOGO/whatsapp) — imágenes cuadradas de
      1080 px, CSV y textos listos.
- [ ] Definir los mensajes automáticos: bienvenida, fuera de horario, catálogo.
- [ ] Las macros de atención están en [whatsapp-macros.md](arquitectura-agente-tienda/operacion/whatsapp-macros.md).

### Facebook e Instagram

- [ ] Crear o vincular las cuentas con el mismo nombre de usuario.
- [ ] Completar la ficha: foto de perfil (sello), biografía, horarios, dirección, WhatsApp.
- [ ] Subir las fotos del catálogo como publicaciones iniciales.
- [ ] Usar la grilla de contenidos: [05-Grilla-Contenidos-Lanzamiento.md](arquitectura-agente-tienda/05-Grilla-Contenidos-Lanzamiento.md).

---

## Semana próxima: reels y vivos de TikTok

- [ ] Definir los tres primeros reels (guiones base en la grilla de contenidos).
- [ ] Preparar el guion del vivo: qué se muestra, qué se responde, qué se ofrece.
- [ ] Probar la luz y el audio del lugar donde se va a transmitir.
- [ ] Definir frecuencia: cuántos reels por semana y qué día el vivo.

---

## Deuda técnica del catálogo

Cosas que quedaron anotadas y no bloquean, pero conviene resolver:

- **Fin de semana tiene 2.** Faltan remera y buzo, que son las de más rotación en esa categoría.
- **Fotos de etiqueta en primer plano.** Camisa, jean, chomba: tres tomas chicas que van como
  segunda o tercera foto y responden la objeción de marca antes de que la hagan.
- **La etiqueta de las bermudas dice "Classic Wear"** y la de la gabardina recto dice "ROMER
  JEANS". Falta definir si son segundas líneas o reventa, porque cambia lo que se puede afirmar
  en la ficha.
- **El jean no tiene foto de cuerpo entero**, como sí tiene la gabardina. Falta para publicar.
- **Sweter gris**: la foto no sirvió para recortar. Necesita una toma nueva, plano y estirado.
- **Precio de referencia en la grilla**: hoy el botón dice "Consultar". Cuando haya precio, cambia.

---

## Documentos que importan

| Qué | Dónde |
|---|---|
| El catálogo | [CATALOGO/catalogo.html](CATALOGO/catalogo.html) |
| Mapa de todo | [INDICE.md](INDICE.md) |
| Criterio de categorías | [categorias-por-ocasion.md](arquitectura-agente-tienda/catalogo/categorias-por-ocasion.md) |
| Esquema de producto | [esquema-producto.md](arquitectura-agente-tienda/catalogo/esquema-producto.md) |
| Herramientas de foto | [herramientas/LEEME.md](arquitectura-agente-tienda/herramientas/LEEME.md) |
| La landing | [landing/index.html](arquitectura-agente-tienda/landing/index.html) |

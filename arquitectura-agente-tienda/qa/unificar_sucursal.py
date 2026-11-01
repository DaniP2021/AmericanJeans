"""Unifica el sitio en una sola sucursal (Av. Rivadavia 2713), que también es depósito.

El plan original comunicaba cuatro locales. Hasta que las otras direcciones se publiquen,
todo el sitio habla de una: prometer una red y mostrar una sola dirección abre una pregunta
que nadie va a responder.
"""

import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "landing"))

CAMBIOS = {
    "index.html": [
        # promesas
        ("<h2 class=\"promesa__t\">Retiro en 2 horas</h2>\n        <p class=\"promesa__d\">Con cita confirmada, de lunes a sábado de 9 a 19. Si comprás después de las 19, se prepara al abrir.</p>",
         "<h2 class=\"promesa__t\">Retiro en 2 horas</h2>\n        <p class=\"promesa__d\">En Av. Rivadavia 2713, con cita confirmada, de lunes a sábado de 9 a 19. Si comprás después de las 19, se prepara al abrir.</p>"),

        ("<h2 class=\"promesa__t\">Cambios gratis en 4 sucursales</h2>\n        <p class=\"promesa__d\">No importa dónde compraste: lo cambiás en la sucursal que te quede cerca, con cita previa.</p>",
         "<h2 class=\"promesa__t\">Cambios gratis en el local</h2>\n        <p class=\"promesa__d\">Lo compraste online o en el mostrador: lo cambiás en Rivadavia 2713, con cita previa, de 9 a 19.</p>"),

        ("<p class=\"promesa__d\">Stock unificado: lo que mostramos online sale del mismo depósito que abastece a los locales.</p>",
         "<p class=\"promesa__d\">Vendemos desde el mismo depósito del local: si el talle aparece disponible, está en la góndola.</p>"),

        # talles
        ("Si te queda justo o te sobra, el cambio es gratis en cualquiera de las 4 sucursales.",
         "Si te queda justo o te sobra, el cambio es gratis en la sucursal de Rivadavia 2713."),

        # faq
        ("Si estás entre dos, elegí el mayor. Si te equivocás, el cambio es gratis en cualquiera de las 4 sucursales.",
         "Si estás entre dos, elegí el mayor. Si te equivocás, el cambio es gratis en Rivadavia 2713."),

        ("<p>Sí, en cualquiera de las 4 sucursales, con la prenda sin uso y con etiqueta. Coordinamos por WhatsApp con cita previa, de lunes a sábado de 9 a 19.</p>",
         "<p>Sí, en Av. Rivadavia 2713, con la prenda sin uso y con etiqueta. Coordinamos por WhatsApp con cita previa, de lunes a sábado de 9 a 19.</p>"),

        ("<p>Sí. Preparás el pedido y lo retirás en 2 horas, con cita confirmada, de lunes a sábado de 9 a 19. Las compras que entran después de las 19 se preparan al abrir el siguiente día hábil.</p>",
         "<p>Sí. Preparás el pedido y lo retirás en 2 horas en Av. Rivadavia 2713, con cita confirmada, de lunes a sábado de 9 a 19. Las compras que entran después de las 19 se preparan al abrir el siguiente día hábil.</p>"),

        # footer
        ("<p class=\"footer__d\">Indumentaria masculina. Cuatro sucursales en Buenos Aires.</p>",
         "<p class=\"footer__d\">Indumentaria masculina. Sucursal y depósito en Av. Rivadavia 2713, CABA.</p>"),

        ("""      <h2 class="footer__t">Sucursales</h2>
      <ul class="footer__lista">
        <!-- COMPLETAR con dirección y teléfono de cada local -->
        <li>Sucursal 1 — dirección a confirmar</li>
        <li>Sucursal 2 — dirección a confirmar</li>
        <li>Sucursal 3 — dirección a confirmar</li>
        <li>Sucursal 4 — dirección a confirmar</li>
      </ul>
      <p class="footer__d">Atención: lunes a sábado, de 9 a 19.</p>""",
         """      <h2 class="footer__t">Sucursal</h2>
      <ul class="footer__lista">
        <li>Av. Rivadavia 2713, CABA</li>
        <li><a href="https://www.google.com/maps/search/?api=1&amp;query=Av.+Rivadavia+2713,+CABA" rel="noopener" target="_blank">Ver en el mapa</a></li>
        <li>Lunes a sábado, de 9 a 19</li>
        <li>Retiro y cambios con cita previa</li>
      </ul>
      <p class="footer__d">En el mismo local funciona el depósito: los pedidos online se preparan ahí.</p>"""),
    ],

    "talles.html": [
        ("El cambio es gratis en cualquiera de las 4 sucursales.", "El cambio es gratis en la sucursal de Rivadavia 2713."),
        ("Lo cambiás en la sucursal que te quede cerca, con cita previa, de lunes a sábado de 9 a 19.",
         "Lo cambiás en Av. Rivadavia 2713, con cita previa, de lunes a sábado de 9 a 19."),
        ("Sí. Con cita previa para asegurarte el talle, de lunes a sábado de 9 a 19.",
         "Sí. En Av. Rivadavia 2713, con cita previa, de lunes a sábado de 9 a 19."),
    ],

    os.path.join("legal", "cambios.html"): [
        ("Cómo cambiar una prenda en cualquiera de las 4 sucursales, plazos, condiciones y cómo pedir una devolución.",
         "Cómo cambiar una prenda en la sucursal de Av. Rivadavia 2713, plazos, condiciones y cómo pedir una devolución."),
        ("<strong>La regla corta:</strong> cambio gratis en cualquiera de las 4 sucursales, con la prenda sin uso",
         "<strong>La regla corta:</strong> cambio gratis en Av. Rivadavia 2713, con la prenda sin uso"),
        ("<td>En cualquier sucursal, con ticket o número de pedido</td>", "<td>En Av. Rivadavia 2713, con ticket o número de pedido</td>"),
        ("<td>En cualquier sucursal, con el número de pedido</td>", "<td>En Av. Rivadavia 2713, con el número de pedido</td>"),
        ("<td>Sin cargo en sucursal; con envío, costo del flete a cargo del comprador</td>",
         "<td>Sin cargo en el local; con envío, costo del flete a cargo del comprador</td>"),
        ("Puede pedir el cambio en cualquier sucursal", "Puede pedir el cambio en Av. Rivadavia 2713"),
    ],

    os.path.join("legal", "terminos.html"): [
        ("en cuatro sucursales y por canales digitales.", "en su sucursal de Av. Rivadavia 2713 (CABA) y por canales digitales."),
        ("y cambios gratis en cualquiera de las cuatro sucursales.", "y cambios gratis en la sucursal de Av. Rivadavia 2713."),
        ("<li><strong>Retiro en sucursal:</strong> con cita confirmada, en un plazo de 2 horas",
         "<li><strong>Retiro en sucursal:</strong> en Av. Rivadavia 2713, con cita confirmada, en un plazo de 2 horas"),
    ],

    os.path.join("legal", "arrepentimiento.html"): [
        ("<li>En cualquier sucursal, con el ticket.</li>", "<li>En Av. Rivadavia 2713, con el ticket.</li>"),
        ("Coordinamos el retiro o la entrega en sucursal, sin costo para vos.",
         "Coordinamos el retiro o la entrega en Av. Rivadavia 2713, sin costo para vos."),
    ],
}

for pagina, reemplazos in CAMBIOS.items():
    ruta = os.path.join(BASE, pagina)
    with open(ruta, encoding="utf-8") as f:
        html = f.read()

    aplicados = 0
    for viejo, nuevo in reemplazos:
        if viejo in html:
            html = html.replace(viejo, nuevo)
            aplicados += 1
        else:
            print(f"  · no encontrado en {pagina}: {viejo[:60]}…")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{pagina:40} {aplicados}/{len(reemplazos)} reemplazos")

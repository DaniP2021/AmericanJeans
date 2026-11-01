"""Alinea los materiales de cara al cliente con la decisión de publicar una sola sucursal.

No toca los documentos que describen el negocio (el plan, el benchmark, la política de precios):
ahí "4 locales" es un hecho, no una promesa. Solo cambia lo que se le dice al cliente.
"""

import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

CAMBIOS = {
    "04-Identidad-American-Jeans.md": [
        ('- Cambios: **"Cambio gratis en cualquiera de las 4 sucursales, con cita previa, de lunes a sábado de 9 a 19."**',
         '- Cambios: **"Cambio gratis en Av. Rivadavia 2713, con cita previa, de lunes a sábado de 9 a 19."**\n'
         '  *(Hasta que se publiquen las otras direcciones, no se menciona la red: prometer cuatro locales y mostrar uno abre una pregunta que nadie responde.)*'),
    ],
    "05-Grilla-Contenidos-Lanzamiento.md": [
        ('asunto "Abrimos la sucursal virtual: 4 locales, una línea nueva"',
         'asunto "Abrimos la sucursal virtual: una línea nueva"'),
        ('> Texto en pantalla: "Por eso tenemos 4 locales."', '> Texto en pantalla: "Por eso tenemos local propio."'),
    ],
    os.path.join("operacion", "whatsapp-macros.md"): [
        ("> Tenemos 4 sucursales en Buenos Aires: podés retirar en 2 horas con cita o te lo enviamos.",
         "> Estamos en Av. Rivadavia 2713 (CABA), con retiro en 2 horas con cita o envío a todo el país."),
        ("el cambio es gratis en cualquiera de las 4 sucursales.",
         "el cambio es gratis en el local de Rivadavia 2713."),
        ("> Sí, el cambio es gratis en cualquiera de las 4 sucursales. Necesitás:",
         "> Sí, el cambio es gratis en Av. Rivadavia 2713. Necesitás:"),
        ("· Decime qué sucursal te queda mejor y coordinamos día y hora. Si el talle que querés no está en esa sucursal, lo pedimos al local que lo tenga.",
         "· Coordinamos día y hora por WhatsApp, de lunes a sábado de 9 a 19. Si el talle que querés no está, te aviso cuando entra."),
    ],
    os.path.join("contenido", "blog", "01-como-saber-tu-talle.md"): [
        ("el cambio es gratis en cualquiera de nuestras 4 sucursales.",
         "el cambio es gratis en nuestra sucursal de Av. Rivadavia 2713."),
    ],
    os.path.join("contenido", "blog", "02-que-ponerse-para-trabajar.md"): [
        ("el cambio es gratis en cualquiera de las 4 sucursales.",
         "el cambio es gratis en nuestra sucursal de Av. Rivadavia 2713."),
    ],
    os.path.join("qa", "checklist-lanzamiento.md"): [
        ("| 3 | Direcciones de las 4 sucursales cargadas | 🔴 | Dueño |",
         "| 3 | Dirección publicada: Av. Rivadavia 2713, CABA, y número de WhatsApp real | ✅ | Dueño |"),
        ("| 37 | Proceso de cambios explicado al personal de las 4 sucursales | 🟡 | Dueño |",
         "| 37 | Proceso de cambios explicado al personal del local | 🟡 | Dueño |"),
    ],
}

for archivo, reemplazos in CAMBIOS.items():
    ruta = os.path.join(BASE, archivo)
    with open(ruta, encoding="utf-8") as f:
        txt = f.read()
    ok = 0
    for viejo, nuevo in reemplazos:
        if viejo in txt:
            txt = txt.replace(viejo, nuevo)
            ok += 1
        else:
            print(f"  · no encontrado en {archivo}: {viejo[:55]}…")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"{archivo:52} {ok}/{len(reemplazos)}")

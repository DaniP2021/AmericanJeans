"""Genera la planilla de guía de talles de American Jeans.

La equivalencia de talles (letra · número · talle de pantalón) ya es definitiva y va cargada.
Las medidas en centímetros quedan como celdas a completar con la moldería.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

NEGRO = "0E0E0E"
ROJO = "B0232B"
GRIS_INPUT = "F2F1EF"
GRIS_TXT = "5A5A5A"
GRIS_SUAVE = "F7F6F4"

# talle, número, equivalencia (pantalón)
TALLES = [
    ("S", 1, 38),
    ("M", 2, 40),
    ("L", 3, 42),
    ("XL", 4, 44),
    ("XXL", 5, 46),
    ("XXXL", 6, 48),
]

thin = Side(style="thin", color="D9D6D1")
borde = Border(left=thin, right=thin, top=thin, bottom=thin)


def titulo(ws, fila, texto, ancho, color=NEGRO, alto=26):
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=ancho)
    c = ws.cell(row=fila, column=1, value=texto)
    c.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=color)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[fila].height = alto
    return fila + 1


def encabezado(ws, fila, valores, alto=32):
    for i, v in enumerate(valores, start=1):
        c = ws.cell(row=fila, column=i, value=v)
        c.font = Font(name="Calibri", size=10, bold=True, color=NEGRO)
        c.fill = PatternFill("solid", fgColor="E9E6E2")
        c.border = borde
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[fila].height = alto
    return fila + 1


def celda_input(ws, fila, col, decimales="0.0"):
    c = ws.cell(row=fila, column=col)
    c.fill = PatternFill("solid", fgColor=GRIS_INPUT)
    c.border = borde
    c.number_format = decimales
    c.alignment = Alignment(horizontal="center")


def celda_fija(ws, fila, col, valor, bold=False, fondo=None):
    c = ws.cell(row=fila, column=col, value=valor)
    c.font = Font(name="Calibri", size=10, bold=bold)
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = borde
    if fondo:
        c.fill = PatternFill("solid", fgColor=fondo)
    return c


wb = Workbook()

# ============================================================ Hoja 1
ws = wb.active
ws.title = "Guía de talles"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 11
ws.column_dimensions["B"].width = 7
ws.column_dimensions["C"].width = 11
for col in "DEFGH":
    ws.column_dimensions[col].width = 13
ws.column_dimensions["I"].width = 26

fila = titulo(ws, 1, "AMERICAN JEANS · GUÍA DE TALLES", 9)

ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=9)
c = ws.cell(row=2, column=1, value=(
    "La equivalencia de talles ya está completa y no se toca. "
    "Completá sólo las celdas grises con las medidas en centímetros, midiendo 3 prendas por talle "
    "y cargando el promedio. Tolerancia aceptada: ±2 cm."
))
c.font = Font(name="Calibri", size=9, italic=True, color=GRIS_TXT)
c.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
ws.row_dimensions[2].height = 34

# --- 1. Equivalencia (definitiva)
fila = 4
fila = titulo(ws, fila, "1 · EQUIVALENCIA DE TALLES  ·  completa, no modificar", 9, color=ROJO)
fila = encabezado(ws, fila, ["Talle", "N.º", "Equivale a", "Qué significa", "", "", "", "", ""])
for talle, numero, equiv in TALLES:
    celda_fija(ws, fila, 1, talle, bold=True, fondo=GRIS_SUAVE)
    celda_fija(ws, fila, 2, numero, fondo=GRIS_SUAVE)
    celda_fija(ws, fila, 3, equiv, bold=True, fondo=GRIS_SUAVE)
    ws.merge_cells(start_row=fila, start_column=4, end_row=fila, end_column=9)
    c = ws.cell(row=fila, column=4, value=f"Talle {numero} · equivale al {equiv} de pantalón")
    c.font = Font(name="Calibri", size=10, color=GRIS_TXT)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    c.fill = PatternFill("solid", fgColor=GRIS_SUAVE)
    fila += 1

# --- 2. Medidas del cuerpo
fila += 1
fila = titulo(ws, fila, "2 · MEDIDAS DEL CUERPO (cm)  ·  completar", 9)
fila = encabezado(ws, fila, ["Talle", "N.º", "Equivale a", "Pecho", "Cintura", "Cadera",
                             "Largo de torso", "Manga", "Progresión"])
inicio_cuerpo = fila
for i, (talle, numero, equiv) in enumerate(TALLES):
    celda_fija(ws, fila, 1, talle, bold=True)
    celda_fija(ws, fila, 2, numero)
    celda_fija(ws, fila, 3, equiv)
    for col in range(4, 9):
        celda_input(ws, fila, col)
    if i == 0:
        formula = f'=IF(D{fila}="","","—")'
    else:
        formula = (f'=IF(OR(D{fila}="",D{fila-1}=""),"",'
                   f'IF(D{fila}<=D{fila-1},"⚠ revisar","OK"))')
    c = ws.cell(row=fila, column=9, value=formula)
    c.alignment = Alignment(horizontal="center")
    c.border = borde
    c.font = Font(size=9, color=GRIS_TXT)
    fila += 1

# --- 3. Medida de la prenda
fila += 1
fila = titulo(ws, fila, "3 · MEDIDA DE LA PRENDA (cm)  ·  apoyada en la mesa, sin estirar  ·  completar", 9)
fila = encabezado(ws, fila, ["Talle", "N.º", "Equivale a", "Ancho de pecho", "Ancho de cintura",
                             "Largo total", "Largo de manga", "Sisa", "Observación"])
for talle, numero, equiv in TALLES:
    celda_fija(ws, fila, 1, talle, bold=True)
    celda_fija(ws, fila, 2, numero)
    celda_fija(ws, fila, 3, equiv)
    for col in range(4, 9):
        celda_input(ws, fila, col)
    c = ws.cell(row=fila, column=9)
    c.fill = PatternFill("solid", fgColor=GRIS_INPUT)
    c.border = borde
    c.alignment = Alignment(wrap_text=True, vertical="center")
    fila += 1

fila += 1
ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=9)
c = ws.cell(row=fila, column=1, value=(
    "REGLA: si el cliente está entre dos talles, se recomienda el mayor. "
    "Ningún competidor del polo de Avellaneda publica medidas en cm: es el diferencial más barato de construir."
))
c.font = Font(name="Calibri", size=9, italic=True, color=ROJO)
c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
ws.row_dimensions[fila].height = 40

ws.freeze_panes = f"A{inicio_cuerpo}"

# ============================================================ Hoja 2
ws2 = wb.create_sheet("Cómo medir")
ws2.sheet_view.showGridLines = False
ws2.column_dimensions["A"].width = 4
ws2.column_dimensions["B"].width = 26
ws2.column_dimensions["C"].width = 78

fila = titulo(ws2, 1, "CÓMO MEDIR · texto para la ficha de producto y para el local", 3)
filas = [
    ("Pecho", "Cinta alrededor del torso, a la altura de los pezones, con los brazos sueltos. "
              "Pasa por la parte más ancha del pecho y por debajo de las axilas."),
    ("Cintura", "Cinta alrededor de la cintura natural, la parte más angosta. No apretar: "
                "tiene que pasar un dedo."),
    ("Cadera", "Cinta alrededor de la parte más ancha de la cadera, con los pies juntos."),
    ("Largo de torso", "Desde el hueso del hombro (junto al cuello) hasta el ruedo, por delante."),
    ("Manga", "Desde el centro de la espalda, pasando por el hombro, hasta el final del puño, "
              "con el brazo apenas flexionado."),
    ("Prenda apoyada", "Prenda cerrada sobre la mesa, sin estirar. Ancho de pecho = de sisa a sisa. "
                       "Largo total = desde el hombro hasta el ruedo."),
]
fila = 2
for nombre, detalle in filas:
    ws2.cell(row=fila, column=2, value=nombre).font = Font(bold=True, size=10)
    ws2.cell(row=fila, column=2).alignment = Alignment(vertical="top")
    c = ws2.cell(row=fila, column=3, value=detalle)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=10)
    ws2.row_dimensions[fila].height = 42
    fila += 1

fila += 1
fila = titulo(ws2, fila, "CÓMO SE MIDE EN EL LOCAL (equipo de atención)", 3)
pasos = [
    "Medir sobre ropa interior fina o remera liviana, nunca sobre campera.",
    "La cinta va horizontal, paralela al piso: el error más común es medir en diagonal.",
    "Anotar en cm enteros, sin redondear a favor del cliente.",
    "Si el cliente está entre dos talles: recomendar el mayor y avisar que el cambio es gratis en el local.",
    "Registrar qué talle se llevó y si después lo cambió: ese dato alimenta la tabla.",
]
for p in pasos:
    ws2.cell(row=fila, column=2, value="•").alignment = Alignment(horizontal="center", vertical="top")
    c = ws2.cell(row=fila, column=3, value=p)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=10)
    ws2.row_dimensions[fila].height = 32
    fila += 1

# ============================================================ Hoja 3
ws3 = wb.create_sheet("Uso en la ficha")
ws3.sheet_view.showGridLines = False
ws3.column_dimensions["A"].width = 4
ws3.column_dimensions["B"].width = 30
ws3.column_dimensions["C"].width = 82

fila = titulo(ws3, 1, "CÓMO SE USA ESTA TABLA EN LA WEB, EL LOCAL Y WHATSAPP", 3)
bloques = [
    ("Bloque de la ficha", "«¿Qué talle sos?» (no «Guía de talles»: la pregunta convierte mejor)."),
    ("Equivalencia siempre visible", "«S / 1 / 38». El cliente que usa 42 de pantalón entiende su talle en un segundo."),
    ("Frase de entrada", "«Medí con una cinta y compará con la tabla. Si estás entre dos, elegí el mayor: "
                         "el cambio es gratis en Av. Rivadavia 2713.»"),
    ("Mientras faltan las medidas", "«Las medidas en centímetros están en proceso. Escribinos con tu altura y "
                                    "tu contorno de pecho y te decimos el talle.»"),
    ("Respuesta tipo WhatsApp", "«Hola [nombre], ¿me pasás tu altura y el contorno de pecho? También me sirve "
                                "qué talle usás en jean. Estamos de lunes a sábado de 9 a 19.»"),
    ("Error a evitar", "Publicar la tabla sólo como imagen: no se copia, no se indexa y no la lee un lector de pantalla."),
    ("Cuándo se actualiza", "Cada vez que cambia un proveedor o una moldería. Versión y fecha visibles al pie."),
]
for titulo_fila, texto in bloques:
    ws3.cell(row=fila, column=2, value=titulo_fila).font = Font(bold=True, size=10)
    ws3.cell(row=fila, column=2).alignment = Alignment(vertical="top", wrap_text=True)
    c = ws3.cell(row=fila, column=3, value=texto)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=10)
    ws3.row_dimensions[fila].height = 46
    fila += 1

wb.save("Guia-Talles-American-Jeans.xlsx")
print("OK")

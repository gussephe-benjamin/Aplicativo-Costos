import pandas as pd
from openpyxl import load_workbook
from config import Config
from datetime import datetime

# Archivo de Excel
EXCEL_FILE = Config.EXCEL_FILE

# Crear DataFrame de prueba para cada tabla
productos_data = [
    {"id": 1, "nombre": "Leche", "descripcion": "Leche entera 1L", "precio_unitario": 2.50, "stock": 100, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 2, "nombre": "Pan", "descripcion": "Pan integral", "precio_unitario": 1.00, "stock": 50, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 3, "nombre": "Huevos", "descripcion": "Docena de huevos", "precio_unitario": 3.00, "stock": 30, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 4, "nombre": "Queso", "descripcion": "Queso fresco 500g", "precio_unitario": 4.00, "stock": 20, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 5, "nombre": "Mantequilla", "descripcion": "Mantequilla sin sal 200g", "precio_unitario": 2.80, "stock": 40, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
]
productos_df = pd.DataFrame(productos_data)

mano_obra_data = [
    {"id": 1, "nombre_empleado": "Juan", "costo_por_hora": 10, "producto_id": 1, "horas_requeridas": 2, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 2, "nombre_empleado": "Ana", "costo_por_hora": 12, "producto_id": 1, "horas_requeridas": 1, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 3, "nombre_empleado": "Luis", "costo_por_hora": 15, "producto_id": 2, "horas_requeridas": 1.5, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 4, "nombre_empleado": "Sofía", "costo_por_hora": 8, "producto_id": 3, "horas_requeridas": 1, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 5, "nombre_empleado": "Carlos", "costo_por_hora": 9, "producto_id": 4, "horas_requeridas": 1.5, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 6, "nombre_empleado": "Miguel", "costo_por_hora": 11, "producto_id": 5, "horas_requeridas": 2, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
]
mano_obra_df = pd.DataFrame(mano_obra_data)

materia_prima_data = [
    {"id": 1, "nombre": "Leche cruda", "cantidad_disponible": 100, "precio_por_unidad": 1.20, "producto_id": 1, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},	
    {"id": 2, "nombre": "Envase de cartón", "cantidad_disponible": 50, "precio_por_unidad": 0.30, "producto_id": 1, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 3, "nombre": "Harina integral", "cantidad_disponible": 50, "precio_por_unidad": 0.50, "producto_id": 2, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 4, "nombre": "Levadura", "cantidad_disponible": 20, "precio_por_unidad": 0.20, "producto_id": 2, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 5, "nombre": "Huevos frescos", "cantidad_disponible": 60, "precio_por_unidad": 2.00, "producto_id": 3, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 6, "nombre": "Sal", "cantidad_disponible": 30, "precio_por_unidad": 0.05, "producto_id": 3, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 7, "nombre": "Leche fresca", "cantidad_disponible": 20, "precio_por_unidad": 1.50, "producto_id": 4, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 8, "nombre": "Cultura bacteriana", "cantidad_disponible": 10, "precio_por_unidad": 2.00, "producto_id": 4, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 9, "nombre": "Crema de leche", "cantidad_disponible": 40, "precio_por_unidad": 1.80, "producto_id": 5, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"id": 10, "nombre": "Sal refinada", "cantidad_disponible": 15, "precio_por_unidad": 0.10, "producto_id": 5, "fecha_agregado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
]
materia_prima_df = pd.DataFrame(materia_prima_data)

costos_indirectos_data = [
    {"id": 1, "tipo": "Electricidad", "monto": 150, "descripcion": "Costo mensual de electricidad"},
    {"id": 2, "tipo": "Alquiler", "monto": 300, "descripcion": "Alquiler mensual del local"},
    {"id": 3, "tipo": "Maquinaria", "monto": 200, "descripcion": "Costo por uso de maquinaria"},
    {"id": 4, "tipo": "Agua", "monto": 50, "descripcion": "Costo de agua mensual"}
]
costos_indirectos_df = pd.DataFrame(costos_indirectos_data)

# Leer las hojas existentes para preservar datos
try:
    with pd.ExcelFile(EXCEL_FILE) as reader:
        existing_sheets = {sheet: pd.read_excel(EXCEL_FILE, sheet_name=sheet) for sheet in reader.sheet_names}
except FileNotFoundError:
    existing_sheets = {}

# Actualizar las hojas existentes o añadir nuevas
with pd.ExcelWriter(EXCEL_FILE, mode='w', engine='openpyxl') as writer:
    for sheet_name, sheet_df in existing_sheets.items():
        sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
    productos_df.to_excel(writer, sheet_name="productos", index=False)
    mano_obra_df.to_excel(writer, sheet_name="mano_obra", index=False)
    materia_prima_df.to_excel(writer, sheet_name="materia_prima", index=False)
    costos_indirectos_df.to_excel(writer, sheet_name="costos_indirectos", index=False)

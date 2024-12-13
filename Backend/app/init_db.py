import os
import pandas as pd

EXCEL_FILE = 'data/data.xlsx'

def inicializar_datos():
    # Verificamos si el archivo existe
    if not os.path.exists(EXCEL_FILE):
        print(f"El archivo {EXCEL_FILE} no existe. Creando nuevo archivo...")
        
        # Crear un DataFrame vacío para cada hoja necesaria
        hojas = {
            'usuarios': pd.DataFrame(columns=['id', 'nombre', 'email', 'contraseña', 'rol', 'fecha_registro']),
            'productos': pd.DataFrame(columns=['id', 'nombre', 'descripcion', 'precio_unitario', 'stock', 'fecha_agregado']),
            'materia_prima': pd.DataFrame(columns=['id', 'nombre', 'descripcion', 'stock', 'fecha_agregado']),
            'mano_obra': pd.DataFrame(columns=['id', 'nombre', 'descripcion', 'precio', 'stock', 'fecha_agregado']),
            'costos_indirectos': pd.DataFrame(columns=['id', 'nombre', 'descripcion', 'monto', 'fecha_agregado']),
            'ordenes_pedido': pd.DataFrame(columns=['id', 'id_usuario', 'productos', 'fecha_pedido', 'estado']),
        }
        
        # Crear el archivo Excel con las hojas necesarias
        with pd.ExcelWriter(EXCEL_FILE) as writer:
            for sheet_name, df in hojas.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"Archivo {EXCEL_FILE} creado exitosamente con las hojas iniciales.")
    else:
        print(f"El archivo {EXCEL_FILE} ya existe. No es necesario crear uno nuevo.")

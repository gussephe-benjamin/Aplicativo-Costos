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
            'productos': pd.DataFrame(columns=['id', 'nombre_producto', 'descripcion', 'precio_unitario', 'stock', 'fecha_agregado', 'fecha_actualizado']),
            'materia_prima': pd.DataFrame(columns=['id', 'nombre_materia_prima', 'cantidad_disponible', 'precio_por_unidad', 'producto_id', 'fecha_agregado']),
            'mano_obra': pd.DataFrame(columns=['id', 'nombre_empleado', 'costo_por_hora', 'horas_requeridas', 'producto_id', 'fecha_agregado']),
            'costos_indirectos': pd.DataFrame(columns=['id', 'tipo', 'monto', 'descripcion']),
            'ordenes_pedido': pd.DataFrame(columns=['id', 'usuario_id', 'producto_id', 'cantidad','total_costos_directos', 'total_costos_indirectos', 'total_costos','precio_unitario', 'fecha_entrega']),
        }
        
        # Crear el archivo Excel con las hojas necesarias
        with pd.ExcelWriter(EXCEL_FILE) as writer:
            for sheet_name, df in hojas.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"Archivo {EXCEL_FILE} creado exitosamente con las hojas iniciales.")
    else:
        print(f"El archivo {EXCEL_FILE} ya existe. No es necesario crear uno nuevo.")


inicializar_datos()
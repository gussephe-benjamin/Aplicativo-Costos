import pandas as pd
from config import Config

# Cargar el archivo de Excel y la hoja de Materia Prima
df_materia_prima = pd.read_excel(Config.EXCEL_FILE, sheet_name="materia_prima")

# Función para obtener todos los registros de materia prima
def obtener_materia_prima():
    return df_materia_prima.to_dict(orient='records')

# Función para obtener un registro de materia prima por id
def obtener_materia_prima_por_id(id):
    record = df_materia_prima[df_materia_prima['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear un nuevo registro de materia prima
def crear_materia_prima(nombre, cantidad_disponible, precio_por_unidad):
    nuevo_id = df_materia_prima['id'].max() + 1  # Genera un nuevo ID único
    nuevo_registro = {
        'id': nuevo_id,
        'nombre': nombre,
        'cantidad_disponible': cantidad_disponible,
        'precio_por_unidad': precio_por_unidad
    }
    df_materia_prima = df_materia_prima.append(nuevo_registro, ignore_index=True)
    df_materia_prima.to_excel(Config.EXCEL_FILE, sheet_name='materia_prima', index=False)
    return nuevo_registro

# Función para actualizar un registro de materia prima
def actualizar_materia_prima(id, nombre=None, cantidad_disponible=None, precio_por_unidad=None):
    index = df_materia_prima[df_materia_prima['id'] == id].index[0]
    
    if nombre:
        df_materia_prima.at[index, 'nombre'] = nombre
    if cantidad_disponible:
        df_materia_prima.at[index, 'cantidad_disponible'] = cantidad_disponible
    if precio_por_unidad:
        df_materia_prima.at[index, 'precio_por_unidad'] = precio_por_unidad
    
    df_materia_prima.to_excel(Config.EXCEL_FILE, sheet_name='materia_prima', index=False)
    return df_materia_prima.iloc[index].to_dict()

# Función para eliminar un registro de materia prima
def eliminar_materia_prima(id):
    global df_materia_prima
    df_materia_prima = df_materia_prima[df_materia_prima['id'] != id]
    df_materia_prima.to_excel(Config.EXCEL_FILE, sheet_name='materia_prima', index=False)
    return {'mensaje': 'Registro eliminado exitosamente'}

# Nueva función para obtener materia prima por producto
def obtener_materia_prima_por_producto(producto_id):
    """Obtiene los registros de materia prima asociados a un producto específico"""
    try:
        # Filtrar la materia prima que pertenece al producto dado
        materia_prima = df_materia_prima[df_materia_prima['producto_id'] == producto_id]
        return materia_prima.to_dict(orient='records')  # Convertir a lista de diccionarios
    except KeyError:
        print("Error: La columna 'producto_id' no existe en la hoja de materia_prima.")
        return []
    except Exception as e:
        print(f"Error al obtener materia prima por producto: {e}")
        return []
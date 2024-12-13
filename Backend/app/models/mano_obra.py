import pandas as pd
from config import Config

# Cargar el archivo de Excel
df_mano_obra = pd.read_excel(Config.EXCEL_FILE, sheet_name="mano_obra")

# Función para obtener todos los registros de mano de obra
def obtener_mano_obra():
    return df_mano_obra.to_dict(orient='records')

# Función para obtener un registro de mano de obra por id
def obtener_mano_obra_por_id(id):
    record = df_mano_obra[df_mano_obra['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear un nuevo registro de mano de obra
def crear_mano_obra(nombre_empleado, costo_por_hora, producto_id, horas_requeridas):
    nuevo_id = df_mano_obra['id'].max() + 1  # Genera un nuevo ID único
    nuevo_registro = {
        'id': nuevo_id,
        'nombre_empleado': nombre_empleado,
        'costo_por_hora': costo_por_hora,
        'producto_id': producto_id,
        'horas_requeridas': horas_requeridas
    }
    df_mano_obra = df_mano_obra.append(nuevo_registro, ignore_index=True)
    df_mano_obra.to_excel(Config.EXCEL_FILE, sheet_name='mano_obra', index=False)
    return nuevo_registro

# Función para actualizar un registro de mano de obra
def actualizar_mano_obra(id, nombre_empleado=None, costo_por_hora=None, producto_id=None, horas_requeridas=None):
    index = df_mano_obra[df_mano_obra['id'] == id].index[0]
    
    if nombre_empleado:
        df_mano_obra.at[index, 'nombre_empleado'] = nombre_empleado
    if costo_por_hora:
        df_mano_obra.at[index, 'costo_por_hora'] = costo_por_hora
    if producto_id:
        df_mano_obra.at[index, 'producto_id'] = producto_id
    if horas_requeridas:
        df_mano_obra.at[index, 'horas_requeridas'] = horas_requeridas
    
    df_mano_obra.to_excel(Config.EXCEL_FILE, sheet_name='mano_obra', index=False)
    return df_mano_obra.iloc[index].to_dict()

# Función para eliminar un registro de mano de obra
def eliminar_mano_obra(id):
    global df_mano_obra
    df_mano_obra = df_mano_obra[df_mano_obra['id'] != id]
    df_mano_obra.to_excel(Config.EXCEL_FILE, sheet_name='mano_obra', index=False)
    return {'mensaje': 'Registro eliminado exitosamente'}

# Función para obtener registros de mano de obra asociados a un producto
def obtener_mano_obra_por_producto(producto_id):
    """Obtiene todos los registros de mano de obra asociados a un producto específico"""
    try:
        # Filtrar los registros que coincidan con el producto_id
        mano_obra = df_mano_obra[df_mano_obra['producto_id'] == producto_id]
        return mano_obra.to_dict(orient='records')  # Convertir el resultado a una lista de diccionarios
    except KeyError:
        print("Error: La columna 'producto_id' no existe en la hoja de mano_obra.")
        return []
    except Exception as e:
        print(f"Error al obtener mano de obra por producto: {e}")
        return []
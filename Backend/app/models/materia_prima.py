import pandas as pd
from config import Config

EXCEL_FILE = Config.EXCEL_FILE
SHEET_NAME = "materia_prima"

def leer_materia_prima():
    """Leer todos los registros de materia prima."""
    try:
        df = pd.read_excel(Config.EXCEL_FILE, sheet_name="materia_prima")
        df['id'] = df['id'].astype(int)  # Convertimos la columna id a entero
        return df
    except Exception as e:
        print(f"Error al leer materia prima: {e}")
        return pd.DataFrame(columns=['id', 'nombre', 'cantidad_disponible', 'precio_por_unidad', 'producto_id'])


def guardar_materia_prima(df):
    """Guardar los registros actualizados de materia prima."""
    try:
        with pd.ExcelWriter(Config.EXCEL_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='materia_prima', index=False)
    except Exception as e:
        print(f"Error al guardar materia prima: {e}")

def obtener_materia_prima():
    """Obtener todos los registros de materia prima."""
    df = leer_materia_prima()
    return df.to_dict(orient='records')

def obtener_materia_prima_por_id(id):
    """Obtener un registro de materia prima por ID."""
    df = leer_materia_prima()
    record = df[df['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

def crear_materia_prima(nombre, cantidad_disponible, precio_por_unidad, producto_id=None):
    """Crear un nuevo registro de materia prima."""
    try:
        df = leer_materia_prima()
        nuevo_id = int(df['id'].max() + 1) if not df.empty else 1
        nuevo_registro = pd.DataFrame([{
            'id': nuevo_id,
            'nombre_materia_prima': nombre,
            'cantidad_disponible': cantidad_disponible,
            'precio_por_unidad': precio_por_unidad,
            'producto_id': producto_id,
            'fecha_agregado': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        }])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        guardar_materia_prima(df)
        return nuevo_registro.iloc[0].to_dict()
    except Exception as e:
        print(f"Error al crear materia prima: {e}")
        return {"error": "Hubo un error al crear la materia prima"}

def actualizar_materia_prima(id, nombre=None, cantidad_disponible=None, precio_por_unidad=None, producto_id=None):
    """Actualizar un registro de materia prima."""
    try:
        df = leer_materia_prima()
        if id not in df['id'].values:
            return {"error": "Registro no encontrado"}
        
        if nombre:
            df.loc[df['id'] == id, 'nombre'] = nombre
        if cantidad_disponible:
            df.loc[df['id'] == id, 'cantidad_disponible'] = cantidad_disponible
        if precio_por_unidad:
            df.loc[df['id'] == id, 'precio_por_unidad'] = precio_por_unidad
        if producto_id is not None:
            df.loc[df['id'] == id, 'producto_id'] = producto_id
        
        guardar_materia_prima(df)
        return {"success": "Registro actualizado exitosamente"}
    except Exception as e:
        print(f"Error al actualizar materia prima: {e}")
        return {"error": "Hubo un error al actualizar la materia prima"}

def eliminar_materia_prima(id):
    """Eliminar un registro de materia prima."""
    try:
        # Leer la hoja actualizada de materia prima
        df = leer_materia_prima()

        # Asegurarse de que la columna id es tipo entero
        df['id'] = df['id'].astype(int)

        # Verificar si el ID existe
        if id not in df['id'].values:
            return {"error": "Registro no encontrado"}

        # Eliminar el registro con el ID especificado
        df = df[df['id'] != id]

        # Guardar los cambios
        guardar_materia_prima(df)
        return {"success": "Registro eliminado exitosamente"}
    except Exception as e:
        print(f"Error al eliminar materia prima: {e}")
        return {"error": "Hubo un error al eliminar la materia prima"}

def obtener_materia_prima_por_producto(producto_id):
    """Obtener registros de materia prima asociados a un producto específico."""
    try:
        df = leer_materia_prima()
        materia_prima = df[df['producto_id'] == producto_id]
        return materia_prima.to_dict(orient='records')
    except KeyError:
        print("Error: La columna 'producto_id' no existe en la hoja de materia_prima.")
        return []
    except Exception as e:
        print(f"Error al obtener materia prima por producto: {e}")
        return []

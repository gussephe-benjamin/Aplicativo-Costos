import pandas as pd
from config import Config  # Importamos Config para acceder a la configuración
import datetime

# Archivo Excel donde se almacenan los productos
EXCEL_FILE = Config.EXCEL_FILE  # Usamos la ruta del archivo desde la configuración
SHEET_NAME = "productos"  # Nombre de la hoja donde están los productos

def leer_productos():
    """Leer todos los productos desde el archivo Excel y devolver un array de diccionarios"""
    try:
        # Leer la hoja de Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

        # Reemplazar NaN con None para evitar errores en la serialización JSON
        df = df.where(pd.notnull(df), None)

        # Convertir a lista de diccionarios
        return df.to_dict(orient='records')

    except Exception as e:
        print(f"Error al leer productos: {e}")
        return []  # Devuelve una lista vacía en caso de error
    
def guardar_productos(df):
    """Guardar los productos actualizados en la hoja correspondiente del archivo Excel"""
    try:
        with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    except Exception as e:
        print(f"Error al guardar productos: {e}")

def agregar_producto(nombre, descripcion, precio_unitario, stock, fecha_agregado):
    """Agregar un nuevo producto en la hoja de Excel"""
    try:
        # Leer los productos actuales desde el archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        
        # Crear un nuevo producto
        nuevo_producto = pd.DataFrame([{
            'id': len(df) + 1,  # Asignamos un ID único
            'nombre_producto': nombre,
            'descripcion': descripcion,
            'precio_unitario': precio_unitario,
            'stock': stock,
            'fecha_agregado': fecha_agregado
        }])
        
        # Concatenar el nuevo producto al DataFrame existente
        df = pd.concat([df, nuevo_producto], ignore_index=True)
        
        # Guardar los cambios en la hoja de Excel
        guardar_productos(df)
        
        return {"success": "Producto agregado exitosamente"}
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        return {"error": "Hubo un error al agregar el producto"}


def actualizar_producto(id, nombre=None, descripcion=None, precio_unitario=None, stock=None, fecha_actualizado=None):
    """Actualizar un producto existente en la hoja de Excel"""
    try:
        # Leer los productos desde el archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        
        # Convertir el tipo de la columna 'id' a entero para evitar problemas de comparación
        df['id'] = df['id'].astype(int)
        
        # Verificar si el producto existe
        producto_index = df[df['id'] == id].index
        
        if not producto_index.empty:
            # Actualizamos los campos proporcionados (solo los que no son None)
            if nombre is not None:
                df.loc[producto_index, 'nombre'] = nombre
            if descripcion is not None:
                df.loc[producto_index, 'descripcion'] = descripcion
            if precio_unitario is not None:
                df.loc[producto_index, 'precio_unitario'] = precio_unitario
            if stock is not None:
                df.loc[producto_index, 'stock'] = stock
            if fecha_actualizado is not None:
                df.loc[producto_index, 'fecha_actualizado'] = fecha_actualizado
            
            # Guardamos los cambios
            guardar_productos(df)
            return {"success": "Producto actualizado exitosamente"}
        else:
            return {"error": "Producto no encontrado"}
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return {"error": "Hubo un error al actualizar el producto"}


def eliminar_producto(id):
    """Eliminar un producto de la hoja de Excel"""
    try:
        # Leer los productos desde el archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        
        # Eliminar el producto con el ID especificado
        df = df[df['id'] != id]
        
        # Guardamos los cambios
        guardar_productos(df)
        return {"success": "Producto eliminado exitosamente"}
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return {"error": "Hubo un error al eliminar el producto"}

def obtener_producto_por_id(id):
    """Obtener un producto por su ID"""
    try:
        # Leer los productos desde el archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        
        # Buscar el producto con el ID especificado
        producto = df[df['id'] == id]
        
        # Verificar si existe el producto
        if not producto.empty:
            return producto.iloc[0].to_dict()  # Convertimos el producto a diccionario y lo devolvemos
        else:
            return None  # Si no se encuentra, devolvemos None
    except Exception as e:
        print(f"Error al obtener producto por ID: {e}")
        return None
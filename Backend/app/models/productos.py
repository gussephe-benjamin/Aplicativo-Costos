import pandas as pd
from config import Config  # Importamos Config para acceder a la configuración
import datetime

# Archivo Excel donde se almacenan los productos
EXCEL_FILE = Config.EXCEL_FILE  # Usamos la ruta del archivo desde la configuración
SHEET_NAME = "productos"  # Nombre de la hoja donde están los productos

def leer_productos():
    """Leer todos los productos desde el archivo Excel y devolverlos como una lista de diccionarios"""
    try:
        # Leemos la hoja 'productos' del archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        return df.to_dict(orient='records')  # Convertimos el DataFrame a lista de diccionarios
    except Exception as e:
        print(f"Error al leer productos: {e}")
        return []

def guardar_productos(df):
    """Guardar los productos actualizados en la hoja correspondiente del archivo Excel"""
    try:
        # Guardamos el DataFrame en la hoja 'productos' del archivo Excel
        df.to_excel(EXCEL_FILE, sheet_name=SHEET_NAME, index=False)
    except Exception as e:
        print(f"Error al guardar productos: {e}")

def agregar_producto(nombre, descripcion, precio_unitario, stock, fecha_agregado):
    """Agregar un nuevo producto en la hoja de Excel"""
    try:
        # Leer los productos actuales desde el archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        
        # Crear un nuevo producto
        nuevo_producto = {
            'id': len(df) + 1,  # Asignamos un ID único
            'nombre': nombre,
            'descripcion': descripcion,
            'precio_unitario': precio_unitario,
            'stock': stock,
            'fecha_agregado': fecha_agregado
        }
        
        # Agregar el nuevo producto al DataFrame
        df = df.append(nuevo_producto, ignore_index=True)
        
        # Guardar los cambios en la hoja de Excel
        guardar_productos(df)
        
        return {"success": "Producto agregado exitosamente"}
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        return {"error": "Hubo un error al agregar el producto"}

def actualizar_producto(id, nombre, descripcion, precio_unitario, stock, fecha_agregado):
    """Actualizar un producto existente en la hoja de Excel"""
    try:
        # Leer los productos desde el archivo Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        
        # Verificar si el producto existe
        producto = df[df['id'] == id]
        if not producto.empty:
            # Actualizamos el producto
            df.loc[df['id'] == id, ['nombre', 'descripcion', 'precio_unitario', 'stock', 'fecha_agregado']] = [nombre, descripcion, precio_unitario, stock, fecha_agregado]
            
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
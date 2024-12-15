import pandas as pd
from config import Config
from models.productos import obtener_producto_por_id
from models.materia_prima import obtener_materia_prima_por_producto
from models.mano_obra import obtener_mano_obra_por_producto
from models.costos_indirectos import obtener_costos_indirectos

# Variables globales para archivo y hoja
EXCEL_FILE = Config.EXCEL_FILE
SHEET_NAME = "ordenes_pedido"

# Función para leer las órdenes de pedido
def leer_ordenes_pedido():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    except Exception:
        return pd.DataFrame(columns=[
            'id', 'usuario_id', 'producto_id', 'cantidad', 'fecha_entrega',
            'total_costos_directos', 'total_costos_indirectos', 'total_costos',
            'precio_unitario', 'fecha_creacion'
        ])

# Función para guardar las órdenes de pedido
def guardar_ordenes_pedido(df):
    try:
        with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    except Exception as e:
        print(f"Error al guardar las órdenes de pedido: {e}")

# Función para obtener todas las órdenes de pedido
def obtener_ordenes_pedido():
    df = leer_ordenes_pedido()
    return df.to_dict(orient='records')

# Función para obtener una orden por ID
def obtener_orden_por_id(id):
    df = leer_ordenes_pedido()
    record = df[df['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear una nueva orden de pedido
def crear_orden_de_pedido(usuario_id, producto_id, cantidad, fecha_entrega):
    df = leer_ordenes_pedido()
    
    # Verificar si el producto existe
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return {"error": "Producto no encontrado"}
    
    # Cálculos de costos
    materia_prima = obtener_materia_prima_por_producto(producto_id)
    costo_materia_prima = sum([m['cantidad_disponible'] * m['precio_por_unidad'] for m in materia_prima])

    mano_obra = obtener_mano_obra_por_producto(producto_id)
    costo_mano_obra = sum([m['horas_requeridas'] * m['costo_por_hora'] for m in mano_obra])

    costos_indirectos = obtener_costos_indirectos()
    costo_indirecto = sum([c['monto'] for c in costos_indirectos])

    costo_total = costo_materia_prima + costo_mano_obra + costo_indirecto
    precio_unitario = costo_total / cantidad

    # Generar nuevo ID
    nuevo_id = int(df['id'].max() + 1) if not df.empty else 1

    # Nuevo registro
    nuevo_registro = {
        'id': nuevo_id,
        'usuario_id': usuario_id,
        'producto_id': producto_id,
        'cantidad': cantidad,
        'fecha_entrega': fecha_entrega,
        'total_costos_directos': costo_materia_prima + costo_mano_obra,
        'total_costos_indirectos': costo_indirecto,
        'total_costos': costo_total,
        'precio_unitario': precio_unitario,
        'fecha_creacion': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Guardar en Excel
    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    guardar_ordenes_pedido(df)
    
    return nuevo_registro

# Función para actualizar una orden existente
def actualizar_orden_de_pedido(id, cantidad=None, fecha_entrega=None):
    df = leer_ordenes_pedido()
    index = df[df['id'] == id].index

    if not index.empty:
        if cantidad:
            df.at[index[0], 'cantidad'] = cantidad
        if fecha_entrega:
            df.at[index[0], 'fecha_entrega'] = fecha_entrega
        guardar_ordenes_pedido(df)
        return {"success": "Orden actualizada exitosamente"}
    return {"error": "Orden no encontrada"}

# Función para eliminar una orden de pedido
def eliminar_orden_de_pedido(id):
    df = leer_ordenes_pedido()
    if id not in df['id'].values:
        return {"error": "Orden no encontrada"}
    
    df = df[df['id'] != id]
    guardar_ordenes_pedido(df)
    return {"success": "Orden eliminada exitosamente"}

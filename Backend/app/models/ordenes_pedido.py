import pandas as pd
from config import Config
from models.productos import obtener_producto_por_id
from models.materia_prima import obtener_materia_prima_por_producto
from models.mano_obra import obtener_mano_obra_por_producto
from models.costos_indirectos import obtener_costos_indirectos

# Cargar el archivo de Excel y la hoja de Órdenes de Pedido
df_ordenes_pedido = pd.read_excel(Config.EXCEL_FILE, sheet_name="ordenes_pedido")

# Función para obtener todas las órdenes de pedido
def obtener_ordenes_pedido():
    return df_ordenes_pedido.to_dict(orient='records')

# Función para obtener una orden de pedido por id
def obtener_orden_por_id(id):
    record = df_ordenes_pedido[df_ordenes_pedido['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear una nueva orden de pedido
def crear_orden_de_pedido(usuario_id, producto_id, cantidad, fecha_entrega):
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return None

    # Cálculos de los costos directos
    materia_prima = obtener_materia_prima_por_producto(producto_id)
    costo_materia_prima = sum([m['cantidad'] * m['precio'] for m in materia_prima])

    mano_obra = obtener_mano_obra_por_producto(producto_id)
    costo_mano_obra = sum([m['horas'] * m['costo_hora'] for m in mano_obra])

    # Cálculos de los costos indirectos
    costos_indirectos = obtener_costos_indirectos()
    costo_indirecto = sum([c['monto'] for c in costos_indirectos])

    # Cálculo del precio total
    costo_total = costo_materia_prima + costo_mano_obra + costo_indirecto
    precio_unitario = costo_total / cantidad

    nuevo_id = df_ordenes_pedido['id'].max() + 1  # Genera un nuevo ID único
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
        'fecha_creacion': pd.Timestamp.now()
    }

    df_ordenes_pedido = df_ordenes_pedido.append(nuevo_registro, ignore_index=True)
    df_ordenes_pedido.to_excel(Config.EXCEL_FILE, sheet_name='ordenes_pedido', index=False)
    return nuevo_registro

# Función para actualizar una orden de pedido
def actualizar_orden_de_pedido(id, cantidad=None, fecha_entrega=None):
    index = df_ordenes_pedido[df_ordenes_pedido['id'] == id].index[0]
    
    if cantidad:
        df_ordenes_pedido.at[index, 'cantidad'] = cantidad
    if fecha_entrega:
        df_ordenes_pedido.at[index, 'fecha_entrega'] = fecha_entrega
    
    # Recalcular los costos
    usuario_id = df_ordenes_pedido.at[index, 'usuario_id']
    producto_id = df_ordenes_pedido.at[index, 'producto_id']
    nuevo_costo = crear_orden_de_pedido(usuario_id, producto_id, df_ordenes_pedido.at[index, 'cantidad'], df_ordenes_pedido.at[index, 'fecha_entrega'])

    return nuevo_costo

# Función para eliminar una orden de pedido
def eliminar_orden_de_pedido(id):
    global df_ordenes_pedido
    df_ordenes_pedido = df_ordenes_pedido[df_ordenes_pedido['id'] != id]
    df_ordenes_pedido.to_excel(Config.EXCEL_FILE, sheet_name='ordenes_pedido', index=False)
    return {'mensaje': 'Orden eliminada exitosamente'}


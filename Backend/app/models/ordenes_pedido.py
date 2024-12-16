import pandas as pd
from config import Config
from models.productos import obtener_producto_por_id
from models.materia_prima import obtener_materia_prima_por_producto, actualizar_materia_prima
from models.mano_obra import obtener_mano_obra_por_producto
from models.costos_indirectos import obtener_costos_indirectos
from collections import OrderedDict
from datetime import datetime, timedelta
from fpdf import FPDF
import os
from models.usuarios import obtener_usuario_por_id

# Variables globales para archivo y hoja
EXCEL_FILE = Config.EXCEL_FILE
SHEET_NAME = "ordenes_pedido"
OUTPUT_DIR = "generated_pdfs"

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

# Función para validar la fecha de entrega
def validar_fecha_entrega(producto_id, cantidad, fecha_entrega):
    try:
        mano_obra = obtener_mano_obra_por_producto(producto_id)
        if not mano_obra:
            return {"error": "No se encontró mano de obra para el producto."}

        horas_requeridas = sum([m['horas_requeridas'] for m in mano_obra]) * cantidad
        capacidad_diaria = 8 * 5  # Ejemplo: 8 horas por día para 5 empleados
        fecha_actual = datetime.now()

        dias_requeridos = -(-horas_requeridas // capacidad_diaria)  # División redondeada hacia arriba
        fecha_viable = fecha_actual + timedelta(days=dias_requeridos)

        if datetime.strptime(fecha_entrega, "%Y-%m-%d") < fecha_viable:
            return {
                "error": "Fecha no viable",
                "fecha_minima_viable": fecha_viable.strftime("%Y-%m-%d")
            }
        return {"success": "Fecha viable"}
    except Exception as e:
        return {"error": f"Error al validar la fecha de entrega: {e}"}

# Función para gestionar inventarios
def gestionar_inventario(producto_id, cantidad):
    try:
        materia_prima = obtener_materia_prima_por_producto(producto_id)
        if not materia_prima:
            return {"error": "No se encontró materia prima para el producto."}

        for material in materia_prima:
            if 'cantidad_disponible' not in material or 'precio_por_unidad' not in material:
                return {"error": f"El material {material['nombre']} no tiene las claves necesarias."}
            requerido = cantidad
            if material['cantidad_disponible'] < requerido:
                return {
                    "error": f"Materia prima insuficiente: {material['nombre']}",
                    "faltante": requerido - material['cantidad_disponible']
                }

        for material in materia_prima:
            material['cantidad_disponible'] -= cantidad
            actualizar_materia_prima(material['id'], cantidad_disponible=material['cantidad_disponible'])

        return {"success": "Inventario actualizado"}
    except Exception as e:
        return {"error": f"Error al gestionar el inventario: {e}"}

def crear_orden_de_pedido(usuario_id, producto_id, cantidad, fecha_entrega):
    try:
        print("Iniciando la creación de orden...")
        df = leer_ordenes_pedido()
        print(f"Órdenes actuales en el archivo: {df.shape[0]} filas.")

        validacion_fecha = validar_fecha_entrega(producto_id, cantidad, fecha_entrega)
        if "error" in validacion_fecha:
            print(f"Error en validación de fecha: {validacion_fecha}")
            return validacion_fecha

        gestion_inventario = gestionar_inventario(producto_id, cantidad)
        if "error" in gestion_inventario:
            print(f"Error en gestión de inventario: {gestion_inventario}")
            return gestion_inventario

        producto = obtener_producto_por_id(producto_id)
        if not producto:
            print("Error: Producto no encontrado.")
            return {"error": "Producto no encontrado"}

        print("Calculando costos...")
        materia_prima = obtener_materia_prima_por_producto(producto_id)
        costo_materia_prima = sum([m['cantidad_disponible'] * m['precio_por_unidad'] for m in materia_prima])

        mano_obra = obtener_mano_obra_por_producto(producto_id)
        costo_mano_obra = sum([m['horas_requeridas'] * m['costo_por_hora'] for m in mano_obra])

        costos_indirectos = obtener_costos_indirectos()
        costo_indirecto = sum([c['monto'] for c in costos_indirectos])

        costo_total = costo_materia_prima + costo_mano_obra + costo_indirecto
        precio_unitario = costo_total / cantidad

        nuevo_id = int(df['id'].max() + 1) if not df.empty else 1
        print(f"Nuevo ID generado: {nuevo_id}")

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

        print("Nuevo registro:", nuevo_registro)

        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        print("Guardando orden en el archivo...")
        guardar_ordenes_pedido(df)
        print("Orden guardada exitosamente.")
        return nuevo_registro
    except Exception as e:
        print(f"Error general: {e}")
        return {"error": f"Error al crear la orden de pedido: {e}"}


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

def obtener_ordenes_pedido():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        return df.to_dict(orient='records')
    except Exception:
        return []
    
def obtener_orden_por_id(id):
    df = leer_ordenes_pedido()
    record = df[df['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None


OUTPUT_DIR = "generated_pdfs"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generar_pdf_orden(orden_id):
    # Obtener datos de la orden
    orden = obtener_orden_por_id(orden_id)
    if not orden:
        return {"error": "Orden no encontrada"}

    producto = obtener_producto_por_id(orden["producto_id"])
    usuario = obtener_usuario_por_id(orden["usuario_id"])

    if not producto or not usuario:
        return {"error": "No se pudo obtener datos adicionales"}

    # Validar claves existentes en producto y usuario
    nombre_producto = producto.get("nombre_producto", "Producto sin nombre")
    email_usuario = usuario.get("email", "Email no disponible")

    # Crear un nuevo PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Resumen de Pedido", ln=True, align="C")
    pdf.ln(10)

    # Datos de la orden
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"ID de la Orden: {orden['id']}", ln=True)
    pdf.cell(0, 10, txt=f"Cliente: {email_usuario}", ln=True)
    pdf.cell(0, 10, txt=f"Producto: {nombre_producto}", ln=True)
    pdf.cell(0, 10, txt=f"Cantidad: {orden['cantidad']}", ln=True)
    pdf.cell(0, 10, txt=f"Fecha de Creación: {orden['fecha_creacion']}", ln=True)
    pdf.cell(0, 10, txt=f"Fecha de Entrega: {orden['fecha_entrega']}", ln=True)
    pdf.ln(10)

    # Detalles de costos
    pdf.cell(0, 10, txt="Costos:", ln=True)
    pdf.cell(0, 10, txt=f"Costos Directos: {orden['total_costos_directos']}", ln=True)
    pdf.cell(0, 10, txt=f"Costos Indirectos: {orden['total_costos_indirectos']}", ln=True)
    pdf.cell(0, 10, txt=f"Total: {orden['total_costos']}", ln=True)
    pdf.cell(0, 10, txt=f"Precio Unitario: {orden['precio_unitario']}", ln=True)

    # Guardar el archivo PDF
    pdf_file = os.path.join(OUTPUT_DIR, f"orden_{orden_id}.pdf")
    pdf.output(pdf_file)
    return {"success": "PDF generado exitosamente", "file_path": pdf_file}
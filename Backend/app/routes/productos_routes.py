from flask import Blueprint, request, jsonify
from models.productos import leer_productos, agregar_producto, actualizar_producto, eliminar_producto
from datetime import datetime

productos_bp = Blueprint('productos', __name__)

# Crear producto
@productos_bp.route('/crear', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    precio_unitario = data['precio_unitario']
    stock = data['stock']
    fecha_agregado = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    agregar_producto(nombre, descripcion, precio_unitario, stock, fecha_agregado)
    return jsonify({'message': 'Producto creado exitosamente'}), 201

# Obtener todos los productos
@productos_bp.route('/getAll', methods=['GET'])
def obtener_productos():
    productos = leer_productos()
    return jsonify(productos), 200

# Actualizar producto
from flask import request, jsonify
from datetime import datetime
from models.productos import actualizar_producto

@productos_bp.route('/actualizar', methods=['PUT'])
def actualizar_producto_route():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        id = data.get('id')  # Usar .get() para evitar KeyError si no se envía algún campo
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio_unitario = data.get('precio_unitario')
        stock = data.get('stock')
        fecha_actualizado = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Validar que el ID fue enviado
        if id is None:
            return jsonify({'error': 'El campo "id" es obligatorio.'}), 400

        # Llamar a la función de actualización
        resultado = actualizar_producto(id, nombre, descripcion, precio_unitario, stock, fecha_actualizado)
        
        # Manejar respuestas según el resultado de la función
        if "success" in resultado:
            return jsonify({'message': 'Producto actualizado exitosamente'}), 200
        else:
            return jsonify(resultado), 404  # Producto no encontrado o error específico
    except Exception as e:
        print(f"Error en actualizar_producto_route: {e}")
        return jsonify({'error': 'Error interno en el servidor'}), 500

# Eliminar producto
@productos_bp.route('/eliminar', methods=['DELETE'])
def eliminar_producto_route():
    
    data = request.get_json()
    id = data['id']
    eliminar_producto(id)
    return jsonify({'message': 'Producto eliminado exitosamente'}), 200

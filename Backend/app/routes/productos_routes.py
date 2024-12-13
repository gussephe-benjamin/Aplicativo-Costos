from flask import Blueprint, request, jsonify
from models.productos import leer_productos, agregar_producto, actualizar_producto, eliminar_producto

productos_bp = Blueprint('productos', __name__)

# Crear producto
@productos_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    precio_unitario = data['precio_unitario']
    stock = data['stock']
    fecha_agregado = data['fecha_agregado']

    agregar_producto(nombre, descripcion, precio_unitario, stock, fecha_agregado)
    return jsonify({'message': 'Producto creado exitosamente'}), 201

# Obtener todos los productos
@productos_bp.route('/productos', methods=['GET'])
def obtener_productos():
    productos = leer_productos()
    return jsonify(productos), 200

# Actualizar producto
@productos_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto_route(id):
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    precio_unitario = data['precio_unitario']
    stock = data['stock']
    fecha_agregado = data['fecha_agregado']

    actualizar_producto(id, nombre, descripcion, precio_unitario, stock, fecha_agregado)
    return jsonify({'message': 'Producto actualizado exitosamente'}), 200

# Eliminar producto
@productos_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto_route(id):
    eliminar_producto(id)
    return jsonify({'message': 'Producto eliminado exitosamente'}), 200

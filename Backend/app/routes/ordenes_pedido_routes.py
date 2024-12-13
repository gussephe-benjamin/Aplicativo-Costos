from flask import Blueprint, request, jsonify
from models.ordenes_pedido import (
    obtener_ordenes_pedido,
    obtener_orden_por_id,
    crear_orden_de_pedido,
    actualizar_orden_de_pedido,
    eliminar_orden_de_pedido
)

ordenes_pedido_bp = Blueprint('ordenes_pedido', __name__)

# Ruta para obtener todas las órdenes de pedido
@ordenes_pedido_bp.route('/ordenes-pedido', methods=['GET'])
def get_ordenes_pedido():
    return jsonify(obtener_ordenes_pedido()), 200

# Ruta para obtener una orden de pedido por ID
@ordenes_pedido_bp.route('/ordenes-pedido/<int:id>', methods=['GET'])
def get_orden_por_id(id):
    orden = obtener_orden_por_id(id)
    if orden:
        return jsonify(orden), 200
    return jsonify({'mensaje': 'Orden de pedido no encontrada'}), 404

# Ruta para crear una nueva orden de pedido
@ordenes_pedido_bp.route('/ordenes-pedido', methods=['POST'])
def create_orden_de_pedido_route():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    fecha_entrega = data.get('fecha_entrega')

    if not usuario_id or not producto_id or not cantidad or not fecha_entrega:
        return jsonify({'mensaje': 'Faltan datos requeridos'}), 400

    nueva_orden = crear_orden_de_pedido(usuario_id, producto_id, cantidad, fecha_entrega)
    if nueva_orden:
        return jsonify(nueva_orden), 201
    return jsonify({'mensaje': 'Producto no encontrado'}), 404

# Ruta para actualizar una orden de pedido
@ordenes_pedido_bp.route('/ordenes-pedido/<int:id>', methods=['PUT'])
def update_orden_de_pedido_route(id):
    data = request.get_json()
    cantidad = data.get('cantidad')
    fecha_entrega = data.get('fecha_entrega')

    orden_actualizada = actualizar_orden_de_pedido(id, cantidad, fecha_entrega)
    if orden_actualizada:
        return jsonify(orden_actualizada), 200
    return jsonify({'mensaje': 'Orden de pedido no encontrada'}), 404

# Ruta para eliminar una orden de pedido
@ordenes_pedido_bp.route('/ordenes-pedido/<int:id>', methods=['DELETE'])
def delete_orden_de_pedido_route(id):
    resultado = eliminar_orden_de_pedido(id)
    if 'mensaje' in resultado:
        return jsonify(resultado), 200
    return jsonify({'mensaje': 'Orden de pedido no encontrada'}), 404

from flask import Blueprint, request, jsonify
from collections import OrderedDict

from models.productos import obtener_producto_por_id
from models.usuarios import obtener_usuario_por_id

from models.ordenes_pedido import (
    obtener_ordenes_pedido,
    obtener_orden_por_id,
    crear_orden_de_pedido,
    actualizar_orden_de_pedido,
    eliminar_orden_de_pedido
)

ordenes_pedido_bp = Blueprint('ordenes_pedido', __name__)

# Ruta para obtener todas las órdenes de pedido
@ordenes_pedido_bp.route('/getAll', methods=['GET'])
def get_ordenes_pedido():
    return jsonify(obtener_ordenes_pedido()), 200

# Ruta para obtener una orden de pedido por ID
@ordenes_pedido_bp.route('/get/<int:id>', methods=['GET'])
def get_orden_por_id(id):
    orden = obtener_orden_por_id(id)
    if orden:
        return jsonify(orden), 200
    return jsonify({'mensaje': 'Orden de pedido no encontrada'}), 404

# Ruta para crear una nueva orden de pedido
@ordenes_pedido_bp.route('/post', methods=['POST'])
def crear_orden_pedido_route():
    try:
        data = request.get_json()
        usuario_id = data['usuario_id']
        producto_id = data['producto_id']
        cantidad = data['cantidad']
        fecha_entrega = data['fecha_entrega']

        # Crear la orden de pedido
        nueva_orden = crear_orden_de_pedido(usuario_id, producto_id, cantidad, fecha_entrega)

        if not nueva_orden:
            return jsonify({"error": "No se pudo crear la orden de pedido"}), 400

        # Obtener datos adicionales
        producto = obtener_producto_por_id(producto_id)
        usuario = obtener_usuario_por_id(usuario_id)

        if not producto or not usuario:
            return jsonify({"error": "No se pudo obtener datos adicionales"}), 400

        # Crear un OrderedDict para asegurar el orden de las claves en la respuesta
        respuesta = OrderedDict([
            ('producto', producto['nombre']),
            ('usuario', usuario['email']),
            ('cantidad', nueva_orden['cantidad']),
            ('fecha_creacion', nueva_orden['fecha_creacion']),
            ('fecha_entrega', nueva_orden['fecha_entrega']),
            ('total_costos_directos', nueva_orden['total_costos_directos']),
            ('total_costos_indirectos', nueva_orden['total_costos_indirectos']),
            ('total_costos', nueva_orden['total_costos']),
            ('precio_unitario', nueva_orden['precio_unitario'])
        ])

        return jsonify(respuesta), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar una orden de pedido
@ordenes_pedido_bp.route('/put/<int:id>', methods=['PUT'])
def update_orden_de_pedido_route(id):
    data = request.get_json()
    cantidad = data.get('cantidad')
    fecha_entrega = data.get('fecha_entrega')

    orden_actualizada = actualizar_orden_de_pedido(id, cantidad, fecha_entrega)
    if orden_actualizada:
        return jsonify(orden_actualizada), 200
    return jsonify({'mensaje': 'Orden de pedido no encontrada'}), 404

# Ruta para eliminar una orden de pedido
@ordenes_pedido_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_orden_de_pedido_route(id):
    resultado = eliminar_orden_de_pedido(id)
    
    if 'success' in resultado:
        return jsonify(resultado), 200
    
    return jsonify({'mensaje': 'Orden de pedido no encontrada'}), 404

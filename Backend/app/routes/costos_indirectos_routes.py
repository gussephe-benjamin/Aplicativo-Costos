from flask import Blueprint, request, jsonify

from models.costos_indirectos import (
    obtener_costos_indirectos,
    obtener_costos_indirectos_por_id,
    crear_costos_indirectos,
    actualizar_costos_indirectos,
    eliminar_costos_indirectos
)

costos_indirectos_bp = Blueprint('costos_indirectos', __name__)

# Ruta para obtener todos los registros de costos indirectos
@costos_indirectos_bp.route('/costos-indirectos', methods=['GET'])
def get_costos_indirectos():
    return jsonify(obtener_costos_indirectos()), 200

# Ruta para obtener un registro de costos indirectos por ID
@costos_indirectos_bp.route('/costos-indirectos/<int:id>', methods=['GET'])
def get_costos_indirectos_by_id(id):
    costo_indirecto = obtener_costos_indirectos_por_id(id)
    if costo_indirecto:
        return jsonify(costo_indirecto), 200
    return jsonify({'mensaje': 'Costo Indirecto no encontrado'}), 404

# Ruta para crear un nuevo registro de costos indirectos
@costos_indirectos_bp.route('/costos-indirectos', methods=['POST'])
def create_costos_indirectos():
    data = request.get_json()
    tipo = data.get('tipo')
    monto = data.get('monto')
    descripcion = data.get('descripcion')

    if not tipo or monto is None or not descripcion:
        return jsonify({'mensaje': 'Faltan datos requeridos'}), 400

    nuevo_registro = crear_costos_indirectos(tipo, monto, descripcion)
    return jsonify(nuevo_registro), 201

# Ruta para actualizar un registro de costos indirectos
@costos_indirectos_bp.route('/costos-indirectos/<int:id>', methods=['PUT'])
def update_costos_indirectos(id):
    data = request.get_json()
    tipo = data.get('tipo')
    monto = data.get('monto')
    descripcion = data.get('descripcion')

    actualizado = actualizar_costos_indirectos(id, tipo, monto, descripcion)
    if actualizado:
        return jsonify(actualizado), 200
    return jsonify({'mensaje': 'Costo Indirecto no encontrado'}), 404

# Ruta para eliminar un registro de costos indirectos
@costos_indirectos_bp.route('/costos-indirectos/<int:id>', methods=['DELETE'])
def delete_costos_indirectos(id):
    resultado = eliminar_costos_indirectos(id)
    if 'mensaje' in resultado:
        return jsonify(resultado), 200
    return jsonify({'mensaje': 'Costo Indirecto no encontrado'}), 404

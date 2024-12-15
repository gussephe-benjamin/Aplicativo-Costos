from flask import Blueprint, request, jsonify

from models.materia_prima import (
    obtener_materia_prima,
    obtener_materia_prima_por_id,
    crear_materia_prima,
    actualizar_materia_prima,
    eliminar_materia_prima
)

materia_prima_bp = Blueprint('materia_prima', __name__)

# Ruta para obtener todos los registros de materia prima
@materia_prima_bp.route('/getAll', methods=['GET'])
def get_materia_prima():
    return jsonify(obtener_materia_prima()), 200

# Ruta para obtener un registro de materia prima por ID
@materia_prima_bp.route('/get/<int:id>', methods=['GET'])
def get_materia_prima_by_id(id):
    materia_prima = obtener_materia_prima_por_id(id)
    if materia_prima:
        return jsonify(materia_prima), 200
    return jsonify({'mensaje': 'Materia Prima no encontrada'}), 404

# Ruta para crear un nuevo registro de materia prima
@materia_prima_bp.route('/post', methods=['POST'])
def create_materia_prima():
    data = request.get_json()
    nombre = data.get('nombre')
    cantidad_disponible = data.get('cantidad_disponible')
    precio_por_unidad = data.get('precio_por_unidad')
    producto_id = data.get('producto_id')

    if not nombre or cantidad_disponible is None or precio_por_unidad is None:
        return jsonify({'mensaje': 'Faltan datos requeridos'}), 400

    nuevo_registro = crear_materia_prima(nombre, cantidad_disponible, precio_por_unidad, producto_id)
    return jsonify(nuevo_registro), 201

# Ruta para actualizar un registro de materia prima
@materia_prima_bp.route('/put/<int:id>', methods=['PUT'])
def update_materia_prima(id):
    data = request.get_json()
    nombre = data.get('nombre')
    cantidad_disponible = data.get('cantidad_disponible')
    precio_por_unidad = data.get('precio_por_unidad')

    actualizado = actualizar_materia_prima(id, nombre, cantidad_disponible, precio_por_unidad)
    if actualizado:
        return jsonify(actualizado), 200
    return jsonify({'mensaje': 'Materia Prima no encontrada'}), 404

# Ruta para eliminar un registro de materia prima
@materia_prima_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_materia_prima(id):
    
    resultado = eliminar_materia_prima(id)
    
    if 'success' in resultado:
        return jsonify(resultado), 200
    
    return jsonify({'mensaje': 'Materia Prima no encontrada'}), 404

from flask import Blueprint, request, jsonify
from models.mano_obra import obtener_mano_obra, obtener_mano_obra_por_id, crear_mano_obra, actualizar_mano_obra, eliminar_mano_obra

# Crear un Blueprint para las rutas de mano de obra
mano_obra_bp = Blueprint('mano_obra', __name__)

# Ruta para obtener todos los registros de mano de obra
@mano_obra_bp.route('/mano-obra', methods=['GET'])
def obtener_toda_mano_obra():
    try:
        data = obtener_mano_obra()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener un registro de mano de obra por ID
@mano_obra_bp.route('/mano-obra/<int:id>', methods=['GET'])
def obtener_mano_obra_por_id_route(id):
    try:
        data = obtener_mano_obra_por_id(id)
        if data:
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Registro no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo registro de mano de obra
@mano_obra_bp.route('/mano-obra', methods=['POST'])
def crear_mano_obra_route():
    try:
        data = request.get_json()
        nombre_empleado = data.get('nombre_empleado')
        costo_por_hora = data.get('costo_por_hora')
        producto_id = data.get('producto_id')
        horas_requeridas = data.get('horas_requeridas')
        
        if not nombre_empleado or not costo_por_hora or not producto_id or not horas_requeridas:
            return jsonify({'error': 'Faltan datos'}), 400
        
        nuevo_registro = crear_mano_obra(nombre_empleado, costo_por_hora, producto_id, horas_requeridas)
        return jsonify(nuevo_registro), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar un registro de mano de obra
@mano_obra_bp.route('/mano-obra/<int:id>', methods=['PUT'])
def actualizar_mano_obra_route(id):
    try:
        data = request.get_json()
        nombre_empleado = data.get('nombre_empleado')
        costo_por_hora = data.get('costo_por_hora')
        producto_id = data.get('producto_id')
        horas_requeridas = data.get('horas_requeridas')
        
        actualizado = actualizar_mano_obra(id, nombre_empleado, costo_por_hora, producto_id, horas_requeridas)
        return jsonify(actualizado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un registro de mano de obra
@mano_obra_bp.route('/mano-obra/<int:id>', methods=['DELETE'])
def eliminar_mano_obra_route(id):
    try:
        result = eliminar_mano_obra(id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify

# Crear un Blueprint para las rutas de costos
costos_bp = Blueprint('costos', __name__)

# Ruta para calcular costos (ejemplo básico)
@costos_bp.route('/calcular', methods=['POST'])
def calcular_costos():
    try:
        data = request.get_json()
        if not data or 'orden_id' not in data:
            return jsonify({"error": "El campo 'orden_id' es obligatorio"}), 400
        
        # Simulamos una respuesta con los costos (ajusta con tu lógica)
        orden_id = data['orden_id']
        costos = {
            "orden_id": orden_id,
            "total_costos_directos": 500,
            "total_costos_indirectos": 200,
            "costo_total": 700
        }
        return jsonify(costos), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

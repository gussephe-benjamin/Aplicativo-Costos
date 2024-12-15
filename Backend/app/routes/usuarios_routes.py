from flask import Blueprint, request, jsonify
from models.usuarios import registrar_usuario, obtener_usuario_por_email, generar_token, verificar_token

usuarios_bp = Blueprint('usuarios', __name__)

# Ruta para registrar un nuevo usuario
@usuarios_bp.route('/registro', methods=['POST'])
def registro_usuario():
    data = request.get_json()
    nombre = data['nombre']
    email = data['email']
    contraseña = data['contraseña']
    rol = data['rol']  # El rol debe ser 'cliente' o 'administrador'

    if obtener_usuario_por_email(email):
        return jsonify({'message': 'El correo electrónico ya está registrado'}), 400

    registrar_usuario(nombre, email, contraseña, rol)
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

# Ruta para hacer login
@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data['email']
    contraseña = data['contraseña']

    # Obtener usuario por email
    usuario = obtener_usuario_por_email(email)
    print(usuario)

    if not usuario:
        return jsonify({'message': 'Credenciales incorrectas'}), 401

    # Convertir ambas contraseñas a cadena antes de comparar
    print(str(usuario['contraseña']), str(contraseña))  # Para depuración
    if str(usuario['contraseña']) != str(contraseña):
        return jsonify({'message': 'Credenciales incorrectas'}), 401

    # Generar y devolver el token
    token = generar_token(usuario)
    return jsonify({'token': token}), 200

# Ruta para verificar el rol del usuario (middleware)
@usuarios_bp.route('/rol', methods=['GET'])
def verificar_rol():
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token no proporcionado'}), 401

    decoded = verificar_token(token)
    if not decoded:
        return jsonify({'message': 'Token inválido o expirado'}), 401

    return jsonify({'rol': decoded['rol']}), 200

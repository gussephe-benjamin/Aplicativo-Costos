from flask import Flask
from routes import costos_routes
from routes import usuarios_routes, productos_routes, materia_prima_routes, mano_obra_routes, costos_indirectos_routes, ordenes_pedido_routes, costos_routes
from config import Config
from init_db import inicializar_datos
from flask_cors import CORS
import os

# Inicializamos los datos si no existe el archivo

app = Flask(__name__)

CORS(app)  # Permite solicitudes desde cualquier origen

# Si deseas restringir los orígenes, usa:
# CORS(app, origins=["http://localhost:5173"])

# Configuración de la aplicación
app.config['EXCEL_FILE'] = Config.EXCEL_FILE
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

# Registramos las rutas de la aplicación
app.register_blueprint(usuarios_routes.usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(productos_routes.productos_bp, url_prefix='/productos')
app.register_blueprint(materia_prima_routes.materia_prima_bp, url_prefix='/materia-prima')
app.register_blueprint(mano_obra_routes.mano_obra_bp, url_prefix='/mano-obra')
app.register_blueprint(costos_indirectos_routes.costos_indirectos_bp, url_prefix='/costos-indirectos')
app.register_blueprint(ordenes_pedido_routes.ordenes_pedido_bp, url_prefix='/ordenes-pedido')
app.register_blueprint(costos_routes.costos_bp, url_prefix='/costos')

if __name__ == '__main__':
    
    # Iniciar la aplicación
    app.run(host = '0.0.0.0', port = 5000, debug=True)

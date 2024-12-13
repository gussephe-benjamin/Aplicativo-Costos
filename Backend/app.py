from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Nombre del archivo Excel
EXCEL_FILE = 'data.xlsx'

# Función para verificar si existe el archivo y, si no, crearlo
def ensure_excel_exists():
    if not os.path.exists(EXCEL_FILE):
        # Crear un archivo con columnas básicas
        df = pd.DataFrame(columns=["ID", "Nombre", "Edad"])
        df.to_excel(EXCEL_FILE, index=False)

# Función auxiliar para leer el archivo Excel
def read_excel():
    ensure_excel_exists()
    return pd.read_excel(EXCEL_FILE)

# Función auxiliar para escribir en el archivo Excel
def write_excel(dataframe):
    dataframe.to_excel(EXCEL_FILE, index=False)

# Endpoint para obtener todos los datos
@app.route('/data', methods=['GET'])
def get_data():
    df = read_excel()
    return jsonify(df.to_dict(orient='records'))

# Endpoint para agregar un nuevo registro
@app.route('/data', methods=['POST'])
def add_data():
    new_record = request.json  # JSON recibido en la solicitud
    df = read_excel()
    
    # Verificar si el ID ya existe
    if int(new_record['ID']) in df['ID'].values:
        return jsonify({"message": "ID ya existente"}), 400

    # Agregar el nuevo registro
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    write_excel(df)
    return jsonify({"message": "Registro agregado exitosamente"}), 201

# Endpoint para actualizar un registro por ID
@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    updated_record = request.json
    df = read_excel()

    # Verificar si el ID existe
    if id not in df['ID'].values:
        return jsonify({"message": "Registro no encontrado"}), 404

    # Actualizar el registro
    df.loc[df['ID'] == id, updated_record.keys()] = updated_record.values()
    write_excel(df)
    return jsonify({"message": "Registro actualizado exitosamente"}), 200

# Endpoint para eliminar un registro por ID
@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    df = read_excel()

    # Verificar si el ID existe
    if id not in df['ID'].values:
        return jsonify({"message": "Registro no encontrado"}), 404

    # Eliminar el registro
    df = df[df['ID'] != id]
    write_excel(df)
    return jsonify({"message": "Registro eliminado exitosamente"}), 200

if __name__ == '__main__':
    # Asegurarse de que el archivo Excel existe al iniciar el servidor
    ensure_excel_exists()
    app.run(debug=True)

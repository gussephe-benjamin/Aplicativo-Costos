import pandas as pd
from config import Config

# Variables globales
EXCEL_FILE = Config.EXCEL_FILE
SHEET_NAME = "costos_indirectos"

# Función para cargar la hoja "costos_indirectos"
def leer_costos_indirectos():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    except Exception as e:
        print(f"Error al leer la hoja '{SHEET_NAME}': {e}")
        return pd.DataFrame(columns=['id', 'tipo', 'monto', 'descripcion'])

# Función para guardar los datos actualizados
def guardar_costos_indirectos(df):
    try:
        with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    except Exception as e:
        print(f"Error al guardar datos en '{SHEET_NAME}': {e}")

# Función para obtener todos los registros
def obtener_costos_indirectos():
    df = leer_costos_indirectos()
    return df.to_dict(orient='records')

# Función para obtener un registro por ID
def obtener_costos_indirectos_por_id(id):
    df = leer_costos_indirectos()
    record = df[df['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear un nuevo registro
def crear_costos_indirectos(tipo, monto, descripcion):
    df = leer_costos_indirectos()
    nuevo_id = int(df['id'].max() + 1) if not df.empty else 1  # ID único
    nuevo_registro = {
        'id': nuevo_id,
        'tipo': tipo,
        'monto': monto,
        'descripcion': descripcion
    }
    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    guardar_costos_indirectos(df)
    return nuevo_registro

# Función para actualizar un registro
def actualizar_costos_indirectos(id, tipo=None, monto=None, descripcion=None):
    df = leer_costos_indirectos()
    index = df[df['id'] == id].index
    if not index.empty:
        if tipo:
            df.at[index[0], 'tipo'] = tipo
        if monto is not None:
            df.at[index[0], 'monto'] = monto
        if descripcion:
            df.at[index[0], 'descripcion'] = descripcion
        guardar_costos_indirectos(df)
        return df.loc[index[0]].to_dict()
    return {"error": "Registro no encontrado"}

# Función para eliminar un registro
def eliminar_costos_indirectos(id):
    df = leer_costos_indirectos()
    if id not in df['id'].values:
        return {"error": "Registro no encontrado"}
    df = df[df['id'] != id]
    guardar_costos_indirectos(df)
    return {"success": "Registro eliminado exitosamente"}

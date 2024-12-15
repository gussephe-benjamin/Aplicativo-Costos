import pandas as pd
from config import Config

# Variables globales para el archivo y la hoja de trabajo
EXCEL_FILE = Config.EXCEL_FILE  # Ruta del archivo Excel
SHEET_NAME = "mano_obra"  # Nombre de la hoja

# Función para cargar la hoja "mano_obra" desde el archivo Excel
def leer_mano_obra():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    except Exception as e:
        print(f"Error al leer la hoja '{SHEET_NAME}': {e}")
        return pd.DataFrame(columns=['id', 'nombre_empleado', 'costo_por_hora', 'producto_id', 'horas_requeridas', 'fecha_agregado'])

# Función para guardar los datos actualizados en el Excel
def guardar_mano_obra(df):
    try:
        with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    except Exception as e:
        print(f"Error al guardar los datos en '{SHEET_NAME}': {e}")

# Función para obtener todos los registros
def obtener_mano_obra():
    df = leer_mano_obra()
    return df.to_dict(orient='records')

# Función para obtener un registro por ID
def obtener_mano_obra_por_id(id):
    df = leer_mano_obra()
    record = df[df['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear un nuevo registro
def crear_mano_obra(nombre_empleado, costo_por_hora, producto_id, horas_requeridas):
    df = leer_mano_obra()
    nuevo_id = int(df['id'].max() + 1) if not df.empty else 1  # ID único
    nuevo_registro = {
        'id': nuevo_id,
        'nombre_empleado': nombre_empleado,
        'costo_por_hora': costo_por_hora,
        'producto_id': producto_id,
        'horas_requeridas': horas_requeridas,
        'fecha_agregado': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    guardar_mano_obra(df)
    return nuevo_registro

# Función para actualizar un registro
def actualizar_mano_obra(id, nombre_empleado=None, costo_por_hora=None, producto_id=None, horas_requeridas=None):
    df = leer_mano_obra()
    index = df[df['id'] == id].index
    if not index.empty:
        if nombre_empleado:
            df.at[index[0], 'nombre_empleado'] = nombre_empleado
        if costo_por_hora:
            df.at[index[0], 'costo_por_hora'] = costo_por_hora
        if producto_id:
            df.at[index[0], 'producto_id'] = producto_id
        if horas_requeridas:
            df.at[index[0], 'horas_requeridas'] = horas_requeridas
        guardar_mano_obra(df)
        return df.loc[index[0]].to_dict()
    return {"error": "Registro no encontrado"}

# Función para eliminar un registro
def eliminar_mano_obra(id):
    df = leer_mano_obra()
    if id not in df['id'].values:
        return {"error": "Registro no encontrado"}
    df = df[df['id'] != id]
    guardar_mano_obra(df)
    return {"success": "Registro eliminado exitosamente"}

# Función para obtener registros asociados a un producto
def obtener_mano_obra_por_producto(producto_id):
    df = leer_mano_obra()
    mano_obra = df[df['producto_id'] == producto_id]
    return mano_obra.to_dict(orient='records')

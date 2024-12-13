import pandas as pd
from config import Config

# Cargar el archivo de Excel y la hoja de Costos Indirectos
df_costos_indirectos = pd.read_excel(Config.EXCEL_FILE, sheet_name="costos_indirectos")

# Función para obtener todos los registros de costos indirectos
def obtener_costos_indirectos():
    return df_costos_indirectos.to_dict(orient='records')

# Función para obtener un registro de costos indirectos por id
def obtener_costos_indirectos_por_id(id):
    record = df_costos_indirectos[df_costos_indirectos['id'] == id]
    if not record.empty:
        return record.iloc[0].to_dict()
    return None

# Función para crear un nuevo registro de costos indirectos
def crear_costos_indirectos(tipo, monto, descripcion):
    nuevo_id = df_costos_indirectos['id'].max() + 1  # Genera un nuevo ID único
    nuevo_registro = {
        'id': nuevo_id,
        'tipo': tipo,
        'monto': monto,
        'descripcion': descripcion
    }
    df_costos_indirectos = df_costos_indirectos.append(nuevo_registro, ignore_index=True)
    df_costos_indirectos.to_excel(Config.EXCEL_FILE, sheet_name='costos_indirectos', index=False)
    return nuevo_registro

# Función para actualizar un registro de costos indirectos
def actualizar_costos_indirectos(id, tipo=None, monto=None, descripcion=None):
    index = df_costos_indirectos[df_costos_indirectos['id'] == id].index[0]
    
    if tipo:
        df_costos_indirectos.at[index, 'tipo'] = tipo
    if monto is not None:
        df_costos_indirectos.at[index, 'monto'] = monto
    if descripcion:
        df_costos_indirectos.at[index, 'descripcion'] = descripcion
    
    df_costos_indirectos.to_excel(Config.EXCEL_FILE, sheet_name='costos_indirectos', index=False)
    return df_costos_indirectos.iloc[index].to_dict()

# Función para eliminar un registro de costos indirectos
def eliminar_costos_indirectos(id):
    global df_costos_indirectos
    df_costos_indirectos = df_costos_indirectos[df_costos_indirectos['id'] != id]
    df_costos_indirectos.to_excel(Config.EXCEL_FILE, sheet_name='costos_indirectos', index=False)
    return {'mensaje': 'Registro eliminado exitosamente'}

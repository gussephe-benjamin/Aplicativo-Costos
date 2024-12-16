import pandas as pd
import jwt
import datetime
from config import Config  # Importamos Config para acceder a la configuración


# Archivo Excel donde se almacenan los usuarios
EXCEL_FILE = Config.EXCEL_FILE  # Usamos la ruta del archivo desde el archivo de configuración
SHEET_NAME = "usuarios"  # Nombre de la hoja donde están los usuarios

# Clave secreta para generar y verificar los JWTs
SECRET_KEY = Config.JWT_SECRET_KEY  # Usamos la clave secreta para JWT desde la configuración

def leer_usuarios():
    """Leer todos los usuarios desde el archivo Excel y devolverlos como una lista de diccionarios"""
    try:
        # Leer usuarios desde Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        print("Usuarios leídos correctamente:", df.to_dict(orient='records'))
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print("Archivo no encontrado. Creando estructura vacía.")
        return []
    except Exception as e:
        print(f"Error al leer usuarios: {e}")
        return []

def guardar_usuarios(df):
    """Guardar los usuarios actualizados en la hoja correspondiente del archivo Excel"""
    try:
        with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
        print("Usuarios guardados correctamente.")
    except FileNotFoundError:
        print("No se encontró el archivo. Creando uno nuevo...")
        df.to_excel(EXCEL_FILE, sheet_name=SHEET_NAME, index=False)
    except Exception as e:
        print(f"Error al guardar usuarios: {e}")

def registrar_usuario(nombre, email, contraseña, rol="usuario"):
    """Registrar un nuevo usuario en la hoja de Excel"""
    try:
        try:
            df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['id', 'nombre', 'email', 'contraseña', 'rol', 'fecha_registro'])

        if 'email' not in df.columns:
            raise KeyError("La columna 'email' no existe en la hoja de Excel.")

        # Verificar duplicados
        if email in df['email'].values:
            return {"error": "El usuario ya existe."}

        nuevo_usuario = {
            'id': len(df) + 1 if not df.empty else 1,
            'nombre': nombre,
            'email': email,
            'contraseña': contraseña,
            'rol': rol,
            'fecha_registro': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Agregar al DataFrame
        df = pd.concat([df, pd.DataFrame([nuevo_usuario])], ignore_index=True)

        # Guardar usuarios
        guardar_usuarios(df)
        return {"success": "Usuario registrado exitosamente"}

    except KeyError as e:
        print(f"Error: {e}")
        return {"error": f"Faltan columnas necesarias: {e}"}
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return {"error": "Hubo un error al registrar el usuario"}


def obtener_usuario_por_email(email):
    """Obtener un usuario por su email desde la hoja de Excel"""
    try:
        # Leer los usuarios desde la hoja de Excel
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        usuario = df[df['email'] == email]
       
        if not usuario.empty:
            return usuario.iloc[0].to_dict()  # Devuelve el primer usuario que coincida
        return None
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
        return None

def generar_token(usuario):
    """Generar un token JWT para un usuario"""
    payload = {
        'id': usuario['id'],
        'nombre': usuario['nombre'],
        'email': usuario['email'],
        'rol': usuario['rol'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expira en 24 horas
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verificar_token(token):
    """Verificar un token JWT"""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "El token ha expirado"}
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}

def verificar_credenciales(email, contraseña):
    """Verificar si las credenciales del usuario son correctas"""
    usuario = obtener_usuario_por_email(email)
    if usuario and usuario['contraseña'] == contraseña:
        return usuario
    return None

def obtener_usuario_por_id(usuario_id):
    """Obtener un usuario por su ID desde la hoja de Excel"""
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

        if 'id' not in df.columns:
            raise KeyError("La columna 'id' no existe en la hoja de Excel.")

        df['id'] = df['id'].astype(int)
        usuario = df[df['id'] == usuario_id]

        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        else:
            print("Usuario no encontrado.")
            return None

    except KeyError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
        return None

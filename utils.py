import json
from datetime import datetime

def load_json(route):
    """
    Carga datos desde un archivo JSON ubicado en la ruta especificada.

    Args:
        route (str): Ruta del archivo JSON.

    Retorna:
        list | dict: Contenido del archivo JSON si existe; una lista vacía si el archivo no se encuentra.

    Lanza:
        json.JSONDecodeError: Si el contenido del archivo no es un JSON válido.
    """
    try:
        with open(route, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(route, data):
    """
    Guarda datos en formato JSON en la ruta especificada.

    Args:
        route (str): Ruta donde se desea guardar el archivo.
        data (list | dict): Datos que se desean guardar en formato JSON.
    """
    with open(route, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_record(user, action):
    """
    Registra una acción realizada por un usuario en un archivo de bitácora.

    Args:
        user (str): Identificador o nombre del usuario que realizó la acción.
        action (str): Descripción de la acción realizada.

    Proceso:
        - Genera una marca de tiempo con fecha y hora actual.
        - Escribe una línea en el archivo 'bitacora.txt' registrando la acción del usuario.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("bitacora.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] Usuario {user} realizó {action}\n")

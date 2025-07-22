import json
import os
import re
from usuario_dto import User

USERS_FILE = "Docs/users.json"

VALID_TYPES = {"fisica", "juridica", "dimex", "pasaporte"}
VALID_ROLES = {"administrador", "asistente"}

def load_users():
    """
    Carga los datos de usuarios desde un archivo JSON.

    Retorna:
        list: Lista de usuarios si el archivo existe; de lo contrario, una lista vacía.

    Lanza:
        json.JSONDecodeError: Si el contenido del archivo no es un JSON válido.
    """
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    """
    Guarda la lista de usuarios en un archivo JSON.

    Args:
        users (list): Lista de usuarios que se desea guardar.
    """
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def input_validated(prompt, validate_fn, error_msg):
    while True:
        value = input(prompt)
        if validate_fn(value):
            return value
        print(f"❌ {error_msg}")

def validate_id_number(id_type, id_number):
    """
    Solicita al usuario una entrada que será validada mediante una función dada.

    Args:
        prompt (str): Texto que se muestra al usuario para solicitar la entrada.
        validate_fn (Callable): Función que valida el valor ingresado. Debe retornar True si es válido.
        error_msg (str): Mensaje de error que se muestra cuando la validación falla.

    Retorna:
        str: El valor ingresado que pasó la validación.
    """
    if id_type == "fisica":
        return id_number.isdigit() and len(id_number) == 9 and 1 <= int(id_number[0]) <= 7
    elif id_type == "dimex":
        return id_number.isdigit() and len(id_number) in [11, 12]
    elif id_type == "pasaporte":
        return re.match(r"^[A-Za-z0-9]{6,12}$", id_number) is not None
    elif id_type == "juridica":
        return id_number.isdigit() and len(id_number) == 10
    return False

def create_user():
    """
    Registra un nuevo usuario en el sistema, validando todos los datos proporcionados.

    Proceso:
        - Solicita el tipo y número de identificación, verificando su validez según el formato correspondiente.
        - Comprueba que no exista un usuario con la misma identificación.
        - Solicita y valida los demás datos del usuario: nombre completo, correo electrónico, contraseña y rol.
        - Crea una instancia de `User` y guarda el nuevo usuario en el archivo correspondiente.

    Muestra:
        - Mensajes de error si los datos son inválidos o si el usuario ya existe.
        - Confirmación si el usuario fue creado correctamente.

    Requiere:
        - Las funciones auxiliares `input_validated`, `validate_id_number`, `load_users`, `save_users`.
        - La clase `User` y las constantes `VALID_TYPES` y `VALID_ROLES`.
    """
    id_type = input_validated(
        "Tipo de identificación (fisica/juridica/dimex/pasaporte): ",
        lambda x: x.lower() in VALID_TYPES,
        "Tipo inválido. Debe ser: fisica, juridica, dimex o pasaporte."
    )
    id_user = input_validated(
        "Número de identificación: ",
        lambda x: validate_id_number(id_type, x),
        "Número de identificación inválido para el tipo seleccionado."
    )

    users = load_users()
    if any(u["id_user"] == id_user for u in users):
        print("❌ Ya existe un usuario con esa identificación.")
        return

    name_user = input_validated(
        "Nombre completo: ",
        lambda x: x.replace(" ", "").isalpha() and len(x.strip()) > 3,
        "El nombre debe tener más de 3 letras y no contener números."
    )
    email = input_validated(
        "Correo electrónico: ",
        lambda x: re.match(r"^[\w.-]+@[\w.-]+\.\w+$", x),
        "Correo inválido. Debe tener formato nombre@dominio.com"
    )
    password = input_validated(
        "Contraseña (8-12 caracteres): ",
        lambda x: 8 <= len(x) <= 12,
        "Contraseña inválida. Debe tener entre 8 y 12 caracteres."
    )
    rol = input_validated(
        "Rol (administrador/asistente): ",
        lambda x: x.lower() in VALID_ROLES,
        "Rol inválido. Debe ser: administrador, asistente o cliente."
    )



    new_user = User(id_type, id_user, name_user, email, password, rol)
    users.append(new_user.to_dict())
    save_users(users)
    print("✅ Usuario creado correctamente.")

def list_users():
    """
    Muestra en consola la lista de todos los usuarios registrados.

    Proceso:
        - Carga los usuarios desde el archivo correspondiente.
        - Verifica si existen registros.
        - Si los hay, imprime para cada usuario su identificación, nombre y rol.

    Muestra:
        - Un mensaje si no hay usuarios registrados.
        - El listado formateado de usuarios en caso contrario.
    """
    users = load_users()
    if not users:
        print("No hay usuarios registrados.")
        return
    for u in users:
        print(f"{u['id_user']} - {u['name_user']} ({u['rol']})")

def edit_user():
    """
    Permite modificar los datos de un usuario existente en el sistema.

    Proceso:
        - Solicita el ID del usuario que se desea editar.
        - Busca el usuario correspondiente en la lista cargada.
        - Si se encuentra, permite actualizar nombre, correo y contraseña, conservando los valores actuales si no se ingresan nuevos.
        - Valida los datos modificados antes de guardarlos.
        - Guarda los cambios en el archivo de usuarios.

    Muestra:
        - Mensajes de error si los nuevos datos son inválidos o si el usuario no fue encontrado.
        - Mensaje de confirmación si el usuario fue actualizado correctamente.
    """
    users = load_users()
    id_user = input("Ingrese el ID del usuario que desea modificar: ")
    for u in users:
        if u["id_user"] == id_user:
            print(f"Editando usuario: {u['name_user']}")
            new_name_user = input(f"Nuevo nombre [{u['name_user']}]: ") or u["name_user"]
            new_email = input(f"Nuevo correo [{u['email']}]: ") or u["email"]
            new_password = input(f"Nueva contraseña (8-12 caracteres) [{u['password']}]: ") or u["password"]

            if not new_name_user.replace(" ", "").isalpha() or len(new_name_user.strip()) <= 3:
                print("❌ Nombre inválido.")
                return
            if not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", new_email):
                print("❌ Correo inválido.")
                return
            if len(new_password) < 8 or len(new_password) > 12:
                print("❌ Contraseña inválida.")
                return

            u["name_user"] = new_name_user
            u["email"] = new_email
            u["password"] = new_password
            save_users(users)
            print("✅ Usuario actualizado.")
            return
    print("❌ Usuario no encontrado.")

def delete_user():
    """
    Elimina un usuario del sistema a partir de su número de identificación.

    Proceso:
        - Solicita al usuario el ID del usuario que desea eliminar.
        - Filtra la lista de usuarios para excluir al que coincide con el ID.
        - Si no hay cambios en la lista, significa que no se encontró el usuario.
        - Si se elimina, guarda la nueva lista en el archivo.

    Muestra:
        - Mensaje de éxito si el usuario fue eliminado.
        - Mensaje de error si no se encontró un usuario con el ID proporcionado.
    """
    users = load_users()
    id_user = input("Ingrese el ID del usuario que desea eliminar: ")
    news = [u for u in users if u["id_user"] != id_user]
    if len(news) == len(users):
        print("❌ Usuario no encontrado.")
    else:
        save_users(news)
        print("🗑️ Usuario eliminado correctamente.")

def menu_users():
    while True:
        print("\n=== Gestión de Usuarios ===")
        print("1. Crear nuevo usuario")
        print("2. Listar usuarios")
        print("3. Editar usuario")
        print("4. Eliminar usuario")
        print("5. Volver al menú principal")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            edit_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")
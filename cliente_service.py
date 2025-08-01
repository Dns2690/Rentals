import json
import os
import re
from cliente_dto import Cliente

CLIENTS_FILE = "Docs/clients.json"

VALID_TYPES = {"1":"fisica",
               "2":"juridica",
               "3":"dimex",
               "4":"pasaporte"}


def load_clients():
    """
    Carga los datos de clientes desde un archivo JSON.

    Retorna:
        list: Una lista con los datos de los clientes si el archivo existe; de lo contrario, una lista vacía.

    Lanza:
        json.JSONDecodeError: Si el archivo contiene un JSON inválido.
    """
    if not os.path.exists(CLIENTS_FILE):
        return []
    with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_clients(clients):
    """
    Guarda la lista de clientes en un archivo JSON.

    Args:
        clients (list): Lista de clientes que se desea guardar.
    """
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2)

def input_validated(prompt, validate_fn, error_msg):
    """
    Solicita al usuario una entrada que será validada mediante una función proporcionada.

    Args:
        prompt (str): Mensaje mostrado al usuario.
        validate_fn (Callable): Función que valida la entrada. Debe devolver True si es válida.
        error_msg (str): Mensaje de error que se muestra si la validación falla.

    Retorna:
        str: Entrada válida proporcionada por el usuario.
    """
    while True:
        value = input(prompt)
        if validate_fn(value):
            return value
        print(f"❌ {error_msg}")

def validate_id_number(id_type, id_number):
    """
    Valida un número de identificación según su tipo.

    Args:
        id_type (str): Tipo de identificación. Puede ser "fisica", "dimex", "pasaporte" o "juridica".
        id_number (str): Número de identificación a validar.

    Retorna:
        bool: True si el número es válido según el tipo especificado; False en caso contrario.

    Validaciones:
        - "fisica": 9 dígitos numéricos, empezando con un dígito entre 1 y 7.
        - "dimex": 11 o 12 dígitos numéricos.
        - "pasaporte": Entre 6 y 12 caracteres alfanuméricos.
        - "juridica": 10 dígitos numéricos.
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

def create_client():
    """
    Registra un nuevo cliente en el sistema, validando todos los datos ingresados.

    Proceso:
        - Solicita el tipo y número de identificación, validándolos según el formato correspondiente.
        - Verifica que no exista un cliente previamente registrado con la misma identificación.
        - Solicita y valida los datos personales del cliente: nombre, correo, contraseña, profesión, dirección y dirección del trabajo.
        - Crea una instancia de Cliente y la guarda en el archivo de clientes.

    Muestra:
        Mensajes informativos sobre errores de validación o confirmación del registro exitoso.

    Requiere:
        La clase `Cliente` y las funciones auxiliares `input_validated`, `validate_id_number`, `load_clients` y `save_clients`.
    """
    id_type = input_validated(
        "Tipo de identificación (1.fisica/2.juridica/3.dimex/4.pasaporte): ",
        lambda x: x in VALID_TYPES.keys(),
        "Opción inválida. Debe ser 1, 2, 3 o 4."
    )
    id_user = input_validated(
        "Número de identificación: ",
        lambda x: validate_id_number(VALID_TYPES[id_type], x),
        "Número de identificación inválido para el tipo seleccionado."
    )

    clients = load_clients()
    if any(c["id_user"] == id_user for c in clients):
        print("❌ Ya existe un cliente con esa identificación.")
        return

    name = input_validated(
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
    profession = input_validated(
        "Profesión: ",
        lambda x: x.replace(" ", "").isalpha() and len(x.strip()) > 3,
        "La profeción debe tener más de 3 letras y no contener números."
    )
    address = input_validated(
        "Dirección: ",
        lambda x: x.replace(" ", "").isalpha() and len(x.strip()) > 3,
        "La dirección debe tener más de 3 letras y no contener números."
    )
    job = input_validated(
        "Dirección trabajo: ",
        lambda x: x.replace(" ", "").isalpha() and len(x.strip()) > 3,
        "La dirección del trabajo debe tener más de 3 letras y no contener números."
    )

    new_client = Cliente(VALID_TYPES[id_type], id_user, name, email, password, profession, address, job)
    clients.append(new_client.to_dict())
    save_clients(clients)
    print("✅ Cliente creado correctamente.")

def list_clients():
    """
    Muestra en consola la lista de todos los clientes registrados.

    Proceso:
        - Carga los clientes desde el archivo correspondiente.
        - Verifica si existen registros.
        - Si hay clientes, imprime sus datos: identificación, nombre, profesión y correo electrónico.

    Muestra:
        Un mensaje si no hay clientes registrados, o el listado formateado de cada cliente.
    """
    clients = load_clients()
    if not clients:
        print("No hay cliente registrados.")
        return
    for c in clients:
        print(f"{c['id_user']} - {c['name_user']} | {c['profession']} | {c['email']}")

def edit_client():
    """
    Permite editar los datos de un cliente existente en el sistema.

    Proceso:
        - Solicita al usuario el ID del cliente que se desea modificar.
        - Busca el cliente en la lista cargada desde el archivo.
        - Si se encuentra, permite actualizar nombre, correo, contraseña, profesión, dirección y trabajo.
          Si el usuario no ingresa un nuevo valor, se mantiene el actual.
        - Guarda los cambios en el archivo.

    Muestra:
        - Mensaje de confirmación si el cliente fue actualizado exitosamente.
        - Mensaje de error si no se encuentra el cliente.
    """
    clients = load_clients()
    id_user = input("Ingrese el ID del cliente que desea modificar: ")
    for c in clients:
        if c["id_user"] == id_user:
            print(f"Editando cliente: {c['name_user']}")
            c["name_user"] = input(f"Nuevo nombre [{c['name_user']}]: ") or c["name_user"]
            c["email"] = input(f"Nuevo correo [{c['email']}]: ") or c["email"]
            c["user"] = c["email"]
            c["password"] = input(f"Nueva contraseña [{c['password']}]: ") or c["password"]
            c["profession"] = input(f"Nueva profesión [{c['profession']}]: ") or c["profession"]
            c["address"] = input(f"Nueva dirección [{c['address']}]: ") or c["address"]
            c["job"] = input(f"Nuevo trabajo [{c['job']}]: ") or c["job"]
            save_clients(clients)
            print("✅ Cliente actualizado.")
            return
    print("❌ Cliente no encontrado.")

def delete_client():
    """
    Elimina un cliente del sistema a partir de su ID.

    Proceso:
        - Solicita al usuario el ID del cliente que se desea eliminar.
        - Filtra la lista de clientes excluyendo al que tenga el ID indicado.
        - Si no se encuentra coincidencia, informa que el cliente no fue hallado.
        - Si se encuentra y elimina, guarda la lista actualizada en el archivo.

    Muestra:
        - Mensaje de éxito si el cliente fue eliminado.
        - Mensaje de error si no se encontró un cliente con el ID proporcionado.
    """
    clients = load_clients()
    id_user = input("Ingrese el ID del usuario que desea eliminar: ")
    new_list = [c for c in clients if c["id_user"] != id_user]
    if len(new_list) == len(clients):
        print("❌ Cliente no encontrado.")
    else:
        save_clients(new_list)
        print("🗑️ Usuario eliminado correctamente.")

def view_own_client(logged_user):
    print("\n=== Mi Perfil ===")
    print(f"Cédula: {logged_user['id_user']}")
    print(f"Nombre: {logged_user['name_user']}")
    print(f"Correo: {logged_user['email']}")
    print(f"Profesión: {logged_user['profession']}")
    print(f"Dirección: {logged_user['address']}")
    print(f"Trabajo: {logged_user['job']}")

def edit_own_client(logged_user):
    clients = load_clients()
    for c in clients:
        if c["id_user"] == logged_user["id_user"]:
            print("Editando tu perfil:")
            c["name_user"] = input(f"Nuevo nombre [{c['name_user']}]: ") or c["name_user"]
            c["email"] = input(f"Nuevo correo [{c['email']}]: ") or c["email"]
            c["password"] = input(f"Nueva contraseña [{c['password']}]: ") or c["password"]
            c["profession"] = input(f"Nueva profesión [{c['profession']}]: ") or c["profession"]
            c["address"] = input(f"Nueva dirección [{c['address']}]: ") or c["address"]
            c["job"] = input(f"Nuevo trabajo [{c['job']}]: ") or c["job"]
            save_clients(clients)
            print("✅ Perfil actualizado.")
            return
    print("❌ No se encontró tu perfil.")

def menu_clients(logged_user):
    while True:
        print("\n=== Gestión de Clientes ===")
        if logged_user["rol"] == "cliente":
            print("1. Ver mi perfil")
            print("2. Editar mi perfil")
            print("3. Volver al menú principal")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                view_own_client(logged_user)
            elif choice == "2":
                edit_own_client(logged_user)
            elif choice == "3":
                break
            else:
                print("❌ Opción inválida.")
        else:
            print("1. Crear cliente")
            print("2. Listar clientes")
            print("3. Editar cliente")
            print("4. Eliminar cliente")
            print("5. Volver al menú principal")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                create_client()
            elif choice == "2":
                list_clients()
            elif choice == "3":
                edit_client()
            elif choice == "4":
                delete_client()
            elif choice == "5":
                break
            else:
                print("❌ Opción inválida.")
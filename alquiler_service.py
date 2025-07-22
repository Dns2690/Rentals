import json
import os
from datetime import datetime
from alquiler_dto import Rental
from vehiculo_service import list_vehicles, save_vehicles

RENTALS_FILE = "Docs/rentals.json"
VEHICLES_FILE = "Docs/vehicles.json"

def load_rentals():
    """
    Carga los registros de alquiler desde un archivo JSON.

    Retorna:
        list: Una lista con los registros de alquiler si el archivo existe; de lo contrario, una lista vacía.

    Lanza:
        json.JSONDecodeError: Si el archivo existe pero contiene un JSON inválido.
    """
    if not os.path.exists(RENTALS_FILE):
        return []
    with open(RENTALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_rentals(rentals):
    """
    Guarda los registros de alquiler en un archivo JSON.

    Args:
        rentals (list): Lista de registros de alquiler que se desea guardar.
    """
    with open(RENTALS_FILE, "w", encoding="utf-8") as f:
        json.dump(rentals, f, indent=2)

def load_vehicles():
    """
    Carga los datos de vehículos desde un archivo JSON.

    Retorna:
        list: Una lista con los datos de vehículos si el archivo existe; de lo contrario, una lista vacía.

    Lanza:
        json.JSONDecodeError: Si el archivo existe pero contiene un JSON inválido.
    """
    if not os.path.exists(VEHICLES_FILE):
        return []
    with open(VEHICLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def input_validated(prompt, validate_fn, error_msg):
    """
    Solicita al usuario una entrada validada mediante una función de validación.

    Args:
        prompt (str): Mensaje que se muestra al usuario para solicitar la entrada.
        validate_fn (Callable): Función que recibe la entrada y devuelve True si es válida.
        error_msg (str): Mensaje de error que se muestra si la validación falla.

    Retorna:
        str: El valor ingresado por el usuario que cumple con la validación.
    """
    while True:
        value = input(prompt)
        if validate_fn(value):
            return value
        print(f"{error_msg}")

def validate_date(date_str):
    """
    Valida que una cadena de texto tenga el formato de fecha 'YYYY-MM-DD'.

    Args:
        date_str (str): Cadena que representa una fecha.

    Retorna:
        bool: True si la cadena tiene el formato de fecha válido, False en caso contrario.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def validate_expiry(expiry_str):
    """
    Valida que una fecha de vencimiento esté en el formato 'MM-YYYY' y sea posterior a la fecha actual.

    Args:
        expiry_str (str): Cadena que representa una fecha de vencimiento.

    Retorna:
        bool: True si la fecha tiene el formato correcto y no está vencida; False en caso contrario.
    """
    try:
        exp = datetime.strptime(expiry_str, "%m-%Y")
        return exp > datetime.now()
    except:
        return False

def create_rental(logged_user):
    """
    Crea un nuevo registro de alquiler y actualiza el estado del vehículo a 'RENTADO'.

    Args:
        logged_user (dict): Diccionario con los datos del usuario actualmente autenticado.
                            Se utiliza para obtener el ID si el usuario tiene rol de cliente.

    Proceso:
        - Carga la lista de alquileres y vehículos desde sus archivos respectivos.
        - Solicita los datos necesarios para el alquiler, incluyendo validaciones.
        - Verifica que el vehículo exista y esté disponible.
        - Registra el alquiler y actualiza el estado del vehículo.
        - Guarda los cambios en los archivos correspondientes.

    Muestra:
        Mensajes informativos y de error al usuario en caso de datos inválidos o vehículo no disponible.
    """
    rentals = load_rentals()
    vehicles = load_vehicles()

    client_id = logged_user["id_user"] if logged_user["rol"] == "cliente" else input("Cédula del cliente: ")
    print("----Listado de vehículos----")
    list_vehicles()
    print("----------------------------")
    plate = input("Placa del vehículo: ")

    vehicle = next((v for v in vehicles if v["plate"] == plate), None)
    if not vehicle:
        print("❌ Vehículo no encontrado.")
        return

    if vehicle.get("state", "").upper() == "RENTADO":
        print(f"❌ El vehículo con placa {plate} no está disponible (estado: {vehicle['state']}).")
        return


    start_date = input_validated("Fecha de inicio (YYYY-MM-DD): ", validate_date, "❌ Fecha inválida.")
    end_date = input_validated("Fecha de devolución (YYYY-MM-DD): ", lambda x: validate_date(x) and x > start_date, "❌ Fecha inválida o anterior al inicio.")
    cost_day = int(input_validated("Costo por día: ", lambda x: x.isdigit() and int(x) > 0, "❌ Debe ser un número positivo."))
    card = input_validated("Número de tarjeta: ", lambda x: x.isdigit() and len(x) in [13, 16], "❌ Número de tarjeta inválido.")
    expiry = input_validated("Vencimiento (MM-AAAA): ", validate_expiry, "❌ Fecha de vencimiento inválida o pasada.")

    rental = Rental(plate, client_id, start_date, end_date, cost_day, card, expiry)
    rentals.append(rental.to_dict())
    save_rentals(rentals)
    vehicle["state"] = "RENTADO"
    save_vehicles(vehicles)
    print("✅ Alquiler registrado correctamente.")

def update_rental_status(from_status, to_status):
    """
    Actualiza el estado de un alquiler específico y, si corresponde, cambia el estado del vehículo a 'DISPONIBLE'.

    Args:
        from_status (str): Estado actual que debe tener el alquiler para ser actualizado.
        to_status (str): Nuevo estado que se asignará al alquiler.

    Proceso:
        - Solicita al usuario la placa del vehículo y la cédula del cliente.
        - Busca un alquiler que coincida con la placa, cédula y estado indicado.
        - Si lo encuentra, actualiza su estado.
        - Si el nuevo estado es 'DEVUELTO', también actualiza el estado del vehículo.
        - Guarda los cambios en los archivos correspondientes.

    Muestra:
        Mensajes indicando si la actualización fue exitosa o si el alquiler no fue encontrado o no estaba en el estado esperado.
    """
    rentals = load_rentals()
    vehicles = load_vehicles()
    plate = input("Placa del vehículo: ")
    client_id = input("Cédula del cliente: ")

    for r in rentals:
        if r["plate"] == plate and r["id_client"] == client_id and r["state"] == from_status:
            r["state"] = to_status
            save_rentals(rentals)
            if to_status == "DEVUELTO":
                vehicle = next((v for v in vehicles if v["plate"] == plate), None)
                vehicle["state"] = "DISPONIBLE"
                save_vehicles(vehicles)
            print(f"✅ Estado actualizado a {to_status}.")
            return
    print("❌ Alquiler no encontrado o no en estado correcto.")

def list_rentals(logged_user):
    """
    Muestra en consola la lista de alquileres registrados, filtrando según el rol del usuario.

    Args:
        logged_user (dict): Diccionario con los datos del usuario autenticado.
                            Si el usuario tiene rol de cliente, solo se muestran sus propios alquileres.

    Proceso:
        - Carga los alquileres desde el archivo.
        - Verifica si hay registros disponibles.
        - Si el usuario es cliente, filtra los alquileres que le pertenecen.
        - Muestra información básica de cada alquiler: placa, cliente, estado y fechas.

    Muestra:
        Mensajes informativos si no hay alquileres o si se listan correctamente.
    """
    rentals = load_rentals()
    if not rentals:
        print("No hay alquileres registrados.")
        return

    print("\n=== Lista de Alquileres ===")
    for r in rentals:
        # Filtrar si el usuario es cliente
        if logged_user["rol"] == "cliente" and r["id_client"] != logged_user["id_user"]:
            continue
        print(f"Vehículo: {r['plate']} | Cliente: {r['id_client']} | Estado: {r['state']} | Del {r['start_date']} al {r['end_date']}")

def menu_rentals(logged_user):
    """
    Despliega el menú de gestión de alquileres y dirige al usuario a la opción seleccionada según su rol.

    Args:
        logged_user (dict): Diccionario con los datos del usuario autenticado, incluyendo su rol.

    Proceso:
        - Muestra opciones distintas según si el usuario es cliente, asistente o administrador.
        - Permite registrar un nuevo alquiler, listar alquileres, cambiar el estado del vehículo al ser entregado o devuelto, o salir al menú principal.
        - Valida las opciones ingresadas y ejecuta la función correspondiente.

    Muestra:
        Mensajes con opciones disponibles y alertas ante selecciones inválidas.
    """
    while True:
        print("\n=== Gestión de Alquileres ===")
        print("1. Registrar nuevo alquiler")
        print("2. Ver mis alquileres" if logged_user["rol"] == "cliente" else "2. Ver todos los alquileres")

        if logged_user["rol"] in ["administrador", "asistente"]:
            print("3. Entregar vehículo (PREPARADO → ACTIVO)")
            print("4. Recibir vehículo (ACTIVO → DEVUELTO)")
            print("5. Volver al menú principal")
        else:
            print("3. Volver al menú principal")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            create_rental(logged_user)
        elif choice == "2":
            list_rentals(logged_user)
        elif choice == "3" and logged_user["rol"] in ["administrador", "asistente"]:
            update_rental_status("PREPARADO", "ACTIVO")
        elif choice == "4" and logged_user["rol"] in ["administrador", "asistente"]:
            update_rental_status("ACTIVO", "DEVUELTO")
        elif (choice == "3" and logged_user["rol"] == "cliente") or \
             (choice == "5" and logged_user["rol"] in ["administrador", "asistente"]):
            break
        else:
            print("❌ Opción inválida.")
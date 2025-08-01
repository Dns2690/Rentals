import json
import os
from vehiculo_dto import Vehicle

VEHICLES_FILE = "Docs/vehicles.json"

def load_vehicles():
    """
    Carga los datos de vehículos desde un archivo JSON.

    Retorna:
        list: Lista de vehículos si el archivo existe; de lo contrario, una lista vacía.

    Lanza:
        json.JSONDecodeError: Si el contenido del archivo no es un JSON válido.
    """
    if not os.path.exists(VEHICLES_FILE):
        return []
    with open(VEHICLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vehicles(vehicles):
    """
    Guarda la lista de vehículos en un archivo JSON.

    Args:
        vehicles (list): Lista de vehículos que se desea guardar.
    """
    with open(VEHICLES_FILE, "w", encoding='utf-8') as f:
        json.dump(vehicles, f, indent=2)

def input_validated(prompt, validate_fn, error_msg):
    """
    Solicita al usuario una entrada validada utilizando una función personalizada.

    Args:
        prompt (str): Texto mostrado al usuario para solicitar la entrada.
        validate_fn (Callable): Función que valida el valor ingresado y devuelve True si es válido.
        error_msg (str): Mensaje de error mostrado si la validación falla.

    Retorna:
        str: Valor ingresado que ha pasado la validación.
    """
    while True:
        value = input(prompt)
        if validate_fn(value):
            return value
        print(f"{error_msg}")

def create_vehicle():
    """
    Registra un nuevo vehículo en el sistema, validando todos los datos ingresados.

    Proceso:
        - Solicita el número de placa y verifica que no exista otro vehículo con la misma.
        - Solicita y valida los datos del vehículo: marca, modelo, año, color y número de pasajeros.
        - Crea una instancia de `Vehicle` y guarda la información en el archivo correspondiente.

    Muestra:
        - Mensajes de error si la placa ya existe o si los datos ingresados son inválidos.
        - Confirmación si el vehículo fue registrado correctamente.

    Requiere:
        - La clase `Vehicle` y las funciones `load_vehicles`, `save_vehicles` e `input_validated`.
    """
    plate = input_validated(
        "Número de placa: ",
        lambda x: len(x) == 6,
        "❌ Placa inválida. Debe tener 6 caracteres."
    )
    vehicles = load_vehicles()
    if any(v["plate"] == plate for v in vehicles):
        print("❌ Ya existe un vehículo con esa placa.")
        return

    brand = input_validated(
        "Marca: ",
        lambda x: x.replace(" ", "").isalpha() and len(x) >= 3,
        "❌ Marca inválida. Debe tener al menos 3 caracteres."
    )
    model = input_validated(
        "Modelo: ",
        lambda x: x.replace(" ", "").isalnum() and len(x) >= 2,
        "❌ Modelo inválido. Debe tener al menos 3 caracteres."
    )
    year = input_validated(
        "Año (ej. 2023): ",
        lambda x: x.isdigit() and 1990 <= int(x) <= 2025,
        "❌ Año inválido. Debe estar entre 1990 y 2025."
    )
    color = input_validated(
        "Color: ",
        lambda x: x.replace(" ", "").isalpha() and len(x) >= 3,
        "❌ Color inválido. Debe tener al menos 3 caracteres."
    )
    passenger = int(input_validated(
        "Pasajeros (1-15): ",
        lambda x: x.isdigit() and 1 <= int(x) <= 15,
        "❌ Cantidad inválida. Debe ser un número entre 1 y 15."
    ))

    new_vehicle = Vehicle(plate, brand, model, int(year), color, passenger)
    vehicles.append(new_vehicle.to_dict())
    save_vehicles(vehicles)
    print("✅ Vehículo creado correctamente.")

def list_vehicles():
    """
    Muestra en consola la lista de vehículos registrados en el sistema.

    Proceso:
        - Carga los vehículos desde el archivo correspondiente.
        - Verifica si existen registros.
        - Si los hay, imprime los datos de cada vehículo: placa, marca, modelo, año, color, capacidad y estado.

    Muestra:
        - Un mensaje si no hay vehículos registrados.
        - El listado detallado de vehículos si existen registros.
    """
    vehicles = load_vehicles()
    if not vehicles:
        print("No hay vehículos registrados.")
        return
    for v in vehicles:
        print(f"{v['plate']} - {v['brand']} {v['model']} ({v['year']}) | Color: {v['color']} | Capacidad: {v['passenger']} | Estado: {v['state']}")

def edit_vehicle():
    """
    Permite modificar los datos de un vehículo registrado en el sistema.

    Proceso:
        - Solicita la placa del vehículo a editar.
        - Si se encuentra, permite actualizar los campos: marca, modelo, año, color y capacidad.
          Si no se proporciona un nuevo valor, se mantiene el actual.
        - Realiza validaciones básicas para asegurar que los nuevos datos sean válidos.
        - Guarda los cambios en el archivo correspondiente si todas las validaciones son correctas.

    Muestra:
        - Mensaje de confirmación si el vehículo fue actualizado correctamente.
        - Mensajes de error si algún dato es inválido o si el vehículo no fue encontrado.
    """
    vehicles = load_vehicles()
    plate = input("Ingrese la placa del vehículo que desea modificar: ")
    for v in vehicles:
        if v["plate"] == plate:
            print(f"Editando vehículo: {v['plate']}")
            v["brand"] = input(f"Nueva marca [{v['brand']}]: ") or v["brand"]
            v["model"] = input(f"Nuevo modelo [{v['model']}]: ") or v["model"]
            v["year"] = input(f"Nuevo año [{int(v['year'])}]: ") or int(v["year"])
            v["color"] = input(f"Nuevo color [{v['color']}]: ") or v["color"]
            v["passenger"] = input(f"Nueva capacidad [{int(v['passenger'])}]: ") or int(v["passenger"])

            # Validaciones simples
            if not v["brand"].replace(" ", "").isalpha() or len(v["brand"]) < 3:
                print("❌ Marca inválida.")
                return
            if not v["model"].replace(" ", "").isalnum() or len(v["model"]) < 2:
                print("❌ Modelo inválido.")
                return
            if not str(v["year"]).isdigit() or not (1990 <= int(v["year"]) <= 2025):
                print("❌ Año inválido.")
                return
            if not v["color"].replace(" ", "").isalpha() or len(v["color"]) < 3:
                print("❌ Color inválido.")
                return
            if not str(v["passenger"]).isdigit() or not (1 <= int(v["passenger"]) <= 15):
                print("❌ Capacidad inválida.")
                return

            save_vehicles(vehicles)
            print("✅ Vehículo actualizado.")
            return
    print("❌ Vehículo no encontrado.")

def delete_vehicle():
    """
    Elimina un vehículo del sistema a partir de su número de placa.

    Proceso:
        - Solicita al usuario la placa del vehículo que desea eliminar.
        - Filtra la lista de vehículos, excluyendo el que coincide con la placa indicada.
        - Si no hay cambios en la lista, significa que no se encontró el vehículo.
        - Si se elimina, guarda la lista actualizada en el archivo correspondiente.

    Muestra:
        - Mensaje de éxito si el vehículo fue eliminado.
        - Mensaje de error si no se encontró un vehículo con la placa proporcionada.
    """
    vehicles = load_vehicles()
    plate = input("Ingrese la placa del vehículo que desea eliminar: ")
    updated = [v for v in vehicles if v["plate"] != plate]
    if len(updated) == len(vehicles):
        print("❌ Vehículo no encontrado.")
    else:
        save_vehicles(updated)
        print("🗑️ Vehículo eliminado correctamente.")

def menu_vehicles():
    while True:
        print("\n=== Gestión de Vehículos ===")
        print("1. Crear nuevo vehículo")
        print("2. Listar vehículos")
        print("3. Editar vehículo")
        print("4. Eliminar vehículo")
        print("5. Volver al menú principal")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            create_vehicle()
        elif choice == "2":
            list_vehicles()
        elif choice == "3":
            edit_vehicle()
        elif choice == "4":
            delete_vehicle()
        elif choice == "5":
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")
from cliente_service import menu_clients
from alquiler_service import menu_rentals
from utils import load_json, save_json, log_record
from usuarios_service import menu_users
from vehiculo_service import menu_vehicles

class Sistema:
    def __init__(self):
        self.users = load_json('Docs/users.json')
        self.cars = load_json("Docs/vehicles.json")
        self.clients = load_json("Docs/clients.json")
        self.rentals = load_json("Docs/rentals.json")
        self.logged_user = None

    def iniciar(self):
        print("=== SISTEMA DE ALQUILER DE VEHÍCULOS ===")
        self.login()
        if self.logged_user:
            log_record(self.logged_user["user"], "ENTRADA")
            self.menu_principal()

    def login(self):
        attemps=1
        while attemps<=3:
            user = input("Usuario: ")
            password = input("Contraseña: ")
            for u in self.users + self.clients:
                if u["user"] == user and u["password"] == password:
                    self.logged_user = u
                    print(f"Bienvenido, {u['name_user']} ({u['rol']})")
                    return
            print("Usuario o contraseña incorrectos.")
            attemps+=1
        print("Se alcanzó el número máximo de intentos. Acceso denegado.")

    def menu_principal(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            rol = self.logged_user["rol"]

            if rol == "cliente":
                print("1. Mi perfil")
                print("2. Alquiler de Vehículos")
                print("3. Salir del sistema")
                choice = input("Seleccione una opción: ")

                if choice == "1":
                    menu_clients(self.logged_user)  # Puede permitir editar solo su propio perfil
                elif choice == "2":
                    menu_rentals(self.logged_user)  # Solo registra su propio alquiler
                elif choice == "3":
                    log_record(self.logged_user["user"], "SALIDA")
                    print("👋 Cerrando el sistema.")
                    break
                else:
                    print("❌ Opción inválida. Intente de nuevo.")
            else:
                print("1. Gestión de Usuarios")
                print("2. Gestión de Vehículos")
                print("3. Gestión de Clientes")
                print("4. Gestión de Alquileres")
                print("5. Salir del sistema")
                choice = input("Seleccione una opción: ")

                if choice == "1":
                    menu_users()
                elif choice == "2":
                    menu_vehicles()
                elif choice == "3":
                    menu_clients(self.logged_user)
                elif choice == "4":
                    menu_rentals(self.logged_user)
                elif choice == "5":
                    log_record(self.logged_user["user"], "SALIDA")
                    print("👋 Cerrando el sistema.")
                    break
                else:
                    print("❌ Opción inválida. Intente de nuevo.")
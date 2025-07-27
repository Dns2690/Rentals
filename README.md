## 📋 Características principales

- Gestión de **usuarios administrativos** y **clientes**.
- Validación de **credenciales de acceso**.
- CRUD para:
  - Usuarios
  - Clientes
  - Vehículos
  - Alquileres
- Control de **estado del vehículo** (`DISPONIBLE`, `RENTADO`).
- Validaciones de datos (fechas, tarjetas, correos, cédulas, etc.).
- Registro de **bitácora de acceso** de los usuarios.
- Menú personalizado según el **rol del usuario**.

---

## 📁 Estructura del proyecto
```
├── Docs/
│   ├── users.json
│   ├── clients.json
│   ├── vehicles.json
│   └── rentals.json
├── cliente_dto.py
├── vehiculo_dto.py
├── alquiler_dto.py
├── usuario_dto.py
├── cliente_service.py
├── vehiculo_service.py
├── alquiler_service.py
├── usuarios_service.py
├── utils.py
├── sistema.py
└── bitacora.txt
```

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10+**
- Almacenamiento de datos en **archivos JSON**
- Entrada/salida por **consola**
- Control de fechas con `datetime`
- Validaciones con expresiones regulares (`re`)

---

## 🧠 Lógica del sistema

El sistema sigue una arquitectura modular, con cada entidad manejada por su propio módulo (service), y los datos se almacenan en archivos `.json`.  
Las operaciones de lectura y escritura están unificadas mediante funciones utilitarias.  
Se aplica validación rigurosa a toda entrada de usuario y se controlan los flujos de estado de los vehículos y alquileres.

---

## 📌 Notas adicionales

- El sistema guarda registros de acceso en `bitacora.txt`.
- Puedes migrar fácilmente a una base de datos relacional con mínimas modificaciones.
"""

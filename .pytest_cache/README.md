Sistema de Gestión para Clínica Veterinaria
Aplicación completa desarrollada con Python + Streamlit + MySQL, diseñada para facilitar la gestión diaria de una clínica veterinaria: clientes, mascotas, personal, citas y control de saldo.
Descripción del proyecto
Este sistema permite administrar de forma sencilla y eficiente los distintos elementos que intervienen en una clínica veterinaria. Su objetivo es agilizar tareas administrativas, reducir errores y mejorar la organización del trabajo diario.
Características principales:
Gestión de Clientes
	•	Registro, edición y eliminación de clientes.
	•	Visualización en tabla completa.
	•	Integración con mascotas mediante relación cliente ↔ mascota.
Gestión de Mascotas
	•	Registro de mascotas con atributos completos:
	◦	nombre, especie, raza, sexo, edad, estado de salud, dueño.
	•	Gráficos automáticos de distribución por especie.
	•	Edición y eliminación.
	•	Asociación directa con clientes de la base de datos.
Gestión de Personal
	•	Registro de veterinarios y auxiliares.
	•	Asignación de turnos.
	•	Calendario mensual visual del personal.
Gestión de Citas
	•	Registro de citas con:
	◦	mascota, veterinario, motivo, fecha, hora y estado.
	•	Control automático de disponibilidad:
	◦	No permite solapamiento de citas para un mismo veterinario.
	•	Edición y eliminación de citas.
	•	Gráficos de motivos y estados de citas.
	•	Integración futura con facturación.
Gestión de Saldo
	•	Registro automático de ingresos por tratamientos o servicios.
	•	Tabla detallada con:
	◦	tipo de operación, concepto, monto, saldo anterior y saldo nuevo.
 
Tecnologías utilizadas
Python 3.10+, Streamlit (Interfaz), MySQL (base de datos principal), Pandas (manejo de datos y tablas), Plotly Express (gráficos interactivos) y CSS (estilo visual y tema rosa).
Estructura del proyecto
VETERINARIA/
│
├── streamlit_app/
│   ├── app.py                   --> Página de inicio
│   ├── pages/
│   │   ├── 1_Clientes.py
│   │   ├── 2_Mascotas.py
│   │   ├── 3_Personal.py
│   │   ├── 4_Citas.py
│   │   ├── 5_Saldo.py
│   └── logo_vet.png                     --> Imagen del logo personalizado
│
├── src/
│   ├── database/
│   │   ├── db.py                    --> Conector MySQL actualmente en uso
│   │   ├── sqlalchemy_connector.py  --> Conector ORM preparado para el 
 
futuro
│   │   └── orm/
│   │        ├── base.py
│   │        ├── cliente_orm.py
│   │        ├── mascota_orm.py
│   │        ├── empleado_orm.py
│   │        └── cita_orm.py
│   ├── modulos/
│       ├── saldo.py
│       └── ...
│
└── README.md
Instalación y ejecución
1. Clonar el repositorio
2. Crear un entorno virtual
3. Instalar dependencias
4. Configurar MySQL
5. Ejecutar la aplicación
streamlit run streamlit_app/app.py
 
Variables de conexión
Editar en:
src/database/db.py
Ejemplo:
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="veterinaria"
)
 
Diseño
La app utiliza:
	•	Fondo rosa claro #FFF9FB
	•	Pink boxes decorativas
	•	Iconos para cada sección
	•	Logo personalizado de las veterinarias (dos chicas)
 
MySQL + ORM: cómo conviven en este proyecto
Actualmente la aplicación utiliza MySQL mediante consultas directas gracias al archivo db.py, sin embargo, el proyecto incluye un sistema ORM completo preparado, mediante:
src/database/sqlalchemy_connector.py
src/database/orm/*.py
El ORM contiene:
	•	Modelos completos para Cliente, Mascota, Empleado y Cita
	•	Relaciones definidas con relationship()
	•	Base.metadata.create_all() listo para generar tablas
Plan para migrar a SQLAlchemy en el futuro
Cuando se desee migrar la aplicación a usar ORM completo:
1. Reemplazar el conector actual
En vez de:
from src.database.db import DataBaseConnector
Usar:
from src.database.sqlalchemy_connector import SessionLocal
 
2. Cambiar las consultas SQL por ORM
Ejemplo actual:
clientes = db.ejecutar_query("SELECT * FROM clientes")
Con ORM:
session = SessionLocal()
clientes = session.query(ClienteORM).all()
 
3. Usar las relaciones del ORM
Se podrá hacer cosas como:
cliente.mascotas
veterinario.citas
mascota.cliente
Sin escribir JOINs manualmente.
 
4. Actualizar CRUDs para usar session.add() / delete()
session.add(nuevo_cliente)
session.commit()
 
5. Activar validaciones automáticas
 
6. Futuras ventajas al usar ORM 
- Menos SQL manual- Código más limpio y seguro- Preparado para escalar la aplicación
 
Posibles mejoras futuras
	•	Historial clínico completo.
	•	Facturas PDF por cita.
	•	Notificaciones por correo.
	•	Panel avanzado de estadísticas.
	•	Sistema de roles (admin vs personal).
	•	Migración completa a SQLAlchemy ORM para un backend escalable
 
Autores
Proyecto realizado por:
	•	Marta López-Manzanares Pérez
	•	Celia Cogollos Bustamante
 

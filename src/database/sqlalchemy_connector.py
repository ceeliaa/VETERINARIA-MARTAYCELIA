from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base


# URL base de datos
DATABASE_URL = "mysql+pymysql://root:12345678@localhost/clinica_veterinaria"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Configurar sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# IMPORTACIONES ORM — DEBEN IR AL FINAL
from src.database.orm.cliente_orm import ClienteORM
from src.database.orm.mascota_orm import MascotaORM
from src.database.orm.empleado_orm import EmpleadoORM
from src.database.orm.cita_orm import CitaORM

# Crear tablas
Base.metadata.create_all(bind=engine)

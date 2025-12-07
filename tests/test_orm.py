import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.base import Base
from src.database.orm.cliente_orm import ClienteORM
from src.database.orm.mascota_orm import MascotaORM
from src.database.orm.empleado_orm import EmpleadoORM
from src.database.orm.cita_orm import CitaORM, EstadoCita
from datetime import datetime



# BD TEMPORAL PARA TESTS
@pytest.fixture
def session():
    # Usamos SQLite temporal en RAM
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSession = sessionmaker(bind=engine)

    # Crear tablas para el test
    Base.metadata.create_all(engine)

    # Crear sesión
    db = TestingSession()

    yield db  # lo que recibe cada test

    # Cerrar sesión después
    db.close()


# 1. Test ClienteORM

def test_crear_cliente_orm(session):
    cliente = ClienteORM(
        nombre="Dani",
        apellidos="Pitarch",
        dni="00011122A",
        telefono="600111222",
        correo="dani@mail.com"
    )

    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    assert cliente.id is not None
    assert cliente.nombre == "Dani"


# 2. Test MascotaORM con cliente

def test_crear_mascota_con_cliente(session):
    cliente = ClienteORM(
        nombre="Celia",
        apellidos="Moreno",
        dni="00223344B",
        telefono="611223344",
        correo="celia@mail.com"
    )
    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    mascota = MascotaORM(
        nombre="Milo",
        especie="Perro",
        raza="Labrador",
        sexo="Macho",
        edad=3,
        estado_salud="Sano",
        cliente_id=cliente.id
    )

    session.add(mascota)
    session.commit()
    session.refresh(mascota)

    assert mascota.id is not None
    assert mascota.cliente_id == cliente.id
    assert mascota.cliente.nombre == "Celia"


# 3. Test EmpleadoORM

def test_crear_empleado_orm(session):
    empleado = EmpleadoORM(
        nombre="Laura",
        apellidos="Serrano",
        puesto="Veterinaria",
        telefono="600000111"
    )

    session.add(empleado)
    session.commit()
    session.refresh(empleado)

    assert empleado.id is not None
    assert empleado.puesto == "Veterinaria"


# 4. Test CitaORM + Relaciones

def test_crear_cita(session):
    # Crear cliente
    cliente = ClienteORM(
        nombre="Juan",
        apellidos="López",
        dni="55667788C",
        telefono="600999888",
        correo="juan@mail.com"
    )
    session.add(cliente)
    session.commit()

    # Crear mascota
    mascota = MascotaORM(
        nombre="Kira",
        especie="Gato",
        raza="Siamés",
        sexo="Hembra",
        edad=2,
        estado_salud="Sano",
        cliente_id=cliente.id
    )
    session.add(mascota)
    session.commit()

    # Crear empleado
    empleado = EmpleadoORM(
        nombre="Pablo",
        apellidos="Torres",
        puesto="Veterinario",
        telefono="600777666"
    )
    session.add(empleado)
    session.commit()

    # Crear cita
    cita = CitaORM(
        fecha=datetime(2025, 1, 1, 10, 0, 0),
        motivo="Vacunación",
        mascota_id=mascota.id,
        empleado_id=empleado.id,
        estado=EstadoCita.Pendiente,
    )

    session.add(cita)
    session.commit()
    session.refresh(cita)

    assert cita.id is not None
    assert cita.mascota_id == mascota.id
    assert cita.empleado_id == empleado.id
    assert cita.estado == EstadoCita.Pendiente

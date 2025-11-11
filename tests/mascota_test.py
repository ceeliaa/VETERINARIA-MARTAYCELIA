import pytest
from src.modulos.mascota import Mascota

def test_crear_mascota():
    mascota = Mascota(
        nombre="Milo",
        id_mascota=1,
        especie="Perro",
        raza="Labrador",
        sexo="Macho",
        edad=3,
        estado_salud="Sano",
        dni_cliente="12345678A"
    )

    assert mascota.nombre == "Milo"
    assert mascota.especie == "Perro"
    assert mascota.raza == "Labrador"
    assert mascota.sexo == "Macho"
    assert mascota.edad == 3
    assert mascota.estado_salud == "Sano"
    assert mascota.dni_cliente == "12345678A"
    assert mascota.historial_consultas == []  # al principio sin consultas

def test_agregar_consulta():
    mascota = Mascota("Milo", 1, "Perro", "Labrador", "Macho", 3, "Sano", "12345678A")
    mascota.agregar_consulta("Revisión general")

    assert len(mascota.historial_consultas) == 1
    assert mascota.historial_consultas[0] == "Revisión general"

# tras hacer el primer pytest, da error porque no hemos creado la clase Mascota. Vamos al archivo mascota.py y la creamos


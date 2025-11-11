import pytest
from src.modulos.cliente import Cliente

def test_crear_cliente():
    cliente = Cliente(
        nombre="Maria",
        apellidos="Blanco Gonzalez",
        dni="12345678A",
        telefono="612345678",
        correo="maria@mail.com"
    )

    assert cliente.nombre == "Maria"
    assert cliente.apellidos == "Blanco Gonzalez"
    assert cliente.dni == "12345678A"
    assert cliente.telefono == "612345678"
    assert cliente.correo == "maria@mail.com"
    assert cliente.mascotas == []  # dejamos este campo vacío porque al principio no tiene mascotas

def test_agregar_mascota():
    cliente = Cliente("Maria", "Blanco", "12345678A", "612345678", "maria@mail.com")
    cliente.agregar_mascota("Milo") # añadimos la mascota asociada al cliente

    assert len(cliente.mascotas) == 1
    assert cliente.mascotas[0] == "Milo"

# El primer error que nos da al hacer pytest es que no tenemos la clase Cliente creada, por lo que vamos al 
# archivo cliente.py y creamos la clase cliente.

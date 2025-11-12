import pytest
from src.modulos.personal import Personal

def test_crear_personal():
    trabajador = Personal(
        nombre="Lucia",
        apellidos="López",
        dni="12345678B",
        telefono="600123456",
        correo="lucia@mail.com",
        tipo="Veterinario",
        disponibilidad=True
    )

    assert trabajador.nombre == "Lucia"
    assert trabajador.apellidos == "López"
    assert trabajador.dni == "12345678B"
    assert trabajador.telefono == "600123456"
    assert trabajador.correo == "lucia@mail.com"
    assert trabajador.tipo == "Veterinario"
    assert trabajador.disponibilidad is True
    assert trabajador.dinero_cobrado == 0
    assert trabajador.consultas == []


def test_asignar_consulta():
    trabajador = Personal("Ana", "Pérez", "98765432C", "611223344", "ana@mail.com", "Auxiliar", True)
    trabajador.asignar_consulta("Consulta 1")

    assert len(trabajador.consultas) == 1
    assert trabajador.consultas[0] == "Consulta 1"


def test_pagar_empleado_aumenta_dinero_cobrado():
    trabajador = Personal("Ana", "Pérez", "98765432C", "611223344", "ana@mail.com", "Auxiliar", True)
    trabajador.pagar_empleado(100)

    assert trabajador.dinero_cobrado == 100

# El primer error que nos da al hacer pytest es que no tenemos la clase Personal creada, por lo que vamos al 
# archivo personal.py y creamos la clase Personal.
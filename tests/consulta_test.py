import pytest
from src.modulos.consulta import Consulta

def test_crear_consulta():
    consulta = Consulta(
        fecha="2025-11-12",
        hora="10:30",
        veterinario="Marta López",
        motivo="Vacunación",
        id_mascota=1
    )

    assert consulta.fecha == "2025-11-12"
    assert consulta.hora == "10:30"
    assert consulta.veterinario == "Marta López"
    assert consulta.motivo == "Vacunación"
    assert consulta.id_mascota == 1
    assert consulta.consulta_realizada is False
    assert consulta.diagnostico == ""


def test_confirmar_realizacion_consulta():
    consulta = Consulta("2025-11-12", "10:30", "Marta López", "Revisión", 1)
    consulta.confirmar_realizacion()
    assert consulta.consulta_realizada is True


def test_registrar_diagnostico():
    consulta = Consulta("2025-11-12", "10:30", "Marta López", "Vacunación", 1)
    consulta.registrar_diagnostico("Mascota sana y vacunada")
    assert consulta.diagnostico == "Mascota sana y vacunada"

# El primer error que nos da al hacer pytest es que no tenemos la clase Consulta creada, por lo que vamos al 
# archivo consulta.py y creamos la clase Consulta.
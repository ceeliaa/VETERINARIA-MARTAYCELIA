import pytest
from src.modulos.saldo import Saldo

def test_saldo_inicial():
    saldo = Saldo()
    assert saldo.saldo_inicial == 0
    assert saldo.operaciones == []

def test_cobrar_consulta_aumenta_saldo():
    saldo = Saldo()
    saldo.cobrar_consulta(50, "Maria Blanco")
    assert saldo.saldo_final == 50
    assert len(saldo.operaciones) == 1
    assert saldo.operaciones[0]["tipo"] == "Ingreso"
    assert saldo.operaciones[0]["monto"] == 50

def test_pagar_empleado_disminuye_saldo():
    saldo = Saldo()
    saldo.cobrar_consulta(100, "Cliente A")
    saldo.pagar_empleado(40, "Veterinario 1")
    assert saldo.saldo_final == 60
    assert len(saldo.operaciones) == 2
    assert saldo.operaciones[1]["tipo"] == "Gasto"
    assert saldo.operaciones[1]["monto"] == 40

def test_consultar_saldo():
    saldo = Saldo()
    saldo.cobrar_consulta(200, "Cliente B")
    saldo.pagar_empleado(50, "Auxiliar")
    assert saldo.consultar_saldo() == 150

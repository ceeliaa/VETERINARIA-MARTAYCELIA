class ClinicaError(Exception):
    # Excepción base para la clínica veterinaria
    pass

class ClienteNoEncontradoError(ClinicaError):
    # Se lanza un error cuando no se encuentra un cliente
    pass

class MascotaNoRegistradaError(ClinicaError):
    # Se lanza un error cuando una mascota no está registrada
    pass

class SaldoInsuficienteError(ClinicaError):
    # Se lanza un error cuando no hay suficiente saldo en caja
    pass

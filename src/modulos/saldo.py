class Saldo:
    def __init__(self):
        self.saldo_inicial = 0
        self.saldo_final = 0
        self.operaciones = []

    def cobrar_consulta(self, monto, cliente):
        self.saldo_final += monto
        self.operaciones.append({
            "tipo": "Ingreso",
            "monto": monto,
            "cliente": cliente
        })

    def pagar_empleado(self, monto, empleado):
        self.saldo_final -= monto
        self.operaciones.append({
            "tipo": "Gasto",
            "monto": monto,
            "empleado": empleado
        })

    def consultar_saldo(self):
        return self.saldo_final

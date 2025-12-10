class Saldo:
    """
    Clase para gestionar el saldo desde Streamlit.
    Maneja ingresos y gastos y escribe todo en MySQL.
    """

    def __init__(self, db):
        self.db = db
        self.saldo_actual = self._cargar_saldo()

    # -----------------------------------------------------------
    # Cargar saldo actual desde la BD
    # -----------------------------------------------------------
    def _cargar_saldo(self):
        query = "SELECT saldo_nuevo FROM saldo ORDER BY id DESC LIMIT 1"
        resultado = self.db.ejecutar_query(query)

        if resultado and resultado[0]["saldo_nuevo"] is not None:
            return float(resultado[0]["saldo_nuevo"])

        return 0.0

    # -----------------------------------------------------------
    # Registrar movimiento interno
    # -----------------------------------------------------------
    def _registrar_mov(self, tipo, concepto, monto):
        saldo_anterior = self.saldo_actual

        if tipo == "INGRESO":
            saldo_nuevo = saldo_anterior + monto
        else:
            saldo_nuevo = saldo_anterior - monto

        query = """
            INSERT INTO saldo (fecha, tipo_operacion, concepto, monto, saldo_anterior, saldo_nuevo)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """

        self.db.ejecutar_query(
            query,
            (tipo, concepto, monto, saldo_anterior, saldo_nuevo),
            fetch=False
        )

        self.saldo_actual = saldo_nuevo
        return saldo_nuevo

    # -----------------------------------------------------------
    # API pública
    # -----------------------------------------------------------
    def registrar_ingreso(self, concepto, monto):
        return self._registrar_mov("INGRESO", concepto, monto)

    def registrar_gasto(self, concepto, monto):
        return self._registrar_mov("GASTO", concepto, monto)

    def consultar_saldo(self):
        self.saldo_actual = self._cargar_saldo()
        return self.saldo_actual

    def obtener_historial(self):
        query = """
            SELECT fecha, tipo_operacion, concepto, monto, saldo_anterior, saldo_nuevo
            FROM saldo
            ORDER BY fecha DESC, id DESC
        """
        return self.db.ejecutar_query(query)

    # -----------------------------------------------------------
    # MÉTODOS PARA COMPATIBILIDAD CON TU APP
    # -----------------------------------------------------------

    def cobrar_consulta(self, monto, servicio, cliente):
        concepto = f"{servicio} - Cliente: {cliente}"
        return self.registrar_ingreso(concepto, monto)

    def pagar_empleado(self, empleado, monto):
        concepto = f"Pago a empleado: {empleado}"
        return self.registrar_gasto(concepto, monto)

    def obtener_estadisticas_mes(self):
        query = """
            SELECT 
                SUM(CASE WHEN tipo_operacion='INGRESO' THEN monto ELSE 0 END) AS ingresos,
                SUM(CASE WHEN tipo_operacion='GASTO' THEN monto ELSE 0 END) AS gastos
            FROM saldo
            WHERE MONTH(fecha) = MONTH(NOW())
              AND YEAR(fecha) = YEAR(NOW());
        """

        resultado = self.db.ejecutar_query(query)[0]

        return {
            "ingresos": float(resultado["ingresos"] or 0),
            "gastos": float(resultado["gastos"] or 0)
        }

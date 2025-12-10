from datetime import datetime

class Saldo:

    
    def __init__(self, db_connector):
        """
        Inicializa el gestor de saldo con conexión a la base de datos
        
        Args:
            db_connector: Instancia de DataBaseConnector
        """
        self.db = db_connector
        self.saldo_actual = self._obtener_saldo_actual()
    
    def _obtener_saldo_actual(self):
        """Obtiene el saldo actual de la base de datos"""
        query = "SELECT saldo_nuevo FROM saldo ORDER BY id DESC LIMIT 1"
        resultado = self.db.ejecutar_query(query)

        # Si no hay registros → saldo = 0.0
        if not resultado:
            return 0.0

        ultimo_saldo = resultado[0]['saldo_nuevo']

        # Si el valor es NULL → saldo = 0.0
        if ultimo_saldo is None:
            return 0.0

        return float(ultimo_saldo)


    
    def _registrar_operacion(self, tipo_operacion, concepto, monto):
        """
        Registra una operación en la base de datos
        
        Args:
            tipo_operacion: 'INGRESO' o 'GASTO'
            concepto: Descripción de la operación
            monto: Cantidad de dinero
            
        Returns:
            float: Nuevo saldo después de la operación
            
        Raises:
            ValueError: Si no hay saldo suficiente para un gasto
        """
        saldo_anterior = self.saldo_actual
        
        # Validar saldo suficiente para gastos
        if tipo_operacion == 'GASTO' and monto > saldo_anterior:
            raise ValueError(f"Saldo insuficiente. Disponible: €{saldo_anterior:.2f}, Requerido: €{monto:.2f}")
        
        # Calcular nuevo saldo
        if tipo_operacion == 'INGRESO':
            saldo_nuevo = saldo_anterior + monto
        else:  # GASTO
            saldo_nuevo = saldo_anterior - monto
        
        # Insertar la operación en la base de datos
        query = """
            INSERT INTO saldo (fecha, tipo_operacion, concepto, monto, saldo_anterior, saldo_nuevo, saldo)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s)
        """
        self.db.ejecutar_query(
            query,
            (tipo_operacion, concepto, monto, saldo_anterior, saldo_nuevo, saldo_nuevo),
            fetch=False
        )
        
        # Actualizar saldo en memoria
        self.saldo_actual = saldo_nuevo
        
        return saldo_nuevo
    
    def cobrar_consulta(self, monto, servicio, cliente=None):
        """
        Registra el cobro de una consulta o servicio
        """
        concepto = f"Consulta: {servicio}"
        if cliente:
            concepto += f" - Cliente: {cliente}"
        
        return self._registrar_operacion('INGRESO', concepto, monto)
    
    def pagar_empleado(self, monto, empleado):
        """
        Registra el pago de nómina a un empleado
        """
        concepto = f"Nómina Empleado: {empleado}"
        return self._registrar_operacion('GASTO', concepto, monto)
    
    def pagar_facturas(self, monto, proveedor=None, descripcion=None):
        """
        Registra el pago de facturas
        """
        concepto = "Facturas Proveedores"
        if proveedor:
            concepto += f": {proveedor}"
        if descripcion:
            concepto += f" - {descripcion}"
        
        return self._registrar_operacion('GASTO', concepto, monto)
    
    def registrar_gasto(self, monto, tipo_gasto, descripcion):
        """
        Registra un gasto genérico
        """
        concepto = f"{tipo_gasto}: {descripcion}"
        return self._registrar_operacion('GASTO', concepto, monto)
    
    def registrar_ingreso(self, monto, concepto):
        """
        Registra un ingreso genérico
        """
        return self._registrar_operacion('INGRESO', concepto, monto)

    def consultar_saldo(self):
        """
        Devuelve el saldo actual
        """
        self.saldo_actual = self._obtener_saldo_actual()
        return self.saldo_actual
    
    def obtener_historial(self, limite=None, tipo_operacion=None):
        """
        Obtiene el historial de operaciones
        """
        query = "SELECT * FROM saldo WHERE 1=1"
        params = []
        
        if tipo_operacion:
            query += " AND tipo_operacion = %s"
            params.append(tipo_operacion)
        
        query += " ORDER BY fecha DESC, id DESC"
        
        if limite:
            query += f" LIMIT {limite}"
        
        return self.db.ejecutar_query(query, tuple(params)) if params else self.db.ejecutar_query(query)
    
    def obtener_estadisticas_mes(self):
        """
        Obtiene estadísticas del mes actual
        """
        query_ingresos = """
            SELECT COALESCE(SUM(monto), 0) as total 
            FROM saldo 
            WHERE tipo_operacion='INGRESO' 
            AND MONTH(fecha) = MONTH(CURRENT_DATE())
            AND YEAR(fecha) = YEAR(CURRENT_DATE())
        """
        ingresos = float(self.db.ejecutar_query(query_ingresos)[0]['total'])
        
        query_gastos = """
            SELECT COALESCE(SUM(monto), 0) as total 
            FROM saldo 
            WHERE tipo_operacion='GASTO' 
            AND MONTH(fecha) = MONTH(CURRENT_DATE())
            AND YEAR(fecha) = YEAR(CURRENT_DATE())
        """
        gastos = float(self.db.ejecutar_query(query_gastos)[0]['total'])
        
        return {
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': ingresos - gastos
        }

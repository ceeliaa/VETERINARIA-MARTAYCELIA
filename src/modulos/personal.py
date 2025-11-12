class Personal:
    def __init__(self, nombre, apellidos, dni, telefono, correo, tipo, disponibilidad):
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.telefono = telefono
        self.correo = correo
        self.tipo = tipo  # Veterinario o Auxiliar
        self.disponibilidad = disponibilidad
        self.dinero_cobrado = 0
        self.consultas = []

    def asignar_consulta(self, consulta):
        #Añade una consulta al listado de consultas asignadas al trabajador
        self.consultas.append(consulta)

    def pagar_empleado(self, monto):
        # Suma al total cobrado por el empleado
        self.dinero_cobrado += monto

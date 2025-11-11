class Mascota:
    def __init__(self, nombre, id_mascota, especie, raza, sexo, edad, estado_salud, dni_cliente):
        self.nombre = nombre
        self.id_mascota = id_mascota
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.edad = edad
        self.estado_salud = estado_salud
        self.dni_cliente = dni_cliente
        self.historial_consultas = []

    def agregar_consulta(self, consulta):
        self.historial_consultas.append(consulta)
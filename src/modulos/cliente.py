class Cliente:
    def __init__(self, nombre, apellidos, dni, telefono, correo):
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.telefono = telefono
        self.correo = correo
        self.mascotas = []

    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)

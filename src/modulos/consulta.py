class Consulta:
    def __init__(self, fecha, hora, veterinario, motivo, id_mascota):
        self.fecha = fecha
        self.hora = hora
        self.veterinario = veterinario
        self.motivo = motivo
        self.id_mascota = id_mascota
        self.consulta_realizada = False
        self.diagnostico = ""

    def confirmar_realizacion(self):
        #Marca la consulta como realizada.
        self.consulta_realizada = True

    def registrar_diagnostico(self, texto):
        #Guarda el diagnóstico asociado a la consulta.
        self.diagnostico = texto

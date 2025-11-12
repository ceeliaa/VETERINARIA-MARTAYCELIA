import re

class Utils:
    @staticmethod
    def validar_dni(dni):
        """Valida un DNI español simple."""
        return bool(re.match(r'^\d{8}[A-Za-z]$', dni))

    @staticmethod
    def validar_correo(correo):
        """Comprueba formato básico de email."""
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo))

    @staticmethod
    def edad_valida(edad):
        return isinstance(edad, int) and edad >= 0

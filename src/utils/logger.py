import logging
from datetime import datetime

class Logger:
    @staticmethod
    def configurar_logger(nombre_archivo="clinica.log"):
        logging.basicConfig(
            filename=f"logs/{nombre_archivo}", #Guardamos los logs en nuestro .log
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s" #Este es el formato de texto que queremos para nuestros logs
        )
        return logging.getLogger("ClinicaLogger")

#Creamos la carpeta logs al inicio si no existe
import os
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = Logger.configurar_logger() #Creamos la instancia global del logger

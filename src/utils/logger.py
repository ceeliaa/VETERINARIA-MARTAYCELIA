import logging
from datetime import datetime

class Logger:
    @staticmethod
    def configurar_logger(nombre_archivo="clinica.log"):
        logging.basicConfig(
            filename=f"logs/{nombre_archivo}",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        return logging.getLogger("ClinicaLogger")

# Crear carpeta logs al inicio si no existe
import os
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = Logger.configurar_logger()

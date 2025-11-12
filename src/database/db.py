import mysql.connector
from mysql.connector import Error
from src.utils.logger import logger

class DataBaseConnector:
    def __init__(self, host="localhost", user="root", password="", database="clinica_veterinaria"):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                logger.info("Conexión a la base de datos establecida correctamente.")
        except Error as e:
            logger.error(f"Error de conexión a la base de datos: {e}")
            raise

    def ejecutar_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            logger.info(f"Consulta ejecutada: {query}")
            return cursor
        except Error as e:
            logger.error(f"Error ejecutando query: {e}")
            raise
        finally:
            cursor.close()

    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada.")

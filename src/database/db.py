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

    def ejecutar_query(self, query, params=None, fetch=True):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())

            # Si es SELECT
            if fetch:
                result = cursor.fetchall()  # leer todos los resultados
            else:
                result = None
                self.connection.commit()  # Solo commit para INSERT/UPDATE/DELETE

            return result

        except Error as e:
            logger.error(f"Error ejecutando query: {e}")
            raise

        finally:
            # Asegurarnos de limpiar cualquier resultado pendiente ANTES de cerrar
            try:
                cursor.fetchall()
            except:
                pass
            cursor.close()


    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada.")

"""
Vamos a crear una clase para conectarnos a una base de datos MySQL.
En esta base de datos guardaremos información sobre nuestra clinica
"""

import mysql.connector #Importamos el módulo de MySQL Connector
from mysql.connector import Error #Importamos la clase Error
from src.utils.logger import logger #Cargamos tambien los loggers ya que los usaremos

class DataBaseConnector:
    """
    Cuando creamos un objeto de esta clase, se conecta automaticamente a MySQL
    Podemos cambiar los parametros que le pasamos al constructor __init__ pero tenemos unos predeterminados ya que serán los que usemos
    """
    def __init__(self, host="localhost", user="root", password="", database="clinica_veterinaria"):
        try:
            self.connection = mysql.connector.connect(
                host=host, #Por defecto, la base de datos esta en nuestro ordenador ("localhost")
                user=user, #El administrador de la base de datos será "root" que es el administrador principal de MySQL
                password=password, #contraseña vacia por defecto
                database=database #Nombre de nuestra base de datos
            )
            if self.connection.is_connected():
                logger.info("Conexión a la base de datos establecida correctamente.")
        except Error as e:
            logger.error(f"Error de conexión a la base de datos: {e}")
            raise

    #ejecutar_query() se encarga de ejecutar consultas SQL en nuestra base de datos
    def ejecutar_query(self, query, params=None, fetch=True): #fetch es un valor booleano que nos indicara si queremos preguntar o modificar sobre la base de datos
        #Creamos un cursor e indicamos que las respuestas a las consultas sean diccionarios
        cursor = self.connection.cursor(dictionary=True) 
        try:
            cursor.execute(query, params or ())#Si hay parametros se usan, sino se pasa una tupla vacia

            # Si es SELECT
            if fetch:
                result = cursor.fetchall()  #leer todos los resultados y obtener todas las filas del SELECT
            else:
                result = None
                self.connection.commit()  #Solo commit para INSERT/UPDATE/DELETE

            return result

        except Error as e:
            logger.error(f"Error ejecutando query: {e}")
            raise

        finally:
            # Asegurarnos de limpiar cualquier resultado pendiente ANTES de cerrar el cursor
            try:
                cursor.fetchall()
            except:
                pass
            cursor.close()

    #Nos debemos de asegurar de cerrar la conexión a la base de datos
    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada.")

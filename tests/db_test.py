import sys
import os

# Calcular la ruta raíz del proyecto y añadirla al path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.database.db import DataBaseConnector

db = DataBaseConnector(password="1234")

try:
    resultado = db.ejecutar_query("SELECT DATABASE();")
    print("Base de datos conectada correctamente:", resultado)
except Exception as e:
    print("Error al conectar:", e)

from src.database.sqlalchemy_connector import engine
#Importamos el nombre engine desde el módulo src.database.sqlalchemy_connector
#Es una instancia que representa la conexión a una base de datos

def test_connection():
    try:
        conn = engine.connect()#probamos a abrir la conexión
        conn.close()
        assert True
    except Exception as e:
        assert False, f"Error: {e}"

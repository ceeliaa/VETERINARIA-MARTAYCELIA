from src.database.sqlalchemy_connector import engine

def test_connection():
    try:
        conn = engine.connect()
        conn.close()
        assert True
    except Exception as e:
        assert False, f"Error: {e}"

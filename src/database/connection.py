import sqlite3
import os


INTERPOLATION_DB_PATH = os.path.join("data", "sqlite", "interpolation.db")
SPECS_DB_PATH = os.path.join("data", "sqlite", "specs.db")

def get_connection(db_path: str) -> sqlite3.Connection:
    """Crea y retorna una conexión a la base de datos especificada."""
   
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    return conn
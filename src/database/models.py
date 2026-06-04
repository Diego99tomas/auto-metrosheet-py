from database.connection import get_connection
from config.constants import Functions
import sqlite3


class DataBaseBuilder:
    """Clase base para inicializar la estructura base """

    def __init__(self,db_path:str):
        self.db_path=db_path

    def create_schema(self,value:str, unit:str, frec:str, value1:str,value2:str, optional:str|None=None):
        """Crea las tablas correspondientes para cada función del equipo"""

        conn=get_connection(self.db_path)
        cursor=conn.cursor()
        try:
            for tabla in Functions:
                sql_query = f"""
                CREATE TABLE IF NOT EXISTS {tabla.value} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {value} REAL,
                    {unit} TEXT,
                    {frec} TEXT,
                    {value1} REAL,
                    {value2} REAL
            """ 
                if optional:
                    sql_query += f",\n{optional} INTEGER"
                
                sql_query += "\n)"

                cursor.execute(sql_query)

            conn.commit()
            print(f"Base de datos en '{self.db_path}' creada con éxito.")
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error al crear la base de datos: {e}")
            raise e
        finally:
            conn.close()

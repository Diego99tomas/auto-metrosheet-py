from dataclasses import dataclass
from model_db.constants import Functions
import sqlite3

@dataclass
class Create_DB():

    DB_NAME:str
    EXCEL_NAME:str

    def create_db(self,value:str, unit:str, frec:str, value1:str,value2:str):
        conn=sqlite3.connect(self.DB_NAME)
        cursor=conn.cursor()

        for tabla in Functions:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {tabla.value} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {value} REAL,
                    {unit} TEXT,
                    {frec} TEXT,
                    {value1} REAL,
                    {value2} REAL
                )
            """)

        print('base creada')
        conn.commit()
        return conn
    
    @staticmethod
    def normalizar_unidad(value, magnitud):
        """Convierte cualquier unidad a la unidad base (V, A, Ohm)."""
        conversiones = {
            "mV": 1e-3, "µV": 1e-6,
            "mA": 1e-3, "µA": 1e-6,
            "Ω": 1, "kΩ": 1e3, "MΩ": 1e6,
            "V": 1, "A": 1
        }
        return value * conversiones.get(magnitud, 1)

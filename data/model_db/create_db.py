from dataclasses import dataclass
import sqlite3

@dataclass
class Create_DB():
    TABLAS_MAP = {
    "VOLTAJE DC": "voltaje_dc",
    "CORRIENTE DC": "corriente_dc",
    "RESISTENCIAS": "resistencias",
    "VOLTAJE AC": "voltaje_ac",
    "CORRIENTE AC": "corriente_ac"}
    
    DB_NAME:str
    EXCEL_NAME:str

    def create_db(self,value:str, unit:str, frec:str, value1:str,value2:str):
        conn=sqlite3.connect(self.DB_NAME)
        cursor=conn.cursor()

        for tabla in ["voltaje_dc", "corriente_dc", "resistencias","voltaje_ac", "corriente_ac"]:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {tabla} (
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

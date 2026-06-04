from dataclasses import dataclass
from config.constants import Functions
import sqlite3

@dataclass
class Create_DB():

    DB_NAME:str
    EXCEL_NAME:str

    def create_db(self,value:str, unit:str, frec:str, value1:str,value2:str, optional:str|None=None):
        conn=sqlite3.connect(self.DB_NAME)
        cursor=conn.cursor()

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

        print('base creada')
        conn.commit()
        return conn
    
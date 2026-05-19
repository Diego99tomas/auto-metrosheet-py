import sqlite3
from openpyxl import load_workbook
from model_db.create_db import Create_DB

EXCEL_NAME="specs/specs.xlsx"
DB_NAME="specs/specs.db"

TABLAS_MAP = {
    "VOLTAJE DC": "voltaje_dc",
    "CORRIENTE DC": "corriente_dc",
    "RESISTENCIAS": "resistencias",
    "VOLTAJE AC": "voltaje_ac",
    "CORRIENTE AC": "corriente_ac"
}

class ExportDataSpecsFromExcel():
    

    def migrar_datos(self,conn):
        """Migrar datos de show_specs en excel a Base de Datos"""
        try:
            wb = load_workbook(filename=EXCEL_NAME, data_only=True)
        except FileNotFoundError:
            print("Error: No se encontró el Excel.")
            return

        cursor = conn.cursor()

        for hoja_excel, tabla_sql in TABLAS_MAP.items():
            if hoja_excel not in wb.sheetnames:
                print(f"Saltando {hoja_excel}: No existe en el Excel.")
                continue
                
            ws = wb[hoja_excel]
            es_ac = "ac" in tabla_sql
            
            # Limpiar tabla antes de insertar para evitar duplicados si re-corres el script
            cursor.execute(f"DELETE FROM {tabla_sql}")

           
            for row in ws.iter_rows(min_row=1, max_row=50, values_only=True):
                if row[0] is None: continue  # Saltar filas vacías

                punto,unidad = row[0],row[1]
                valor=Create_DB.normalizar_unidad(punto,unidad)
                

                if es_ac:
                    frec=row[2]
                    decimal=Create_DB.normalizar_unidad(row[3],unidad)
                    show_spec=row[4]
                    
                else:
                    frec=None
                    decimal=Create_DB.normalizar_unidad(row[2],unidad)
                    show_spec=row[3]
                    
                sql=f"INSERT INTO {tabla_sql} (valor, unidad, frecuencia, decimales, show_spec) VALUES (?, ?, ?, ?, ?)"   
                params=(valor,unidad,frec,decimal,show_spec) 

                cursor.execute(sql,params)

        conn.commit()
        print("Migración completada exitosamente.")

if __name__ == "__main__":
    db_specs=Create_DB(DB_NAME=DB_NAME,EXCEL_NAME=EXCEL_NAME)
    conn=db_specs.create_db('valor','unidad','frecuencia','decimales','show_spec')
    export_data=ExportDataSpecsFromExcel()
    export_data.migrar_datos(conn)
    conn.close()
     
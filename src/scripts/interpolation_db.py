from database.models import Create_DB
from config.constants import Functions
from utility.data_processing import normalizar_unidad
from openpyxl import load_workbook

EXCEL_NAME=r"data\raw\interpolation.xlsx"
DB_NAME=r"data\sqlite\interpolation.db"


def migrar_datos(conn):
        
    """Migrar datos de interpolacion en excel a Base de Datos"""
    try:
        wb = load_workbook(filename=EXCEL_NAME, data_only=True)
    except FileNotFoundError:
        print("Error: No se encontró el Excel.")
        return

    cursor = conn.cursor()

    for func in Functions:
        if func.name not in wb.sheetnames:
            print(f"Saltando {func.name}: No existe en el Excel.")
            continue
            
        ws = wb[func.name]
        es_ac = "ac" in func.value
        
        
        cursor.execute(f"DELETE FROM {func.value}")

        
        for row in ws.iter_rows(min_row=1, max_row=40, values_only=True):

            if row[0] is None: continue  # Saltar filas vacías
            valor,unidad=row[0], row[1]
            lectura=normalizar_unidad(valor,unidad)

            if es_ac:
                # row[0]=lectura, row[1]=unidad, row[2]=frecuencia, row[3]=medida, row[4]=incert
                frec=row[2]
                medida=normalizar_unidad(row[3],row[1])
                incert=normalizar_unidad(row[4],row[1])
                
            else:
                # row[0]=lectura, row[1]=unidad, row[2]=medida, row[3]=incert
                frec=None
                medida=normalizar_unidad(row[2],row[1])
                incert=normalizar_unidad(row[3],row[1])
                
            sql=f"INSERT INTO {func.value} (lectura, unidad, frecuencia, medida, incert) VALUES (?, ?, ?, ?, ?)" 
            params= (lectura,unidad,frec,medida,incert)
                

            cursor.execute(sql, params)
        
    conn.commit() 
    print("Migración completada con éxito.")
        

if __name__ == "__main__":
    interp_db=Create_DB(DB_NAME,EXCEL_NAME)
    conn=interp_db.create_db('lectura','unidad','frecuencia','medida','incert')
    migrar_datos(conn)
    conn.close()






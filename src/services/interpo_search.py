from database.connection import get_connection,INTERPOLATION_DB_PATH
from utility.data_processing import normalizar_unidad,desnormalizar_unidad


def interpol_search_in_db(type_table:str,valor:float,unidad:str,frecuencia=None):
    """Busqueda en db de puntos inferior y superior para la interpolacion"""

    if 'ac' in type_table and frecuencia is not None:
        if frecuencia != '60 Hz':
            frecuencia='1 kHz'

    busqueda = normalizar_unidad(valor,unidad)
       
    #consultas 
    query_inf = f"SELECT lectura, medida, incert FROM {type_table} WHERE lectura <= ? AND (frecuencia = ? OR frecuencia IS NULL) ORDER BY lectura DESC LIMIT 1"

    query_sup = f"SELECT lectura, medida, incert FROM {type_table} WHERE lectura >= ? AND (frecuencia = ? OR frecuencia IS NULL) ORDER BY lectura ASC LIMIT 1"
    
    params = (busqueda, frecuencia)
    

    conn = get_connection(INTERPOLATION_DB_PATH)
    
    try:
        cursor= conn.cursor()

        with conn:
            cursor.execute(query_inf, params)
            inf_row = cursor.fetchone()
            
            cursor.execute(query_sup, params)
            sup_row = cursor.fetchone()

        if not inf_row or not sup_row:
            return None 

        inf_val=[inf_row['lectura'],inf_row['medida'],inf_row['incert']]
        sup_val=[sup_row['lectura'],sup_row['medida'],sup_row['incert']]


        if inf_val[0]==sup_val[0]:
            resultado=[0,0,0] + sup_val
        else:
            resultado = inf_val+sup_val
        
        resultado_convertido = [desnormalizar_unidad(val,unidad) for val in resultado]
        return resultado_convertido
    
    finally:
        conn.close()

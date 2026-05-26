import sqlite3
from services.data_processing import normalizar_unidad,desnormalizar_unidad

DB_INTERP_NAME='data/interpolation/interpolation.db'

def interpol_search_in_db(type_table:str,valor:float,unidad:str,frecuencia=None):
    """Busqueda en db de puntos inferior y superior para la interpolacion"""
    conn = sqlite3.connect(DB_INTERP_NAME)
    cursor= conn.cursor()
    
    if 'ac' in type_table and frecuencia is not None:
        if frecuencia != '60 Hz':
            frecuencia='1 kHz'

    busqueda = normalizar_unidad(valor,unidad)
       
    
    query_inf = f"SELECT lectura, medida, incert FROM {type_table} WHERE lectura <= ? AND (frecuencia = ? OR frecuencia IS NULL) ORDER BY lectura DESC LIMIT 1"

    query_sup = f"SELECT lectura, medida, incert FROM {type_table} WHERE lectura >= ? AND (frecuencia = ? OR frecuencia IS NULL) ORDER BY lectura ASC LIMIT 1"
    
    params = (busqueda, frecuencia)
    
    cursor.execute(query_inf, params)
    inf = cursor.fetchone()
    
    cursor.execute(query_sup, params)
    sup = cursor.fetchone()

    if not inf or not sup:
        conn.close()
        return None 

    list_inf= list(inf)
    list_sup= list(sup)

   
    if list_inf[0]==list_sup[0]:
        resultado=[0,0,0] + list_sup
    else:
        resultado = list(inf) + list(sup)
    
    
    resultado_convertido = []
    for val in resultado:
        resultado_convertido.append(desnormalizar_unidad(val, unidad))
        
    return resultado_convertido


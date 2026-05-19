import sqlite3

DB_INTERP_NAME='data/interpolation/interpolation.db'


def normalizar_unidad(value, magnitud):
    """Convierte cualquier unidad a la unidad base (V, A, Ohm)."""
    conversiones = {
        "mV": 1e-3, "µV": 1e-6,
        "mA": 1e-3, "µA": 1e-6,
        "Ω": 1, "kΩ": 1e3, "MΩ": 1e6,
        "V": 1, "A": 1
    }
    return value * conversiones.get(magnitud, 1)

def desnormalizar_unidad(valor, multiplicador):
    """Convierte de la unidad base a la unidad de salida deseada."""
    mult = str(multiplicador).strip() if multiplicador else ""
    conversiones = {
        "mV": 1e3, "µV": 1e6,
        "mA": 1e3, "µA": 1e6,
        "Ω": 1, "kΩ": 1e-3, "MΩ": 1e-6,
        "V": 1, "A": 1
    }
    return valor * conversiones.get(mult, 1)


def interpol_search_in_db(type_table:str,valor:float,unidad:str,frecuencia=None):

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


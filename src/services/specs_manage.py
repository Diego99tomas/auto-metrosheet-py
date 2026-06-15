from database.connection import get_connection,SPECS_DB_PATH
from utility.data_processing import normalizar_unidad
from config.constants import Functions
from models.show_spec import ShowSpec
from config.exceptions import (FrequencyRequiredError,
                                   FrequencyNotRequiredError,
                                   BobinaOnlyInCorrienteError,
                                   DecimalValueError,
                                   IncorrectCoilUseError)
from config.constants import( FUNCTIONS_NO_FQ,
                            FUNCTIONS_CORRIENTE,
                            FUNCTIONS_NEED_FQ)
import sqlite3 


def insert_in_db_specs(function:Functions, spec:ShowSpec, decimal_final:float, show_spec_final:float):
    
    value=normalizar_unidad(spec.valor,spec.unidad)
    decimal_norma=normalizar_unidad(decimal_final,spec.unidad)

    sql=f"INSERT OR ABORT INTO {function} ('valor','unidad','frecuencia','decimales','show_spec','lcomp') VALUES (?, ?, ?, ?, ?, ?)"
    params=(value,spec.unidad,spec.frecuencia,decimal_norma,show_spec_final,spec.lcomp)

    try:  
        with get_connection(SPECS_DB_PATH) as conn:
            cursor=conn.cursor()
            cursor.execute(sql,params)
            conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error de SQLite durante migración: {e}")
        raise
    except Exception as e:
        print(f"Error inesperado al procesar datos: {e}")
        raise


def spec_validation(function:Functions,spec:ShowSpec):
    """Valida que los parámetros de la especificación cumplan con las reglas de negocio."""

    if function in FUNCTIONS_NO_FQ and spec.frecuencia:
        raise FrequencyNotRequiredError(function)

    if function in FUNCTIONS_NEED_FQ and not spec.frecuencia:
        raise FrequencyRequiredError(function)
    
    if spec.lcomp and not function in FUNCTIONS_CORRIENTE:
        raise BobinaOnlyInCorrienteError()

    if spec.lcomp and spec.unidad != "A":
        raise IncorrectCoilUseError()    
    
    if not (0<spec.cantidad_de_decimales<=7):
        raise DecimalValueError() 
    

def spec_transform(spec:ShowSpec)->tuple[float,float]:   
    """Transforma y calcula los valores numéricos finales de la especificación.""" 

    decimal_final=10**-spec.cantidad_de_decimales
    show_spec_final=spec.show_spec/100
    return decimal_final,show_spec_final


def add_show_spec(function:Functions,spec:ShowSpec):
    """Orquesta la validación, transformación y persistencia de la especificación."""
    
    spec_validation(function,spec)
    decimal_final,show_spec_final=spec_transform(spec)
    insert_in_db_specs(function, spec,decimal_final, show_spec_final)
    
   

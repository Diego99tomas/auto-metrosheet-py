import sqlite3
from services.interpo_search import normalizar_unidad,desnormalizar_unidad

def specs_search_in_db(type_table:str,value:float,unid:str, frec=None):
    DB_PATH='data/specs/specs.db'

    is_ac= 'ac' in type_table
    
    busqueda=normalizar_unidad(value,unid)
    
    if type_table == "voltaje_dc":
        busqueda=normalizar_unidad(abs(value),unid)
    
    
    if is_ac:
        query= f"SELECT decimales,show_spec FROM {type_table} WHERE valor=? AND frecuencia=?"
        params=(busqueda,frec)
        
    else:   
        query= f"SELECT decimales,show_spec FROM {type_table} WHERE valor=? "
        params=(busqueda,)

    
    with sqlite3.connect(DB_PATH) as conn:
        cursor=conn.cursor()
        cursor.execute(query,params)
        resultado=cursor.fetchone()
       

    
    if not resultado:
        return (0,0)
    
    decimal = desnormalizar_unidad(resultado[0],unid)
    return [decimal,resultado[1]]
  

# resl=specs_search_in_db('voltaje_dc',0.4,'V')
# print(resl)



























# from openpyxl import load_workbook
# nombre_archivo="SHOW SPEC.xlsx"



# try:
#     libro_cargado=load_workbook(filename=nombre_archivo)
#     print('Archivo cargado')
    
# except FileNotFoundError:
#     print(f'No se encontro el archivo. Verificar {nombre_archivo}')


# def busqueda_showespc(tipo:str,punto_buscado:float, multiplicador:str,frecuencia="")->tuple:
       
#     ws=libro_cargado[f'{tipo}']

#     if tipo[-2:]=="DC" or tipo=="RESISTENCIAS":
#         for lista in ws.iter_rows(min_row=3,max_row=38,min_col=4,max_col=7,values_only=True): 
#             if punto_buscado == lista[0] and multiplicador==lista[1]:
#                 return lista[2],lista[3]
           
#         print(f"No existe el valor buscado {punto_buscado}-{multiplicador}, ingresar")
        
#     elif tipo[-2:]=="AC":
#         for lista in ws.iter_rows(min_row=3,max_row=39,min_col=4,max_col=8,values_only=True):
#             if punto_buscado == lista[0] and multiplicador==lista[1] and frecuencia==lista[2]:
#                 return lista[3],lista[4]     
        
#         print(f"No existe el valor buscado {punto_buscado}-{multiplicador} {frecuencia}, ingresar")

#     return(0,0)
                
            

# abc=busqueda_showespc("RESISTENCIAS",0.4,"MΩ")

# print(abc)
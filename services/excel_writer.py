from services.interpo_search import interpol_search_in_db
from services.specs_search import specs_search_in_db
from services.cmc_verify import cmc_verification
from models.range_parser import RangeParser

    
def fill_excel_data(layout_excel:dict,wb, function_name:str, ranges_list:list[str], mid_index:int|None,frecuencias:list[str]|list[None]):
    """Rellena los rangos, los decimales y el show spec en hoja de medicion. Interpolacion en hoja de calculo"""

    EXCEL_LAYOUT=layout_excel
    datos_sheet=wb['HOJA DE DATOS DE MEDICION']
    calc_sheet=wb["HOJA DE CALCULO"]

    if function_name in ['voltaje_dc','corriente_dc','resistencias']:
        frecuencias=[None]
    

    layout = EXCEL_LAYOUT.get(function_name)
    if not layout:
        return 
    
    current_row = layout['start_row']
    #Buscando punto medio si existe
    mid_val, mid_unit = RangeParser.parse(ranges_list[mid_index]) if mid_index is not None else (None, None)

    for item in ranges_list:
        val, unit = RangeParser.parse(item)
        if val is None or unit is None:
            continue
        
        #Verificar si es punto medio o punto normal
        if mid_val is not None and val == mid_val and mid_unit==unit and 'mid_row' in layout:
            target_row_start = layout['mid_row']
            next_row_logic = layout['after_mid']
            puntos = layout['mid_point']
        else:
            target_row_start = current_row
            next_row_logic = current_row + layout['step']
            puntos = layout['normal_point']
        
        
        # Escribir Valor y Unidad (Columnas B y C)
        datos_sheet.cell(row=target_row_start, column=2, value=val)
        datos_sheet.cell(row=target_row_start, column=3, value=unit)

        # Bucle de puntos y frecuencias
        # Usamos un contador global de filas para este rango específico
        row_offset = 0
        for p in puntos:
            
            for freq in frecuencias:
                punto_buscado=val*p
                
                if item == ranges_list[0]:
                    punto_buscado=cmc_verification(function_name,punto_buscado,unit)

                actual_row = target_row_start + row_offset
                
                # Escribir Frecuencia (Columna F) si existe
                if freq:
                    datos_sheet.cell(row=actual_row, column=6, value=freq)

                decimal, show_espc = specs_search_in_db(function_name, punto_buscado, unit,freq)
                # ESCRITURA EN EXCEL
                datos_sheet.cell(row=actual_row, column=14, value=show_espc)  # Columna N
                datos_sheet.cell(row=actual_row, column=16, value=decimal)    # Columna P
                
                #solo la division entre 50 solo aplica a la interpolacion
                if 'corriente' in function_name and punto_buscado>18:
                    punto_buscado=punto_buscado/50
                interpol=interpol_search_in_db(function_name,punto_buscado,unit,freq)
                
                if interpol:
                    mapping={
                        51:interpol[0],# Lectura Inferior
                        52:interpol[1],# Medida Inferior
                        48:interpol[2],# Incertidumbre Inferior
                        54:interpol[3],# Lectura Superior
                        55:interpol[4],# Medida Superior
                        50:interpol[5]# Incertidumbre Superior
                        }
                    
                    for col, value in mapping.items():
                        calc_sheet.cell(row=actual_row, column=col, value=value)#lectura inferior
                
                row_offset += 1 # Siguiente fila para el siguiente valor/frecuencia
               

        current_row = next_row_logic




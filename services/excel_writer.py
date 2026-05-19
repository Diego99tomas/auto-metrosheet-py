from services.interpo_search import interpol_search_in_db
from services.specs_search import specs_search_in_db
import re


class RangeParser:
    """Utilidad para parsear strings de medidas."""
    
    @staticmethod
    def parse(medida: str):
        # Captura números enteros o decimales y la unidad
        match = re.match(r"([0-9.]+)\s*(.*)", medida)
        if match:
            valor_str, unidad = match.groups()
            valor = float(valor_str) if '.' in valor_str else int(valor_str)
            return valor, unidad
        return None, None
    
def validacion(function_name:str,punto:float,unit:str)->float:
    """VALIDA LOS PUNTOS MINIMOS DE LA CMC"""
    CMC={
    'voltaje_dc':{'min':33,'unit':'mV'},
    'voltaje_ac': {'min':20,'unit':'mV'},
    'corriente_dc':{'min':1,'unit':'mA'},
    'corriente_ac': {'min':1,'unit':'mA'}, 
    'resistencias':{'min':1,'unit':'Ω'}
    }

    cmc_entry=CMC.get(function_name)
    if cmc_entry is None:
        return punto

    if abs(punto) < cmc_entry['min'] and cmc_entry['unit']==unit:
        return float(cmc_entry['min'])
    else:
        return punto
    

def get_layout(type:str):
    """Elige el nuemro de filas correcto para cada tipo de equipo (PINZA O MULT)"""
    EXCEL_LAYOUT = {
    'voltaje_dc':   {'start_row': 41, 'step': 3, 'mid_row': 50, 'after_mid': 55,'normal_point':[0.1,0.9,-0.9],'mid_point':[0.1,-0.1,0.5,0.9,-0.9]},
    'voltaje_ac':   {'start_row': 69, 'step': 2, 'mid_row': 75, 'after_mid': 81,'normal_point':[0.9],'mid_point':[0.1,0.5,0.9]},
    'corriente_dc': {'start_row': 91, 'step': 2, 'mid_row': 97, 'after_mid': 102,'normal_point':[0.1,0.9],'mid_point':[0.1,0.3,0.5,0.7,0.9]},
    'corriente_ac': {'start_row': 113, 'step': 2, 'mid_row': 119, 'after_mid': 124,'normal_point':[0.1,0.9],'mid_point':[0.1,0.3,0.5,0.7,0.9]},
    'resistencias': {'start_row': 135, 'step': 2,'normal_point':[0.1,0.9]}
    }


    if "multimetro" in type:
        MULTI_LAYOUT={
            'corriente_dc': {'start_row': 91, 'step': 2, 'mid_row': 97, 'after_mid': 100,'normal_point':[0.1,0.9],'mid_point':[0.1,0.9,-0.9]},
            'corriente_ac': {'start_row': 113, 'step': 2, 'mid_row': 119, 'after_mid': 121,'normal_point':[0.9],'mid_point':[0.9]},
            'resistencias': {'start_row': 131, 'step': 2,'normal_point':[0.1,0.9]}
        }
        
        return {**EXCEL_LAYOUT,**MULTI_LAYOUT}
    
    return EXCEL_LAYOUT

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
    mid_val, _ = RangeParser.parse(ranges_list[mid_index]) if mid_index is not None else (None, None)

    for item in ranges_list:
        val, unit = RangeParser.parse(item)
        if val is None or unit is None:
            continue
        
        #Verificar si es punto medio o punto normal
        if mid_val is not None and val == mid_val and 'mid_row' in layout:
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

        # 3. Bucle de puntos y frecuencias
        # Usamos un contador global de filas para este rango específico
        row_offset = 0
        for p in puntos:
            
            for freq in frecuencias:
                punto_buscado=val*p
                
                if item == ranges_list[0]:
                    punto_buscado=validacion(function_name,punto_buscado,unit)

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




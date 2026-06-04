
def get_layout(type:str):
    """Elige el numero de filas correcto para cada tipo de equipo (PINZA O MULTIMETRO)"""
    EXCEL_LAYOUT = {
    'voltaje_dc':   {'start_row': 41, 'step': 3, 'mid_row': 50, 'after_mid': 55,'normal_point':[0.1,0.9,-0.9],'mid_point':[0.1,-0.1,0.5,0.9,-0.9],'final_row':63},
    'voltaje_ac':   {'start_row': 69, 'step': 2, 'mid_row': 75, 'after_mid': 81,'normal_point':[0.9],'mid_point':[0.1,0.5,0.9],'final_row':86},
    'corriente_dc': {'start_row': 91, 'step': 2, 'mid_row': 97, 'after_mid': 102,'normal_point':[0.1,0.9],'mid_point':[0.1,0.3,0.5,0.7,0.9],'final_row':107,'is_pinza':True},
    'corriente_ac': {'start_row': 113, 'step': 2, 'mid_row': 119, 'after_mid': 124,'normal_point':[0.1,0.9],'mid_point':[0.1,0.3,0.5,0.7,0.9],'final_row':129,'is_pinza':True,
                     'lcomp':True},
    'resistencias': {'start_row': 135, 'step': 2,'normal_point':[0.1,0.9],'final_row':152}
    }


    if "multimetro" in type:
        MULTI_LAYOUT={
            'corriente_dc': {'start_row': 91, 'step': 2, 'mid_row': 97, 'after_mid': 100,'normal_point':[0.1,0.9],'mid_point':[0.1,0.9,-0.9],'final_row':105,
                             "special_point":[0.5,0.9],'is_mult':True,'special_unit':'A'},
            'corriente_ac': {'start_row': 111, 'step': 2, 'mid_row': 119, 'after_mid': 121,'normal_point':[0.9],'mid_point':[0.9],'final_row':124},
            'resistencias': {'start_row': 129, 'step': 2,'normal_point':[0.1,0.9],'final_row':148}
        }
        
        return {**EXCEL_LAYOUT,**MULTI_LAYOUT}
    
    return EXCEL_LAYOUT
from config.constants import TypeEquipment,FUNCTIONS_NEED_FQ,TEMPLATES
from config.exceptions import (FrequencyRequiredError,
                                   MidPointOutRangeError,
                                   MissingUnitOrValueError)
from config.layout import get_layout
from utility.excel_writer import fill_excel_data
from utility.hide_rows import hide_rows
from utility.range_parser import parse
from models.equipo import Equipment
from openpyxl import load_workbook

def template_validation(funciones:dict[str,list[str]],indices:dict[str,int|None],frecuencias:dict):

    for key,value in funciones.items():
        cant_rangos=len(value)
        cant_indic=indices.get(key)

        if cant_indic:
            if cant_indic>cant_rangos:
                raise MidPointOutRangeError(key.upper())
 
        if key in FUNCTIONS_NEED_FQ and not frecuencias.get(key):
            raise FrequencyRequiredError(key.upper())
        
        for k in value:
            val,unit=parse(k)
            if not val or not unit:
                raise MissingUnitOrValueError(key.upper())
            
def get_template(tipo_de_equipo:TypeEquipment):
    name=TEMPLATES.get(tipo_de_equipo)
    layout=get_layout(tipo_de_equipo)
    
    if not name:
        raise Exception("No se encontro una plantilla")
    
    wb=load_workbook(name,keep_vba=True)
    return wb,layout    
     
            
def create_new_template(equipo:Equipment,funciones,indices,frecuencias):
        NAME_WB = f'{equipo.type} {equipo.manufacturer} {equipo.model},ns {equipo.serie}'
        template_validation(funciones,indices,frecuencias)
        
        wb,layout=get_template(equipo.type)

        for func_name, ranges in funciones.items():
            mid_idx = indices.get(func_name)
            fill_excel_data(layout,wb, func_name, ranges, mid_idx,frecuencias[func_name])
            hide_rows(wb,layout,func_name)    
        
        wb.save(f'{NAME_WB}.xlsm')
        print(f"Archivo guardado como: {NAME_WB}")



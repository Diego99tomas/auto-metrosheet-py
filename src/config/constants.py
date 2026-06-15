from enum import StrEnum
import os 

class TypeEquipment(StrEnum):
    PINZA="PINZA MULTIMETRICA"
    MULTIMETRO="MULTIMETRO DIGITAL"


class Functions(StrEnum):
    VOLTAJE_DC= "voltaje_dc"
    VOLTAJE_AC= "voltaje_ac"
    CORRIENTE_DC= "corriente_dc"
    CORRIENTE_AC = "corriente_ac"
    RESISTENCIAS= "resistencias"


FUNCTIONS_NO_FQ={Functions.VOLTAJE_DC,Functions.CORRIENTE_DC,Functions.RESISTENCIAS}
FUNCTIONS_NEED_FQ={Functions.VOLTAJE_AC,Functions.CORRIENTE_AC}
FUNCTIONS_CORRIENTE={Functions.CORRIENTE_AC,Functions.CORRIENTE_DC}

TEMPLATE_MULTIMETRO=os.path.join('src','templates','plantilla multimetros.xlsm')
TEMPLATE_PINZA=os.path.join('src','templates','plantilla pinzas multimetricas.xlsm')

TEMPLATES={TypeEquipment.MULTIMETRO:TEMPLATE_MULTIMETRO,
           TypeEquipment.PINZA:TEMPLATE_PINZA}
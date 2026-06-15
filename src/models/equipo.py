from dataclasses import dataclass
from config.constants import TypeEquipment

@dataclass
class Equipment:
    type: TypeEquipment
    manufacturer: str
    model: str
    serie: str



    



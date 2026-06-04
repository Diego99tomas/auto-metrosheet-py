from dataclasses import dataclass

@dataclass
class ShowSpec:
    valor: float
    unidad: str
    decimales: float
    show_spec: str
    frecuencia: str|None=None
    lcomp:int|None=None



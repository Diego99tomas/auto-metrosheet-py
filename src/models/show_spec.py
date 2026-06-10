from dataclasses import dataclass

@dataclass(frozen=True)
class ShowSpec:
    valor: float
    unidad: str
    cantidad_de_decimales: int
    show_spec: float
    frecuencia: str|None=None
    lcomp:int|None=None



import re

def parse(medida: str):
    """Utilidad para parsear strings de medidas."""
    # Captura números enteros o decimales y la unidad
    match = re.match(r"([0-9.]+)\s*(.*)", medida)
    if match:
        valor_str, unidad = match.groups()
        valor = float(valor_str) if '.' in valor_str else int(valor_str)
        return valor, unidad
    return None, None
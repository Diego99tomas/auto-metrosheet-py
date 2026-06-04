def normalizar_unidad(value, magnitud):
    """Convierte cualquier unidad a la unidad base (V, A, Ohm)."""
    conversiones = {
        "mV": 1e-3, "µV": 1e-6,
        "mA": 1e-3, "µA": 1e-6,
        "Ω": 1, "kΩ": 1e3, "MΩ": 1e6,
        "V": 1, "A": 1
    }
    return value * conversiones.get(magnitud, 1)

def desnormalizar_unidad(valor, multiplicador):
    """Convierte de la unidad base a la unidad de salida deseada."""
    mult = str(multiplicador).strip() if multiplicador else ""
    conversiones = {
        "mV": 1e3, "µV": 1e6,
        "mA": 1e3, "µA": 1e6,
        "Ω": 1, "kΩ": 1e-3, "MΩ": 1e-6,
        "V": 1, "A": 1
    }
    return valor * conversiones.get(mult, 1)
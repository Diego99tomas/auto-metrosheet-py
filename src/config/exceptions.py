
class FrequencyRequiredError(Exception):
    """Se lanza cuando falta la frecuencia en una función AC."""
    def __init__(self, func, message="Se requiere frecuencia en la función"):
        self.func = func
        super().__init__(f"{message}: {func}")

class FrequencyNotRequiredError(Exception):
    """Se lanza cuando se incluye frecuencia en una función que no la lleva."""
    def __init__(self, func, message="No se requiere frecuencia en"):
        self.func = func
        super().__init__(f"{message}: {func}")
        
class BobinaOnlyInCorrienteError(Exception):
    """Se lanza si se usa la bobina fuera de la función de Corriente."""
    def __init__(self, message="La bobina solo se usa en Corriente"):
        super().__init__(message)

class DecimalValueError(Exception):
    """Se lanza cuando se supera el límite de decimales permitido."""
    def __init__(self, message="Verifique los decimales"):
        super().__init__(message)

class IncorrectCoilUseError(Exception):
    """Se lanza si la bobina se usa en corrientes menores a 4A."""
    def __init__(self, message="La bobina solo se usa para valores >= 4A"):
        super().__init__(message)


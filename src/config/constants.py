from enum import StrEnum

class Functions(StrEnum):
    VOLTAJE_DC= "voltaje_dc"
    VOLTAJE_AC= "voltaje_ac"
    CORRIENTE_DC= "corriente_dc"
    CORRIENTE_AC = "corriente_ac"
    RESISTENCIAS= "resistencias"

    @property
    def label(self)->str:
        """Formatea el valor del enum para mostrarlo en la UI."""
        text=self.value.replace("_"," ").capitalize()
        text=text.replace(" dc"," DC").replace(" ac"," AC")
        return text


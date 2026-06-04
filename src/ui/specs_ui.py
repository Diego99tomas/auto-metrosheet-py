import customtkinter as ctk
from src.config.constants import Functions


UNIDADES_MAP = {
    Functions.VOLTAJE_DC:   ['mV', 'V'],
    Functions.VOLTAJE_AC:   ['mV', 'V'],
    Functions.CORRIENTE_DC: ['µA', 'mA', 'A'],
    Functions.CORRIENTE_AC: ['µA', 'mA', 'A'],
    Functions.RESISTENCIAS: ['Ω', 'kΩ', 'MΩ']
}

class FrameSpecs(ctk.CTkFrame):
    def __init__(self, parent, navegar_callback):
        super().__init__(parent)
        self.navegar = navegar_callback
        
        # Botón Volver
        ctk.CTkButton(
            self, text="← Volver al Menú", fg_color="transparent", 
            text_color=("black", "white"), hover_color=("#dbdbdb", "#2b2b2b"),
            command=lambda: self.navegar("menu")
        ).pack(pady=(10, 0), padx=20, anchor="w")
        
        # Título
        ctk.CTkLabel(self, text="INGRESE SPEC DEL PATRÓN", font=('Arial', 14, 'bold')).pack(pady=(15, 5), padx=20, anchor="w")
        
        # Dropdowns (Función y Unidad)
        funciones_lista = [func.value for func in Functions]
        self.function = ctk.CTkOptionMenu(self, values=funciones_lista, command=self._on_funcion_change)
        self.function.pack(pady=10, padx=20, fill="x")
       
        self.unit = ctk.CTkOptionMenu(self, values=[])
        self.unit.pack(pady=10, padx=20, fill="x")
        

        self._on_funcion_change(funciones_lista[0])

       
        self.frecuencia = ctk.CTkEntry(self, placeholder_text="Frecuencia (Hz)")
        self.frecuencia.pack(pady=10, padx=20, fill="x")
        
        self.decimal = ctk.CTkEntry(self, placeholder_text="Cantidad de Decimales")
        self.decimal.pack(pady=10, padx=20, fill="x")
        
        self.show_spec = ctk.CTkEntry(self, placeholder_text="Valor de Spec")
        self.show_spec.pack(pady=10, padx=20, fill="x")
        
        # Botón guardar
        ctk.CTkButton(self, text="Guardar", command=self._guardar).pack(pady=20, padx=20, fill="x")

    def _on_funcion_change(self, seleccion):
        value_unit = UNIDADES_MAP.get(Functions(seleccion))
        if value_unit:
            self.unit.configure(values=value_unit)
            self.unit.set(value_unit[0])
            

    def _guardar(self):
        # Aquí puedes agregar lógica para leer los campos con self.show_spec.get(), etc.
        pass
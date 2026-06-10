import customtkinter as ctk
from src.config.constants import Functions
from src.models.show_spec import ShowSpec
from src.services.specs_manage import add_show_spec


UNIDADES_MAP = {
    Functions.VOLTAJE_DC:   ['mV', 'V'],
    Functions.VOLTAJE_AC:   ['mV', 'V'],
    Functions.CORRIENTE_DC: ['µA', 'mA', 'A'],
    Functions.CORRIENTE_AC: ['µA', 'mA', 'A'],
    Functions.RESISTENCIAS: ['Ω', 'kΩ', 'MΩ']
}

class FrameSpecs(ctk.CTkFrame):
    def __init__(self, parent, navegar_callback):
        super().__init__(parent, fg_color="transparent") 
        self.navegar = navegar_callback
        
        #
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkButton(
            self.header_frame, text="← Volver al Menú", fg_color="transparent", 
            text_color=("black", "white"), hover_color=("#dbdbdb", "#2b2b2b"),
            width=100, command=lambda: self.navegar("menu")
        ).pack(side="left")
        
        
        ctk.CTkLabel(
            self, text="INGRESE SPEC DEL PATRÓN", 
            font=('Segoe UI', 18, 'bold') # Tipografía más moderna
        ).pack(pady=(10, 15), padx=25, anchor="w")
        
      
        self.form_frame = ctk.CTkFrame(self, corner_radius=12)
        self.form_frame.pack(fill="both", expand=True, padx=25, pady=10)
        
        
        self.form_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.form_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        
        
        funciones_lista = [func.value for func in Functions]
        
        self.crear_etiqueta(self.form_frame, "Función:", 0, 0)
        self.function = ctk.CTkOptionMenu(self.form_frame, values=funciones_lista, command=self._on_funcion_change)
        self.function.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
       
        self.crear_etiqueta(self.form_frame, "Unidad:", 0, 1)
        self.unit = ctk.CTkOptionMenu(self.form_frame, values=[])
        self.unit.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="ew")
        
        self._on_funcion_change(funciones_lista[0])


        self.crear_etiqueta(self.form_frame, "Valor:", 2, 0)
        self.valor = ctk.CTkEntry(self.form_frame, placeholder_text="Ej: 10.5")
        self.valor.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="ew")
       
        self.crear_etiqueta(self.form_frame, "Frecuencia:", 2, 1)
        self.frecuencia = ctk.CTkOptionMenu(self.form_frame, values=["", "60 Hz", "400 Hz", "500 Hz", "1 kHz"])
        self.frecuencia.grid(row=3, column=1, padx=15, pady=(0, 15), sticky="ew")
        
        
        self.crear_etiqueta(self.form_frame, "Cantidad de Decimales:", 4, 0)
        self.decimal = ctk.CTkEntry(self.form_frame, placeholder_text="Ej: 2")
        self.decimal.grid(row=5, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        self.crear_etiqueta(self.form_frame, "Valor de Spec:", 4, 1)
        self.show_spec = ctk.CTkEntry(self.form_frame, placeholder_text="show spec del patrón")
        self.show_spec.grid(row=5, column=1, padx=15, pady=(0, 15), sticky="ew")
        
     
        self.bobina = ctk.CTkCheckBox(self.form_frame, text="¿Requiere uso de bobina?")
        self.bobina.grid(row=6, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

  
        self.lbl_error = ctk.CTkLabel(
            self.form_frame, text="", 
            text_color="#ff4d4d", font=('Segoe UI', 12, 'bold')
        )
      
        self.lbl_error.grid(row=7, column=0, columnspan=2, padx=15, pady=(5, 5), sticky="ew")
        
      
        self.btn_guardar = ctk.CTkButton(
            self.form_frame, text="Guardar Configuración", 
            font=('Segoe UI', 14, 'bold'), height=40,
            command=self._guardar
        )
        self.btn_guardar.grid(row=8, column=0, columnspan=2, padx=15, pady=(5, 20), sticky="ew")



    def crear_etiqueta(self, master, texto, fila, columna):
        """Función auxiliar para mantener las etiquetas del formulario uniformes"""
        lbl = ctk.CTkLabel(master, text=texto, font=('Segoe UI', 12), text_color=("#555555", "#aaaaaa"))
        lbl.grid(row=fila, column=columna, padx=15, pady=(10, 2), sticky="w")


    def _on_funcion_change(self, seleccion):
        value_unit = UNIDADES_MAP.get(Functions(seleccion))
        if value_unit:
            self.unit.configure(values=value_unit)
            self.unit.set(value_unit[0])
            
    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error en la interfaz."""
        self.lbl_error.configure(text=mensaje, text_color="red")
        self.after(3000, lambda: self.lbl_error.configure(text=""))
    
    def _mostrar_exito(self, mensaje):
        """Muestra un mensaje de error en la interfaz."""
        self.lbl_error.configure(text=mensaje, text_color="green")
        self.after(3000, lambda: self.lbl_error.configure(text=""))

    def _use_bobina(self):
        """Asigna el valor 1 si es corriente ac sino None"""
        val_bobina=int(self.bobina.get())
        return val_bobina if val_bobina < 1 and self.function==Functions.CORRIENTE_AC else None
        
    def _guardar(self):
        self.lbl_error.configure(text="")

        txt_funcion=Functions(self.function.get())
        txt_valor=self.valor.get().strip()
        txt_decimales=self.decimal.get().strip()
        txt_show_spec=self.show_spec.get().strip()
        txt_frecuencia=self.frecuencia.get().strip()

        val_lcomp=self._use_bobina()

        if not txt_valor or not txt_decimales or not txt_show_spec:
            self._mostrar_error("Error: Todos los campos obligatorios deben ser llenados.")
            return
        
        try:
            valor_num = float(txt_valor)
            valor_spec = float(txt_show_spec)
        except ValueError:
            self._mostrar_error("Error: El 'Valor' debe ser un número válido.")
            return

        try:
            decimales_num = int(txt_decimales)
        except ValueError:
            self._mostrar_error("Error: 'Cantidad de Decimales' debe ser un número entero.")
            return

        try:
            new_spec = ShowSpec(
                valor=valor_num,
                unidad=self.unit.get(),
                cantidad_de_decimales=decimales_num,
                show_spec=valor_spec,
                frecuencia=txt_frecuencia if txt_frecuencia else None,
                lcomp=val_lcomp
            )

            add_show_spec(txt_funcion,new_spec)
            self._mostrar_exito("Show Spec guardado exitosamente.")
            
            self._limpiar_formulario()
            
        except Exception as e:
            self._mostrar_error(f"Error: {e}")

    def _limpiar_formulario(self):
        """Limpia las entradas de texto tras un guardado exitoso."""
        self.valor.delete(0, 'end')
        self.decimal.delete(0, 'end')
        self.show_spec.delete(0, 'end')   
        

        
from src.config.constants import Functions
from src.models.equipo import Equipment
import customtkinter as ctk 



class FramePlantilla(ctk.CTkFrame):
    def __init__(self, parent, navegar_callback):
        super().__init__(parent)
        self.navegar = navegar_callback

        ctk.CTkButton(self, text="← Volver al Menú", fg_color="transparent", 
                      text_color=("black", "white"), hover_color=("#dbdbdb", "#2b2b2b"),
                      command=lambda: self.navegar("menu")).pack(pady=(10, 0), padx=20, anchor="w")

        # --- DATOS DEL EQUIPO ---
        ctk.CTkLabel(self, text="DATOS DEL EQUIPO", font=('Arial', 14, 'bold')).pack(pady=(10, 5), padx=20, anchor="w")
        
        frame_eq = ctk.CTkFrame(self)
        frame_eq.pack(pady=5, padx=20, fill="x")

        self.eq_vars = {}
        fields = [('Tipo', 'type'), ('Fabricante', 'manufacturer'), ('Modelo', 'model'), 
                  ('Serie', 'serie')]
        
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(frame_eq, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
  
            var = ctk.StringVar()
            ctk.CTkEntry(frame_eq, textvariable=var).grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.eq_vars[key] = var
        frame_eq.columnconfigure(1, weight=1)

        # --- FUNCIONES Y RANGOS ---

        ctk.CTkLabel(self, text="FUNCIONES, RANGOS Y FRECUENCIAS", font=('Arial', 14, 'bold')).pack(pady=(15, 5), padx=20, anchor="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.function_widgets = {}
        self.lista_funciones = Functions

        for func in self.lista_funciones:
            self._create_function_row(func.label)

        # --- BOTONES ---
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", pady=15, padx=20)


        ctk.CTkButton(btn_frame, text="PROCESAR DATOS", command=self.get_all_data, height=35).pack(side="left", expand=True, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="LIMPIAR TODO", command=self.clear_form, height=35, fg_color="gray", hover_color="darkgray").pack(side="right", expand=True, padx=10, pady=10)

    def _create_function_row(self, func_name):
      
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(fill="x", pady=5, padx=5)
        
        frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text=func_name.upper(), font=('Arial', 11, 'bold')).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        enabled_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(frame, text="Activar", variable=enabled_var).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Rangos (sep. por coma):").grid(row=2, column=0, sticky="w", padx=10, pady=2)

        range_var = ctk.StringVar()
        ctk.CTkEntry(frame, textvariable=range_var).grid(row=2, column=1, sticky="ew", padx=10, pady=2)
        
        # Valor por defecto inicial
        if 'resistencias' in func_name:
            range_var.set("60Ω, 600Ω")

        ctk.CTkLabel(frame, text="Punto Medio:").grid(row=3, column=0, sticky="w", padx=10, pady=2)

        index_var = ctk.StringVar()
        ctk.CTkEntry(frame, textvariable=index_var, width=60).grid(row=3, column=1, sticky="w", padx=10, pady=2)


        freq_var = ctk.StringVar()
        if 'ac' in func_name:
            ctk.CTkLabel(frame, text="Frecuencias:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
            ctk.CTkEntry(frame, textvariable=freq_var).grid(row=4, column=1, sticky="ew", padx=10, pady=2)
            
            # Valores por defecto iniciales
            if func_name == 'voltaje_ac': 
                freq_var.set("60 Hz, 400 Hz")
            else: 
                freq_var.set("60 Hz")

        self.function_widgets[func_name] = {
            'enabled': enabled_var,
            'ranges': range_var,
            'index': index_var,
            'freq': freq_var
        }

    def clear_form(self):
        """Limpia todos los campos de la interfaz"""
        for var in self.eq_vars.values():
            var.set("")

        for func_name, widgets in self.function_widgets.items():
            widgets['enabled'].set(False)
            widgets['ranges'].set("")
            widgets['index'].set("")
            
            if 'ac' in func_name:
                if func_name == 'voltaje_ac': 
                    widgets['freq'].set("60 Hz, 400 Hz")
                else: 
                    widgets['freq'].set("60 Hz")
            else:
                widgets['freq'].set("")
                if 'resistencias' in func_name:
                    widgets['ranges'].set("60Ω, 600Ω")
        
        print("Formulario reseteado.")

    def get_all_data(self):
        
        try:
            equipo = Equipment(
                type=self.eq_vars['type'].get().lower(),
                manufacturer=self.eq_vars['manufacturer'].get(),
                model=self.eq_vars['model'].get(),
                serie=self.eq_vars['serie'].get()
            )
        except NameError:
            print("Error: La clase 'Equipment' no está definida en este script.")
            return

        final_funciones_rangos = {}
        final_mapeo_indices = {}
        final_frecuencias = {}

        for func, widgets in self.function_widgets.items():
            if widgets['enabled'].get():
                raw_ranges = widgets['ranges'].get()
                ranges_list = [r.strip() for r in raw_ranges.split(',') if r.strip()]
                final_funciones_rangos[func] = ranges_list

                idx = widgets['index'].get()
                final_mapeo_indices[func] = int(idx)-1 if idx.isdigit() else None

                if 'ac' in func:
                    raw_freq = widgets['freq'].get()
                    final_frecuencias[func] = [f.strip() for f in raw_freq.split(',') if f.strip()]
                else:
                    final_frecuencias[func] = None
                    
        print("Datos procesados con éxito.")
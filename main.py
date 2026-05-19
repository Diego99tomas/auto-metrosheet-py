import tkinter as tk
from models.equipo import Equipment
from tkinter import ttk, messagebox
from openpyxl import load_workbook
from services.excel_writer import fill_excel_data,get_layout


class EquipmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Equipo y Funciones")
        self.root.geometry("620x850")

        # DATOS DEL EQUIPO 
        tk.Label(root, text="DATOS DEL EQUIPO", font=('Arial', 12, 'bold')).pack(pady=10)
        frame_eq = tk.Frame(root)
        frame_eq.pack(pady=5, padx=20, fill="x")

        self.eq_vars = {}
        fields = [('Tipo', 'type'), ('Fabricante', 'manufacturer'), ('Modelo', 'model'), 
                  ('Especificaciones', 'specs'), ('Serie', 'serie')]
        
        for i, (label, key) in enumerate(fields):
            tk.Label(frame_eq, text=label).grid(row=i, column=0, sticky="w")
            var = tk.StringVar()
            tk.Entry(frame_eq, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.eq_vars[key] = var
        frame_eq.columnconfigure(1, weight=1)

        # FUNCIONES Y RANGOS 
        tk.Label(root, text="FUNCIONES, RANGOS Y FRECUENCIAS", font=('Arial', 12, 'bold')).pack(pady=10)

        canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        self.function_widgets = {}
        self.lista_funciones = ['voltaje_dc', 'voltaje_ac', 'corriente_dc', 'corriente_ac', 'resistencias']

        for func in self.lista_funciones:
            self._create_function_row(func)

        # BOTONES 
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", pady=10, padx=20)

        tk.Button(btn_frame, text="PROCESAR DATOS", command=self.get_all_data, bg="#2ecc71", fg="white", height=2, width=20).pack(side="left", expand=True, padx=5)
        tk.Button(btn_frame, text="LIMPIAR TODO", command=self.clear_form, bg="#e74c3c", fg="white", height=2, width=20).pack(side="right", expand=True, padx=5)

    def _create_function_row(self, func_name):
        frame = tk.LabelFrame(self.scrollable_frame, text=func_name.upper(), padx=10, pady=10)
        frame.pack(fill="x", pady=5, padx=5, expand=True)

        enabled_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, text="Activar", variable=enabled_var).grid(row=0, column=0, sticky="w")

    
        label_text = "Rangos (sep. por coma):"
        
        tk.Label(frame, text=label_text).grid(row=1, column=0, sticky="w")
        range_var = tk.StringVar()
        tk.Entry(frame, textvariable=range_var, width=40).grid(row=1, column=1, padx=5)
        if 'resistencias' in func_name:
            range_var.set("60Ω, 600Ω")

        tk.Label(frame, text="Punto Medio:").grid(row=2, column=0, sticky="w")
        index_var = tk.StringVar()
        tk.Entry(frame, textvariable=index_var, width=5).grid(row=2, column=1, sticky="w", padx=5)

        freq_var = tk.StringVar()
        if 'ac' in func_name:
            tk.Label(frame, text="Frecuencias:").grid(row=3, column=0, sticky="w")
            tk.Entry(frame, textvariable=freq_var, width=30).grid(row=3, column=1, sticky="w", padx=5)
            # Valores por defecto
            if func_name == 'voltaje_ac': freq_var.set("60 Hz, 400 Hz")
            else: freq_var.set("60 Hz")

        self.function_widgets[func_name] = {
            'enabled': enabled_var,
            'ranges': range_var,
            'index': index_var,
            'freq': freq_var
        }

    def clear_form(self):
        """Limpia todos los campos de la interfaz"""
        # Limpiar datos del equipo
        for var in self.eq_vars.values():
            var.set("")

        # Limpiar funciones
        for func_name, widgets in self.function_widgets.items():
            widgets['enabled'].set(False)
            widgets['ranges'].set("")
            widgets['index'].set("")
            
            # Resetear frecuencias a sus valores por defecto
            if 'ac' in func_name:
                if func_name == 'voltaje_ac': widgets['freq'].set("60 Hz, 400 Hz")
                else: widgets['freq'].set("60 Hz")
            else:
                widgets['freq'].set("60Ω, 600Ω")
        
        print("Formulario reseteado.")

    def get_all_data(self):
    
        equipo = Equipment(
            type=self.eq_vars['type'].get().lower(),
            manufacturer=self.eq_vars['manufacturer'].get(),
            model=self.eq_vars['model'].get(),
            specs=self.eq_vars['specs'].get(),
            serie=self.eq_vars['serie'].get()
        )

    
        final_funciones_rangos = {}
        final_mapeo_indices = {}
        final_frecuencias = {}

        for func, widgets in self.function_widgets.items():
            if widgets['enabled'].get():
                # Procesar rangos
                raw_ranges = widgets['ranges'].get()
                ranges_list = [r.strip() for r in raw_ranges.split(',') if r.strip()]
                final_funciones_rangos[func] = ranges_list

                # Procesar índice
                idx = widgets['index'].get()
                final_mapeo_indices[func] = int(idx)-1 if idx.isdigit() else None

                # Procesar frecuencias
                if 'ac' in func:
                    raw_freq = widgets['freq'].get()
                    final_frecuencias[func] = [f.strip() for f in raw_freq.split(',') if f.strip()]
                else:
                    final_frecuencias[func] = None



        NAME_WB = f'{equipo.type} {equipo.manufacturer} {equipo.model},ns {equipo.serie}'
        PLANTILLA='templates/plantilla pinzas multimetricas.xlsm'
        # HOJA_DATOS='HOJA DE DATOS DE MEDICION'
        # HOJA_CALCULO="HOJA DE CALCULO"
        
        if 'multimetro' in equipo.type.lower():
            PLANTILLA='templates/plantilla multimetros.xlsm'
    
        try:
            wb=load_workbook(PLANTILLA,keep_vba=True)
            # sheet_medicion=wb[HOJA_DATOS]
            # sheet_calculo=wb[HOJA_CALCULO]
        except FileNotFoundError:
            print(f"Error: No se encontro el archivo {PLANTILLA}")
            return
            
        
        layout=get_layout(equipo.type)
       
        for func_name, ranges in final_funciones_rangos.items():
            mid_idx = final_mapeo_indices.get(func_name)
            fill_excel_data(layout,wb, func_name, ranges, mid_idx,final_frecuencias[func_name])
            
        
        wb.save(f'{NAME_WB}.xlsm')
        print(f"Archivo guardado como: {NAME_WB}")

        messagebox.showinfo("Éxito", f"Se creo la plantilla del {equipo.model}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EquipmentGUI(root)
    root.mainloop()


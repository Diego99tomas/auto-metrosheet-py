import customtkinter as ctk
from src.ui.plantilla import FramePlantilla
from src.ui.specs_ui import FrameSpecs

ctk.set_appearance_mode("dark")        # "dark" o "light"
ctk.set_default_color_theme("blue")   # "blue", "green" o "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AUTO METROSHEET PY")
        self.geometry("620x850")

        # Aquí vivirán los frames
        self.frame_menu = FrameMenu(self, self.navegar)
        self.frame_plantilla = FramePlantilla(self,self.navegar)
        self.frame_specs = FrameSpecs(self,self.navegar)
        self.frame_menu.pack(fill="both", expand=True)

    def navegar(self, destino):
        # Oculta todo
        for frame in [self.frame_menu, self.frame_plantilla,self.frame_specs]:
            frame.pack_forget()
        
        # Muestra el destino
        if destino == "menu":
            self.frame_menu.pack(fill="both", expand=True)
        elif destino == "plantilla":
            self.frame_plantilla.pack(fill="both", expand=True)
        elif destino == "specs":
            self.frame_specs.pack(fill="both", expand=True)


class FrameMenu(ctk.CTkFrame):
    def __init__(self, parent, navegar_callback):
        super().__init__(parent)
        self.navegar = navegar_callback

        ctk.CTkLabel(self, text="Gestión de Calibración", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=40)

        ctk.CTkButton(self, text="Crear Plantilla",
                      command=lambda: self.navegar("plantilla")).pack(pady=10)
        
        ctk.CTkButton(self, text="Ingresar Specs",
                      command=lambda: self.navegar("specs")).pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
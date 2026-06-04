from openpyxl import load_workbook,Workbook

def load_template_excel(EXCEL_PATH:str)-> Workbook | None:
    """Intenta cargar un archivo archivo excel"""
    try:
        return load_workbook(EXCEL_PATH, data_only=True)
    except FileNotFoundError:
        print("Error: No se encontró el Excel.")
        return None
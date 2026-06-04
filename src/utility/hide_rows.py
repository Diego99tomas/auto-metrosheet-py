
def hide_rows(wb,layout,function_name):
    datos='HOJA DE DATOS DE MEDICION'
    calc='HOJA DE CALCULO'
    
    layout = layout.get(function_name)
    if not layout:
        return 
        
    sheet = wb[datos]
    sheet2 = wb[calc]
 
    current_row=layout['start_row']
    final_row=layout['final_row']
    step=layout['step']

    mid_row=layout.get('mid_row')
    
    if mid_row is None:
        mid_row=None
        after_mid=0
    else:
        mid_row=layout['mid_row']
        after_mid=layout['after_mid']
    
    
    while current_row<final_row:
        cell=sheet[f'B{current_row}'].value
        
        if cell is None:
            for j in range(step):
                sheet.row_dimensions[current_row+j].hidden = True
                sheet2.row_dimensions[current_row+j].hidden = True
            current_row+=step  
        
        elif current_row==mid_row:
            current_row=after_mid

        else:
            current_row+=step 
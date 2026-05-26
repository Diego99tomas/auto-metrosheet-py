def cmc_verification(function_name:str,punto:float,unit:str)->float:
    """VALIDA LOS PUNTOS MINIMOS DE LA CMC"""
    CMC={
    'voltaje_dc':{'min':33,'unit':'mV'},
    'voltaje_ac': {'min':20,'unit':'mV'},
    'corriente_dc':{'min':1,'unit':'mA'},
    'corriente_ac': {'min':1,'unit':'mA'}, 
    'resistencias':{'min':1,'unit':'Ω'}
    }

    cmc_entry=CMC.get(function_name)
    if cmc_entry is None:
        return punto

    if abs(punto) < cmc_entry['min'] and cmc_entry['unit']==unit:
        return float(cmc_entry['min'])
    else:
        return punto
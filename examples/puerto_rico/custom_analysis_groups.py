# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 07:35:30 2018

@author: benne
"""
def getCustomGroup(groupNum=1):
    group = {}
    
    # 1) Based on fuel type
    if groupNum==1:
        
        BATT = 'Battery'
        BIO 	= 'Other Renew.' 
        COAL 	= 'Coal'
        DSL 	= 'Petrol.'
        HYDRO 	= 'Other Renew.'
        MSW_LF 	= 'Other Renew.'
        NATGAS 	= 'Natural Gas'
        OIL 	= 'Petrol.'
        SOLAR 	= 'Solar'
        WIND 	= 'Wind'
        
        group = {
        'EX_COAL':COAL,
        'EX_DSL_SIMP':DSL,
        'EX_DSL_CC':DSL,
        'EX_OIL_TYPE1':OIL,
        'EX_OIL_TYPE2':OIL,
        'EX_OIL_TYPE3':OIL,
        'EX_HYDRO':HYDRO,
        'EX_MSW_LF':MSW_LF,
        'EX_NG_CC':NATGAS,
        'EX_SOLPV':SOLAR,
        'EX_WIND':WIND,
        'EC_BATT':BATT,
        'EC_BIO':BIO,
        'EC_COAL':COAL,
        'EC_DSL_CC':DSL,
        'EC_OIL':OIL,
        'EC_NG_CC':NATGAS,
        'EC_NG_OC':NATGAS,
        'EC_SOLPV':SOLAR,
        'EC_WIND':WIND,
        'ED_BATT':BATT,
        'ED_BIO':BIO,
        'ED_NG_OC':NATGAS,
        'ED_SOLPV':SOLAR,
        'ED_WIND':WIND,
        'EI_BATT':BATT,
        'EI_SOLPV':SOLAR}
    
    # 2) Based on generation location
    elif groupNum==2: 
        
        EX = 'Existing'
        EC = 'Central (New)'
        ED = 'Regional (New)'
        EI = 'Distributed (New)'
        
        group2 = {
        'EX_COAL':EX,
        'EX_DSL_SIMP':EX,
        'EX_DSL_CC':EX,
        'EX_OIL_TYPE1':EX,
        'EX_OIL_TYPE2':EX,
        'EX_OIL_TYPE3':EX,
        'EX_HYDRO':EX,
        'EX_MSW_LF':EX,
        'EX_NG_CC':EX,
        'EX_SOLPV':EX,
        'EX_WIND':EX,
        'EC_BATT':EC,
        'EC_BIO':EC,
        'EC_COAL':EC,
        'EC_DSL_CC':EC,
        'EC_OIL':EC,
        'EC_NG_CC':EC,
        'EC_NG_OC':EC,
        'EC_SOLPV':EC,
        'EC_WIND':EC,
        'ED_BATT':ED,
        'ED_BIO':ED,
        'ED_NG_OC':ED,
        'ED_SOLPV':ED,
        'ED_WIND':ED,
        'EI_BATT':EI,
        'EI_SOLPV':EI}
    
    return group
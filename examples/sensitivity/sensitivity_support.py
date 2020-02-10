# ------------------------
# Methods to help format variable and technology names for plotting
# ------------------------
def removeCamelHump(label):
    newLabel = ''
    for s in label:
        if s.isupper():
            newLabel = newLabel + ' ' + s
        else:
            newLabel = newLabel + s
    return newLabel


def formatPlantName(label):
    # Determine Vintage
    if label[0:2] == 'EX':
        vintage = '(Existing)'
    elif label[0:2] == 'EC':
        vintage = '(New, Central)'
    elif label[0:2] == 'ED':
        vintage = '(New, Regional)'
    elif label[0:2] == 'EI':
        vintage = '(New, Small-scale)'
    else:  # If not specified, do not format
        return label

    # Determine Tech
    if label[3:] == 'BATT':
        tech = 'Battery'
    elif label[3:] == 'BIO':
        tech = 'Biomass Plant'
    elif label[3:] == 'COAL':
        tech = 'Coal Plant'
    elif label[3:] == 'DSL_SIMP':
        tech = 'Diesel Plant'
    elif label[3:] == 'DSL_CC':
        tech = 'Diesel Comb. Cyc. Plant'
    elif label[3:] == 'OIL_TYPE1':
        tech = 'Oil Plant 1'
    elif label[3:] == 'OIL_TYPE2':
        tech = 'Oil Plant 2'
    elif label[3:] == 'OIL_TYPE3':
        tech = 'Oil Plant 3'
    elif label[3:] == 'HYDRO':
        tech = 'Hydroelectric Plant'
    elif label[3:] == 'MSW_LF':
        tech = 'Landfill Gas Plant'
    elif label[3:] == 'NG_CC':
        tech = 'Natural Gas Comb. Cyc. Plant'
    elif label[3:] == 'NG_OC':
        tech = 'Natural Gas Plant'
    elif label[3:] == 'SOLPV':
        tech = 'Solar PV Plant'
    elif label[3:] == 'WIND':
        tech = 'Wind Plant'
    else:  # If not specified, do not format
        return label

    newLabel = tech + vintage

    return newLabel


def formatFuelName(label):
    # Determine Tech
    if label == 'BIO':
        tech = 'Biomass'
    elif label == 'COAL':
        tech = 'Coal'
    elif label == 'DSL':
        tech = 'Diesel'
    elif label == 'OIL':
        tech = 'Oil'
    elif label == 'HYDRO':
        tech = 'Hydroelectric'
    elif label == 'MSW_LF':
        tech = 'Landfill Gas'
    elif label == 'NATGAS':
        tech = 'Natural Gas'
    elif label == 'SOLAR':
        tech = 'Solar'
    elif label == 'WIND':
        tech = 'Wind'
    else:  # If not specified, do not format
        return label

    return tech


def formatConnName(label):
    # Determine Vintage
    if label == 'TRANS':
        tech = 'Transmission'
    elif label == 'DIST':
        tech = 'Distribution'
    elif label == 'LOCAL':
        tech = 'Local Connection'
    else:  # If not specified, do not format
        return label

    return tech

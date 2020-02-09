import os
import temoatools as tt

# ===============
# Inputs
# ===============
analyzeSingle = True
onlySimple = False
folder = dbFolder = os.getcwd() + '\\Databases'
dbs = ["A.sqlite", "B.sqlite", "C.sqlite", "D.sqlite"]

# ===============
# Single (only first db)
# ===============
if analyzeSingle:
    # Inputs
    db = dbs[0]
    createPlots = 'Y'  # Create default plots
    saveData = 'Y'  # Do not save data as a csv or xls
    sectorName = 'electric'  # Name of sector to be analyzed

    # Costs
    yearlyCosts, LCOE = tt.getCosts(folder, db)

    # Emissions
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, db)

    # Analyze capacity and activity by fuel types
    switch = 'fuel'
    capacityByFuel = tt.getCapacity(folder, db, switch=switch)
    ActivityByYearFuel = tt.getActivity(folder, db, switch=switch)
    ActivityByTODFuel = tt.getActivityTOD(folder, db, switch=switch)

    # Analyze capacity and activity by technology types
    switch = 'tech'
    capacityByTech = tt.getCapacity(folder, db, switch=switch)
    ActivityByYearFuel = tt.getActivity(folder, db, switch=switch)
    ActivityByTODTech = tt.getActivityTOD(folder, db, switch=switch)

# ===============
# Multiple
# ===============
else:
    # Inputs:
    createPlots = 'Y'  # Create default plots
    saveData = 'Y'  # Do not save data as a csv or xls
    sectorName = 'electric'  # Name of sector to be analyzed

    # Costs
    yearlyCosts, LCOE = tt.getCosts(folder, dbs)

    # Emissions
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs)

    if onlySimple == False:
        # Analyze capacity and activity by fuel types
        switch = 'fuel'
        capacityByFuel = tt.getCapacity(folder, dbs, switch=switch)
        ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch)
        ActivityByTODFuel = tt.getActivityTOD(folder, dbs, switch=switch, sectorName=sectorName, saveData=saveData,
                                              createPlots=createPlots)

        # Analyze capacity and activity by technology types
        switch = 'tech'
        capacityByTech = tt.getCapacity(folder, dbs, switch=switch, )
        ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch)
        ActivityByTODTech = tt.getActivityTOD(folder, dbs, switch=switch, sectorName=sectorName, saveData=saveData,
                                              createPlots=createPlots)

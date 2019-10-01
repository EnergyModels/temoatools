import os
import temoatools as tt
#===============
# Inputs
#===============
analyzeSingle = False
onlySimple = False

folder = os.getcwd() + '\\Databases'
dbs = ["A.sqlite","B.sqlite","C.sqlite","D.sqlite"]

#===============
# Single (only first db)
#===============
if analyzeSingle == True:    
    # Inputs
    db = dbs[0]

createPlots =    'N'         # Create default plots
saveData =       'Y'         # Do not save data as a csv or xls
sectorName =     'electric'  # Name of sector to be analyzed

# Costs
yearlyCosts, LCOE = tt.getCosts(folder, dbs, saveData=saveData, createPlots=createPlots)

# Emissions
yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, saveData=saveData, createPlots=createPlots)

# Analyze capacity and activity by fuel types
switch = 'fuel'
# capacityByFuel = tt.getCapacity(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)

import os
import temoatools as tt

# ===============
# Inputs
# ===============

onlySimple = False
folder = os.getcwd() + '/databases'
dbs = ["A.sqlite", "B.sqlite"]

createPlots = 'Y'  # Create default plots
saveData = 'Y'  # Save data as a csv or xls
sectorName = 'electric'  # Name of sector to be analyzed

# Costs
yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=saveData, create_plots=createPlots)

# Emissions

yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=saveData, create_plots=createPlots)

if not onlySimple:
    # Analyze capacity and activity by fuel types
    switch = 'fuel'
    capacityByFuel = tt.getCapacity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    ActivityByTODFuel = tt.getActivityTOD(folder, dbs, switch=switch, sector_name=sectorName, save_data=saveData, create_plots=createPlots)

    # Analyze capacity and activity by technology types
    switch = 'tech'
    capacityByTech = tt.getCapacity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    ActivityByYearTech = tt.getActivity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    ActivityByTODTech = tt.getActivityTOD(folder, dbs, switch=switch, sectorName=sectorName, save_data=saveData, create_plots=createPlots)

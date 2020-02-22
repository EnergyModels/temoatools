# ======================================================================================================================
# baselines_analyze.py
# Jeff Bennett, jab6ft@virginia.edu
#
# This script provides an example of using Temoatools to analyze Temoa models run with baselines_run.py)
# based on costs, emissions, activity and capacity by year.
#
# Required inputs (lines 29-30)
#   project_path - path to directory that contains this file (expects a subdirectory within named databases)
#   dbs - list that contains each database to be analyzed (located within subdirectory databases)
#
# Optional inputs (lines 33-36)
#   onlySimple - option to limit analysis to cost and emissions(simple) (True or False)
#   createPlots - option to output analysis to .png file (Y or N)
#   saveData -  option to output analysis to .csv file (Y or N)
#   sectorName - name of sector to be analyzed, it is based on the Temoa model, 'electric' in the example
#
# Outputs (all results are put in a subdirectory named results)
#   *.png - analysis results in graphical form
#   *.csv - analysis results in tabular form
# ======================================================================================================================
import os
import temoatools as tt
from pathlib import Path

# ===============
# Inputs
# ===============
project_path = Path('C:/Users/benne/PycharmProjects/temoatools/examples/baselines')  # Path('/home/jab6ft/temoa/project/baselines')
dbs = ["A.sqlite"]#, "B.sqlite", "C.sqlite", "D.sqlite", "E.sqlite", "F.sqlite"]

# optional inputs
onlySimple = False
createPlots = 'Y'  # Create default plots
saveData = 'Y'  # Save data as a csv or xls
sectorName = 'electric'  # Name of sector to be analyzed

# ===============
# Begin analysis
# ===============

# Create pointer to database directory
folder = os.path.join(project_path, 'databases')

# Costs
yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=saveData, create_plots=createPlots)

# Emissions

yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=saveData, create_plots=createPlots)

if not onlySimple:
    # Analyze capacity and activity by fuel types
    switch = 'fuel'
    capacityByFuel = tt.getCapacity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    # ActivityByTODFuel = tt.getActivityTOD(folder, dbs, switch=switch, sectorName=sectorName, save_data=saveData, create_plots=createPlots) # TODO - update function

    # Analyze capacity and activity by technology types
    switch = 'tech'
    capacityByTech = tt.getCapacity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    ActivityByYearTech = tt.getActivity(folder, dbs, switch=switch, save_data=saveData, create_plots=createPlots)
    # ActivityByTODTech = tt.getActivityTOD(folder, dbs, switch=switch, sectorName=sectorName, save_data=saveData, create_plots=createPlots) # TODO - update function

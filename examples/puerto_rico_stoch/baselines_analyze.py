import os
import temoatools as tt
#===============
# Inputs
#===============
onlySimple = False
folder = dbFolder = os.getcwd() + '\\databases'
dbs = ["A.sqlite","B.sqlite","C.sqlite","D.sqlite"]
run_name = "baselines"

# Inputs:
create_plots =   'Y'        # Create default plots
save_data =      'Y'        # Y or N to save data as a csv
sector_name=     'electric' # Name of sector to be analyzed

#===============
# Analysis
#===============

# Costs
yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

# Emissions
yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=save_data,create_plots=create_plots, run_name=run_name)

# Activity
switch = 'fuel'
ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)

# if onlySimple == False:
#     # Analyze capacity and activity by fuel types
#     switch = 'fuel'
#     capacityByFuel = tt.getCapacity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)
#     ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)
#     ActivityByTODFuel = tt.getActivityTOD(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)
#
#     # Analyze capacity and activity by technology types
#     switch = 'tech'
#     capacityByTech = tt.getCapacity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)
#     ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)
#     ActivityByTODTech = tt.getActivityTOD(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots)
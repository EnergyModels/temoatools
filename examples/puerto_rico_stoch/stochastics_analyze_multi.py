import os
import temoatools as tt

# ===============
# Inputs
# ===============
db_folder = os.getcwd() + '\\stochastic_databases'
run_names = ["2019_10_21",]

dbs = ["WA_0.sqlite", "WB_0.sqlite", "WC_0.sqlite", "WD_0.sqlite",
       "XA_0.sqlite", "XB_0.sqlite", "XC_0.sqlite", "XD_0.sqlite",
       "YA_0.sqlite", "YB_0.sqlite", "YC_0.sqlite", "YD_0.sqlite",
       "ZA_0.sqlite", "ZB_0.sqlite", "ZC_0.sqlite", "ZD_0.sqlite"]

create_plots = 'N'  # Create default plots
save_data = 'Y'  # Do not save data as a csv or xls
sector_name = 'electric'  # Name of sector to be analyzed

analyzeCosts = True
analyzeEmissions = False
analyzeActivityFuels = False
analyzeActivityTechs = False

for run_name in run_names:
    folder = db_folder + "\\" + run_name

    # Costs
    if analyzeCosts:
        yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

    # Emissions
    if analyzeEmissions:
        yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=save_data, create_plots=create_plots,
                                                        run_name=run_name)
    # Analyze activity by fuel types
    if analyzeActivityFuels:
        switch = 'fuel'
        ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                                            create_plots=create_plots, run_name=run_name)

    # Analyze activity by fuel types
    if analyzeActivityTechs:
        switch = 'tech'
        sector_name = 'all'
        ActivityByYearTech = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                                            create_plots=create_plots, run_name=run_name)

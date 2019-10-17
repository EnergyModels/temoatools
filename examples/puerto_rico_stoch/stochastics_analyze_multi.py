import os
import temoatools as tt

# ===============
# Inputs
# ===============
db_folder = os.getcwd() + '\\stochastic_databases'
run_names = ["2019_10_17",]

dbs = ["A_0.sqlite", "A_1.sqlite",
       "B_0.sqlite","B_1.sqlite",
       "C_0.sqlite","C_1.sqlite",
       "D_0.sqlite","D_1.sqlite"]

create_plots = 'N'  # Create default plots
save_data = 'Y'  # Do not save data as a csv or xls
sector_name = 'electric'  # Name of sector to be analyzed

analyzeEmissions = True
analyzeCosts = False
analyzeActivityFuels = False
analyzeActivityTechs = False

for run_name in run_names:
    folder = db_folder + "\\" + run_name

    # Emissions
    if analyzeEmissions:
        yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=save_data, create_plots=create_plots,
                                                        run_name=run_name)
    # Costs
    if analyzeCosts:
        yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

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

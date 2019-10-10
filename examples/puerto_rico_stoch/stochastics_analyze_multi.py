import os
import temoatools as tt

# ===============
# Inputs
# ===============
db_folder = os.getcwd() + '\\stochastic_databases'
run_names = ["2019_10_08",]
dbs = ["A_0.sqlite", "A_1.sqlite","A_2.sqlite","A_3.sqlite",
       "B_0.sqlite","B_1.sqlite","B_2.sqlite","B_3.sqlite",
       "C_0.sqlite","C_1.sqlite","C_2.sqlite","C_3.sqlite",
       "D_0.sqlite","D_1.sqlite","D_2.sqlite","D_3.sqlite"]

create_plots = 'Y'  # Create default plots
save_data = 'Y'  # Do not save data as a csv or xls
sector_name = 'electric'  # Name of sector to be analyzed

for run_name in run_names:
    folder = db_folder + "\\" + run_name

    # Emissions
    # yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=save_data, create_plots=create_plots,
    #                                                 run_name=run_name)
    # Costs
    # yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

    # Analyze capacity and activity by fuel types
    # switch = 'fuel'
    # capacityByFuel = tt.getCapacity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots, run_name=run_name)
    # ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
    #                                     create_plots=create_plots, run_name=run_name)

    # Analyze capacity and activity by fuel types
    switch = 'tech'
    sector_name = 'all'
    # capacityByFuel = tt.getCapacity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots, run_name=run_name)
    ActivityByYearTech = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                                        create_plots=create_plots, run_name=run_name)

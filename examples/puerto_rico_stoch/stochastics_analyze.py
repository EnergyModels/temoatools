import os
import temoatools as tt

# ===============
# Inputs
# ===============
db_folder = os.getcwd() + '\\stochastic_databases'
run_names = ["2019_09_25_HAZUS_moderate", "2019_09_27_HAZUS_severe"]
# run_names = ["2019_09_27_HAZUS_severe"]
dbs = ["A.sqlite", "B.sqlite", "C.sqlite", "D.sqlite"]

create_plots = 'Y'  # Create default plots
save_data = 'Y'  # Do not save data as a csv or xls
sector_name = 'electric'  # Name of sector to be analyzed

for run_name in run_names:
    folder = db_folder + "\\" + run_name

    # Emissions
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=save_data, create_plots=create_plots,
                                                    run_name=run_name)
    # Costs
    yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

    # Analyze capacity and activity by fuel types
    switch = 'fuel'
    # capacityByFuel = tt.getCapacity(folder, dbs, switch=switch,sector_name=sector_name,save_data=save_data,create_plots=create_plots, run_name=run_name)
    ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                                        create_plots=create_plots, run_name=run_name)

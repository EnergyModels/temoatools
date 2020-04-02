import os
import pandas as pd
import temoatools as tt
from joblib import Parallel, delayed, parallel_backend


# =======================================================
# Function to evaluate simulations by a single metric
# =======================================================

def analyze_results(task, folder_db, tech_group_dict, prob_type_dict, infra_dict, carbon_tax_dict):
    # Read-in task inputs
    db = task['db']
    metric = task['metric']
    run_name = task['run_name']
    folder_results = task['folder_results']

    # display task inputs
    print(db)
    print(metric)

    # re-arrange for functions
    dbs = [db]
    all_dbs = [db]

    # --------------------------------
    # Analyze with temoatools
    # --------------------------------

    create_plots = 'N'  # Create default plots
    save_data = 'Y'  # Do not save data as a csv or xls
    sector_name = 'electric'  # Name of sector to be analyzed

    # Costs
    if metric == 'costs_yearly':
        tt.getCosts(folder_db, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

    # Emissions
    elif metric == 'emissions_yearly':
        tt.getEmissions(folder_db, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)
    # Analyze activity by fuel types
    elif metric == 'activity_by_fuel':
        switch = 'fuel'
        tt.getActivity(folder_db, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                       create_plots=create_plots, run_name=run_name)

    # Analyze activity by fuel types
    elif metric == 'activity_by_tech':
        switch = 'tech'
        sector_name = 'all'
        tt.getActivity(folder_db, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                       create_plots=create_plots, run_name=run_name)

    # Analyze capacity by fuel types
    elif metric == 'capacity_by_fuel':
        switch = 'fuel'
        tt.getCapacity(folder_db, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                       create_plots=create_plots, run_name=run_name)

    # Analyze capacity by fuel types
    elif metric == 'capacity_by_tech':
        switch = 'tech'
        sector_name = 'all'
        tt.getCapacity(folder_db, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                       create_plots=create_plots, run_name=run_name)

    # --------------------------------
    # Move to results directory
    # --------------------------------
    cwd = os.getcwd()
    try:
        os.stat(folder_results)
    except:
        os.mkdir(folder_results)
    os.chdir(folder_results)

    # --------------------------------
    # Prepare for plotting
    # --------------------------------

    # Naming conventions and conversions
    if metric == 'costs_yearly':
        filename = "costs_yearly.csv"
        conversion = 1.0 / 100.0  # Convert from cents/kWh to $/kWh/yr
        id_vars = ["database", "scenario"]
        col_renames = {"scenario": "s", "database": "Scenario"}
        csv_file = "costs_yearly_toPlot.csv"

    elif metric == 'emissions_yearly':
        filename = "emissions_yearly.csv"
        conversion = 1.0 / 1000.0  # Convert from kton/yr to Mton/yr
        id_vars = ["database", "scenario"]
        col_renames = {"scenario": "s", "database": "Scenario"}
        csv_file = "emissions_yearly_toPlot.csv"

    elif metric == 'activity_by_fuel':
        filename = "activity_by_fuel.csv"
        conversion = 1.0 / 1000.0  # GWh to TWh
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "activity_by_fuel_toPlot.csv"

    elif metric == 'activity_by_tech':
        filename = "activity_by_tech.csv"
        conversion = 1.0 / 1000.0  # GWh to TWh
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "activity_by_tech_toPlot.csv"

    elif metric == 'capacity_by_fuel':
        filename = "capacity_by_fuel.csv"
        conversion = 1.0  # GW
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "capacity_by_fuel_toPlot.csv"

    elif metric == 'capacity_by_tech':
        filename = "capacity_by_tech.csv"
        conversion = 1.0  # GW
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "capacity_by_tech_toPlot.csv"

    # Load and Process data
    df = pd.read_csv(filename, index_col=0)
    for col in df.columns:
        if 'Unnamed' in col:
            df = df.drop(col, axis=1)
    df2 = pd.melt(df, id_vars=id_vars, var_name="Year", value_name="Value")
    df2.case = "unknown"
    df2.Value = df2.Value * conversion

    for db in all_dbs:
        ind = df2.loc[:, "database"] == db
        df2.loc[ind, "case"] = prob_type_dict[db] + "-" + infra_dict[db] + "-" + carbon_tax_dict[db]
        df2.loc[ind, "database"] = tech_group_dict[db]
        df2.loc[ind, "prob_type"] = prob_type_dict[db]
        df2.loc[ind, "infra"] = infra_dict[db]
        df2.loc[ind, "carbon_tax"] = carbon_tax_dict[db]
        df2.loc[ind, "infra_and_carbon_tax"] = infra_dict[db] + "-" + carbon_tax_dict[db]

        # Add columns to match stochastic simulations
        df2.loc[ind, "Unnamed: 0"] = 1
        df2.loc[ind, "entry"] = 1

    df2 = df2.rename(columns=col_renames)

    # rename s to differentiate
    df2.loc[:, "s"] = db

    # Save file
    df2.to_csv(csv_file)

    # --------------------------------
    # Return to original directory
    # --------------------------------
    os.chdir(cwd)


# ================================
# Main body of script
# ================================
if __name__ == '__main__':
    ncpus = 3  # int(os.getenv('NUM_PROCS'))

    db_folder = os.path.join(os.getcwd(), 'databases')
    result_folder = os.path.join(os.getcwd(), 'results')

    print("running")

    # Names of databases simulated
    dbs = ["T.sqlite", "U.sqlite", "V.sqlite"]

    # Technology Groups
    tech_group = ['All', 'All w/o Distributed Wind']
    tech_group_dict = {"T.sqlite": tech_group[0], "U.sqlite": tech_group[0], "V.sqlite": tech_group[0]}

    # Historical or Climate Change Probabilities
    prob = ["None"]
    prob_type_dict = {"T.sqlite": prob[0], "U.sqlite": prob[0], "V.sqlite": prob[0]}

    # Infrastructure Type
    infra = ["All"]
    infra_dict = {"T.sqlite": infra[0], "U.sqlite": infra[0], "V.sqlite": infra[0]}

    # Carbon Tax
    carbon_tax = ["No IRP", "IRP", "Tax"]
    carbon_tax_dict = {"T.sqlite": carbon_tax[0], "U.sqlite": carbon_tax[1], "V.sqlite": carbon_tax[2]}

    # create tasks
    entries = ['db', 'metric', 'run_name', 'folder_results']
    tasks = pd.DataFrame(columns=entries)
    for db in dbs:

        # metrics available
        # metrics = ['costs_yearly', 'emissions_yearly', 'activity_by_fuel', 'activity_by_tech', 'capacity_by_fuel',
        #            'capacity_by_tech']

        # For our analysis we only use the following metrics
        metrics = ['costs_yearly', 'emissions_yearly', 'activity_by_fuel', 'activity_by_tech', 'capacity_by_fuel',
                    'capacity_by_tech']

        for metric in metrics:
            t = pd.Series(index=entries)
            t['db'] = db
            t['metric'] = metric
            t['run_name'] = tt.remove_ext(db)
            t['folder_results'] = os.path.join(result_folder, t['run_name'])
            tasks = tasks.append(t, ignore_index=True)

    # Perform simulations in parallel
    with parallel_backend('multiprocessing', n_jobs=ncpus):
        Parallel(n_jobs=ncpus, verbose=5)(
            delayed(analyze_results)(task, db_folder,
                                     tech_group_dict, prob_type_dict, infra_dict, carbon_tax_dict) for index, task in
            tasks.iterrows())

        # -------------------
        # combine the results
        # -------------------
        costs_yearly = []
        emissions_yearly = []
        activity_by_fuel = []
        activity_by_tech = []

        for index, task in tasks.iterrows():
            db = task['db']
            metric = task['metric']
            run_name = task['run_name']
            folder_results = task['folder_results']

            os.chdir(folder_results)

            if metric == 'costs_yearly':
                temp = pd.read_csv('costs_yearly_toPlot.csv')
                if len(costs_yearly) == 0:
                    costs_yearly = temp
                else:
                    costs_yearly = pd.concat([costs_yearly, temp])

            elif metric == 'emissions_yearly':
                temp = pd.read_csv('emissions_yearly_toPlot.csv')
                if len(emissions_yearly) == 0:
                    emissions_yearly = temp
                else:
                    emissions_yearly = pd.concat([emissions_yearly, temp])

            elif metric == 'activity_by_fuel':
                temp = pd.read_csv('activity_by_fuel_toPlot.csv')
                if len(activity_by_fuel) == 0:
                    activity_by_fuel = temp
                else:
                    activity_by_fuel = pd.concat([activity_by_fuel, temp])

            elif metric == 'activity_by_tech':
                temp = pd.read_csv('activity_by_tech_toPlot.csv')
                if len(activity_by_tech) == 0:
                    activity_by_tech = temp
                else:
                    activity_by_tech = pd.concat([activity_by_tech, temp])

        # save
        os.chdir(result_folder)
        costs_yearly.to_csv('costs_yearly_toPlot_baselines.csv')
        emissions_yearly.to_csv('emissions_yearly_toPlot_baselines.csv')
        activity_by_fuel.to_csv('activity_by_fuel_toPlot_baselines.csv')
        activity_by_tech.to_csv('activity_by_tech_toPlot_baselines.csv')
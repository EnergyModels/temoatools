import os
import pandas as pd
import temoatools as tt
from joblib import Parallel, delayed, parallel_backend


# =======================================================
# Function to evaluate simulations by a single metric
# =======================================================

def analyze_results(task, folder_db, all_dbs_dict, db_shift, node_prob,
                    tech_group_dict, prob_type_dict, infra_dict, carbon_tax_dict):
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
    all_dbs = [db, all_dbs_dict[db]]

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
    # Expand Results (only costs and emissions)
    # --------------------------------

    if metric == 'costs_yearly' or metric == 'emissions_yearly' \
            or metric == 'activity_by_fuel' or metric == 'activity_by_tech':

        if metric == 'costs_yearly':
            filename = 'costs_yearly'
        elif metric == 'emissions_yearly':
            filename = 'emissions_yearly'
        elif metric == 'activity_by_fuel':
            filename = 'activity_by_fuel'
        elif metric == 'activity_by_tech':
            filename = 'activity_by_tech'

        tt.stoch_expand(folder_results, filename, db_shift)

    # --------------------------------
    # Resample Results (only costs and emissions)
    # --------------------------------
    if metric == 'costs_yearly' or metric == 'emissions_yearly' \
            or metric == 'activity_by_fuel' or metric == 'activity_by_tech':

        if metric == 'costs_yearly':
            filename = 'costs_yearly_exp'
        elif metric == 'emissions_yearly':
            filename = 'emissions_yearly_exp'
        elif metric == 'activity_by_fuel':
            filename = 'activity_by_fuel_exp'
        elif metric == 'activity_by_tech':
            filename = 'activity_by_tech_exp'

        tt.stoch_resample(folder_results, filename, node_prob)

    # --------------------------------
    # Move to results directory
    # --------------------------------
    cwd = os.getcwd()
    os.chdir(folder_results)

    # --------------------------------
    # Prepare for plotting
    # --------------------------------

    # Naming conventions and conversions
    if metric == 'costs_yearly':
        filename = "costs_yearly_exp_resampled.csv"
        conversion = 1.0 / 100.0  # Convert from cents/kWh to $/kWh/yr
        id_vars = ["database", "scenario", "entry"]
        col_renames = {"scenario": "s", "database": "Scenario"}
        csv_file = "costs_yearly_toPlot.csv"

    elif metric == 'emissions_yearly':
        filename = "emissions_yearly_exp_resampled.csv"
        conversion = 1.0 / 1000.0  # Convert from kton/yr to Mton/yr
        id_vars = ["database", "scenario", "entry"]
        col_renames = {"scenario": "s", "database": "Scenario"}
        csv_file = "emissions_yearly_toPlot.csv"

    elif metric == 'activity_by_fuel':
        filename = "activity_by_fuel_exp_resampled.csv"
        conversion = 1.0 / 1000.0  # GWh to TWh
        id_vars = ["database", "scenario", "fuelOrTech", "entry"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "activity_by_fuel_toPlot.csv"

    elif metric == 'activity_by_tech':
        filename = "activity_by_tech_exp_resampled.csv"
        conversion = 1.0 / 1000.0  # GWh to TWh
        id_vars = ["database", "scenario", "fuelOrTech", "entry"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "activity_by_tech_toPlot.csv"

    elif metric == 'capacity_by_fuel':
        filename = "capacity_by_fuel.csv"  # Don't expand and resample these results
        conversion = 1.0  # GW
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "capacity_by_fuel_toPlot.csv"

    elif metric == 'capacity_by_tech':
        filename = "capacity_by_tech.csv"  # Don't expand and resample these results
        conversion = 1.0  # GW
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "capacity_by_tech_toPlot.csv"

    # Load and Process data
    df = pd.read_csv(filename, index_col=0)
    if metric == 'costs_yearly' or metric == 'emissions_yearly' or metric == 'activity_by_fuel' or metric == 'activity_by_tech':
        df = df.drop("prob", axis=1)
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
    df2 = df2.rename(columns=col_renames)

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
    ncpus = int(os.getenv('NUM_PROCS'))

    db_folder = os.path.join(os.getcwd(), 'stochastic_databases')
    result_folder = os.path.join(os.getcwd(), 'results')

    print("running")

    # Names of databases simulated
    dbs = ["T_0.sqlite", "T2_0.sqlite", "U_0.sqlite", "U2_0.sqlite", "V_0.sqlite", "V2_0.sqlite",
           "WA_0.sqlite", "WB_0.sqlite", "WC_0.sqlite", "WD_0.sqlite", "WE_0.sqlite", "WF_0.sqlite",
           "XA_0.sqlite", "XB_0.sqlite", "XC_0.sqlite", "XD_0.sqlite",
           "YA_0.sqlite", "YB_0.sqlite", "YC_0.sqlite",
           "ZA_0.sqlite", "ZB_0.sqlite", "ZC_0.sqlite"]

    # Node probabilities by case (0 is simulated, 1 is calculated)
    node_prob = {"0": [0.52, 0.32, 0.16],  # Historical (sum must equal 1)
                 "1": [0.2, 0.32, 0.48]}  # Climate Change

    # Dictionary relating simulated databases to calculated results using different distributions
    db_shift = {"WA_0": "WA_1", "WB_0": "WB_1", "WC_0": "WC_1", "WD_0": "WD_1", "WE_0": "WE_1", "WF_0": "WF_1",
                "XA_0": "XA_1", "XB_0": "XB_1", "XC_0": "XC_1", "XD_0": "XD_1",
                "YA_0": "YA_1", "YB_0": "YB_1", "YC_0": "YC_1",
                "ZA_0": "ZA_1", "ZB_0": "ZB_1", "ZC_0": "ZC_1",
                "T_0": "T_1", "T2_0": "T2_1",
                "U_0": "U_1", "U2_0": "U2_1",
                "V_0": "V_1", "V2_0": "V2_1"}

    # Dictionary relating databases after applying different distributions
    all_dbs_dict = {"WA_0.sqlite": "WA_1.sqlite", "WB_0.sqlite": "WB_1.sqlite", "WC_0.sqlite": "WC_1.sqlite",
                    "WD_0.sqlite": "WD_1.sqlite", "WE_0.sqlite": "WE_1.sqlite", "WF_0.sqlite": "WF_1.sqlite",
                    "XA_0.sqlite": "XA_1.sqlite", "XB_0.sqlite": "XB_1.sqlite", "XC_0.sqlite": "XC_1.sqlite",
                    "XD_0.sqlite": "XD_1.sqlite",
                    "YA_0.sqlite": "YA_1.sqlite", "YB_0.sqlite": "YB_1.sqlite", "YC_0.sqlite": "YC_1.sqlite",
                    "ZA_0.sqlite": "ZA_1.sqlite", "ZB_0.sqlite": "ZB_1.sqlite", "ZC_0.sqlite": "ZC_1.sqlite",
                    "T_0.sqlite": "T_1.sqlite", "T2_0.sqlite": "T2_1.sqlite",
                    "U_0.sqlite": "U_1.sqlite", "U2_0.sqlite": "U2_1.sqlite",
                    "V_0.sqlite": "V_1.sqlite", "V2_0.sqlite": "V2_1.sqlite"}

    # Technology Groups
    tech_group = ['Centralized', 'Distributed',
                  'Distributed w/o Wind', 'Business-as-usual', 'All', 'All w/o Distributed Wind',
                  'Centralized - Natural Gas', 'Distributed - Natural Gas', ]
    tech_group_dict = {"WA_0.sqlite": tech_group[0], "WA_1.sqlite": tech_group[0], "WB_0.sqlite": tech_group[1],
                       "WB_1.sqlite": tech_group[1], "WC_0.sqlite": tech_group[2], "WC_1.sqlite": tech_group[2],
                       "WD_0.sqlite": tech_group[3], "WD_1.sqlite": tech_group[3],
                       "WE_0.sqlite": tech_group[6], "WE_1.sqlite": tech_group[6],
                       "WF_0.sqlite": tech_group[7], "WF_1.sqlite": tech_group[7],
                       "XA_0.sqlite": tech_group[0], "XA_1.sqlite": tech_group[0], "XB_0.sqlite": tech_group[1],
                       "XB_1.sqlite": tech_group[1], "XC_0.sqlite": tech_group[2], "XC_1.sqlite": tech_group[2],
                       "XD_0.sqlite": tech_group[3], "XD_1.sqlite": tech_group[3],
                       "YA_0.sqlite": tech_group[0], "YA_1.sqlite": tech_group[0], "YB_0.sqlite": tech_group[1],
                       "YB_1.sqlite": tech_group[1], "YC_0.sqlite": tech_group[2], "YC_1.sqlite": tech_group[2],
                       "ZA_0.sqlite": tech_group[0], "ZA_1.sqlite": tech_group[0], "ZB_0.sqlite": tech_group[1],
                       "ZB_1.sqlite": tech_group[1], "ZC_0.sqlite": tech_group[2], "ZC_1.sqlite": tech_group[2],
                       "T_0.sqlite": tech_group[4], "T_1.sqlite": tech_group[4],
                       "T2_0.sqlite": tech_group[5], "T2_1.sqlite": tech_group[5],
                       "U_0.sqlite": tech_group[4], "U_1.sqlite": tech_group[4],
                       "U2_0.sqlite": tech_group[5], "U2_1.sqlite": tech_group[5],
                       "V_0.sqlite": tech_group[4], "V_1.sqlite": tech_group[4],
                       "V2_0.sqlite": tech_group[5], "V2_1.sqlite": tech_group[5]}

    # Historical or Climate Change Probabilities
    prob = ["Historical", "Climate Change"]
    prob_type_dict = {"WA_0.sqlite": prob[0], "WA_1.sqlite": prob[1], "WB_0.sqlite": prob[0], "WB_1.sqlite": prob[1],
                      "WC_0.sqlite": prob[0], "WC_1.sqlite": prob[1], "WD_0.sqlite": prob[0], "WD_1.sqlite": prob[1],
                      "WE_0.sqlite": prob[0], "WE_1.sqlite": prob[1], "WF_0.sqlite": prob[0], "WF_1.sqlite": prob[1],
                      "XA_0.sqlite": prob[0], "XA_1.sqlite": prob[1], "XB_0.sqlite": prob[0], "XB_1.sqlite": prob[1],
                      "XC_0.sqlite": prob[0], "XC_1.sqlite": prob[1], "XD_0.sqlite": prob[0], "XD_1.sqlite": prob[1],
                      "YA_0.sqlite": prob[0], "YA_1.sqlite": prob[1], "YB_0.sqlite": prob[0], "YB_1.sqlite": prob[1],
                      "YC_0.sqlite": prob[0], "YC_1.sqlite": prob[1],
                      "ZA_0.sqlite": prob[0], "ZA_1.sqlite": prob[1], "ZB_0.sqlite": prob[0], "ZB_1.sqlite": prob[1],
                      "ZC_0.sqlite": prob[0], "ZC_1.sqlite": prob[1],
                      "T_0.sqlite": prob[0], "T_1.sqlite": prob[1], "T2_0.sqlite": prob[0], "T2_1.sqlite": prob[1],
                      "U_0.sqlite": prob[0], "U_1.sqlite": prob[1], "U2_0.sqlite": prob[0], "U2_1.sqlite": prob[1],
                      "V_0.sqlite": prob[0], "V_1.sqlite": prob[1], "V2_0.sqlite": prob[0], "V2_1.sqlite": prob[1]}

    # Infrastructure Type
    infra = ["Current", "Hardened", "All"]
    infra_dict = {"WA_0.sqlite": infra[0], "WA_1.sqlite": infra[0], "WB_0.sqlite": infra[0], "WB_1.sqlite": infra[0],
                  "WC_0.sqlite": infra[0], "WC_1.sqlite": infra[0], "WD_0.sqlite": infra[0], "WD_1.sqlite": infra[0],
                  "WE_0.sqlite": infra[0], "WE_1.sqlite": infra[0], "WF_0.sqlite": infra[0], "WF_1.sqlite": infra[0],
                  "XA_0.sqlite": infra[1], "XA_1.sqlite": infra[1], "XB_0.sqlite": infra[1], "XB_1.sqlite": infra[1],
                  "XC_0.sqlite": infra[1], "XC_1.sqlite": infra[1], "XD_0.sqlite": infra[1], "XD_1.sqlite": infra[1],
                  "XE_0.sqlite": infra[1], "XE_1.sqlite": infra[1], "XF_0.sqlite": infra[1], "XF_1.sqlite": infra[1],
                  "YA_0.sqlite": infra[0], "YA_1.sqlite": infra[0], "YB_0.sqlite": infra[0], "YB_1.sqlite": infra[0],
                  "YC_0.sqlite": infra[0], "YC_1.sqlite": infra[0],
                  "ZA_0.sqlite": infra[1], "ZA_1.sqlite": infra[1], "ZB_0.sqlite": infra[1], "ZB_1.sqlite": infra[1],
                  "ZC_0.sqlite": infra[1], "ZC_1.sqlite": infra[1],
                  "T_0.sqlite": infra[2], "T_1.sqlite": infra[2], "T2_0.sqlite": infra[2], "T2_1.sqlite": infra[2],
                  "U_0.sqlite": infra[2], "U_1.sqlite": infra[2], "U2_0.sqlite": infra[2], "U2_1.sqlite": infra[2],
                  "V_0.sqlite": infra[2], "V_1.sqlite": infra[2], "V2_0.sqlite": infra[2], "V2_1.sqlite": infra[2]}

    # Carbon Tax
    carbon_tax = ["No IRP", "IRP", "New IRP"]
    carbon_tax_dict = {"WA_0.sqlite": carbon_tax[0], "WA_1.sqlite": carbon_tax[0], "WB_0.sqlite": carbon_tax[0],
                       "WB_1.sqlite": carbon_tax[0], "WC_0.sqlite": carbon_tax[0], "WC_1.sqlite": carbon_tax[0],
                       "WD_0.sqlite": carbon_tax[0], "WD_1.sqlite": carbon_tax[0],
                       "WE_0.sqlite": carbon_tax[0], "WE_1.sqlite": carbon_tax[0],
                       "WF_0.sqlite": carbon_tax[0], "WF_1.sqlite": carbon_tax[0],
                       "XA_0.sqlite": carbon_tax[0], "XA_1.sqlite": carbon_tax[0], "XB_0.sqlite": carbon_tax[0],
                       "XB_1.sqlite": carbon_tax[0], "XC_0.sqlite": carbon_tax[0], "XC_1.sqlite": carbon_tax[0],
                       "XD_0.sqlite": carbon_tax[0], "XD_1.sqlite": carbon_tax[0],
                       "YA_0.sqlite": carbon_tax[1], "YA_1.sqlite": carbon_tax[1], "YB_0.sqlite": carbon_tax[1],
                       "YB_1.sqlite": carbon_tax[1], "YC_0.sqlite": carbon_tax[1], "YC_1.sqlite": carbon_tax[1],
                       "ZA_0.sqlite": carbon_tax[1], "ZA_1.sqlite": carbon_tax[1], "ZB_0.sqlite": carbon_tax[1],
                       "ZB_1.sqlite": carbon_tax[1], "ZC_0.sqlite": carbon_tax[1], "ZC_1.sqlite": carbon_tax[1],
                       "T_0.sqlite": carbon_tax[0], "T_1.sqlite": carbon_tax[0],
                       "T2_0.sqlite": carbon_tax[0], "T2_1.sqlite": carbon_tax[0],
                       "U_0.sqlite": carbon_tax[1], "U_1.sqlite": carbon_tax[1],
                       "U2_0.sqlite": carbon_tax[1], "U2_1.sqlite": carbon_tax[1],
                       "V_0.sqlite": carbon_tax[2], "V_1.sqlite": carbon_tax[2],
                       "V2_0.sqlite": carbon_tax[2], "V2_1.sqlite": carbon_tax[2]}

    # create tasks
    entries = ['db', 'metric', 'run_name', 'folder_results']
    tasks = pd.DataFrame(columns=entries)
    for db in dbs:

        # metrics available
        # metrics = ['costs_yearly', 'emissions_yearly', 'activity_by_fuel', 'activity_by_tech', 'capacity_by_fuel',
        #            'capacity_by_tech']

        # For our analysis we only use the following metrics
        if db == "T_0.sqlite" or db == "U_0.sqlite" or db == "V_0.sqlite" or \
                db == "T2_0.sqlite" or db == "U2_0.sqlite" or db == "V2_0.sqlite":
            metrics = ['costs_yearly', 'emissions_yearly', 'activity_by_fuel', 'activity_by_tech', ]
        else:
            metrics = ['costs_yearly', 'emissions_yearly']

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
            delayed(analyze_results)(task, db_folder, all_dbs_dict, db_shift, node_prob,
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
    costs_yearly.to_csv('costs_yearly_toPlot.csv')
    emissions_yearly.to_csv('emissions_yearly_toPlot.csv')
    activity_by_fuel.to_csv('activity_by_fuel_toPlot.csv')
    activity_by_tech.to_csv('activity_by_tech_toPlot.csv')

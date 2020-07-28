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
    save_data = 'Y'  # Save data as a csv or xls
    sector_name = 'electric'  # Name of sector to be analyzed

    # Analyze capacity by fuel types
    if metric == 'capacity_by_fuel':
        switch = 'fuel'
        tt.getCapacityNew(folder_db, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                          create_plots=create_plots, run_name=run_name)

    # Analyze capacity by fuel types
    elif metric == 'capacity_by_tech':
        switch = 'tech'
        sector_name = 'all'
        tt.getCapacityNew(folder_db, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                          create_plots=create_plots, run_name=run_name)


# ================================
# Main body of script
# ================================
if __name__ == '__main__':
    try:
        ncpus = int(os.getenv('NUM_PROCS'))  # try to use variable defined in sbatch script
    except:
        ncpus = 6  # otherwise default to this number of cores

    db_folder = os.path.abspath('..//..//temoa_stochastic//data_files')
    result_folder = os.path.join(os.getcwd(), 'results')

    print("running")

    # Names of databases simulated - only looking at cases presented in study
    dbs = ["T_0.sqlite",
           "U_0.sqlite",
           "V_0.sqlite",
           "WA_0.sqlite", "WB_0.sqlite", "WD_0.sqlite", "WE_0.sqlite", "WF_0.sqlite",
           "YA_0.sqlite", "YB_0.sqlite",
           "AA_0.sqlite", "AB_0.sqlite", "AD_0.sqlite", "AE_0.sqlite", "AF_0.sqlite"]

    # Node probabilities by case (0 is simulated, 1 is calculated)
    node_prob = {"0": [0.52, 0.32, 0.16],  # Historical (sum must equal 1)
                 "1": [0.2, 0.32, 0.48]}  # Climate Change

    # Dictionary relating simulated databases to calculated results using different distributions
    db_shift = {"WA_0": "WA_1", "WB_0": "WB_1", "WD_0": "WD_1", "WE_0": "WE_1", "WF_0": "WF_1",
                "XA_0": "XA_1", "XB_0": "XB_1", "XD_0": "XD_1",
                "YA_0": "YA_1", "YB_0": "YB_1",
                "ZA_0": "ZA_1", "ZB_0": "ZB_1",
                "T_0": "T_1",
                "U_0": "U_1",
                "V_0": "V_1",
                "AA_0": "AA_1", "AB_0": "AB_1", "AD_0": "AD_1", "AE_0": "AE_1", "AF_0": "AF_1"}

    # Dictionary relating databases after applying different distributions
    all_dbs_dict = {"WA_0.sqlite": "WA_1.sqlite", "WB_0.sqlite": "WB_1.sqlite",
                    "WD_0.sqlite": "WD_1.sqlite", "WE_0.sqlite": "WE_1.sqlite", "WF_0.sqlite": "WF_1.sqlite",
                    "XA_0.sqlite": "XA_1.sqlite", "XB_0.sqlite": "XB_1.sqlite",
                    "XD_0.sqlite": "XD_1.sqlite",
                    "YA_0.sqlite": "YA_1.sqlite", "YB_0.sqlite": "YB_1.sqlite",
                    "ZA_0.sqlite": "ZA_1.sqlite", "ZB_0.sqlite": "ZB_1.sqlite",
                    "T_0.sqlite": "T_1.sqlite",
                    "U_0.sqlite": "U_1.sqlite",
                    "V_0.sqlite": "V_1.sqlite",
                    "AA_0.sqlite": "AA_1.sqlite", "AB_0.sqlite": "AB_1.sqlite",
                    "AD_0.sqlite": "AD_1.sqlite", "AE_0.sqlite": "AE_1.sqlite", "AF_0.sqlite": "AF_1.sqlite", }

    # Technology Groups
    tech_group = ['Centralized', 'Distributed',
                  'Distributed w/o Wind', 'Business-as-usual', 'All', 'All w/o Distributed Wind',
                  'Centralized - Natural Gas', 'Distributed - Natural Gas', ]
    tech_group_dict = {"WA_0.sqlite": tech_group[0], "WA_1.sqlite": tech_group[0],
                       "WB_0.sqlite": tech_group[1], "WB_1.sqlite": tech_group[1],
                       "WD_0.sqlite": tech_group[3], "WD_1.sqlite": tech_group[3],
                       "WE_0.sqlite": tech_group[6], "WE_1.sqlite": tech_group[6],
                       "WF_0.sqlite": tech_group[7], "WF_1.sqlite": tech_group[7],
                       "XA_0.sqlite": tech_group[0], "XA_1.sqlite": tech_group[0],
                       "XB_0.sqlite": tech_group[1], "XB_1.sqlite": tech_group[1],
                       "XD_0.sqlite": tech_group[3], "XD_1.sqlite": tech_group[3],
                       "YA_0.sqlite": tech_group[0], "YA_1.sqlite": tech_group[0],
                       "YB_0.sqlite": tech_group[1], "YB_1.sqlite": tech_group[1],
                       "ZA_0.sqlite": tech_group[0], "ZA_1.sqlite": tech_group[0],
                       "ZB_0.sqlite": tech_group[1], "ZB_1.sqlite": tech_group[1],
                       "T_0.sqlite": tech_group[4], "T_1.sqlite": tech_group[4],
                       "U_0.sqlite": tech_group[4], "U_1.sqlite": tech_group[4],
                       "V_0.sqlite": tech_group[4], "V_1.sqlite": tech_group[4],
                       "AA_0.sqlite": tech_group[0], "AA_1.sqlite": tech_group[0],
                       "AB_0.sqlite": tech_group[1], "AB_1.sqlite": tech_group[1],
                       "AD_0.sqlite": tech_group[3], "AD_1.sqlite": tech_group[3],
                       "AE_0.sqlite": tech_group[6], "AE_1.sqlite": tech_group[6],
                       "AF_0.sqlite": tech_group[7], "AF_1.sqlite": tech_group[7]
                       }

    # Historical or Climate Change Probabilities
    prob = ["Historical", "Climate Change", "None"]
    prob_type_dict = {"WA_0.sqlite": prob[0], "WA_1.sqlite": prob[1],
                      "WB_0.sqlite": prob[0], "WB_1.sqlite": prob[1],
                      "WD_0.sqlite": prob[0], "WD_1.sqlite": prob[1],
                      "WE_0.sqlite": prob[0], "WE_1.sqlite": prob[1],
                      "WF_0.sqlite": prob[0], "WF_1.sqlite": prob[1],
                      "XA_0.sqlite": prob[0], "XA_1.sqlite": prob[1],
                      "XB_0.sqlite": prob[0], "XB_1.sqlite": prob[1],
                      "XD_0.sqlite": prob[0], "XD_1.sqlite": prob[1],
                      "YA_0.sqlite": prob[0], "YA_1.sqlite": prob[1],
                      "YB_0.sqlite": prob[0], "YB_1.sqlite": prob[1],
                      "ZA_0.sqlite": prob[0], "ZA_1.sqlite": prob[1],
                      "ZB_0.sqlite": prob[0], "ZB_1.sqlite": prob[1],
                      "T_0.sqlite": prob[0], "T_1.sqlite": prob[1],
                      "U_0.sqlite": prob[0], "U_1.sqlite": prob[1],
                      "V_0.sqlite": prob[0], "V_1.sqlite": prob[1],
                      "AA_0.sqlite": prob[0], "AA_1.sqlite": prob[1],
                      "AB_0.sqlite": prob[0], "AB_1.sqlite": prob[1],
                      "AD_0.sqlite": prob[0], "AD_1.sqlite": prob[1],
                      "AE_0.sqlite": prob[0], "AE_1.sqlite": prob[1],
                      "AF_0.sqlite": prob[0], "AF_1.sqlite": prob[1]}

    # Infrastructure Type
    infra = ["Current", "Hardened", "All"]
    infra_dict = {"WA_0.sqlite": infra[0], "WA_1.sqlite": infra[0],
                  "WB_0.sqlite": infra[0], "WB_1.sqlite": infra[0],
                  "WD_0.sqlite": infra[0], "WD_1.sqlite": infra[0],
                  "WE_0.sqlite": infra[0], "WE_1.sqlite": infra[0],
                  "WF_0.sqlite": infra[0], "WF_1.sqlite": infra[0],
                  "XA_0.sqlite": infra[1], "XA_1.sqlite": infra[1],
                  "XB_0.sqlite": infra[1], "XB_1.sqlite": infra[1],
                  "XD_0.sqlite": infra[1], "XD_1.sqlite": infra[1],
                  "YA_0.sqlite": infra[0], "YA_1.sqlite": infra[0],
                  "YB_0.sqlite": infra[0], "YB_1.sqlite": infra[0],
                  "ZA_0.sqlite": infra[1], "ZA_1.sqlite": infra[1],
                  "ZB_0.sqlite": infra[1], "ZB_1.sqlite": infra[1],
                  "T_0.sqlite": infra[2], "T_1.sqlite": infra[2],
                  "U_0.sqlite": infra[2], "U_1.sqlite": infra[2],
                  "V_0.sqlite": infra[2], "V_1.sqlite": infra[2],
                  "AA_0.sqlite": infra[0], "AA_1.sqlite": infra[0],
                  "AB_0.sqlite": infra[0], "AB_1.sqlite": infra[0],
                  "AD_0.sqlite": infra[0], "AD_1.sqlite": infra[0],
                  "AE_0.sqlite": infra[0], "AE_1.sqlite": infra[0],
                  "AF_0.sqlite": infra[0], "AF_1.sqlite": infra[0]}

    # Carbon Tax
    carbon_tax = ["No IRP", "IRP", "Tax"]
    carbon_tax_dict = {"WA_0.sqlite": carbon_tax[0], "WA_1.sqlite": carbon_tax[0],
                       "WB_0.sqlite": carbon_tax[0], "WB_1.sqlite": carbon_tax[0],
                       "WD_0.sqlite": carbon_tax[0], "WD_1.sqlite": carbon_tax[0],
                       "WE_0.sqlite": carbon_tax[0], "WE_1.sqlite": carbon_tax[0],
                       "WF_0.sqlite": carbon_tax[0], "WF_1.sqlite": carbon_tax[0],
                       "XA_0.sqlite": carbon_tax[0], "XA_1.sqlite": carbon_tax[0],
                       "XB_0.sqlite": carbon_tax[0], "XB_1.sqlite": carbon_tax[0],
                       "XD_0.sqlite": carbon_tax[0], "XD_1.sqlite": carbon_tax[0],
                       "YA_0.sqlite": carbon_tax[1], "YA_1.sqlite": carbon_tax[1],
                       "YB_0.sqlite": carbon_tax[1], "YB_1.sqlite": carbon_tax[1],
                       "ZA_0.sqlite": carbon_tax[1], "ZA_1.sqlite": carbon_tax[1],
                       "ZB_0.sqlite": carbon_tax[1], "ZB_1.sqlite": carbon_tax[1],
                       "T_0.sqlite": carbon_tax[0], "T_1.sqlite": carbon_tax[0],
                       "U_0.sqlite": carbon_tax[1], "U_1.sqlite": carbon_tax[1],
                       "V_0.sqlite": carbon_tax[2], "V_1.sqlite": carbon_tax[2],
                       "AA_0.sqlite": carbon_tax[2], "AA_1.sqlite": carbon_tax[2],
                       "AB_0.sqlite": carbon_tax[2], "AB_1.sqlite": carbon_tax[2],
                       "AD_0.sqlite": carbon_tax[2], "AD_1.sqlite": carbon_tax[2],
                       "AE_0.sqlite": carbon_tax[2], "AE_1.sqlite": carbon_tax[2],
                       "AF_0.sqlite": carbon_tax[2], "AF_1.sqlite": carbon_tax[2]}

    # create tasks
    entries = ['db', 'metric', 'run_name', 'folder_results']
    tasks = pd.DataFrame(columns=entries)
    for db in dbs:

        metrics = ['capacity_by_tech']

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
    capacity_by_fuel = []
    capacity_by_tech = []

    for index, task in tasks.iterrows():
        db = task['db']
        metric = task['metric']
        run_name = task['run_name']
        folder_results = task['folder_results']

        os.chdir(folder_results)

        if metric == 'capacity_by_fuel':
            temp = pd.read_csv('capacity_by_fuel.csv')
            if len(capacity_by_fuel) == 0:
                capacity_by_fuel = temp
            else:
                capacity_by_fuel = pd.concat([capacity_by_fuel, temp])

        elif metric == 'capacity_by_tech':
            temp = pd.read_csv('capacity_by_tech.csv')
            if len(capacity_by_tech) == 0:
                capacity_by_tech = temp
            else:
                capacity_by_tech = pd.concat([capacity_by_tech, temp])

    # save
    os.chdir(result_folder)
    if len(capacity_by_fuel) > 0:
        toSave = pd.melt(capacity_by_fuel, id_vars=['fuelOrTech', 'database'],
                         value_vars=['2016', '2021', '2026', '2031', '2036'],
                         var_name='Year', value_name='Value')
        toSave.to_csv('capacity_by_fuel_toAnalyze.csv')
    if len(capacity_by_tech) > 0:
        toSave = pd.melt(capacity_by_tech, id_vars=['fuelOrTech', 'database'],
                         value_vars=['2016', '2021', '2026', '2031', '2036'],
                         var_name='Year', value_name='Value')
        toSave.to_csv('capacity_by_tech_toAnalyze.csv')

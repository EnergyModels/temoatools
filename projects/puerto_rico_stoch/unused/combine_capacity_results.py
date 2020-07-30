import os
import pandas as pd
import temoatools as tt
from joblib import Parallel, delayed, parallel_backend


if __name__ == '__main__':
    try:
        ncpus = int(os.getenv('NUM_PROCS'))  # try to use variable defined in sbatch script
    except:
        ncpus = 2  # otherwise default to this number of cores

    db_folder = os.path.join(os.getcwd(), 'stochastic_databases')
    result_folder = os.path.join(os.getcwd(), 'results')

    print("running")

    # Names of databases simulated
    dbs = ["T_0.sqlite",
           "U_0.sqlite",
           "V_0.sqlite",
           "T.sqlite",
           "U.sqlite",
           "V.sqlite",
           ]

    # create tasks
    entries = ['db', 'metric', 'run_name', 'folder_results']
    tasks = pd.DataFrame(columns=entries)
    for db in dbs:

        # metrics available
        # metrics = ['costs_yearly', 'emissions_yearly', 'activity_by_fuel', 'activity_by_tech', 'capacity_by_fuel',
        #            'capacity_by_tech']

        # For our analysis we only use the following metrics
        if db == "T_0.sqlite" or db == "U_0.sqlite" or db == "V_0.sqlite":
            metrics = ['capacity_by_fuel', 'capacity_by_tech']

        for metric in metrics:
            t = pd.Series(index=entries)
            t['db'] = db
            t['metric'] = metric
            t['run_name'] = tt.remove_ext(db)
            t['folder_results'] = os.path.join(result_folder, t['run_name'])
            tasks = tasks.append(t, ignore_index=True)

    # -------------------
    # combine the results
    # -------------------
    costs_yearly = []
    emissions_yearly = []
    activity_by_fuel = []
    activity_by_tech = []
    capacity_by_fuel = []
    capacity_by_tech = []

    for index, task in tasks.iterrows():
        db = task['db']
        metric = task['metric']
        run_name = task['run_name']
        folder_results = task['folder_results']

        os.chdir(folder_results)

        if metric == 'capacity_by_fuel':
            temp = pd.read_csv('capacity_by_fuel_toPlot.csv')
            if len(capacity_by_fuel) == 0:
                capacity_by_fuel = temp
            else:
                capacity_by_fuel = pd.concat([capacity_by_fuel, temp])

        elif metric == 'capacity_by_tech':
            temp = pd.read_csv('capacity_by_tech_toPlot.csv')
            if len(capacity_by_tech) == 0:
                capacity_by_tech = temp
            else:
                capacity_by_tech = pd.concat([capacity_by_tech, temp])

    # save
    os.chdir(result_folder)
    capacity_by_fuel.to_csv('capacity_by_fuel_toPlot.csv')
    capacity_by_tech.to_csv('capacity_by_tech_toPlot.csv')


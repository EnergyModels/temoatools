import os
import pandas as pd
import temoatools as tt
from joblib import Parallel, delayed, parallel_backend


if __name__ == '__main__':
    ncpus = 2 # int(os.getenv('NUM_PROCS'))

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

        elif metric == 'capacity_by_fuel':
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


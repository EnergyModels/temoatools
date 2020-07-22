# ======================================================================================================================
# monte_carlo_run.py
# Jeff Bennett, jab6ft@virginia.edu
#
# This script provides an example of using Temoatools to build and run Monte Carlo simluations using Temoa models.
# The approach remains from the baselines example to build models from two .xlsx files. The first
# provides all possible system and technology data (named data.xlsx in the example). The second specifies scenarios
# that make use of specified combinations of technology data (named Scenarios.xlsx in the example).
#
# Required inputs (lines 106-116)
#   temoa_path - path to Temoa directory that contains temoa_model/
#   project_path - path to directory that contains this file (expects a subdirectory within named data)
#   modelInputs_XLSX_list - list that contains the *.xlsx file with model data (within data subdirectory)
#   scenarioInputs - identifies which technologies are used for each scenario (within data subdirectory)
#   scenarioNames_list - names of each scenario to perform a monte carlo simulation with (named within ScenarioInputs)
#   sensitivityInputs - identifies which parameters to vary in monte carlo study
#   sensitivityMultiplier - percent perturbation for each sensitivity variable
#   ncpus - number of cores to use, -1 for all, -2 for all but one, replace with int(os.getenv('NUM_PROCS')) for cluster
#   solver - leave as '' to use system default, other options include 'cplex', 'gurobi'
#   n_cases - number of simulations to run
#
# Outputs (paths are all relative to project_path)
#   data/data.db - universal database that contains input data in a .sqlite database
#   configs/config_*.txt - a separate configuration file for each Temoa run
#   databases/*.dat - a separate .sqlite database for each Temoa run
#   databases/*.sqlite - a separate .sqlite database for each Temoa run
# ======================================================================================================================
import os
from joblib import Parallel, delayed, parallel_backend
import pandas as pd
import temoatools as tt
from pathlib import Path
import numpy as np


# =======================================================
# Function to evaluate a single model
# =======================================================
def evaluateMonteCarlo(modelInputs, scenarioXLSX, scenarioName, temoa_path, project_path, solver, cases, caseNum):
    # Unique filename
    model_filename = scenarioName + '_MC_' + str(caseNum)

    # Prepare monte carlo inputs
    cols = ['type', 'variable', 'tech', caseNum]
    MCinputs = cases.loc[:, cols]
    MCinputs = MCinputs.rename(columns={caseNum: 'multiplier'})

    # Build Model
    tt.build(modelInputs, scenarioXLSX, scenarioName, model_filename, MCinputs=MCinputs, path=project_path)

    # Run Model
    error = tt.run(model_filename, temoa_path=temoa_path, saveEXCEL=False, solver=solver)

    # Analyze Results
    folder = os.path.join(project_path, 'databases')
    db = model_filename + '.sqlite'
    if not error:
        yearlyCosts, LCOE = tt.getCosts(folder, db)
        yearlyCosts = yearlyCosts.drop(columns=['database', 'scenario'])
        yearlyEmissions, avgEmissions = tt.getEmissions(folder, db)
        yearlyEmissions = yearlyEmissions.drop(columns=['database', 'scenario'])

        # Capacity and Activity by Fuel By Year
        switch = 'fuel'
        capacityByFuel = tt.getCapacity(folder, db, switch=switch)
        capacityByFuel = capacityByFuel.drop(columns=['database', 'scenario'])
        capacityByFuel = capacityByFuel.set_index('fuelOrTech')
        ActivityByYearFuel = tt.getActivity(folder, db, switch=switch)
        ActivityByYearFuel = ActivityByYearFuel.drop(columns=['database', 'scenario'])
        ActivityByYearFuel = ActivityByYearFuel.set_index('fuelOrTech')

    # Package Outputs
    output = pd.Series()
    output['db'] = db
    output['caseNum'] = caseNum
    if not error:
        output['LCOE'] = LCOE.loc[0, 'LCOE']
        output['avgEmissions'] = avgEmissions.loc[0, 'avgEmissions']
    else:
        output['LCOE'] = np.nan
        output['avgEmissions'] = np.nan
    for col in yearlyCosts.columns:
        label = 'cost-' + str(col)
        output[label] = yearlyCosts.loc[0, col]
    for col in yearlyEmissions.columns:
        label = 'emis-' + str(col)
        output[label] = yearlyEmissions.loc[0, col]
    # CapacityByYearFuel
    for ind in capacityByFuel.index:
        for col in capacityByFuel.columns:
            label = 'cap_' + str(col) + '-' + str(ind)
            output[label] = capacityByFuel.loc[ind, col]
    # ActivityByYearFuel
    for ind in ActivityByYearFuel.index:
        for col in ActivityByYearFuel.columns:
            label = 'act_' + str(col) + '-' + str(ind)
            output[label] = ActivityByYearFuel.loc[ind, col]
    return output


if __name__ == '__main__':

    # =======================================================
    # Model Inputs
    # =======================================================
    temoa_path = Path('C:/temoa-energysystem')  # Path('/home/jab6ft/temoa/temoa')
    project_path = Path(os.getcwd())
    modelInputs_XLSX = 'data.xlsx'
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames = ['A']
    sensitivityInputs = 'sensitivityVariables.xlsx'
    sensitivityMultiplier = 10.0  # percent perturbation
    ncpus = 6   # default, unless otherwise specified in sbatch script
    solver = ''  # leave blank to let temoa decide which solver to use of those installed
    n_cases = 10

    # =======================================================
    # begin script
    # =======================================================
    try:
        ncpus = int(os.getenv('NUM_PROCS'))  # try to use variable defined in sbatch script
    except:
        ncpus = ncpus  # otherwise default to this number of cores

    # =======================================================
    # Move modelInputs_XLSX to database
    # =======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path=project_path)

    # =======================================================
    # Create directories - best completed before using multiprocessing
    # =======================================================
    mc_dir = 'monte_carlo'
    tt.create_dir(project_path=project_path, optional_dir=mc_dir)

    # ====================================
    # Perform Simulations
    # ====================================

    for scenarioName in scenarioNames:
        # Create monte carlo cases

        cases = tt.createMonteCarloCases(scenarioInputs, scenarioName, sensitivityInputs, sensitivityMultiplier,
                                         n_cases=n_cases, path=project_path)
        # Save cases
        os.chdir(os.path.join(project_path, mc_dir))
        cases.to_csv('MonteCarloInputs_' + scenarioName + '.csv')
        os.chdir(project_path)

        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=ncpus):
            outputs = Parallel(n_jobs=ncpus, verbose=5)(
                delayed(evaluateMonteCarlo)(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, solver,
                                            cases,
                                            caseNum) for
                caseNum in range(n_cases))

        # Save results to a csv
        os.chdir(os.path.join(project_path, mc_dir))
        df = pd.DataFrame(outputs, dtype='float64')
        df.to_csv('MonteCarloResults_' + scenarioName + '.csv')
        os.chdir(project_path)

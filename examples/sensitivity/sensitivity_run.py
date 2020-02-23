# ======================================================================================================================
# sensitivity_run.py
# Jeff Bennett, jab6ft@virginia.edu
#
# This script provides an example of using Temoatools to build and run a sensitivity study on Temoa models.
# The approach is very similar to the monte_carlo example, where a list of variables are perturbed. The key difference
# from the monte_carlo example is that only one variable is perturbed at a time.
#
# Required inputs (lines 86-94)
#   temoa_path - path to Temoa directory that contains temoa_model/
#   project_path - path to directory that contains this file (expects a subdirectory within named data)
#   modelInputs_XLSX_list - list that contains the *.xlsx file with model data (within data subdirectory)
#   scenarioInputs - identifies which technologies are used for each scenario (within data subdirectory)
#   scenarioNames_list - names of each scenario to perform a monte carlo simulation with (named within ScenarioInputs)
#   sensitivityInputs - identifies which parameters to vary in monte carlo study
#   sensitivityMultiplier - percent perturbation for each sensitivity variable
#   ncpus - number of cores to use, -1 for all, -2 for all but one, replace with int(os.getenv('NUM_PROCS')) for cluster
#   solver - leave as '' to use system default, other options include 'cplex', 'gurobi'
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


# =======================================================
# Function to evaluate a single model
# =======================================================
def evaluateModelSensitivity(modelInputs, scenarioXLSX, scenarioName, temoa_path, project_path, solver, cases, caseNum):
    # Unique filename
    model_filename = scenarioName + '_Sens_' + str(caseNum)

    # Prepare sensitivity
    sensitivity = cases.loc[caseNum]

    # Build Model
    tt.build(modelInputs, scenarioXLSX, scenarioName, model_filename, sensitivity=sensitivity, path=project_path)

    # Run Model
    tt.run(model_filename, temoa_path=temoa_path, saveEXCEL=False, solver=solver)

    # Analyze Results
    folder = os.path.join(project_path, 'databases')
    db = model_filename + '.sqlite'
    yearlyCosts, LCOE = tt.getCosts(folder, db)
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, db)

    # Package Outputs
    output = pd.Series()
    output['type'] = cases.loc[caseNum, 'type']
    output['tech'] = cases.loc[caseNum, 'tech']
    output['variable'] = cases.loc[caseNum, 'variable']
    output['multiplier'] = cases.loc[caseNum, 'multiplier']
    output['db'] = db
    output['caseNum'] = caseNum
    output['LCOE'] = LCOE.loc[0, 'LCOE']
    output['avgEmissions'] = avgEmissions.loc[0, 'avgEmissions']

    return output


if __name__ == '__main__':

    # =======================================================
    # Model Inputs
    # =======================================================
    temoa_path = Path('C:/temoa/temoa')  # Path('/home/jab6ft/temoa/temoa')
    project_path = Path(
        'C:/Users/benne/PycharmProjects/temoatools/examples/sensitivity')  # Path('/home/jab6ft/temoa/project/sensitivity')
    modelInputs_XLSX = 'data.xlsx'
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames = ['A']
    sensitivityInputs = 'sensitivityVariables.xlsx'
    sensitivityMultiplier = 10.0  # percent perturbation
    ncpus = 6  # int(os.getenv('NUM_PROCS'))
    solver = ''  # 'gurobi'

    # =======================================================
    # Move modelInputs_XLSX to database
    # =======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path=project_path)

    # =======================================================
    # Create directories - best completed before using multiprocessing
    # =======================================================
    sens_dir = 'sensitivity'
    tt.create_dir(project_path=project_path, optional_dir=sens_dir)

    # ====================================
    # Perform Simulations
    # ====================================

    for scenarioName in scenarioNames:
        # Create sensitivity cases
        cases = tt.createSensitivityCases(scenarioInputs, scenarioName, sensitivityInputs, sensitivityMultiplier,
                                          project_path)

        # Save sensitivity cases
        os.chdir(os.path.join(project_path, sens_dir))
        cases.to_csv('SensitivityInputs_' + scenarioName + '.csv')
        os.chdir(project_path)

        # Count number of cases
        n_cases = len(cases)

        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=ncpus):
            outputs = Parallel(n_jobs=ncpus, verbose=5)(
                delayed(evaluateModelSensitivity)(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, solver,
                                                  cases, caseNum) for
                caseNum in range(n_cases))

        # Save results to a csv
        os.chdir(os.path.join(project_path, sens_dir))
        df = pd.DataFrame(outputs)
        df.to_csv('SensitivityResults_' + scenarioName + '.csv')
        os.chdir(project_path)

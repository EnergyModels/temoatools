# ======================================================================================================================
# monte_carlo_run.py
# Jeff Bennett, jab6ft@virginia.edu
#
# This script provides an example of using Temoatools to build and run Monte Carlo simluations using Temoa models.
# The approach remains from the baselins example to build models from two .xlsx files. The first
# provides all possible system and technology data (named data.xlsx in the example). The second specifies scenarios
# that make use of specified combinations of technology data (named Scenarios.xlsx in the example).
#
# Required inputs (lines 46-50)
#   temoa_path - path to Temoa directory that contains temoa_model/
#   project_path - path to directory that contains this file (expects a subdirectory within named data)
#   modelInputs_XLSX_list - list that contains the *.xlsx file with model data (within data subdirectory)
#   scenarioInputs - TODO
#   scenarioNames_list - names of each scenario to perform a monte carlo simulation with (named within ScenarioInputs file)
#   sensitivityInputs  TODO
#   sensitivityMultiplier - percent perturbation TODO
#
# Outputs (paths are all relative to project_path) TODO
#   data/data.db - universal database that contains input data in a .sqlite database TODO
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
def evaluateMonteCarlo(modelInputs, scenarioXLSX, scenarioName, temoa_path, project_path, cases, caseNum):
    # Unique filename
    model_filename = scenarioName + '_MC_' + str(caseNum)

    # Prepare monte carlo inputs
    cols = ['type', 'variable', 'tech', caseNum]
    MCinputs = cases.ix[:, cols]
    MCinputs = MCinputs.rename(columns={caseNum: 'multiplier'})

    # Build Model
    tt.build(modelInputs, scenarioXLSX, scenarioName, model_filename, MCinputs=MCinputs, path=project_path)

    # Run Model
    tt.run(model_filename, temoa_path=temoa_path, saveEXCEL=False)

    # Analyze Results
    folder = os.getcwd() + '\\Databases'  # TODO
    db = model_filename + '.sqlite'
    yearlyCosts, LCOE = tt.getCosts(folder, db)
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, db)

    # Capacity and Activity by Fuel By Year
    createPlots = 'N'  # Create default plots
    saveData = 'N'  # Do not save data as a csv or xls
    sectorName = 'electric'  # Name of sector to be analyzed
    switch = 'fuel'
    capacityByFuel = tt.getCapacity(folder, db, switch=switch)
    key = capacityByFuel.keys()[0]
    cap = capacityByFuel[key]
    ActivityByYearFuel = tt.getActivity(folder, db, switch=switch)
    key = ActivityByYearFuel.keys()[0]
    act = ActivityByYearFuel[key]

    # Move results to series
    col = yearlyCosts.columns[0]
    yearlyCosts = yearlyCosts[col]
    LCOE = LCOE[col]
    col = yearlyEmissions.columns[0]
    yearlyEmissions = yearlyEmissions[col]
    avgEmissions = avgEmissions[col]

    # Package Outputs
    output = pd.Series()
    output['db'] = db
    output['caseNum'] = caseNum
    output['LCOE'] = LCOE
    output['avgEmissions'] = avgEmissions
    for ind in yearlyCosts.index:
        label = 'cost-' + str(ind)
        output[label] = yearlyCosts.loc[ind]
    for ind in yearlyEmissions.index:
        label = 'emis-' + str(ind)
        output[label] = yearlyEmissions.loc[ind]
    # CapacityByYearFuel
    for ind in cap.index:
        for col in cap.columns:
            label = 'cap_' + str(col) + '-' + str(ind)
            output[label] = cap.loc[ind, col]
    # ActivityByYearFuel
    for ind in act.index:
        for col in act.columns:
            label = 'act_' + str(col) + '-' + str(ind)
            output[label] = act.loc[ind, col]
    return output


if __name__ == '__main__':

    # =======================================================
    # Model Inputs
    # =======================================================
    temoa_path = Path('C:/temoa/temoa')
    project_path = Path('C:/Users/benne/PycharmProjects/temoatools/examples/monte_carlo')
    modelInputs_XLSX = 'data.xlsx'
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames = ['A', 'B', 'C', 'D']
    sensitivityInputs = 'sensitivityVariables.xlsx'
    sensitivityMultiplier = 10.0  # percent perturbation

    # =======================================================
    # Move modelInputs_XLSX to database
    # =======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path=project_path)

    # =======================================================
    # Create directory to hold inputs and outputs
    # =======================================================
    workDir = os.getcwd()
    sensDir = os.path.join(workDir, "monteCarlo")
    try:
        os.stat(sensDir)
    except:
        os.mkdir(sensDir)

    # ====================================
    # Perform Simulations
    # ====================================

    for scenarioName in scenarioNames:
        # Create monte carlo cases
        n_cases = 10
        cases = tt.createMonteCarloCases(scenarioInputs, scenarioName, sensitivityInputs, sensitivityMultiplier,
                                         n_cases=n_cases, path=project_path)

        # Save cases
        os.chdir(sensDir)
        cases.to_csv('MonteCarloInputs_' + scenarioName + '.csv')
        os.chdir(workDir)

        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=-2):
            outputs = Parallel(n_jobs=-2, verbose=5)(
                delayed(evaluateMonteCarlo)(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, cases,
                                            caseNum) for
                caseNum in range(n_cases))

        # Save results to a csv
        os.chdir(sensDir)
        df = pd.DataFrame(outputs)
        df.to_csv('MonteCarloResults_' + scenarioName + '.csv')
        os.chdir(workDir)

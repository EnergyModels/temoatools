import os
from joblib import Parallel, delayed, parallel_backend
import pandas as pd
import temoatools as tt
from pathlib import Path

# =======================================================
# Function to evaluate a single model
# =======================================================
def evaluateMonteCarlo(modelInputs, scenarioXLSX, scenarioName, temoa_path, cases, caseNum):
    # Unique filename
    model_filename = scenarioName + '_MC_' + str(caseNum)

    # Prepare monte carlo inputs
    cols = ['type', 'variable', 'tech', caseNum]
    MCinputs = cases.ix[:, cols]
    MCinputs = MCinputs.rename(columns={caseNum: 'multiplier'})

    # Build Model
    tt.build(modelInputs, scenarioXLSX, scenarioName, model_filename, MCinputs=MCinputs, path='data')

    # Run Model
    tt.run(model_filename, temoa_path=temoa_path, saveEXCEL=False)

    # Analyze Results
    folder = os.getcwd() + '\\Databases'
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
    modelInputs_XLSX = 'data.xlsx'
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames = ['A', 'B', 'C', 'D']
    temoa_path = Path('C:/temoa/temoa')  # path to temoa directory that contains temoa_model/
    sensitivityInputs = 'sensitivityVariables.xlsx'
    sensitivityMultiplier = 10.0  # percent perturbation

    # =======================================================
    # Move modelInputs_XLSX to database
    # =======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path='data')

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
                                         n_cases=n_cases, path='data')

        # Save cases
        os.chdir(sensDir)
        cases.to_csv('MonteCarloInputs_' + scenarioName + '.csv')
        os.chdir(workDir)

        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=-2):
            outputs = Parallel(n_jobs=-2, verbose=5)(
                delayed(evaluateMonteCarlo)(modelInputs, scenarioInputs, scenarioName, temoa_path, cases, caseNum) for
                caseNum in range(n_cases))

        # Save results to a csv
        os.chdir(sensDir)
        df = pd.DataFrame(outputs)
        df.to_csv('MonteCarloResults_' + scenarioName + '.csv')
        os.chdir(workDir)

# ======================================================================================================================
# baselines_run.py
# Jeff Bennett, jab6ft@virginia.edu
#
# This script provides an example of using Temoatools to build and run Temoa models from two .xlsx files. The first
# provides all possible system and technology data (named data.xlsx in the example). The second specifies scenarios
# that make use of specified combinations of technology data (named Scenarios.xlsx in the example).
#
# Required inputs (lines 49-55)
#   temoa_path - path to Temoa directory that contains temoa_model/
#   project_path - path to directory that contains this file (expects a subdirectory within named data)
#   modelInputs_XLSX_list - list that contains the *.xlsx file with model data (within data subdirectory)
#   scenarioInputs - identifies which technologies are used for each scenario (within data subdirectory)
#   scenarioNames_list - names of each scenario to be run from the scenarioInputs file (named within ScenarioInputs file)
#   ncpus - number of cores to use, -1 for all, -2 for all but one, replace with int(os.getenv('NUM_PROCS')) for cluster
#   solver - leave as '' to use system default, other options include 'cplex', 'gurobi'
#
# Outputs (paths are all relative to project_path)
#   data/data.db - universal database that contains input data in a .sqlite database
#   configs/config_*.txt - a separate configuration file for each Temoa run
#   databases/*.dat - a separate .sqlite database for each Temoa run
#   databases/*.sqlite - a separate .sqlite database for each Temoa run
# ======================================================================================================================
import temoatools as tt
from joblib import Parallel, delayed, parallel_backend
from pathlib import Path
import os


# =======================================================
# Function to evaluate a single model
# =======================================================
def evaluateModel(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, solver):
    # Unique filename
    model_filename = scenarioName

    # Build Model
    tt.build(modelInputs, scenarioInputs, scenarioName, model_filename, path=project_path)

    # Run Model
    tt.run(model_filename, saveEXCEL=False, temoa_path=temoa_path, debug=True, solver=solver)


if __name__ == '__main__':

    # =======================================================
    # Model Inputs
    # =======================================================
    temoa_path = os.path.abspath('../../temoa-energysystem')
    project_path = os.getcwd()
    modelInputs_XLSX_list = ['data.xlsx']
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames_list = [['A', 'B', 'C', 'D', 'E', 'F']]
    ncpus = 6   # default, unless otherwise specified in sbatch script
    solver = ''  # leave blank to let temoa decide which solver to use of those installed

    # =======================================================
    # begin script
    # =======================================================
    try:
        ncpus = int(os.getenv('NUM_PROCS'))  # try to use variable defined in sbatch script
    except:
        ncpus = ncpus  # otherwise default to this number of cores

    for modelInputs_XLSX, scenarioNames in zip(modelInputs_XLSX_list, scenarioNames_list):

        # =======================================================
        # Move modelInputs_XLSX to database
        # =======================================================
        modelInputs = tt.move_data_to_db(modelInputs_XLSX, path=project_path)

        # =======================================================
        # Create directories - best completed before using multiprocessing
        # =======================================================
        tt.create_dir(project_path=project_path, optional_dir='results')

        # ====================================
        # Perform Simulations
        option = 2  # 1 - Run single, 2 - Run all
        # ====================================

        if option == 1:
            # Perform single simulation
            evaluateModel(modelInputs, scenarioInputs, scenarioNames[0], temoa_path)

        elif option == 2:
            # Perform simulations in parallel
            with parallel_backend('multiprocessing', n_jobs=ncpus):
                Parallel(n_jobs=ncpus, verbose=5)(
                    delayed(evaluateModel)(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, solver)
                    for
                    scenarioName in
                    scenarioNames)

import temoatools as tt
from joblib import Parallel, delayed, parallel_backend
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
    temoa_path =  os.path.normcase('/home/jab6ft/puerto_rico/temoa_stochastic') # os.path.normcase('C:/Users/benne/PycharmProjects/temoatools/temoa_stochastic')
    project_path = os.path.normcase('/home/jab6ft/puerto_rico/puerto_rico_stoch/') # os.path.normcase('C:/Users/benne/PycharmProjects/temoatools/projects/puerto_rico_stoch')
    modelInputs_XLSX_list = ['data_T.xlsx', 'data_U.xlsx', 'data_V.xlsx', 'data_W.xlsx', 'data_X.xlsx', 'data_Y.xlsx', 'data_Z.xlsx']
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames_list = [['T','T2','T3','T4'], ['U','U2','U3','U4'], ['V','V2','V3','V4'],
                          ['WA', 'WB', 'WC', 'WD','WE','WF'], ['XA', 'XB', 'XC','XD'],
                          ['YA', 'YB', 'YC'],
                          ['ZA', 'ZB', 'ZC']]
    ncpus = int(os.getenv('NUM_PROCS'))
    solver = 'gurobi'

    for modelInputs_XLSX, scenarioNames in zip(modelInputs_XLSX_list, scenarioNames_list):

        # =======================================================
        # Move modelInputs_XLSX to database
        # =======================================================
        modelInputs = tt.move_data_to_db(modelInputs_XLSX, path=project_path)

        # ====================================
        # Perform Simulations
        option = 2  # 1 - Run single, 2 - Run all
        # ====================================

        if option == 1:
            # Perform single simulation
            evaluateModel(modelInputs, scenarioInputs, scenarioNames[0], temoa_path, project_path, solver)

        elif option == 2:
            # Perform simulations in parallel

            with parallel_backend('multiprocessing', n_jobs=ncpus):
                Parallel(n_jobs=ncpus, verbose=5)(
                    delayed(evaluateModel)(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, solver)
                    for scenarioName in
                    scenarioNames)

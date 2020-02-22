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
    temoa_path = Path('C:/temoa/temoa')  # Path('/home/jab6ft/temoa/temoa')
    project_path = Path(
        'C:/Users/benne/PycharmProjects/temoatools/projects/puerto_rico_stoch')  # Path('/home/jab6ft/temoa/project/puerto_rico_stoch')
    modelInputs_XLSX_list = ['data_T.xlsx', 'data_U.xlsx', 'data_W.xlsx', 'data_X.xlsx', 'data_Y.xlsx', 'data_Z.xlsx']
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames_list = [['T'], ['U'], ['WA', 'WB', 'WC', 'WD', 'WE', 'WF'], ['XA', 'XB', 'XC', 'XD', 'XE', 'XF'],
                          ['YA', 'YB', 'YC', 'YD', 'YE', 'YF'],
                          ['ZA', 'ZB', 'ZC', 'ZD', 'ZE', 'ZF']]
    ncpus = 6  # int(os.getenv('NUM_PROCS'))
    solver = ''  # 'gurobi'

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
            evaluateModel(modelInputs, scenarioInputs, scenarioNames[0], temoa_path)

        elif option == 2:
            # Perform simulations in parallel
            with parallel_backend('multiprocessing', n_jobs=ncpus):
                Parallel(n_jobs=ncpus, verbose=5)(
                    delayed(evaluateModel)(modelInputs, scenarioInputs, scenarioName, temoa_path, project_path, solver)
                    for scenarioName in
                    scenarioNames)

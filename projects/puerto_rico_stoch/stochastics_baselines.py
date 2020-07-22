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
    temoa_path = os.path.abspath('..//..//temoa_stochastic')
    project_path = os.getcwd()
    modelInputs_XLSX_list = ['data_T.xlsx', 'data_U.xlsx', 'data_V.xlsx', 'data_W.xlsx', 'data_X.xlsx', 'data_Y.xlsx',
                             'data_Z.xlsx', 'data_A.xlsx']
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames_list = [['T'], ['U'], ['V'],
                          ['WA', 'WB', 'WD', 'WE', 'WF'], ['XA', 'XB', 'XD'],
                          ['YA', 'YB', ],
                          ['ZA', 'ZB', ], ['AA', 'AB', 'AD', 'AE', 'AF'], ]
    solver = ''  # leave blank to let temoa decide which solver to use of those installed
    try:
        ncpus = int(os.getenv('NUM_PROCS'))  # try to use variable defined in sbatch script
    except:
        ncpus = 6  # otherwise default to this number of cores

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

import temoatools as tt
from joblib import Parallel, delayed, parallel_backend
from pathlib import Path
import shutil
import calendar;
import time;


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
    temoa_path = Path('/Users/rogerzhu/Documents/temoa/temoa-energysystem')  # Path('/home/jab6ft/temoa/temoa')
    project_path = Path('/Users/rogerzhu/Documents/temoa/temoa-va/virginia')  # Path('/home/jab6ft/temoa/project/baselines')
    modelInputs_XLSX_list = ['data_virginia.xlsx']
    scenarioInputs = 'scenarios_multiple.xlsx'
    scenarioNames_list = [['A' , 'B']]
    ncpus = 6  # int(os.getenv('NUM_PROCS'))
    solver = ''  # 'gurobi'

    #shutil.copy2('/Users/rogerzhu/Documents/temoa/temoa-va/virginia/data/data_virginia.xlsx', '/Users/rogerzhu/Documents/temoa/temoa-va/virginia/data/data_virginia_'+str(calendar.timegm(time.gmtime()))+'.xlsx');
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

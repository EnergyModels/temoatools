import temoatools as tt
from joblib import Parallel, delayed, parallel_backend


# ==============
# =========================================
# Function to evaluate a single model
# =======================================================
def evaluateModel(modelInputs, scenarioInputs, scenarioName, temoa_path):
    # Unique filename
    model_filename = scenarioName

    # Build Model
    tt.build(modelInputs, scenarioInputs, scenarioName, model_filename, path='data')

    # Run Model
    saveEXCEL = True
    tt.run(model_filename, temoa_path=temoa_path, saveEXCEL=False, debug=False)


if __name__ == '__main__':

    # =======================================================
    # Model Inputs
    # =======================================================
    modelInputs_XLSX = 'data.xlsx'
    scenarioInputs = 'scenarios.xlsx'
    scenarioNames = ['A', 'B', 'C', 'D']
    temoa_path = 'C:/temoa/temoa' # path to temoa directory that contains temoa_model/

    # =======================================================
    # Move modelInputs_XLSX to database
    # =======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path='data')

    # ====================================
    # Perform Simulations
    option = 2  # 1 - Run single, 2 - Run all
    # ====================================

    if option == 1:
        # Perform single simulation
        evaluateModel(modelInputs, scenarioInputs, scenarioNames[0], temoa_path)

    elif option == 2:
        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=-2):
            Parallel(n_jobs=-2, verbose=5)(
                delayed(evaluateModel)(modelInputs, scenarioInputs, scenarioName, temoa_path) for scenarioName in
                scenarioNames)

import temoatools as tt
from joblib import Parallel, delayed, parallel_backend


# =======================================================
# Function to evaluate a single model
# =======================================================
def evaluateModel(modelInputs, scenarioInputs, scenarioName, temoa_path):
    # Unique filename
    model_filename = scenarioName

    # Build Model
    tt.build(modelInputs, scenarioInputs, scenarioName, model_filename, path='data')

    # Run Model
    saveEXCEL = True
    tt.run(model_filename, saveEXCEL=False, temoa_path=temoa_path, debug=False)


if __name__ == '__main__':

    # =======================================================
    # Model Inputs - without Carbon Pricing
    # =======================================================
    modelInputs_XLSX_list = ['data.xlsx']
    scenarioNames_list = [['A', 'B', 'C', 'D', 'E', 'F']]
    temoa_path = 'C:/temoa/temoa'  # path to temoa directory that contains temoa_model/

    scenarioInputs = 'scenarios.xlsx'

    for modelInputs_XLSX, scenarioNames in zip(modelInputs_XLSX_list, scenarioNames_list):

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

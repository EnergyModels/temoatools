import os
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
import pandas as pd
import temoatools as tt

#=======================================================
# Function to evaluate a single model
#=======================================================
def evaluateModelSensitivity(modelInputs, scenarioXLSX, scenarioName, temoa_paths, cases, caseNum):

    # Unique filename
    model_filename = scenarioName + '_Sens_' + str(caseNum)
    
    # Prepare sensitivity
    sensitivity = cases.loc[caseNum]
    
    # Build Model
    tt.build(modelInputs,scenarioXLSX,scenarioName,model_filename,sensitivity=sensitivity,path='data')

    # Run Model
    saveEXCEL=False
    tt.run(model_filename,temoa_paths,saveEXCEL=saveEXCEL)
    
    # Analyze Results
    folder = os.getcwd() + '\\databases'
    db = model_filename + '.sqlite'
    print "db: " + db
    yearlyCosts, LCOE = tt.getCosts(folder, db)
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, db)

    # Move results to series
    col = yearlyCosts.columns[0]
    yearlyCosts = yearlyCosts[col]
    LCOE = LCOE[col]
    col = yearlyEmissions.columns[0]
    yearlyEmissions = yearlyEmissions[col]
    avgEmissions = avgEmissions[col]

    # Package Outputs
    output                    = sensitivity.copy() # Inputs
    output['db']              = db
    output['caseNum']         = caseNum
    output['LCOE']            = LCOE
    output['avgEmissions']    = avgEmissions
    for ind in yearlyCosts.index:
        label = 'cost_' + str(ind)
        output[label] = yearlyCosts[ind]
    for ind in yearlyEmissions.index:
        label = 'emis_' + str(ind)
        output[label] = yearlyEmissions[ind]
    
    return output


if __name__ == '__main__':

    #=======================================================
    # Model Inputs
    #=======================================================
    modelInputs_XLSX        = 'data.xlsx'
    scenarioInputs          = 'scenarios.xlsx'
    scenarioNames           = ['A','B','C','D'] 
    paths                   = 'paths.csv'
    sensitivityInputs       = 'sensitivityVariables.xlsx'
    sensitivityMultiplier   = 10.0 # percent perturbation
    
    #=======================================================
    # Move modelInputs_XLSX to database
    #=======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path='data')
    
    #=======================================================
    # Create directory to hold sensitivity inputs and outputs
    #=======================================================
    workDir = os.getcwd()
    sensDir = workDir + "\\sensitivity"
    try:
        os.stat(sensDir)
    except:
        os.mkdir(sensDir)
            
    #====================================    
    # Perform Simulations
    #====================================
    num_cores = multiprocessing.cpu_count() -1 # Save one core for other processes
    
    for scenarioName in scenarioNames:
    
        # Create sensitivity cases
        cases = tt.createSensitivityCases(scenarioInputs, scenarioName, sensitivityInputs,sensitivityMultiplier,path='data')
        
        # Save sensitivity cases
        os.chdir(sensDir)
        cases.to_csv('SensitivityInputs_'+scenarioName+'.csv')
        os.chdir(workDir)
        
        # Count number of cases
        n_cases = len(cases)
        
        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=num_cores):
            outputs = Parallel(n_jobs=num_cores,verbose=5)(delayed(evaluateModelSensitivity)(modelInputs, scenarioInputs, scenarioName, paths, cases, caseNum) for caseNum in range(n_cases))
    
        # Save results to a csv
        os.chdir(sensDir)
        df = pd.DataFrame(outputs)
        df.to_csv('SensitivityResults_'+scenarioName+'.csv')
        os.chdir(workDir)
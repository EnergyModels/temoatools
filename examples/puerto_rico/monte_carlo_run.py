# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 18:21:13 2018

@author: benne
"""
#=======================================================
# Imports
#=======================================================
# General
import os
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
import pandas as pd

# TemoaTools
os.chdir("TemoaTools")
from XLS2DB import moveXLS2DB
from TemoaModelBuild import BuildModel, createMonteCarloCases
from TemoaModelRun   import RunModel
import AnalyzeCosts         as Costs
import AnalyzeEmissions     as Emissions
os.chdir("..")

#=======================================================
# Function to evaluate a single model
#=======================================================
def evaluateMonteCarlo(modelInputs, scenarioXLSX, scenarioName, temoa_paths, cases, caseNum):  

    # Unique filename
    model_filename = scenarioName + '_MC_' + str(caseNum)
    
    # Prepare monte carlo inputs
    cols = ['type', 'variable', 'tech', caseNum]
    MCinputs = cases.ix[:,cols]
    MCinputs = MCinputs.rename(columns={caseNum:'multiplier'})
    
    # Build Model
    BuildModel(modelInputs,scenarioXLSX,scenarioName,model_filename,MCinputs=MCinputs)

    # Run Model
    saveEXCEL=False
    RunModel(model_filename,temoa_paths,saveEXCEL=saveEXCEL)
    
    # Analyze Results
    folder = os.getcwd() + '\\Databases'
    db = model_filename + '.sqlite'
    yearlyCosts, LCOE = Costs.SingleDB(folder, db)
    yearlyEmissions, avgEmissions = Emissions.SingleDB(folder, db)
    
    # Package Outputs
    output = pd.Series()
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
    modelInputs_XLSX        = 'A_Input_Data.xlsx'
    scenarioInputs          = 'A_Input_Scenarios.xlsx'
    scenarioNames           = ['A','B','C','D'] 
    paths                   = 'A_Input_Paths.csv'
    sensitivityInputs       = 'A_Input_Sensitivity_Variables.xlsx'
    sensitivityMultiplier   = 10.0 # percent perturbation
    
    #=======================================================
    # Move modelInputs_XLSX to database
    #=======================================================
    modelInputs = moveXLS2DB(modelInputs_XLSX)
    
    #=======================================================
    # Create directory to hold inputs and outputs
    #=======================================================
    workDir = os.getcwd()
    sensDir = workDir + "\\monteCarlo"
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
        n_cases = 1000
        cases = createMonteCarloCases(scenarioInputs, scenarioName, sensitivityInputs,sensitivityMultiplier,n_cases=n_cases)
        
        # Save cases
        os.chdir(sensDir)
        cases.to_csv('MonteCarloInputs_'+scenarioName+'.csv')
        os.chdir(workDir)
                
        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=num_cores):
            outputs = Parallel(n_jobs=num_cores,verbose=5)(delayed(evaluateMonteCarlo)(modelInputs, scenarioInputs, scenarioName, paths, cases, caseNum) for caseNum in range(n_cases))     
    
        # Save results to a csv
        os.chdir(sensDir)
        df = pd.DataFrame(outputs)
        df.to_csv('MonteCarloResults_'+scenarioName+'.csv')
        os.chdir(workDir)
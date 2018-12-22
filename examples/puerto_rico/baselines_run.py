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

# TemoaTools
os.chdir("TemoaTools")
from XLS2DB import moveXLS2DB
from TemoaModelBuild import BuildModel
from TemoaModelRun   import RunModel
os.chdir("..")

#=======================================================
# Function to evaluate a single model
#=======================================================
def evaluateModel(modelInputs, scenarioXLSX, scenarioName, temoa_paths):  

    # Unique filename
    model_filename = scenarioName
    
    # Build Model
    BuildModel(modelInputs,scenarioXLSX,scenarioName,model_filename)
    
    # Run Model
    saveEXCEL=True
    RunModel(model_filename,temoa_paths,saveEXCEL=saveEXCEL)
    
if __name__ == '__main__':
    
    #=======================================================
    # Model Inputs
    #=======================================================
    modelInputs_XLSX  = 'A_Input_Data.xlsx'
    scenarioInputs    = 'A_Input_Scenarios.xlsx'
    scenarioNames     = ['A','B','C','D']
    paths             = 'A_Input_Paths.csv'

    #=======================================================
    # Move modelInputs_XLSX to database
    #=======================================================
    modelInputs = moveXLS2DB(modelInputs_XLSX)
    
    #====================================    
    # Perform Simulations
    option = 2 # 1 - Run single, 2 - Run all
    #====================================
    num_cores = multiprocessing.cpu_count() -1 # Save one core for other processes
    
    if option==1:
        # Perform single simulation
        evaluateModel(modelInputs, scenarioInputs, scenarioNames[0], paths)
    
    elif option == 2:
        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=num_cores):
            Parallel(n_jobs=num_cores,verbose=5)(delayed(evaluateModel)(modelInputs, scenarioInputs, scenarioName, paths) for scenarioName in scenarioNames)     
    
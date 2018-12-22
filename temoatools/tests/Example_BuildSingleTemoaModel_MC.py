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

# TemoaTools
os.chdir("TemoaTools")
from XLS2DB import moveXLS2DB
from TemoaModelBuild import BuildModel,createMonteCarloCases,applySensitivity
import TemoaModelBuild as BTM
os.chdir("..")

#=======================================================
# Model Inputs
#=======================================================
modelInputs_XLSX  = 'A_Input_Data.xlsx'
scenarioInputs    = 'A_Input_Scenarios.xlsx'
scenarioName      = 'A'
paths             = 'A_Input_Paths.csv'
sensitivityInputs       = 'A_Input_Sensitivity_Variables.xlsx'
sensitivityMultiplier   = 10.0 # percent perturbation

# Select which approach to use (both do the same thing, one makes the steps more clear)
option = 2

#=======================================================
# Move modelInputs to database
#=======================================================
modelInputs = moveXLS2DB(modelInputs_XLSX)


# Create monte carlo cases
n_cases = 1
caseNum = 0
cases = createMonteCarloCases(scenarioInputs, scenarioName, sensitivityInputs,sensitivityMultiplier,n_cases=n_cases)
cols = ['type', 'variable', 'tech', caseNum]
MCinputs = cases.loc[:,cols]
MCinputs = MCinputs.rename(columns={caseNum:'multiplier'})

#=======================================================
# Option 1 - Run Temoa Model Builder with single function
#=======================================================
if option == 1:
#    from TemoaModelBuild import BuildModel
    model_filename = modelInputs[:modelInputs.find('.')] + '_' + scenarioName
    BuildModel(modelInputs,scenarioInputs,scenarioName,model_filename)

#=======================================================
# Option 2 - Run Temoa Model Builder with access to all inputs, local variables and outputs
#=======================================================
if option == 2:
#    import TemoaModelBuild as BTM
    # Get empty dictionary of local variables
    local = BTM.getEmptyLocalDict()
    
    # Process scenarios
    local = BTM.processScenarios(scenarioInputs,scenarioName,local)
    
    # Read-in inputs as dictionary
    inputs = BTM.inputs2Dict(modelInputs)
    
    # Apply Monte Carlo to inputs
#    if not len(MCinputs)==0: # if dictionary is empty, it will evaluae to false, and no monte carlo will be performed
#        for i in range(len(MCinputs)):
#            inputs,local = applySensitivity(inputs,MCinputs.loc[i,:],local)
    
    # Create empty dictionary of temoa outputs
    outputs = BTM.getEmptyTemoaDict()
    
    # System parameters
    local,outputs = BTM.processSystem(inputs,local,outputs)
    
    # PowerPlants
    local,outputs = BTM.processPowerPlants(inputs,local,outputs)
    
    # Fuels
    local,outputs = BTM.processFuels(inputs,local,outputs)
    
    # Connections
    local,outputs = BTM.processConnections(inputs,local,outputs)
    
    # Copy db_schema_temoa_mod.db and write(commit) outputs to it
    model_filename = modelInputs[:modelInputs.find('.')] + '_' + scenarioName
    BTM.Write2Temoa(outputs,model_filename)
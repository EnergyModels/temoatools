# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 17:19:50 2018

@author: jab6ft
"""
#=======================================================
# Imports
#=======================================================
# General
import os

# TemoaTools
os.chdir("TemoaTools")
import AnalyzeCosts         as Costs
import AnalyzeEmissions     as Emissions
import AnalyzeCapacity      as Capacity
import AnalyzeActivityYear  as ActivityYear
import AnalyzeActivityTOD   as ActivityTOD
os.chdir("..")

#===============
# Inputs
#===============
analyzeSingle = False
onlySimple = False
folder = dbFolder = os.getcwd() + '\\Databases'
dbs = ["A.sqlite","B.sqlite","C.sqlite","D.sqlite"]
#dbs = ["A.sqlite","B.sqlite","D.sqlite"]

#===============
# Single (only first db)
#===============
if analyzeSingle == True:    
    # Inputs
    db = dbs[0]
    createPlots =    'Y'         # Create default plots
    saveData =       'Y'         # Do not save data as a csv or xls
    sectorName =     'electric'  # Name of sector to be analyzed
    
    # Costs
    yearlyCosts, LCOE = Costs.SingleDB(folder, db, saveData=saveData, createPlots=createPlots)
    
    # Emissions
    yearlyEmissions, avgEmissions = Emissions.SingleDB(folder, db, saveData=saveData, createPlots=createPlots)
    
    # Analyze capacity and activity by fuel types
    switch = 'fuel'
    capacityByFuel = Capacity.SingleDB(folder, db, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
    ActivityByYearFuel = ActivityYear.SingleDB(folder, db, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
    ActivityByTODFuel = ActivityTOD.SingleDB(folder, db, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
    
    # Analyze capacity and activity by technology types
    switch = 'tech'
    capacityByTech = Capacity.SingleDB(folder, db, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
    ActivityByYearFuel = ActivityYear.SingleDB(folder, db, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
    ActivityByTODTech = ActivityTOD.SingleDB(folder, db, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)

#===============
# Multiple
#===============
else:  
    # Inputs:
    createPlots =   'Y'        # Create default plots
    saveData =      'Y'        # Do not save data as a csv or xls
    sectorName=     'electric' # Name of sector to be analyzed
    
    # Costs
    yearlyCosts, LCOE = Costs.MultipleDB(folder, dbs, saveData=saveData, createPlots=createPlots)
    
    # Emissions
    yearlyEmissions, avgEmissions = Emissions.MultipleDB(folder, dbs, saveData=saveData,createPlots=createPlots)
    
    if onlySimple == False:
        # Analyze capacity and activity by fuel types
        switch = 'fuel'
        capacityByFuel = Capacity.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
        ActivityByYearFuel = ActivityYear.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
        ActivityByTODFuel = ActivityTOD.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
        
        # Analyze capacity and activity by technology types
        switch = 'tech'
        capacityByTech = Capacity.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
        ActivityByYearFuel = ActivityYear.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
        ActivityByTODTech = ActivityTOD.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,saveData=saveData,createPlots=createPlots)
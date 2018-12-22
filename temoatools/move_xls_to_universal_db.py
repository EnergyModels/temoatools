# -*- coding: utf-8 -*-
"""
Moves XLS into DB format using DB_Schema.db

Written by Jeff Bennett, 11/16/2018
JAB6ft@virginia.edu
"""
#=============================================================================
# Imports
#=============================================================================
import os
import shutil
import sqlite3
import pandas as pd
import numpy as np

def move_xls_to_db(XLSX):
    
    #=============================================================================
    # Begin Function
    #=============================================================================
    
    # Empty db with set schema (expected to be within the same folder)
    emptydB  = "db_schema_universal.db"
    
    # Create output filename using inputfilename
    outputdB = XLSX[:-5] + ".db"
    
    # Keep track of sheet_names and corresponding number of columns to read-in
    sheets = [("representativeDays",3),("timesOfDay",3),("Connections",11),("ConnectionsExisting",4),
                   ("Demand",4),("DiscountRate",2),("Fuels",12),("FuelsExisting",4),("PowerPlants",8),
                   ("PowerPlantsPerformance",9),("PowerPlantsCosts",7),("PowerPlantsConstraints",7),
                   ("PowerPlantsExisting",4),("ReserveMargin",2),("capacityFactorTOD",5),("ref",6)]
    
    #----------
    # sqlite file prep
    #----------
    # Delete old *.sqlite file (if it already exists) and copy/rename copy of temoa_schema.sqlite
    if os.path.isfile(outputdB):
        os.remove(outputdB)
    shutil.copyfile(emptydB, outputdB)
    
    # Set-up sqlite connection
    conn = sqlite3.connect(outputdB)
    c = conn.cursor()
    
    #----------
    # sqlite file prep
    #----------
    for sheet in sheets:
        
        # Extract sheet_name and number of columns for each sheet:
        sheet_name = sheet[0]
        sheet_col  = sheet[1]
        
        # Read XLS sheet
        df = pd.read_excel(XLSX,sheetname = sheet_name)
        df = df.drop([0]) # Remove first row (units)
        
        # Create SQL command based on number of entries
        command = 'INSERT INTO ' + sheet_name + ' VALUES (?'
        for i in range(sheet_col-1):
            command = command + ',?'
        command = command + ')'
            
        # Execute SQL command
        c.executemany(command,np.array(df))
    
    #----------
    # Save(commit) the changes and close sqlite file
    #----------
    conn.commit()
    conn.close()
    
    return outputdB
    #=============================================================================
    # End Function
    #=============================================================================
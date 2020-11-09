"""
Moves XLS into DB format using DB_Schema.db

Written by Jeff Bennett, 11/16/2018
JAB6ft@virginia.edu
"""
import os
import shutil
import sqlite3
import pandas as pd
import numpy as np
import temoatools as tt
from pathlib import Path


def move_data_to_db(XLSX, path=os.path.normcase('.')):
    # =============================================================================
    # Begin Function
    # =============================================================================
    data_path = os.path.join(path, 'data')
    print(data_path)

    workDir = os.getcwd()
    os.chdir(data_path)

    # Empty db with set schema (expected to be within the same folder)

    emptydB = os.path.join(tt.resource_path, "db_schema_universal.db")

    # Create output filename using inputfilename
    outputdB = tt.remove_ext(XLSX) + ".db"

    # Keep track of sheet_names and corresponding number of columns to read-in
    sheets = [("representativeDays", 3), ("timesOfDay", 3), ("Connections", 16), ("ConnectionsExisting", 4),
              ("Demand", 4), ("DiscountRateGlobal", 2), ("DiscountRateTech", 4), ("Emission", 5), ("Fuels", 15),
              ("FuelsExisting", 4), ("PowerPlants", 10),
              ("PowerPlantsPerformance", 9), ("PowerPlantsCosts", 10), ("PowerPlantsConstraints", 10),
              ("PowerPlantsExisting", 4), ("ReserveMargin", 2), ("capacityFactorTOD", 5), ("ref", 6)]

    # ----------
    # sqlite file prep
    # ----------
    # Delete old *.sqlite file (if it already exists) and copy/rename copy of temoa_schema.sqlite
    if os.path.isfile(outputdB):
        os.remove(outputdB)
    shutil.copyfile(emptydB, outputdB)

    # Set-up sqlite connection
    conn = sqlite3.connect(outputdB)
    c = conn.cursor()

    # ----------
    # sqlite file prep
    # ----------
    for sheet in sheets:

        # Extract sheet_name and number of columns for each sheet:
        sheet_name = sheet[0]
        sheet_col = sheet[1]

        # Read XLS sheet
        df = pd.read_excel(XLSX, sheet_name=sheet_name)
        df = df.drop([0])  # Remove first row (units)

        # Create SQL command based on number of entries
        command = 'INSERT INTO ' + sheet_name + ' VALUES (?'
        for i in range(sheet_col - 1):
            command = command + ',?'
        command = command + ')'

        # Execute SQL command
        try:
            c.executemany(command, np.array(df))
        except:
            print(command)
            print(np.array(df))
            c.executemany(command, np.array(df))

    # ----------
    # Save(commit) the changes and close sqlite file
    # ----------
    conn.commit()
    conn.close()

    os.chdir(workDir)
    return outputdB
    # =============================================================================
    # End Function
    # =============================================================================

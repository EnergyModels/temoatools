# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:38:20 2018

@author: benne
"""
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

debug = False
resolution = 1000 #DPI

#==============================================================================
# Remove filetype from filename
def name(db):
    return db[:db.find('.')]
#==============================================================================
def MultipleDB(folders,dbs,switch='fuel',sectorName='electric',saveData='N',createPlots='N',conversion=277.777778):
#    inputs:
#    1) folders         - paths containing dbs (list or single string if all in the same path)
#    2) dbs             - names of databases (list)
#    3) switch          - 'fuel' or 'tech', basis of categorization
#    4) sectorName      - name of temoa sector to be analyzed
#    5) saveData         - 'Y' or 'N', default is 'N' 
#    6) createPlot      - 'Y' or 'N', default is 'N' 
#    7) conversion      - conversion to GWh, default is 277.778 (from PJ)

#    outputs:
#    1) activity     - pandas DataFrame holding capacity for each model year
#==============================================================================
    # Save original directory
    origDir = os.getcwd()
    
    # If only a single folder provided, create a list of the same folder
    if type(folders)==str:
        fldrs = []
        for db in dbs:
            fldrs.append(folders)
        folders = fldrs
    
    # Create dictionary to hold each capacity_single series
    activity = {}
    
    # Iterate through each db
    for folder,db in zip(folders,dbs):
        activity[name(db)] = SingleDB(folder,db,switch=switch,sectorName=sectorName,conversion=conversion)
      
    # Directory to hold results
    if saveData == 'Y' or createPlots == 'Y':
        resultsDir = origDir + "\\Results"
        try:
            os.stat(resultsDir)
        except:
            os.mkdir(resultsDir)
        os.chdir(resultsDir)
        
    if createPlots == 'Y':
        # Create plots
        n_subplots = len(dbs)
        f,a = plt.subplots(n_subplots,1,sharex=True, sharey=True)
        a = a.ravel()
        # Create subplots
        for idx,ax in enumerate(a):
            db = dbs[idx]
            if switch == 'fuel':
                titlename = name(db) + ' by fuel'
            elif switch == 'tech':
                titlename = name(db) + ' by tech'
            activity[name(db)].plot.bar(ax=ax,stacked=True, title=titlename)
            ax.set_xlabel("Year [-]")
            ax.set_ylabel("Activity [GWh]")

        if switch == 'fuel':
            savename  = 'Results_yearlyActivity_byFuel.png'
        elif switch == 'tech':
            savename  = 'Results_yearlyActivity_byTech.png'
        fig = ax.get_figure()
        fig.savefig(savename,dpi=resolution)
    
    
    # Save results to Excel
    if saveData == 'Y':
        # Create savename based on switch
        if switch == 'fuel':
            savename  = 'Results_yearlyActivity_byFuel.xls'
        elif switch == 'tech':
            savename  = 'Results_yearlyActivity_byTech.xls'
        # Create connection to excel
        writer = pd.ExcelWriter(savename)
        for db in dbs:
            activity[name(db)].to_excel(writer,db)
        # Save
        writer.save()
        
    # Return to original directory
    os.chdir(origDir)
    
    # return capacity as a dictionary
    return activity

#==============================================================================
def SingleDB(folder,db,switch='fuel',sectorName='electric',saveData='N',createPlots='N',conversion=277.777778):
#    inputs:
#    1) folder          - path containing db
#    2) db              - name of databas
#    3) switch          - 'fuel' or 'tech', basis of categorization
#    4) sectorName      - name of temoa sector to be analyzed
#    5) saveData         - 'Y' or 'N', default is 'N' 
#    6) createPlot      - 'Y' or 'N', default is 'N' 
#    7) conversion      - conversion to GWh, default is 277.778 (from PJ)

#    outputs:
#    1) activity     - pandas DataFrame holding capacity for each model year
#==============================================================================
    
    if switch == 'fuel':
        savename = 'Results_yearlyActivity_byFuel_' + name(db)
    elif switch == 'tech':
        savename = 'Results_yearlyActivity_byTech_' + name(db)
       
    # save original folder
    origDir = os.getcwd()
    
    # move to folder
    os.chdir(folder)
        
    # Connect to Database
    con = sqlite3.connect(db)
    cur = con.cursor()
    
    # Read from database:
    #   Select All Efficiencies
    qry = "SELECT * FROM Efficiency"
    cur.execute(qry)
    db_efficiency = cur.fetchall()
    #   Select All time_periods
    qry = "SELECT * FROM time_periods"
    cur.execute(qry)
    db_t_periods = cur.fetchall()
    #   Select All technologies
    qry = "SELECT * FROM technologies"
    cur.execute(qry)
    db_technologies = cur.fetchall()
    #   Select All Flows
    qry = "SELECT * FROM Output_VFlow_Out"
    cur.execute(qry)
    db_Output_VFlow_Out = cur.fetchall()
    
    # Review db_t_periods to select future time periods
    future_t_periods = []
    for t_periods, flag in db_t_periods:    
        if flag == 'f':
            if t_periods not in future_t_periods:
                future_t_periods.append(t_periods)
            
    # Review db_technologies to select related sector
    techs = []
    for tech, flag, sector, tech_desc, tech_category in db_technologies:    
        if sector == sectorName:
            if tech not in techs:
                techs.append(tech)
    
    # Review db_efficiency to create a dictionary of fuels
    d = {}
    for input_comm, tech,vintage,output_comm,efficiency,ef_notes in db_efficiency:    
        if tech in techs:
            if tech not in d.keys():
                d[tech] = input_comm
    
    # Sort data and assign as columns and rows
    if switch == 'fuel':
        cols = sorted(set(d.values()))
    elif switch == 'tech':
        cols = sorted(techs)
    
    future_t_periods = sorted(future_t_periods)
    rows = future_t_periods[:-1] # Last period is not calculated
    
    # Create dataframe initialized to zero
    df = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    ## Review db_Output_VFlow_Out to fill data frame
    for scenario, sector, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm, vflow_out in db_Output_VFlow_Out:    
        if sector == sectorName:
            if switch == 'fuel':
                df.loc[t_periods,d[tech]] = df.loc[t_periods,d[tech]] + vflow_out*conversion
            elif switch == 'tech':
                df.loc[t_periods,tech] = df.loc[t_periods,tech] + vflow_out*conversion
            
    # Find empty columns and then drop from the dataframe
    empty = []
    for col in cols:
        if df[col].sum()==0.0:
            empty.append(str(col))
    df2 = df.drop(empty,axis=1)

    
    # Directory to hold results
    if saveData == 'Y' or createPlots == 'Y':
        resultsDir = origDir + "\\Results"
        try:
            os.stat(resultsDir)
        except:
            os.mkdir(resultsDir)
        os.chdir(resultsDir)
    
    # Plot Results
    if createPlots == 'Y':
        if switch == 'fuel':
            titlename = name(db) + ' by fuel'
        elif switch == 'tech':
            titlename = name(db) + ' by tech'
        ax = df2.plot.bar(stacked=True, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Activity [GWh]")
        fig = ax.get_figure()
        fig.savefig(savename + '.png',dpi=resolution)
    
    # Save as CSV (include all technologies in case comparing multiple scenarios)
    if saveData == 'Y' or saveData == 'y':
        df.to_csv(savename + '.csv')
        
    # return to original folder
    os.chdir(origDir)
        
    # return capacity as a DataFrame
    activity = df2
    return activity
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:15:42 2018

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
def getCapacity(folders,dbs,switch='fuel',group={},sectorName='electric',saveData='N',createPlots='N'):
#    inputs:
#    1) folders         - paths containing dbs (list or single string if all in the same path)
#    2) dbs             - names of databases (list)
#    3) switch          - 'fuel' or 'tech' or 'techgroup', basis of categorization
#    4) group           - custom dictionary used for techgroup
#    5) sectorName      - name of temoa sector to be analyzed
#    6) saveData         - 'Y' or 'N', default is 'N' 
#    7) createPlot      - 'Y' or 'N', default is 'N' 
#
#    outputs:
#    1) capacity     - pandas DataFrame holding capacity for each model year
#==============================================================================
    # Save original directory
    origDir = os.getcwd()

    # If only a single db and folder provided, change to a list
    if type(dbs) == str and type(folders) == str:
        dbs = [dbs]
        folders = [folders]
    # If a list of folders is provided with one database, only use first folder
    elif type(dbs) == str:
        dbs = [dbs]
        folders = [folders[0]]
    # If only a single folder provided, create a list of the same folder
    elif type(folders) == str:
        fldrs = []
        for db in dbs:
            fldrs.append(folders)
        folders = fldrs
    
    # Create dictionary to hold each capacity_single series
    capacity = {}
    
    # Iterate through each db
    for folder,db in zip(folders,dbs):
        capacity[name(db)] = SingleDB(folder,db,switch=switch,group=group,sectorName=sectorName)
    
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

        if n_subplots>1:
            f, a = plt.subplots(n_subplots, 1, sharex=True, sharey=True)
            a = a.ravel()
            # Create subplots
            for idx,ax in enumerate(a):
                db = dbs[idx]
                if switch == 'fuel':
                    titlename = name(db) + ' by fuel'
                elif switch == 'tech':
                    titlename = name(db) + ' by tech'
                elif switch == 'techgroup':
                    titlename = name(db) + ' by tech group'
                capacity[name(db)].plot.bar(ax=ax,stacked=True, title=titlename)
                ax.set_xlabel("Year [-]")
                ax.set_ylabel("Capacity [GW]")
        else:
            db = dbs[0]
            if switch == 'fuel':
                titlename = name(db) + ' by fuel'
            elif switch == 'tech':
                titlename = name(db) + ' by tech'
            elif switch == 'techgroup':
                titlename = name(db) + ' by tech group'
            ax = capacity[name(db)].plot.bar(stacked=True, title=titlename)
            ax.set_xlabel("Year [-]")
            ax.set_ylabel("Capacity [GW]")

        if switch == 'fuel':
            savename  = 'Results_yearlyCapacity_byFuel.png'
        elif switch == 'tech':
            savename  = 'Results_yearlyCapacity_byTech.png'
        elif switch == 'tech':
            savename  = 'Results_yearlyCapacity_byTechGroup.png'
        fig = ax.get_figure()
        fig.savefig(savename,dpi=resolution)
        
    # Save results to Excel
    if saveData == 'Y':
        # Create savename based on switch
        if switch == 'fuel':
            savename  = 'Results_yearlyCapacity_byFuel.xls'
        elif switch == 'tech':
            savename  = 'Results_yearlyCapacity_byTech.xls'
        elif switch == 'techgroup':
            savename  = 'Results_yearlyCapacity_byTechGroup.xls'
        # Create connection to excel
        writer = pd.ExcelWriter(savename)
        for db in dbs:
            capacity[name(db)].to_excel(writer,db)
        # Save
        writer.save()
        
    # Return to original directory
    os.chdir(origDir)
            
    # return capacity as a dictionary
    return capacity

#==============================================================================
def SingleDB(folder,db,switch='fuel',group={},sectorName='electric',saveData='N',createPlots='N'):
#    inputs:
#    1) folder          - path containing db
#    2) db              - name of databas
#    3) switch          - 'fuel' or 'tech' or 'techgroup, basis of categorization
#    4) group           - custom dictionary used for techgroup
#    5) sectorName      - name of temoa sector to be analyzed
#    6) saveData         - 'Y' or 'N', default is 'N' 
#    7) createPlot      - 'Y' or 'N', default is 'N' 
#
#    outputs:
#    1) capacity     - pandas DataFrame holding capacity for each model year
#==============================================================================
    if switch == 'fuel':
        savename = 'Results_yearlyCapacity_byFuel_' + name(db)
    elif switch == 'tech':
        savename = 'Results_yearlyCapacity_byTech_' + name(db)
    elif switch == 'techgroup':
        savename = 'Results_yearlyCapacity_byTechGroup_' + name(db)
        
    # save original folder
    origDir = os.getcwd()
    
    # move to folder
    os.chdir(folder)
    
    if debug ==True:
        print db
        
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
    #   Select All Capacities
    qry = "SELECT * FROM Output_CapacityByPeriodAndTech"
    cur.execute(qry)
    db_Output_CapacityByPeriodAndTech = cur.fetchall()
    
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
            # for switch=='fuel'
            if tech not in d.keys():
                d[tech] = input_comm
            # for switch=='techgroup'
            if tech not in group.keys():
                group[tech] = tech # if tech is not grouped, save original tech name
                                   
    # Sort data and assign as columns and rows
    if switch == 'fuel':
        cols = sorted(set(d.values()))
    elif switch == 'tech':
        cols = sorted(techs)
    elif switch=='techgroup':
        cols = sorted(set(group.values()))
    
    future_t_periods = sorted(future_t_periods)
    rows = future_t_periods[:-1]
    
    # Create dataframe initialized to zero
    df = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    ## Review db_Output_CapacityByPeriodAndTech to fill data frame
    for scenario, sector, t_periods, tech, capacity in db_Output_CapacityByPeriodAndTech:    
        if sector == sectorName:
            if switch == 'fuel':
                df.loc[t_periods,d[tech]] = df.loc[t_periods,d[tech]] + capacity
            elif switch == 'tech':
                df.loc[t_periods,tech] = df.loc[t_periods,tech] + capacity
            elif switch == 'techgroup':
                df.loc[t_periods,group[tech]] = df.loc[t_periods,group[tech]] + capacity
            
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
        elif switch == 'techgroup':
            titlename = name(db) + ' by tech group'
        ax = df2.plot.bar(stacked=True, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Capacity [GW]")
        fig = ax.get_figure()
        fig.savefig(savename + '.png',dpi=resolution)
    
    # Save as CSV (include all technologies in case comparing multiple scenarios)
    if saveData == 'Y' or saveData == 'y':
        df.to_csv(savename+ '.csv')
        
    # return to original folder
    os.chdir(origDir)
    
    # return capacity as a DataFrame
    capacity = df2
    return capacity
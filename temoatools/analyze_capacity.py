from __future__ import print_function
import os
import sqlite3
import pandas as pd
from help_functions import create_results_dir

debug = False
resolution = 1000 #DPI

#==============================================================================
# Remove filetype from filename
def name(db):
    return db[:db.find('.')]
#==============================================================================
def getCapacity(folders,dbs,switch='fuel',group={},sector_name='electric',save_data='N',create_plots='N', run_name=''):
#    inputs:
#    1) folders         - paths containing dbs (list or single string if all in the same path)
#    2) dbs             - names of databases (list)
#    3) switch          - 'fuel' or 'tech' or 'techgroup', basis of categorization
#    4) group           - custom dictionary used for techgroup
#    5) sectorName      - name of temoa sector to be analyzed
#    6) saveData         - 'Y' or 'N', default is 'N' 
#    7) createPlot      - 'Y' or 'N', default is 'N'
#    8) run_name         - Used for saving results in dedicated folder
#
#    outputs:
#    1) capacity     - pandas DataFrame holding capacity for each model year
#==============================================================================
    # Save original directory
    wrkdir = os.getcwd()

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
    capacity = pd.DataFrame()
    
    # Iterate through each db
    for folder,db in zip(folders,dbs):
        capacity_single = SingleDB(folder,db,switch=switch,group=group,sector_name=sector_name)
        capacity = pd.concat([capacity,capacity_single])
    
    # Directory to hold results
    if save_data == 'Y' or create_plots == 'Y':
        create_results_dir(wrkdir=wrkdir, run_name=run_name)

    # Save results to Excel
    if save_data == 'Y':
        # Create savename based on switch
        if switch == 'fuel':
            savename = 'Results_yearlyCapacity_byFuel.xls'
        elif switch == 'tech':
            savename = 'Results_yearlyCapacity_byTech.xls'
        elif switch == 'techgroup':
            savename = 'Results_yearlyCapacity_byTechGroup.xls'
        # Save
        capacity.to_csv(savename)

    # Create plots
    if create_plots == 'Y':
        if switch == 'fuel':
            titlename = 'By fuel'
            savename = 'Results_yearlyCapacity_byFuel.png'
        elif switch == 'tech':
            titlename = 'By tech'
            savename = 'Results_yearlyCapacity_byTech.png'
        elif switch == 'techgroup':
            titlename = 'By tech group'
            savename = 'Results_yearlyCapacity_byTechGroup.png'
        # Plot
        ax = capacity.plot.bar(stacked=True, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Activity [GWh]")
        # Save
        fig = ax.get_figure()
        fig.savefig(savename,dpi=resolution)

    # Return to original directory
    os.chdir(wrkdir)
            
    # return capacity as a dictionary
    return capacity

#==============================================================================
def SingleDB(folder,db,switch='fuel',group={},sector_name='electric'):
#    inputs:
#    1) folder          - path containing db
#    2) db              - name of databas
#    3) switch          - 'fuel' or 'tech' or 'techgroup, basis of categorization
#    4) group           - custom dictionary used for techgroup
#    5) sectorName      - name of temoa sector to be analyzed
#
#    outputs:
#    1) capacity     - pandas DataFrame holding capacity for each model year
#==============================================================================
    print("Analyzing db: ", db)

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
        if sector == sector_name:
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
    
    # Review db_Output_CapacityByPeriodAndTech to fill data frame
    for scenario, sector, t_periods, tech, capacity in db_Output_CapacityByPeriodAndTech:    
        if sector == sector_name or sector_name == "all":
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

    # return to original folder
    os.chdir(origDir)
    
    # return capacity as a DataFrame
    capacity = df2
    return capacity
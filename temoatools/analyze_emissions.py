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
def getEmissions(folders, dbs, conversion=1E-6, saveData='N', createPlots='N'):
#==============================================================================      
#    inputs:
#    1) folders         - paths containing dbs (list or single string if all in the same path)
#    2) dbs             - names of databases (list)
#    3) conversion      - converts from emission units to Mton
#           default is conversion from kton to Mton is 1E-6
#    4) saveData         - 'Y' or 'N', default is 'N' 
#    5) createPlots     - 'Y' or 'N', default is 'N' 
#
#    outputs:
#    1) yearlyEmissions     - pandas DataFrame holding yearly emissions
#    2) avgEmissions        - dictionary holding average emissions
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

    # Create a dataframe
    yearlyEmissions = pd.DataFrame()
    avgEmissions = {}
        
    # Iterate through each db
    for folder,db in zip(folders,dbs):
    
        # Move to folder
        os.chdir(folder)
        
        # Access costs
        yearlyEmissions_single, avgEmissions_single = SingleDB(folder, db, conversion=conversion)
    
        # Store costs
        yearlyEmissions[name(db)] = yearlyEmissions_single
        avgEmissions[name(db)] = avgEmissions_single
        
    # Sort data
    yearlyEmissions = yearlyEmissions.sort_index()
    
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
        # yearlyEmissions
        titlename = 'Yearly Emissions'
        ax = yearlyEmissions.plot(stacked=False, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Emissions [Mton]")
        fig = ax.get_figure()
        fig.savefig('Results_yearlyEmissions.png',dpi=resolution)
        
        # avgEmissions
        titlename = 'Average Emissions'
        df_avgEmissions = pd.DataFrame.from_dict(avgEmissions,orient='index')
        ax = df_avgEmissions.plot.bar(stacked=False, title=titlename)
        ax.set_xlabel("Scenario [-]")
        ax.set_ylabel("Average Emissions [Mton]")
        fig = ax.get_figure()
        fig.savefig('Results_totalEmissions.png',dpi=resolution)
        
    # Save results to Excel
    if saveData == 'Y':
        savename  = 'Results_Emissions.xls'
        # Create connection to excel
        writer = pd.ExcelWriter(savename)
        # Write data
        yearlyEmissions.to_excel(writer,'yearlyEmisssions')
        df_avgEmissions.to_excel(writer,'avgEmissions')
        # Save
        writer.save()
        
    # Return to original directory
    os.chdir(origDir)
        
    return yearlyEmissions, avgEmissions
    
#==============================================================================
def SingleDB(folder,db,conversion=1E-6,saveData='N', createPlots='N'):
#    inputs:
#    1) folder          - path containing db
#    2) db              - name of databas
#    3) conversion      - converts from emission units to Mton
#           default is conversion from kton to Mton is 1E-6
#    4) saveData         - 'Y' or 'N', default is 'N' 
#
#    outputs:
#    1) yearlyEmissions     - pandas DataFrame holding yearly emissions
#    2) avgEmissions        - dictionary holding average emissions
#==============================================================================      
    if debug==True:
        print db
    
    # Save original directory
    origDir = os.getcwd()
    
    # Create pandas Series to hold yearlyEmission
    yearlyEmissions = pd.Series()

    # Move to folder
    os.chdir(folder)

    # Connect to Database
    con = sqlite3.connect(db)
    cur = con.cursor()
    
    #   Select All time_periods
    qry = "SELECT * FROM time_periods"
    cur.execute(qry)
    db_t_periods = cur.fetchall()
    
    # Review db_t_periods to select future time periods
    future_t_periods = []
    for t_periods, flag in db_t_periods:    
        if flag == 'f':
            if t_periods not in future_t_periods:
                future_t_periods.append(t_periods)
                
    n_years = len(future_t_periods)
    future_t_periods = sorted(future_t_periods)
    future_t_periods = future_t_periods[:-1] # no calculations are performed for the last time_period
    for period in future_t_periods:
        yearlyEmissions[str(period)] = 0.0
           
    # Read from database:
    qry = "SELECT * FROM Output_Emissions"
    cur.execute(qry)
    db_Output_Emissions = cur.fetchall()
    
    ## Review db_Output_CapacityByPeriodAndTech to fill data frame
    for scenario,sector,t_period,emissions_comm,tech,vintage,emissions in db_Output_Emissions:    
        yearlyEmissions[str(t_period)] = yearlyEmissions[str(t_period)] + emissions            
        if debug == True:
            print 't_period:  ' + str(t_period)
            print 'emissions: ' + str(emissions)
            print yearlyEmissions
            
    # Close connection
    con.close()
    
    # Sort data
#    yearlyEmissions = yearlyEmissions.sort_index()
    
    # Sum average emissions
    avgEmissions = yearlyEmissions.sum()/n_years
        
    # Directory to hold results
    if saveData == 'Y' or createPlots == 'Y':
        resultsDir = origDir + "\\Results"
        try:
            os.stat(resultsDir)
        except:
            os.mkdir(resultsDir)
        os.chdir(resultsDir)
    
    #------------
    # Save Results to CSV
    #------------
    if saveData == 'Y':
        savename = 'Results_Emissions_' + name(db) + '.csv'
        series = yearlyEmissions.copy()
        
        series['avgEmissions'] = avgEmissions
        series.to_csv(savename)
    
    #------------
    # Create Plot
    #------------
    if createPlots == 'Y':
        savename = 'Results_yearlyEmissions_' + name(db) + '.png'
        
        titlename = 'Yearly Emissions: ' + name(db)
        df = pd.DataFrame(yearlyEmissions)
        ax = df.plot(stacked=False, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Emissions [Mton]")
        fig = ax.get_figure()
        fig.savefig(savename,dpi=resolution)
    
    # Return to original directory
    os.chdir(origDir)
    
    return yearlyEmissions, avgEmissions
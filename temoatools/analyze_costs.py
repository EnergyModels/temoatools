# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 12:15:47 2018

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
def getCosts(folders, dbs, elc_dmd='ELC_DMD', conversion=0.359971, saveData='N', createPlots ='N'):
#    inputs:
#    1) folders         - paths containing dbs (list or single string if all in the same path)
#    2) dbs             - names of databases (list)
#    3) elc_dmd         - quantity that represents electricity demand
#    4) conversion      - converts from cost units per activity to cents/kWH
#           default is conversion from M$/PJ to cents/KWh (1E6*100 / (2.778E8))
#    5) saveData         - 'Y' or 'N', default is 'N' 
#    6) createPlots     - 'Y' or 'N', default is 'N' 
#
#    outputs:
#    1) yearlyCosts     - pandas DataFrame holding yearly_costs
#    2) LCOE            - dictionary holding LCOE, calculated wrt first model year
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
    yearlyCosts = pd.DataFrame()
    LCOE = {}
        
    # Iterate through each db
    for folder,db in zip(folders,dbs):
        
        # Access costs
        yearlyCosts_single, LCOE_single = SingleDB(folder, db, elc_dmd=elc_dmd, conversion=conversion)
    
        # Store costs
        yearlyCosts[name(db)] = yearlyCosts_single
        LCOE[name(db)] = LCOE_single
        
    # Directory to hold results
    if saveData == 'Y' or createPlots == 'Y':
        resultsDir = origDir + "\\results"
        try:
            os.stat(resultsDir)
        except:
            os.mkdir(resultsDir)
        os.chdir(resultsDir)
        
    # Plot Results
    if createPlots == 'Y':
        # yearlyCosts
        titlename = 'Yearly Costs'
        ax = yearlyCosts.plot(stacked=False, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Costs [cents/kWh]")
        fig = ax.get_figure()
        fig.savefig('Results_yearlyCosts.png',dpi=resolution)
        
        # LCOE
        titlename = 'LCOE'
        df_LCOE = pd.DataFrame.from_dict(LCOE,orient='index')
        ax = df_LCOE.plot.bar(stacked=False, title=titlename)
        ax.set_xlabel("Scenario [-]")
        ax.set_ylabel("Levelized Cost of Electricity [cents/kWh]")
        fig = ax.get_figure()
        fig.savefig('Results_LCOE.png',dpi=resolution)
        
        
    # Save results to Excel
    if saveData == 'Y':
        savename  = 'Results_Costs.xls'
        # Create connection to excel
        writer = pd.ExcelWriter(savename)
        # Write data
        yearlyCosts.to_excel(writer,'yearlyCosts')
        df_LCOE.to_excel(writer,'LCOE')
        # Save
        writer.save()
        
    # Return to original directory
    os.chdir(origDir)
        
    return yearlyCosts, LCOE

#==============================================================================
def SingleDB(folder, db, elc_dmd='ELC_DMD', conversion=0.359971, saveCSV='N', createPlots='N'):
#    inputs:
#    1) folder          - path containing db
#    2) db              - names of databases
#    3) elc_dmd         - quantity that represents electricity demand
#    4) conversion      - converts from cost units per activity to cents/kWH
#    5) saveCSV - 'Y' or 'N' to save results to csv
#
#    outputs:
#    1) yearlyCosts     - pandas Series holding yearly costs
#    2) LCOE            - LCOE (float), calculated wrt first model year
#==============================================================================
    # Save original directory
    origDir = os.getcwd()
    
    # Move to folder
    os.chdir(folder)
    
    # Connect to Database
    con = sqlite3.connect(db)
    cur = con.cursor()
        
    # Review time_periods, only interested in future periods
    qry = "SELECT * FROM time_periods"
    cur.execute(qry)
    db_t_periods = cur.fetchall()
    
    t_periods =[]
    for t_period, flag in db_t_periods:  
        if flag == 'f':
            t_periods.append(t_period)
    
    t_periods = sorted(t_periods)
    t_periods = t_periods[:-1]
    
    # Review technologies  
    qry = "SELECT * FROM technologies"
    cur.execute(qry)
    db_tech = cur.fetchall()
    
    techs =[]
    for tech, flag, sector, tech_desc, tech_category in db_tech:  
        techs.append(tech)
        
    # Create dataframe to hold yearly costs (initialized to zero)
    rows = t_periods
    cols = ['CostInvest','CostFixed','CostVariable','CostTotal','ELC_DMD','ELC_Cost']
    df = pd.DataFrame(data=0.0,index=rows,columns = cols)
        
    #------------
    # CostInvest
    #------------
    # Access database
    qry = "SELECT * FROM CostInvest"
    cur.execute(qry)
    db_CostInvest = cur.fetchall()  
    
    # Create dataframe to hold technology costs (initialized to zero)
    rows = t_periods
    cols = techs
    df_CostInvest = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for tech, vintage, cost_invest, cost_invest_units, cost_invest_notes in db_CostInvest:
        if vintage in t_periods and tech in techs:
            df_CostInvest.loc[vintage,tech] = cost_invest
    
    #------------
    # CostFixed
    #------------
    # Access database
    qry = "SELECT * FROM CostFixed"
    cur.execute(qry)
    db_CostFixed = cur.fetchall()  
    
    # Create dataframe to hold technology costs (initialized to zero)
    rows = t_periods
    cols = techs
    df_CostFixed = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for periods, tech, vintage, cost_fixed, cost_fixed_units, cost_fixed_notes in db_CostFixed:
        if periods in t_periods and tech in techs:
            df_CostFixed.loc[periods,tech] = cost_fixed   
    
    #------------
    # CostVariable
    #------------
    # Access database
    qry = "SELECT * FROM CostVariable"
    cur.execute(qry)
    db_CostVariable = cur.fetchall()  
    
    # Create dataframe to hold technology costs (initialized to zero)
    rows = t_periods
    cols = techs
    df_CostVariable = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for periods, tech, vintage, cost_variable, cost_variable_units, cost_variable_notes in db_CostVariable:
        if periods in t_periods and tech in techs:
            df_CostVariable.loc[periods,tech] = cost_variable  
    
    #------------
    # Activity
    #------------
    # Access database
    qry = "SELECT * FROM Output_VFlow_Out"
    cur.execute(qry)
    db_activity = cur.fetchall()  
    
    # Create dataframe to hold activity (initialized to zero)
    rows = t_periods
    cols = techs
    df_activity = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for scenario, sector, t_period, t_season, t_day, input_comm, tech, vintage, output_comm, vflow_out in db_activity:
        # Store Activity for each technology
        if t_period in t_periods and tech in techs:
            df_activity.loc[t_period,tech] = df_activity.loc[t_period,tech] + vflow_out
        # Store electricity demand
        if output_comm == elc_dmd:
            df.loc[t_period,'ELC_DMD'] = df.loc[t_period,'ELC_DMD'] + vflow_out
            
    #------------
    # New Capacity
    #------------
    # Access database
    qry = "SELECT * FROM Output_V_Capacity"
    cur.execute(qry)
    db_newCapacity = cur.fetchall()  
    
    # Create dataframe to hold yearly installs (initialized to zero)
    rows = t_periods
    cols = techs
    df_newCapacity = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for scenario, sector, tech, vintage, capacity, in db_newCapacity:
        if vintage in t_periods and tech in techs:
            df_newCapacity.loc[vintage,tech] = capacity  
            
            
    #------------
    # Active Capacity
    #------------
    # Access database
    qry = "SELECT * FROM Output_CapacityByPeriodAndTech"
    cur.execute(qry)
    db_activeCapacity = cur.fetchall()  
    
    # Create dataframe to hold yearly installs (initialized to zero)
    rows = t_periods
    cols = techs
    df_activeCapacity = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for scenario, sector, t_period, tech, capacity, in db_activeCapacity:
        if t_period in t_periods and tech in techs:
            df_activeCapacity.loc[t_period,tech] = capacity  
    
    #------------
    # Discount Rate
    #------------
    qry = "SELECT * FROM GlobalDiscountRate"
    cur.execute(qry)
    db_rate = cur.fetchall()  
    rate = db_rate[0][0]
    
    #------------
    # LifetimeLoanTech
    #------------
    # Access database
    qry = "SELECT * FROM LifetimeLoanTech"
    cur.execute(qry)
    db_loanLife = cur.fetchall()  
    
    # Create dataframe to hold yearly installs (initialized to zero)
    rows = techs
    cols = ["loan"]
    df_loanLife = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    # Store Data
    for tech, loan, loan_notes, in db_loanLife:
        df_loanLife.loc[tech,"loan"] = loan 
    
    
    #------------
    # Investments
    #------------
    # Create dataframe (initialized to zero)
    rows = t_periods
    cols = techs
    df_investments = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    for year in t_periods:
        for tech in techs:
            costInvest = df_newCapacity.loc[year,tech] * df_CostInvest.loc[year,tech]
            df_investments.loc[year,tech] = df_investments.loc[year,tech] + costInvest
    
    #------------
    # Translate Investments to Loans
    #------------
    # Create dataframe (initialized to zero)
    rows = t_periods
    cols = techs
    df_loanPayments = pd.DataFrame(data=0.0,index=rows,columns = cols)
    
    for tech in techs:
        for buildYear in t_periods:
            
            if df_investments.loc[buildYear,tech] > 0:
                loan = df_investments.loc[buildYear,tech]
                N = df_loanLife.loc[tech,"loan"]
                # Assume Fixed-Rate Payment (https://www.investopedia.com/terms/f/fixed-rate-payment.asp)
                annualPayment = rate/ (1-(1+rate)**-N)*loan
                if debug == True:
                    print "Tech: " + tech + ",Year: " + str(buildYear) + ",YearlyPayment: " +str(annualPayment)
                
                for year in t_periods:
                    if buildYear<=year and year<=buildYear+N:
                        df_loanPayments.loc[year,tech] = df_loanPayments.loc[year,tech] + annualPayment
            
    #------------
    # Translate to yearly costs
    #------------
    for year in t_periods:
        for tech in techs:
            
            # CostInvest (loan payments)
            costInvest = df_loanPayments.loc[year,tech]
            df.loc[year,'CostInvest'] = df.loc[year,'CostInvest'] + costInvest
            
            # CostFixed
            costFixed = df_activeCapacity.loc[year,tech] * df_CostFixed.loc[year,tech]
            df.loc[year,'CostFixed'] = df.loc[year,'CostFixed'] + costFixed
     
            # CostVariable
            costVariable = df_activity.loc[year,tech] * df_CostVariable.loc[year,tech]
            df.loc[year,'CostVariable'] = df.loc[year,'CostVariable'] + costVariable
            
            # Sum Costs
            totalTechCost = costInvest + costFixed + costVariable
            df.loc[year,'CostTotal'] = df.loc[year,'CostTotal'] + totalTechCost
            
        # Calculate Yearly Cost of Electricity
        df.loc[year,'ELC_Cost'] =df.loc[year,'CostTotal'] / df.loc[year,'ELC_DMD'] * conversion
        
    yearlyCosts = df.ELC_Cost
    
    #------------
    # Calculate LCOE (based on initial year)
    # based on: https://www.energy.gov/sites/prod/files/2015/08/f25/LCOE.pdf
    #------------
    num = 0.0
    denom = 0.0
    
    for year in t_periods:
        t = year - t_periods[0]
        num = num + df.loc[year,'CostTotal'] / (1.0 + rate)**t
        denom = denom + df.loc[year,'ELC_DMD'] / (1.0 + rate)**t
    
    LCOE = num/denom * conversion
    
    df.loc[t_periods[0],'LCOE'] = LCOE
       
    # Directory to hold results
    if saveCSV == 'Y' or createPlots == 'Y':
        resultsDir = origDir + "\\results"
        try:
            os.stat(resultsDir)
        except:
            os.mkdir(resultsDir)
        os.chdir(resultsDir)
    
    #------------
    # Save Results to CSV
    #------------
    if saveCSV == 'Y':
        savename = 'Results_Costs_' + name(db) + '.csv'
        df.to_csv(savename,columns=['ELC_Cost','LCOE'])
    
    #------------
    # Create Plot
    #------------
    if createPlots == 'Y':
        savename = 'Results_yearlyCosts_' + name(db) + '.png'
        
        titlename = 'Yearly Costs: ' + name(db)
        ax = yearlyCosts.plot(stacked=False, title=titlename)
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Costs [cents/kWh]")
        fig = ax.get_figure()
        fig.savefig(savename,dpi=resolution)
    
    # Return to original directory
    os.chdir(origDir)
    
    #------------
    # Return Calculations
    #------------
    return yearlyCosts, LCOE
import os
import sqlite3
import pandas as pd
import temoatools as tt

debug = False
resolution = 600  # DPI


# ==============================================================================
def getEmissions(folders, dbs, conversion=1E-6, save_data='N', create_plots='N', run_name=''):
    # ==============================================================================
    #    inputs:
    #    1) folders         - paths containing dbs (list or single string if all in the same path)
    #    2) dbs             - names of databases (list)
    #    3) conversion      - converts from emission units to Mton
    #           default is conversion from kton to Mton is 1E-6
    #    4) save_data        - 'Y' or 'N', default is 'N'
    #    5) create_plots     - 'Y' or 'N', default is 'N'
    #    6) run_name         - Used for saving results in dedicated folder
    #
    #    outputs:
    #    1) yearlyEmissions     - pandas DataFrame holding yearly emissions
    #    2) avgEmissions        - dictionary holding average emissions
    # ==============================================================================
    print("Analyzing emissions")

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

    # Create a dataframe
    yearlyEmissions = pd.DataFrame(dtype='float64')
    avgEmissions = pd.DataFrame(dtype='float64')

    # Iterate through each db
    for folder, db in zip(folders, dbs):
        # Move to folder
        os.chdir(folder)

        # Access costs
        yearlyEmissions_single, avgEmissions_single = SingleDB(folder, db, conversion=conversion)

        # Store costs
        yearlyEmissions = pd.concat([yearlyEmissions, yearlyEmissions_single])
        avgEmissions = pd.concat([avgEmissions, avgEmissions_single])

    # Sort data
    # yearlyEmissions = yearlyEmissions.sort_index()

    # Reset index (remove multi-level indexing, easier to use for processing)
    yearlyEmissions = yearlyEmissions.reset_index()
    avgEmissions = avgEmissions.reset_index()

    # Directory to hold results
    if save_data == 'Y' or create_plots == 'Y':
        tt.create_results_dir(wrkdir=wrkdir, run_name=run_name)

    # Save results to CSV
    if save_data == 'Y':
        yearlyEmissions.to_csv('emissions_yearly.csv')
        avgEmissions.to_csv('emissions_average.csv')

    # Plot Results
    if create_plots == 'Y':
        import matplotlib.pyplot as plt
        import seaborn as sns

        # new figure
        plt.figure()
        # set aesthetics
        sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
        sns.set_context("paper")
        sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

        # wide to long
        df2 = pd.melt(yearlyEmissions, id_vars=['database', 'scenario'], var_name='var', value_name='value')
        # plot
        ax = sns.lineplot(x='var', y='value', hue='database', data=df2)

        # yearlyEmissions
        ax.set_xlabel("Year [-]")
        ax.set_ylabel("Emissions [kton]")
        fig = ax.get_figure()
        savename = 'emissions_yearly.png'
        fig.savefig(savename, dpi=resolution)

        # close figure
        plt.close()

    # Return to original directory
    os.chdir(wrkdir)

    return yearlyEmissions, avgEmissions


# ==============================================================================
def SingleDB(folder, db, conversion=1E-6):
    #    inputs:
    #    1) folder          - path containing db
    #    2) db              - name of database
    #    3) conversion      - converts from emission units to Mton
    #           default is conversion from kton to Mton is 1E-6
    #
    #    outputs:
    #    1) yearlyEmissions     - pandas DataFrame holding yearly emissions
    #    2) avgEmissions        - dictionary holding average emissions
    # ==============================================================================
    print("\tAnalyzing db: ", db)

    # Save original directory
    origDir = os.getcwd()

    # Move to folder
    os.chdir(folder)

    # Connect to Database
    con = sqlite3.connect(db)
    cur = con.cursor()

    #   Identify Unique Scenarios
    qry = "SELECT * FROM Output_Objective"
    cur.execute(qry)
    db_objective = cur.fetchall()
    scenarios = []
    for scenario, objective_name, total_system_cost in db_objective:
        if scenario not in scenarios:
            scenarios.append(scenario)

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

    future_t_periods = sorted(future_t_periods)
    future_t_periods = future_t_periods[:-1]  # no calculations are performed for the last time_period

    # Read from database:
    qry = "SELECT * FROM Output_Emissions"
    cur.execute(qry)
    db_Output_Emissions = cur.fetchall()

    # Close connection
    con.close()

    # Create pandas DataFrame to hold yearlyEmissions
    index = pd.MultiIndex.from_product([[db], scenarios], names=['database', 'scenario'])
    yearlyEmissions = pd.DataFrame(index=index, columns=future_t_periods, dtype='float64')
    yearlyEmissions = yearlyEmissions.fillna(0.0)  # Default value to zero
    avgEmissions = pd.DataFrame(index=index, columns=['avgEmissions'], dtype='float64')
    avgEmissions = avgEmissions.fillna(0.0)  # Default value to zero

    # Iterate through scenarios
    for s in scenarios:
        print("\t\tAnalyzing Scenario: ", s)
        # Review db_Output_Emissions to fill data frame
        for scenario, sector, t_period, emissions_comm, tech, vintage, emissions in db_Output_Emissions:
            if scenario == s:
                yearlyEmissions.loc[(db, s), t_period] = yearlyEmissions.loc[(db, s), t_period] + emissions
                if debug == True:
                    print('scenario:  ' + scenario)
                    print('t_period:  ' + str(t_period))
                    print('emissions: ' + str(emissions))
                    print(yearlyEmissions)

        # Sum average emissions
        avgEmissions.loc[(db, s),] = yearlyEmissions.loc[(db, s),].mean()

    # Return to original directory
    os.chdir(origDir)

    return yearlyEmissions, avgEmissions

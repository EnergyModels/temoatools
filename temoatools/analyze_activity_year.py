import os
import sqlite3
import pandas as pd
import temoatools as tt

debug = False
resolution = 600  # DPI


# ==============================================================================
def getActivity(folders, dbs, switch='fuel', sector_name='electric', save_data='N', create_plots='N',
                conversion=277.777778, run_name=''):
    #    inputs:
    #    1) folders         - paths containing dbs (list or single string if all in the same path)
    #    2) dbs             - names of databases (list)
    #    3) switch          - 'fuel' or 'tech', basis of categorization
    #    4) sectorName      - name of temoa sector to be analyzed
    #    5) save_data         - 'Y' or 'N', default is 'N'
    #    6) create_plots      - 'Y' or 'N', default is 'N'
    #    7) conversion      - conversion to GWh, default is 277.778 (from PJ).
    #    8) run_name         - Used for saving results in dedicated folder

    #    outputs:
    #    1) activity     - pandas DataFrame holding capacity for each model year
    # ==============================================================================
    print("Analyzing activity by year")

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
    activity = pd.DataFrame(dtype='float64')

    # Iterate through each db
    for folder, db in zip(folders, dbs):
        activity_single = SingleDB(folder, db, switch=switch, sector_name=sector_name, conversion=conversion)
        activity = pd.concat([activity, activity_single])

    # Reset index (remove multi-level indexing, easier to use in Excel)
    activity = activity.reset_index()

    # Directory to hold results
    if save_data == 'Y' or create_plots == 'Y':
        tt.create_results_dir(wrkdir=wrkdir, run_name=run_name)

    # Save results to CSV
    if save_data == 'Y':
        # Create savename based on switch
        if switch == 'fuel':
            savename = 'activity_by_fuel.csv'
        else:
            savename = 'activity_by_tech.csv'
        activity.to_csv(savename)

    if create_plots == 'Y':
        import matplotlib.pyplot as plt
        import seaborn as sns

        # new figure
        plt.figure()
        # set aesthetics
        sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
        sns.set_context("talk")
        # sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

        # wide to long
        df2 = pd.melt(activity, id_vars=['database', 'scenario', 'fuelOrTech'], var_name='var', value_name='value')
        # plot
        sns.relplot(x='var', y='value', hue='database', data=df2, kind='line', col='fuelOrTech', col_wrap=4)

        # save
        if switch == 'fuel':
            savename = 'yearlyActivity_byFuel.png'
        else:
            savename = 'yearlyActivity_byTech.png'
        plt.savefig(savename, dpi=resolution)

        # close figure
        plt.close()

    # Return to original directory
    os.chdir(wrkdir)

    # return capacity as a dictionary
    return activity


# ==============================================================================
def SingleDB(folder, db, switch='fuel', sector_name='electric', conversion=277.777778):
    #    inputs:
    #    1) folder          - path containing db
    #    2) db              - name of databas
    #    3) switch          - 'fuel' or 'tech', basis of categorization
    #    4) sectorName      - name of temoa sector to be analyzed
    #    5) conversion      - conversion to GWh, default is 277.778 (from PJ)
    #    outputs:
    #    1) activity     - pandas DataFrame holding capacity for each model year
    # ==============================================================================
    print("\tAnalyzing db: ", db)

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
        if sector == sector_name or sector_name == "all":
            if tech not in techs:
                techs.append(tech)

    # Review db_efficiency to create a dictionary of fuels
    d = {}
    for input_comm, tech, vintage, output_comm, efficiency, ef_notes in db_efficiency:
        if tech in techs:
            if tech not in d.keys():
                d[tech] = input_comm

    # Sort data and assign as columns and rows
    if switch == 'fuel':
        cols = sorted(set(d.values()))
    elif switch == 'tech':
        cols = sorted(techs)

    future_t_periods = sorted(future_t_periods)
    rows = future_t_periods[:-1]  # Last period is not calculated

    #   Identify Unique Scenarios
    qry = "SELECT * FROM Output_Objective"
    cur.execute(qry)
    db_objective = cur.fetchall()
    scenarios = []
    for scenario, objective_name, total_system_cost in db_objective:
        if scenario not in scenarios:
            scenarios.append(scenario)

    # Create pandas DataFrame to hold yearlyEmissions for all scenarios
    index = pd.MultiIndex.from_product([[db], scenarios, cols], names=['database', 'scenario', 'fuelOrTech'])
    df = pd.DataFrame(index=index, columns=future_t_periods[:-1], dtype='float64')
    df = df.fillna(0.0)  # Default value to zero

    ## Review db_Output_VFlow_Out to fill data frame
    for scenario, sector, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm, vflow_out in db_Output_VFlow_Out:
        if sector == sector_name or sector_name == "all":
            if switch == 'fuel':
                df.loc[(db, scenario, d[tech]), t_periods] = df.loc[(db, scenario,
                                                                     d[tech]), t_periods] + vflow_out * conversion
            elif switch == 'tech':
                df.loc[(db, scenario, tech), t_periods] = df.loc[
                                                              (db, scenario, tech), t_periods] + vflow_out * conversion

    # return to original folder
    os.chdir(origDir)

    # return as a DataFrame
    # activity = df2
    return df

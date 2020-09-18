# TODO - keep this?
import os
import sqlite3
import pandas as pd
import temoatools as tt

debug = False
resolution = 600  # DPI


# ==============================================================================
# Remove filetype from filename
def name(db):
    return db[:db.find('.')]


# ==============================================================================
def getActivityTOD(folders, dbs, switch='fuel', sectorName='electric', saveData='N', createPlots='N',
                   conversion=277.777778):
    #    inputs:
    #    1) folders         - paths containing dbs (list or single string if all in the same path)
    #    2) dbs             - names of databases (list)
    #    3) switch          - 'fuel' or 'tech', basis of categorization
    #    4) sectorName      - name of temoa sector to be analyzed
    #    5) saveData         - 'Y' or 'N', default is 'N'
    #    6) createPlots     - 'Y' or 'N', default is 'N'
    #    7) conversion      - conversion to GWh, default is 277.778 (from PJ)

    #    outputs:
    #    1) activity
    #    2) plots - optional
    #    3) Data  - optional
    # ==============================================================================
    print("Analyzing activity by time of day (TOD)")

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

    # Dictionary to store results
    activity = {}

    # Iterate through each db
    for folder, db in zip(folders, dbs):
        activity[name(db)] = SingleDB(folder, db, switch=switch, sectorName=sectorName, saveData=saveData,
                                      createPlots=createPlots, conversion=conversion)

    # if saveData == 'Y':
        # do something
    if createPlots == 'Y':

        import matplotlib.pyplot as plt
        import seaborn as sns

        # new figure
        plt.figure()

        # set aesthetics
        sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
        sns.set_context("talk")
        # sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})


        # create plot

        fig = ax.get_figure()
        fig.savefig('costs_yearly.png', dpi=resolution)

        # close figure
        plt.close()

    return activity


# ==============================================================================
def SingleDB(folder, db, switch='fuel', sectorName='electric', saveData='N', createPlots='N', conversion=277.777778):
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
    # ==============================================================================

    if switch == 'fuel':
        savename = 'Results_ActivityTOD_byFuel_' + name(db)
    elif switch == 'tech':
        savename = 'Results_ActivityTOD_byTech_' + name(db)

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
    #   Select All time_of_day
    qry = "SELECT * FROM time_of_day"
    cur.execute(qry)
    db_time_of_day = cur.fetchall()
    #   Select All time_season
    qry = "SELECT * FROM time_season"
    cur.execute(qry)
    db_time_season = cur.fetchall()
    #   Select All time_periods
    qry = "SELECT * FROM time_periods"
    cur.execute(qry)
    db_time_periods = cur.fetchall()
    #   Select All technologies
    qry = "SELECT * FROM technologies"
    cur.execute(qry)
    db_technologies = cur.fetchall()
    #   Select All Flows
    qry = "SELECT * FROM Output_VFlow_Out"
    cur.execute(qry)
    db_Output_VFlow_Out = cur.fetchall()

    # Review db_time_of_day to select timesOfDay
    tods = []
    for tod in db_time_of_day:
        tods.append(str(tod[0]))

    # Review db_time_season to select seasons
    seasons = []
    for season in db_time_season:
        seasons.append(str(season[0]))
    n_seasons = len(seasons)

    # Review db_time_periods to select future periods
    years = []
    for year, flag in db_time_periods:
        if flag == 'f':
            years.append(str(year))
    n_years = len(years)

    # Review db_technologies to select related sector
    techs = []
    for tech, flag, sector, tech_desc, tech_category in db_technologies:
        if sector == sectorName:
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
    rows = sorted(tods)

    # Directory to hold results
    if save_data == 'Y' or create_plots == 'Y':
        tt.create_results_dir(wrkdir=wrkdir, run_name=run_name)

    # Create plot
    if createPlots == 'Y':
        f, a = plt.subplots(n_years, n_seasons, sharex=True, sharey=True)

    # Create connection to excel
    if saveData == 'Y':
        writer = pd.ExcelWriter(savename + '.xls')

    # Dictionary to store results
    activity = {}

    # Fill-in each subplot
    for i, year in enumerate(years[:-1]):
        for j, season in enumerate(seasons):

            # Create appropriate title
            titlename = str(year) + ' ' + str(season)

            # Create dataframe initialized to zero
            df = pd.DataFrame(data=0.0, index=rows, columns=cols)

            ## Review db_Output_VFlow_Out to fill data frame
            for scenario, sector, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm, vflow_out in db_Output_VFlow_Out:
                if sector == sectorName:
                    if str(t_periods) == year and t_season == season:
                        if switch == 'fuel':
                            df.loc[t_day, d[tech]] = df.loc[t_day, d[tech]] + vflow_out * conversion
                        elif switch == 'tech':
                            df.loc[t_day, tech] = df.loc[t_day, tech] + vflow_out * conversion

            # Store results              
            activity[str(year) + '_' + str(season)] = df

            # Plot
            if createPlots == 'Y':
                # Access corresponding subplot    
                ax = a[i, j]

                # Legend
                if i == 0 and j == len(seasons) - 1:
                    df.plot.bar(ax=ax, stacked=True, title=titlename, legend=True)
                    a[i, j].legend(bbox_to_anchor=(1.7, -0.2), ncol=1)
                else:
                    df.plot.bar(ax=ax, stacked=True, title=titlename, legend=False)

                if i == len(years) - 1:  # Only bottom of plot
                    ax.set_xlabel("Year [-]")

                if j == 0:  # Only leftside of plot
                    ax.set_ylabel("Activity [GWh]")

            # Store to excel
            if saveData == 'Y':
                sheetname = str(year) + '_' + str(season)
                df.to_excel(writer, sheetname)

    # Save plot
    if createPlots == 'Y':
        fig = ax.get_figure()
        fig.savefig(savename, dpi=resolution, bbox_inches="tight")

        # Save excel file
    if saveData == 'Y':
        writer.save()

    # Return to original directory
    os.chdir(origDir)

    # Return results
    return activity

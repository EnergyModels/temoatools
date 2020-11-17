import os
import pandas as pd
import seaborn as sns
import temoatools as tt
import matplotlib.pyplot as plt

# load data
wrkdir = os.getcwd()
os.chdir('results')  # where results are located, and where files will be saved
df = pd.read_csv('activityTOD_by_fuel.csv')

# select years of interest to plot
years = [2018, 2030, 2050]
for year in df.year.unique():
    if year not in years:
        index_names = df[df.loc[:, 'year'] == year].index
        df.drop(index_names, inplace=True)

# select fuels to plot
fuelOrTechs = ['BIO', 'COAL_TAXED', 'ELC_CENTRAL', 'ELC_DIST', 'HYDRO', 'NATGAS_TAXED', 'NUCLEAR', 'SOLAR', 'WIND']
for fuelOrTech in df.fuelOrTech.unique():
    if fuelOrTech not in fuelOrTechs:
        index_names = df[df.loc[:, 'fuelOrTech'] == fuelOrTech].index
        df.drop(index_names, inplace=True)

# rename fuels to readable format
rename = {'BIO': 'Biomass', 'COAL_TAXED': 'Coal', 'DSL_TAXED': 'Diesel', 'ELC_CENTRAL': 'Central storage',
          'ELC_DIST': 'Distributed storage', 'HYDRO': 'Hydro', 'MSW_LF_TAXED': 'Landfill gas',
          'NATGAS_TAXED': 'Natural gas', 'NUCLEAR': 'Nuclear', 'OIL_TAXED': 'Oil', 'SOLAR': 'Solar', 'WIND': 'Wind'}
for key in rename.keys():
    ind = df.loc[:, 'fuelOrTech'] == key
    df.loc[ind, 'fuelOrTech'] = rename[key]

# rename seasons to readable format
rename = {'spring': 'Spring', 'summer': 'Summer', 'summer2': 'Summer2', 'fall': 'Fall', 'winter': 'Winter',
          'winter2': 'Winter2'}
for key in rename.keys():
    ind = df.loc[:, 'season'] == key
    df.loc[ind, 'season'] = rename[key]

# rename TOD to readable format
rename = {'hr01': 1, 'hr02': 2, 'hr03': 3, 'hr04': 4, 'hr05': 5, 'hr06': 6, 'hr07': 7, 'hr08': 8,
          'hr09': 9, 'hr10': 10, 'hr11': 11, 'hr12': 12, 'hr13': 13, 'hr14': 14, 'hr15': 15, 'hr16': 16,
          'hr17': 17, 'hr18': 18, 'hr19': 19, 'hr20': 20, 'hr21': 21, 'hr22': 22, 'hr23': 23, 'hr24': 24}
for key in rename.keys():
    ind = df.loc[:, 'tod'] == key
    df.loc[ind, 'tod'] = rename[key]

# Rename columns
df = df.rename(
    columns={"year": "Year", "season": "Season", "value": "Activity (GWh)", "tod": "Hour (-)", "fuelOrTech": "Fuel"},
    errors="raise")

# create separate plots for each database
for database in df.database.unique():
    # new figure
    plt.figure()

    # set aesthetics
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("talk")

    # select relevant database
    df2 = df[(df.database == database)]

    # plot
    sns.relplot(x='Hour (-)', y='Activity (GWh)', hue='Fuel', row='Year', col='Season', data=df2, kind='line',
                palette='bright')

    # save
    savename = 'plot_yearlyActivityTOD_byFuel_' + tt.remove_ext(database) + '.pdf'
    plt.savefig(savename, dpi=600)

# return to original directory
os.chdir(wrkdir)

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sensitivity_support import removeCamelHump, formatPlantName, formatFuelName, formatConnName

# ------------------------
# Inputs
# ------------------------
folder = 'sensitivity'
cases = ['SensitivityResults_A.csv', 'SensitivityResults_B.csv', 'SensitivityResults_C.csv', 'SensitivityResults_D.csv']
labels = ["Centralized", "Regionalized", "Small-scale PV + Batt", "Market Driven"]

variables = ['LCOE', 'avgEmissions']
varLabels = ['Levelized Cost of Electricity (cents/kWh)', 'Average Emissions (Mton/yr)']
conversions = [1.0, 1E-3]  # kton/yr to Mton/yr
n_display = 10  # max number of variables to display
resolution = 600

# ------------------------
# Begin program
# ------------------------
# Move to directory of interest (store current folder to return)
workDir = os.getcwd()
os.chdir(os.path.join(workDir, folder))

# Process each case
for case, label in zip(cases, labels):

    # --------
    # Pre-processing
    # --------
    # Read-in csv
    df = pd.read_csv(case)

    # set index as caseNum
    df = df.set_index('caseNum')

    # Convert units
    for var, convert in zip(variables, conversions):
        df.at[:, var] = df.loc[:, var] * convert

    # Keep a copy of the baseline
    baseline = df.loc[0].copy()

    # Remove bad values (and set equal to the baseline)
    for var in variables:
        # Zero values
        ind = df.loc[:, var] == 0.0
        df.at[ind, var] = baseline[var]

        # Null values
        ind = df.loc[:, var].isnull()
        df.at[ind, var] = baseline[var]

        # Normalize results wrt baseline
    for var in variables:
        df.at[1:, var] = df.loc[1:, var] - df.loc[0, var]

    # Remove baseline from dataframe
    df = df.drop([0])

    # Sort data so that the same (type,tech,variable) cases are adjacent and start with negative multiplier
    df = df.sort_values(by=['type', 'tech', 'variable', 'multiplier'])

    # Create dictionary to hold dataframes
    results = {}

    # Create new DataFrame to hold sorted results
    cols = ['name', 'type', 'variable', 'tech', 'low', 'high', 'abs']
    for var in variables:
        results[var] = pd.DataFrame(columns=cols)

    # fill-in data
    i = 1
    while i < len(df):
        # Common
        s = pd.Series()
        s['type'] = df.loc[i, 'type']
        s['tech'] = df.loc[i, 'tech']
        s['variable'] = df.loc[i, 'variable']
        s['multiplier'] = abs(df.loc[i, 'multiplier'])

        # Unique name for displaying in graph
        if df.loc[i, 'type'] == 'Globals':
            s['name'] = removeCamelHump(df.loc[i, 'variable'])
        elif df.loc[i, 'type'] == 'PowerPlants':
            s['name'] = formatPlantName(df.loc[i, 'tech']) + ' - ' + removeCamelHump(df.loc[i, 'variable'])
        elif df.loc[i, 'type'] == 'Fuels':
            s['name'] = formatFuelName(df.loc[i, 'tech']) + ' - ' + removeCamelHump(df.loc[i, 'variable'])
        elif df.loc[i, 'type'] == 'Connections':
            s['name'] = formatConnName(df.loc[i, 'tech']) + ' - ' + removeCamelHump(df.loc[i, 'variable'])

        # Variable specifc
        for var in variables:
            s['low'] = df.loc[i, var]
            s['high'] = df.loc[i + 1, var]
            s['abs'] = max(abs(df.loc[i, var]), abs(df.loc[i + 1, var]))
            results[var] = results[var].append(s, ignore_index=True)
        # Increment i
        i = i + 2
    # --------
    # Sort Results by abs col (absolute value of largest change)
    # --------
    for var in variables:
        results[var] = results[var].sort_values(by=['abs'], ascending=False)

        # Reset index
        results[var] = results[var].reset_index(drop=True)

    # --------
    # Filter null values
    # --------

    # Do something!

    # --------
    # Create Plots
    # --------

    custom_palette = [(0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                      (0.847, 0.000, 0.067)]  # Custom palette

    for var, varLabel in zip(variables, varLabels):
        savename = case[:-4] + '_' + var + '.png'

        n_cases = min(len(results[var]), n_display)
        sns.set(style='darkgrid')
        sns.set_color_codes("dark")

        # Initialize the matplotlib figure
        f, ax = plt.subplots(figsize=(4, 3))

        # Plot the low side
        sns.barplot(x="low", y="name", data=results[var].loc[:n_cases], orient="h", label="-10%",
                    color=custom_palette[2])  # Blue

        # Plot the crashes where alcohol was involved
        sns.barplot(x="high", y="name", data=results[var].loc[:n_cases], label="+10%",
                    color=custom_palette[1])  # Orange

        # Remove spines
        sns.despine(left=True, bottom=True)

        # Adjust ticks
        locs, labels = plt.xticks()
        for i in range(len(locs)):
            labels[i] = str(round(locs[i] + baseline[var], 2))
        ax.set_xticklabels(labels)

        # Set labels and legend
        ax.set_xlabel(varLabel)
        ax.set_ylabel('')
        ax.legend(loc='lower left')

        # Save plot
        f.savefig(savename, dpi=resolution, bbox_inches="tight")

# Return to Original Directory
os.chdir(workDir)

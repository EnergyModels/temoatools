import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot(df_, rows_, row_labels_, figure_name_, switch='activity'):
    # Set style and context using seaborn
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("paper")

    custom_palette = [(0.0, 0.0, 0.0), (0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                      (0.847, 0.000, 0.067), ]  # Custom palette

    resolution = 600

    cols = ['Current-No Tax', 'Hardened-No Tax', 'Current-Tax',
            'Hardened-Tax']  # No difference between historical and climate change here

    hue_order = ['Business-as-usual', 'Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas',
                 'Distributed - Hybrid', ]  # Create figure

    # Analyze each model year
    years = df.Year.unique()
    for year in years:

        # --------------------------
        # Plot
        # --------------------------
        f, a = plt.subplots(nrows=len(rows), ncols=len(cols), sharex=True, sharey=True)

        # Set figure size
        width = 7.48  # Two columns
        height = width
        f.set_size_inches(width, height)

        for i, row in enumerate(rows_):

            for j, col in enumerate(cols):

                # Access current axis
                ax = a[i][j]

                # Select data to plot
                df2 = df_[(df_.Year == year) & (df_.infra_and_carbon_tax == col) & (df_.Type2 == row)]

                # Use groupby to combine rows with the same Type2 value, and then reset index
                df3 = df2.groupby(['Type2', 'Scenario', 's']).sum().reset_index()

                # Plot data
                sns.barplot(x='Scenario', y='Value', data=df3, order=hue_order, ax=ax, palette=custom_palette)

                # Despine and remove ticks
                if j == 0:
                    sns.despine(ax=ax, )
                    ax.tick_params(top=False, right=False)
                else:
                    sns.despine(ax=ax, left=True)
                    ax.tick_params(top=False, right=False, left=False)

                # X-axis labels
                if i == len(rows) - 1:
                    ax.tick_params(axis='x', labelrotation=90)
                else:
                    ax.set_xlabel('')

                # Y-axis labels
                if j == 0:
                    if switch == 'activity':
                        ax.set_ylabel(row_labels[i] +'\n(TWh/yr)')
                    elif switch == 'capacity':
                        ax.set_ylabel(row_labels[i] +'\n(GW)')
                else:
                    ax.set_ylabel('')

                # Set Y limits
                if switch == 'activity':
                    ax.set_ylim(bottom=0.0, top=20.0)
                elif switch == 'capacity':
                    ax.set_ylim(bottom=0.0, top=3.0)

                # Additional Labels
                if i == 0:  # Top labels
                    ax.text(0.5, 1.1, col, horizontalalignment='center', verticalalignment='top',
                            transform=ax.transAxes)
                # if j == len(cols) - 1:  # Side labels
                #     ax.text(1.1, 0.5, row_labels_[i], horizontalalignment='center', verticalalignment='center',
                #             rotation=270, transform=ax.transAxes)

                # Legend
                if i == 0 and j == len(cols) - 1:
                    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), frameon=False, ncol=1)  # fontsize=16,

        # Save figure
        savename = figure_name_ + str(year) + '.png'
        # plt.show()
        plt.savefig(savename, dpi=resolution , bbox_inches="tight")
        plt.close()


# ========================================================================

# Alternate plotting function
def plot2(df_, rows_, row_labels_, figure_name_,switch='activity'):
    # Set style and context using seaborn
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("paper")

    custom_palette = [(0.0, 0.0, 0.0), (0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                      (0.847, 0.000, 0.067), ]  # Custom palette

    resolution = 600

    cols = ['Current-No Tax', 'Hardened-No Tax', 'Current-Tax',
            'Hardened-Tax']  # No difference between historical and climate change here

    hue_order = ['Business-as-usual', 'Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas',
                 'Distributed - Hybrid', ]  # Create figure

    # Analyze each model year
    years = df.Year.unique()
    for col in cols:

        # --------------------------
        # Plot
        # --------------------------
        f, a = plt.subplots(nrows=len(rows), ncols=len(years), sharex=True, sharey=True)

        # Set figure size
        width = 7.48  # Two columns
        height = width
        f.set_size_inches(width, height)

        for i, row in enumerate(rows_):

            for j, year in enumerate(years):

                # Access current axis
                ax = a[i][j]

                # Select data to plot
                df2 = df_[(df_.Year == year) & (df_.infra_and_carbon_tax == col) & (df_.Type2 == row)]

                # Use groupby to combine rows with the same Type2 value, and then reset index
                df3 = df2.groupby(['Type2','Scenario','s']).sum().reset_index()

                # Plot data
                sns.barplot(x='Scenario', y='Value', data=df3, order=hue_order, ax=ax, palette=custom_palette)

                # Despine and remove ticks
                if j == 0:
                    sns.despine(ax=ax, )
                    ax.tick_params(top=False, right=False)
                else:
                    sns.despine(ax=ax, left=True)
                    ax.tick_params(top=False, right=False, left=False)

                # X-axis labels
                if i == len(rows) - 1:
                    ax.tick_params(axis='x', labelrotation=90)
                else:
                    ax.set_xlabel('')

                # Y-axis labels
                if j == 0:
                    if switch == 'activity':
                        ax.set_ylabel(row_labels[i] + '\n(TWh/yr)')
                    elif switch == 'capacity':
                        ax.set_ylabel(row_labels[i] + '\n(GW)')
                else:
                    ax.set_ylabel('')

                # Set Y limits
                if switch == 'activity':
                    ax.set_ylim(bottom=0.0, top=20.0)
                elif switch == 'capacity':
                    ax.set_ylim(bottom=0.0, top=3.0)


                # Additional Labels
                if i == 0:  # Top labels
                    ax.text(0.5, 1.1, str(year), horizontalalignment='center', verticalalignment='top',
                            transform=ax.transAxes)
                # if j == len(years) - 1:  # Side labels
                #     ax.text(1.1, 0.5, row_labels_[i], horizontalalignment='center', verticalalignment='center',
                #             rotation=270, transform=ax.transAxes)

                # Legend
                if i == 0 and j == len(cols) - 1:
                    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), frameon=False, ncol=1)  # fontsize=16,

        # Save figure
        savename = figure_name_ + str(col) + '.png'
        # plt.show()
        plt.savefig(savename, dpi=resolution , bbox_inches="tight")
        plt.close()



# ========================================================================

folders = ['2019_11_07_full']

# Naming conventions
filename_activity_by_fuel = "activity_by_fuel_toPlot.csv"
filename_capacity_by_fuel = "capacity_by_fuel_toPlot.csv"
filename_activity_by_tech = "activity_by_tech_toPlot.csv"
filename_capacity_by_tech = "capacity_by_tech_toPlot.csv"

plotActivityFuel = True
plotCapacityFuel = True
plotActivityTech = True
plotCapacityTech = True

plotByYear = False
plotByScenario = True

# Set style and context using seaborn
sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
sns.set_context("paper")
resolution = 600

# Iterate through model runs
for folder in folders:

    # Move to results directory
    cwd = os.getcwd()
    path = os.getcwd() + '\\results\\' + folder
    os.chdir(path)

    # =====================================================
    # Activity by Fuel
    # =====================================================
    if plotActivityFuel:
        df = pd.read_csv(filename_activity_by_fuel, index_col=0)

        rows = ['Coal', 'Diesel', 'Oil', 'Natural Gas']
        row_labels = ['Coal', 'Diesel', 'Oil', 'Natural Gas']
        figure_name = 'activity_by_fuel_fossil_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='activity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='activity')

        rows = ['Solar', 'Wind', 'Hydro', 'Battery', 'Biomass']
        row_labels = ['Solar', 'Wind', 'Hydro', 'Battery', 'Biomass']
        figure_name = 'activity_by_fuel_renewable_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='activity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='activity')

    # =====================================================
    # Capacity by Fuel
    # =====================================================
    if plotCapacityFuel:
        df = pd.read_csv(filename_capacity_by_fuel, index_col=0)

        rows = ['Coal', 'Diesel', 'Oil', 'Natural Gas']
        row_labels = ['Coal', 'Diesel', 'Oil', 'Natural Gas']
        figure_name = 'capacity_by_fuel_fossil_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='capacity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='capacity')

        rows = ['Solar', 'Wind', 'Hydro', 'Battery', 'Biomass']
        row_labels = ['Solar', 'Wind', 'Hydro', 'Battery', 'Biomass']
        figure_name = 'capacity_by_fuel_renewable_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='capacity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='capacity')

    # =====================================================
    # Activity by Tech
    # =====================================================
    if plotActivityTech:
        df = pd.read_csv(filename_activity_by_tech, index_col=0)

        rows = ['Exist. Fossil', 'Cent. Fossil', 'Dist. Fossil', 'Exist. Renewable', 'Cent. Renewable',
                'Dist. Renewable']
        row_labels = ["Exist.\nFossil", 'Cent.\nFossil', 'Dist.\nFossil', "Exist.\nRenewable", 'Cent.\nRenewable',
                      'Dist.\nRenewable']
        figure_name = 'activity_by_category_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='activity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='activity')

        rows = ['TRANS', 'UGND_TRANS', 'DIST_COND', 'DIST_TWR', 'UGND_DIST']
        row_labels = ['Trans.', 'Ungd. Trans.', 'Dist. Cond.', 'Dist. Tower', 'Ungd Dist.']
        figure_name = 'activity_by_TD_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='activity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='activity')

    # =====================================================
    # Capacity by Tech
    # =====================================================
    if plotCapacityTech:
        df = pd.read_csv(filename_capacity_by_tech, index_col=0)

        rows = ['Exist. Fossil', 'Cent. Fossil', 'Dist. Fossil', 'Exist. Renewable', 'Cent. Renewable',
                'Dist. Renewable']
        row_labels = ["Exist.\nFossil", 'Cent.\nFossil', 'Dist.\nFossil', "Exist.\nRenewable", 'Cent.\nRenewable',
                      'Dist.\nRenewable']
        figure_name = 'capacity_by_category_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='capacity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='capacity')

        rows = ['TRANS', 'UGND_TRANS', 'DIST_COND', 'DIST_TWR', 'UGND_DIST']
        row_labels = ['Trans.', 'Ungd. Trans.', 'Dist. Cond.', 'Dist. Tower', 'Ungd Dist.']
        figure_name = 'capacity_by_TD_'
        if plotByYear:
            plot(df, rows, row_labels, figure_name,switch='capacity')
        if plotByScenario:
            plot2(df, rows, row_labels, figure_name,switch='capacity')

# =================================================
# Return to original directory
os.chdir(cwd)

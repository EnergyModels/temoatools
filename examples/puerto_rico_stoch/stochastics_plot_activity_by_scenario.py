import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ========================================================================

#  plotting function
def plot(df_, cats_, figure_name_):
    # Set style and context using seaborn
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("paper")

    custom_palette = [(0.0, 0.0, 0.0), (0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                      (0.847, 0.000, 0.067), ]  # Custom palette

    colors = sns.color_palette('colorblind')

    resolution = 600

    scenarios = ['Business-as-usual', 'Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas',
                 'Distributed - Hybrid', ]  # Create figure

    configs = ['Current-No Tax', 'Hardened-No Tax', 'Current-Tax',
               'Hardened-Tax']  # No difference between historical and climate change here

    # Analyze each model year
    years = df.Year.unique()
    print years

    for scenario in scenarios:
        for config in configs:

            # --------------------------
            # Plot
            # --------------------------
            f, a = plt.subplots(nrows=len(years), ncols=1, sharex=True, sharey=True)

            # Set figure size
            width = 7.48  # Two columns
            height = width
            f.set_size_inches(width, height)

            for i, year in enumerate(years):

                # Access current axis
                ax = a[i]

                # Get data to plot
                df2 = df_[(df_.Scenario == scenario) & (df_.infra_and_carbon_tax == config) & (df_.Year == year)]
                # df3 = df2.groupby(['Type2']).sum()
                # return df2, df3
                df3 = df2.pivot_table(index='s', columns='Type2', values='Value', aggfunc=np.sum)

                # return df2, df3

                # Add in zero values for missing columns
                for cat in cats_:
                    if cat not in df3.columns:
                        df3.loc[:,cat]=0.0

                # Remove columns not expected
                for col in df3.columns:
                    if col not in cats_:
                        df3 = df3.drop(axis=1,columns=col)
                # plot
                df3.plot.bar(stacked=True, ax=ax)

                # Despine and remove ticks
                sns.despine(ax=ax, )
                ax.tick_params(top=False, right=False)

                # X-axis labels
                if i == len(years) - 1:
                    ax.tick_params(axis='x', labelrotation=90)
                    ax.set_xlabel('Scenario')
                else:
                    ax.set_xlabel('')

                # Y-axis labels
                ax.set_ylabel('Activity (TWh/yr)')

                # Set Y limits
                ax.set_ylim(bottom=0.0,top=20.0)

                # Additional Labels
                ax.text(0.5, 1.1, str(year), horizontalalignment='center', verticalalignment='center',
                        transform=ax.transAxes)

                # Legend
                # if i == len(years) - 1:
                ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), frameon=False, ncol=1)  # fontsize=16,
                # else:
                    # ax.get_legend().remove()

                # Title above plot
                plt.suptitle(scenario + ' : ' + config)
                # Save figure
                savename = figure_name_ + scenario + config + '.png'
                # plt.show()
                plt.savefig(savename, dpi=resolution, bbox_inches="tight")
                plt.close()



# ========================================================================

folders = ['2019_10_30']

# Naming conventions
filename_activity_by_fuel = "activity_by_fuel_toPlot.csv"
filename_activity_by_tech = "activity_by_tech_toPlot.csv"

plotActivityFuel = True
plotActivityTech = True

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


        cats = ['Coal', 'Diesel', 'Oil', 'Natural Gas', 'Solar', 'Wind', 'Hydro', 'Battery', 'Biomass']
        # cats = ['COAL_TAXED', 'DSL_TAXED', 'OIL_TAXED', 'NATGAS_TAXED', 'SOLAR', 'WIND', 'HYDRO', 'MSW_LF_TAXED']
        figure_name = 'activity_by_fuel_'
        plot(df, cats, figure_name)

    # =====================================================
    # Activity by Tech
    # =====================================================
    if plotActivityTech:
        df = pd.read_csv(filename_activity_by_tech, index_col=0)

        cats = ['Exist. Fossil', 'Cent. Fossil', 'Dist. Fossil', 'Exist. Renewable', 'Cent. Renewable',
                'Dist. Renewable']

        figure_name = 'activity_by_category_'
        plot(df, cats, figure_name)

# =================================================
# Return to original directory
os.chdir(cwd)

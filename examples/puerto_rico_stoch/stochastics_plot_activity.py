import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt



folders = ['2019_10_25']

# Naming conventions
filename_activity_by_fuel = "activity_by_fuel_toPlot.csv"
filename_activity_by_tech = "activity_by_tech_toPlot.csv"

plotActivityFuel = 'True'
plotActivityTech = 'True'

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

        # row_order = ["Coal", "Oil", "Diesel", "Natural Gas", "Hydro", "Solar", "Wind", "Battery", "Landfill Gas",
        #              "Biomass"]

        # Bar Plot
        g = sns.FacetGrid(df, col='infra_and_carbon_tax',row='Type', hue='Scenario')
        g = (g.map(plt.bar, 'Year', 'Value').add_legend())
        savename = 'activity_by_fuel.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

    # =====================================================
    # Activity by Tech
    # =====================================================
    if plotActivityTech:
        df = pd.read_csv(filename_activity_by_tech, index_col=0)

        # Bar Plot
        g = sns.FacetGrid(df, col='infra_and_carbon_tax',row='Type', hue='Scenario')
        g = (g.map(plt.bar, 'Year', 'Value').add_legend())
        savename = 'activity_by_fuel.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()


    # =================================================
    # Return to original directory
    os.chdir(cwd)
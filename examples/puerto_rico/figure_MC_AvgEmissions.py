import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#=====================================================
# User Inputs
#=====================================================
figure_name = "figure_MC_AvgEmissinos" # png extension automatically added later


#-----------------------------------------------------
# Process Data
#-----------------------------------------------------
folder = os.getcwd() + '\\MonteCarlo'
caseNames = ['A','B','C','D']
csvs = ['MonteCarloResults_A.csv','MonteCarloResults_B.csv','MonteCarloResults_C.csv','MonteCarloResults_D.csv']
scenarios = ['Centralized - Natural Gas','Centralized - Hybrid','Distributed - Natural Gas','Distributed - Hybrid']

# Move to directory of interest (store current folder to return)
workDir = os.getcwd()
os.chdir(folder)

# Process data
df = pd.DataFrame()
for caseName, csv,scenario in zip(caseNames, csvs,scenarios):
    # Read-in csv
    df1 = pd.read_csv(csv)
    # Add Column for caseName
    df2 = df1.assign(caseName=caseName)
    # Add Column for scenario
    df2 = df2.assign(Scenario=scenario)
    # Flatten indices (remove layers of indexing)
    df2 = df2.reset_index()
    # Remove null values, use cost as indicator
    df2 = df2.fillna(0.0)
    # Add to df
    df = pd.concat([df, df2],sort=False)
# Return to original directory
os.chdir(workDir)


#=================================================
# Version 2
#=================================================

ax = sns.boxplot(x='caseName',y='avgEmissions',data=df,hue='Scenario')

# Save Figure
savename = figure_name + ".png"
plt.savefig(savename, dpi=600, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
# plt.close()

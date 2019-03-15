import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#=============================================================================#
# Common Inputs
#=============================================================================#
folder = os.getcwd() + '\\MonteCarlo'
caseNames = ['A','B','C','D']
csvs = ['MonteCarloResults_A.csv','MonteCarloResults_B.csv','MonteCarloResults_C.csv','MonteCarloResults_D.csv']
labels = ["Centralized","Regionalized","Small-scale","No Policy"]
colors = ['black','blue','green','red']
resolution = 600 # DPI
conf_int = 5 # Confidence interval  (%)
#=============================================================================#
# 0) Process Data
#=============================================================================#
# Move to directory of interest (store current folder to return)
workDir = os.getcwd()
os.chdir(folder)

# Process data
df_all = pd.DataFrame()
d = {}
for caseName,csv in zip(caseNames,csvs):
    
    # Read-in csv
    df1 = pd.read_csv(csv)
    # Convert wide to long
    df2 = pd.wide_to_long(df1,i='caseNum',j='year',stubnames=['cost','emis'],sep='_')
    
    # Add Column for caseName
    df2 = df2.assign(caseName=caseName)
    
    # Flatten indices (remove layers of indexing)
    df2 = df2.reset_index()
    # Coonvert year to numeric
    df2.year = pd.to_numeric(df2.year)
    # Convert emissions from kton/year to Mton/year
    df2.emis = df2.emis/1000.0
    # Remove null values, use cost as indicator
    df2 = df2.dropna()
    # Add to df
    df_all = pd.concat([df_all, df2])

# Return to original directory    
os.chdir(workDir)
#=============================================================================#
# 1) Cost by year
savename = 'Fig_CostByYear_V2.png'
#=============================================================================#

# Create plot
plt.figure()
sns.set(style="darkgrid")
sns.set_palette(colors)

# Plot lines
ax = sns.lineplot(x='year',y='cost',hue='caseName',data=df,legend=False,ci=conf_int,err_style='bars')
# ax = sns.lineplot(x='year',y='cost',hue='caseName',data=df,legend=False,n_boot=10)

# Plot measured data
# x=[2014.,2015.,2016.,2017.,2018.]
# y=[26.39,20.57,18.47,22.16,21.61]
# plt.plot(x,y,label='Actual',marker='o',linestyle='',color='gray')

# Format labels + legend
plt.xlabel("Year (-)")
plt.ylabel("Cost of Electricity (cents/kWh)")
leg = labels+['Actual']
plt.legend(leg,loc = 'upper center',bbox_to_anchor=(0.5, -0.15),ncol=3)

# Adjust layout
plt.tight_layout()

# Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")

#=============================================================================#
# 2) Emissions by year
savename = 'Fig_EmissionsByYear_V2.png'
#=============================================================================#

# Create plot
plt.figure()
sns.set(style="darkgrid")
sns.set_palette(colors)
# Plot lines
ax = sns.lineplot(x='year',y='emis',hue='caseName',data=df,legend=False,ci=conf_int)

# Plot Measured Data
x=[2010.,2015.]
y=[16.0,13.0]
plt.plot(x,y,label='Actual Price',marker='o',linestyle='',color='gray')

# # Plot Measured Data
# x=[2014.,2015.,2016.]
# y=[21.0,22.0,19.0]
# plt.plot(x,y,label='A',marker='o',linestyle='',color='gray')

# Format labels + legend
plt.xlabel("Year (-)")
plt.ylabel("CO$_2$ Emissions (Mton/year)")
leg = labels+['Actual']
#plt.legend(leg)
plt.legend(leg,loc = 'upper center',bbox_to_anchor=(0.5, -0.15),ncol=3)

# Adjust layout
plt.tight_layout()

## Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")
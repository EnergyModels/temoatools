import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

folder = dbFolder = os.getcwd() + '\\Results'
dbs = ["A.sqlite","B.sqlite","C.sqlite","D.sqlite"]
scenarios = ['Centralized - Natural Gas','Centralized - Hybrid','Distributed - Natural Gas','Distributed - Hybrid']
db_dict = {"A":'Centralized - Natural Gas',"B":'Centralized - Hybrid',"C":'Distributed - Natural Gas',"D":'Distributed - Hybrid',"s":"Baseline"}


plotCosts = "Yes"
plotEmissions = "Yes"

# Move to results directory
cwd = os.getcwd()
os.chdir(folder)
#-----------------------------------------------------
# Aesthetics (style + context)
# https://seaborn.pydata.org/tutorial/aesthetics.html
#-----------------------------------------------------
resolution = 1000 # Resolution (DPI - dots per inch)
style = 'white'     # options: "white", "whitegrid", "dark", "darkgrid", "ticks"
context = 'paper'  # options "paper", "notebook", "talk", "poster" (smallest -> largest)
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067),(0.0,0.0,0.0)] # Custom palette

#=====================================================
# Set figure parameters based on experience for each context
#=====================================================
if context=='paper':
    fig_size = [8,6]        # (width followed by height, in inches) Note: OK to leave as an empty list
    leg_coord = [1.6, -0.3] # Legend coordinates (x,y)
    hspace = 0.15           # vertical space between figures
    wspace = 0.15           # horizontal space between figures
elif context=='notebook':
    fig_size = [8,6]
    leg_coord = [1.75, -0.3]
    hspace = 0.2
    wspace = 0.2
elif context == 'talk':
    fig_size = [12,8]
    leg_coord = [1.75, -0.4]
    hspace = 0.3
    wspace = 0.35
elif context == 'poster':
    fig_size = [12,8]
    leg_coord = [1.8, -0.5]
    hspace = 0.3
    wspace = 0.35

#=================================================
# Costs
figure_name = "yearlyCosts_upsampled"
#=================================================
if plotCosts == "Yes":
    # Load and Process data
    df = pd.read_csv("Results_Costs_upsampled.csv",index_col=0)
    df = df.drop("prob",axis=1)
    df2 = pd.melt(df,id_vars=["database","scenario"],var_name="Year",value_name="Value")
    for db, scenario in zip(dbs,scenarios):
        ind = df2.loc[:, "database"]==db
        df2.loc[ind, "database"] = scenario
    df2 = df2.rename(columns={"scenario": "s", "database": "Scenario"})

    # Set style and context using seaborn
    sns.set_style(style)
    sns.set_context(context)

    x_label = "Year (-)"
    y_label = "Cost of Electricity (cents/kWh)"

    # Box and Whisker Plot
    f = plt.figure(figsize=fig_size)
    ax = sns.boxplot(x="Year",y="Value",data=df2,hue='Scenario',palette=custom_palette)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_yscale("log")
    savename = figure_name + "_box_" + context + '.png'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
    plt.close()

    # Violin Plot
    f = plt.figure(figsize=fig_size)
    ax = sns.violinplot(x="Year",y="Value",data=df2,hue='Scenario',palette=custom_palette)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_yscale("log")
    savename = figure_name + "_violin_" + context + '.pdf'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight")
    plt.close()

#=================================================
# Emissions
figure_name = "yearlyEmissions_up"
#=================================================
if plotEmissions == "Yes":
    # Load and Process data
    df = pd.read_csv("Results_Emissions_upsampled.csv",index_col=0)
    df = df.drop("prob",axis=1)
    df2 = pd.melt(df,id_vars=["database","scenario"],var_name="Year",value_name="Value")
    for db, scenario in zip(dbs,scenarios):
        ind = df2.loc[:, "database"]==db
        df2.loc[ind, "database"] = scenario
    df2 = df2.rename(columns={"scenario": "s", "database": "Scenario"})

    # Set style and context using seaborn
    sns.set_style(style)
    sns.set_context(context)

    x_label = "Year (-)"
    y_label = "Emissions (kton/yr)"

    # Box and Whisker Plot
    f = plt.figure(figsize=fig_size)
    ax = sns.boxplot(x="Year",y="Value",data=df2,hue='Scenario',palette=custom_palette)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    savename = figure_name + "_box_" + context + '.png'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight")
    plt.close()

    # Violin Plot
    f = plt.figure(figsize=fig_size)
    ax = sns.violinplot(x="Year",y="Value",data=df2,hue='Scenario',palette=custom_palette)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    savename = figure_name + "_violin_" + context + '.pdf'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight")
    plt.close()

#=====================================================
# Activity
figure_name = "activity"
#=====================================================
fuel_short = ["BIO","COAL","DSL","ELC_CENTRAL","ELC_DIST","HYDRO","MSW_LF","NATGAS","OIL","SOLAR","WIND"]
fuel_long = ["Biomass","Coal","Diesel","Battery","Battery","Hydro","Landfill Gas","Natural Gas","Oil","Solar","Wind"]

# Load and Process data
# df = pd.read_csv("Results_yearlyActivity_byFuel_upsampled.csv")
df = pd.read_csv("Results_yearlyActivity_byFuel.csv",index_col=0)
# df = df.drop("prob",axis=1)
df2 = pd.melt(df,id_vars=["database","scenario","fuelOrTech"],var_name="Year",value_name="Value")
for db, scenario in zip(dbs,scenarios):
    ind = df2.loc[:, "database"]==db
    df2.loc[ind, "database"] = scenario
for short, long in zip(fuel_short, fuel_long):
    ind = df2.loc[:, "fuelOrTech"] == short
    df2.loc[ind, "fuelOrTech"] = long
df2 = df2.rename(columns={"scenario": "s", "database": "Scenario","fuelOrTech":"Type"})

# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

col_order =["Coal","Oil","Diesel","Natural Gas","Hydro","Solar","Wind","Battery","Landfill Gas","Biomass"]

# Box Plot
g = sns.catplot(x="Year", y="Value", hue="Scenario", col="Type", data=df2, kind="box",col_wrap=3,col_order=col_order,palette=custom_palette)#,height=4, aspect=.7)
savename = figure_name + "_box_" + context + '.pdf'
plt.savefig(savename, dpi=resolution, bbox_inches="tight")
plt.close()

# Violin Plot
g = sns.catplot(x="Year", y="Value", hue="Scenario", col="Type", data=df2, kind="violin",col_wrap=3,col_order=col_order,palette=custom_palette)#,height=4, aspect=.7)
savename = figure_name + "_violin_" + context + '.pdf'
plt.savefig(savename, dpi=resolution, bbox_inches="tight")
plt.close()

#=================================================
# Return to original directory
os.chdir(cwd)
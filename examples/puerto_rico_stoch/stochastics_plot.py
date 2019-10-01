import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

folder = dbFolder = os.getcwd() + '\\Results'
dbs = ["A.sqlite","B.sqlite","C.sqlite","D.sqlite"]
scenarios = ['Centralized - Natural Gas','Centralized - Hybrid','Distributed - Natural Gas','Distributed - Hybrid']
db_dict = {"A":'Centralized - Natural Gas',"B":'Centralized - Hybrid',"C":'Distributed - Natural Gas',"D":'Distributed - Hybrid',"s":"Baseline"}


# Move to results directory
cwd = os.getcwd()
os.chdir(folder)
#-----------------------------------------------------
# Aesthetics (style + context)
# https://seaborn.pydata.org/tutorial/aesthetics.html
#-----------------------------------------------------
resolution = 1000 # Resolution (DPI - dots per inch)
style = 'white'     # options: "white", "whitegrid", "dark", "darkgrid", "ticks"
context = 'talk'  # options "paper", "notebook", "talk", "poster" (smallest -> largest)
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
figure_name = "yearlyCosts"
#=================================================
# Load and process data
df = pd.read_excel("Results_Costs.xls",sheet_name="yearlyCosts")
df2 = pd.melt(df,id_vars=["database","scenario"],var_name="Year",value_name="Value")
# for index, row in df2.iterrows(): df2.loc[index,"database"] = df2.loc[index,"scenario"][0]
for index, row in df2.iterrows():
    df2.loc[index,"database"] = db_dict[df2.loc[index,"scenario"][0]]
df2.drop(df2.loc[df2['database']=="Baseline"].index, inplace=True)


# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

# Plot
f = plt.figure(figsize=fig_size)
ax = sns.boxplot(x="Year",y="Value",data=df2,hue='database',palette=custom_palette)
ax.set_xlabel("Year (-)")
ax.set_ylabel("Cost of Electricity (cents/kWh)")
ax.set_yscale("log")

# Save Figure
savename = figure_name + "_" + context + '.png'
plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend

#=================================================
# Emissions
figure_name = "yearlyEmissions"
#=================================================
# Load and process data
df = pd.read_excel("Results_Emissions.xls",sheet_name="yearlyEmissions")
df2 = pd.melt(df,id_vars=["database","scenario"],var_name="Year",value_name="Value")
for index, row in df2.iterrows():
    df2.loc[index,"database"] = db_dict[df2.loc[index,"scenario"][0]]
df2.drop(df2.loc[df2['database']=="Baseline"].index, inplace=True)

# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

# Plot
f = plt.figure(figsize=fig_size)
ax = sns.boxplot(x="Year",y="Value",data=df2,hue='database',palette=custom_palette)
ax.set_xlabel("Year (-)")
ax.set_ylabel("Emissions (kton/yr)")


# Save Figure
savename = figure_name + "_" + context + '.png'
plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend

#=====================================================
# Activity
figure_name = "activity"
#=====================================================
# Load and process data
df = pd.read_excel("Results_yearlyActivity_byFuel.xls",sheet_name="yearlyEmissions")
df2 = pd.melt(df,id_vars=["database","scenario"],var_name="Year",value_name="Value")
for index, row in df2.iterrows():
    df2.loc[index,"database"] = db_dict[df2.loc[index,"scenario"][0]]
df2.drop(df2.loc[df2['database']=="Baseline"].index, inplace=True)


# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

# Create Plots
f, ax = plt.subplots(nrows, ncols)

count = 0
# Iterate Rows (Y variables)
for i in range(nrows):

    # Iterate Columns (X variables)
    for j in range(ncols):

        # Select entries of interest
        y_var = y_vars[count]
        y_label = y_labels[count]
        count = count + 1

        sns.boxplot(x=x_var, y=y_var, data=df, hue='Scenario', palette=custom_palette, ax=ax[i, j])

        # Remove built-in legend
        ax[i, j].get_legend().remove()

        # X-axis Labels (Only bottom)
        if i == nrows-1:
            ax[i,j].set_xlabel(x_label)
        else:
            ax[i,j].get_xaxis().set_visible(False)

        # Y-axis labels (Only left side)
        ax[i,j].set_ylabel(y_label)
        ax[i,j].yaxis.set_label_coords(-0.125, 0.5)

        # Set X and Y Limits
        if len(x_lim)== 2:
            ax[i,j].set_xlim(left=x_lim[0], right=x_lim[1])
        if len(y_lim) ==2 :
            ax[i,j].set_ylim(bottom=y_lim[0],top=y_lim[1])

        # Set X ticks
        if len(x_tick) > 2:
            ax[i,j].xaxis.set_ticks(x_tick)
        else:
            n_ticks = 4
            ax[i, j].locator_params(axis='x', nbins=n_ticks)

        # Set Y ticks (either specified values, or limits number of ticks used)
        if len(y_tick) > 2:
            ax[i,j].yaxis.set_ticks(y_tick)
        else:
            n_ticks = 4
            ax[i, j].locator_params(axis='y', nbins=n_ticks)

# Legend (only for middle bottom)
leg = ax[nrows-1,0].legend(bbox_to_anchor=(leg_coord[0], leg_coord[1]), loc='center', ncol=len(series_labels), frameon = False, scatterpoints = 1)

# Adjust layout
if len(fig_size)>0:
    f.set_size_inches(fig_size)
plt.tight_layout()                         # https://matplotlib.org/users/tight_layout_guide.html
f.subplots_adjust(wspace = wspace,hspace=hspace) # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html

# Save Figure
savename = figure_name + "_" + context + '.png'
plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
# plt.close()


#=================================================
# Return to original directory
os.chdir(cwd)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#=====================================================
# User Inputs
#=====================================================
figure_name = "figure_combine_results_bar" # png extension automatically added later

#-----------------------------------------------------
# Process Data
#-----------------------------------------------------

scenarios = ['Centralized - Natural Gas','Centralized - Hybrid','Distributed - Natural Gas','Distributed - Hybrid']

# Normalized
df = pd.DataFrame({

'Build-back Time': [97.70, 100.0, 31.80, 45.16],
'Initial People without Power': [100.0, 100.0, 58.38, 60.99],
'2052 Emissions': [93.09, 49.80, 100.0, 44.81],
'Average Emissions': [96.35, 75.34, 100.0, 72.74],
'LCOE': [98.70, 97.93, 100.0, 98.04],
})

# Raw
# df = pd.DataFrame({
#
# 'Build-back Time': [212.0, 217.0, 69.0, 98.0],
# 'Initial People without Power': [91.7, 91.7, 53.5, 55.9],
# '2052 Emissions': [5964, 3191, 6407, 2871],
# 'Average Emissions': [7672, 5999, 7963, 5792],
# 'LCOE': [9.08, 9.01, 9.2, 9.02],
# })

#-----------------------------------------------------
# Aesthetics (style + context)
# https://seaborn.pydata.org/tutorial/aesthetics.html
#-----------------------------------------------------
resolution = 1000 # Resolution (DPI - dots per inch)
style = 'white'     # options: "white", "whitegrid", "dark", "darkgrid", "ticks"
context = 'talk'  # options "paper", "notebook", "talk", "poster" (smallest -> largest)

# Series palette options
colorblind_palette = sns.color_palette('colorblind')        # https://seaborn.pydata.org/tutorial/color_palettes.html
xkcd_palette = sns.xkcd_palette(["royal blue", "tangerine", "greyish", "faded green", "raspberry"]) # https://xkcd.com/color/rgb/
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)] # Custom palette

#-----------------------------------------------------
# Plotting Inputs
#-----------------------------------------------------
variables = ['LCOE','2052 Emissions' ,'Initial People without Power', 'Build-back Time']
# labels = ['LCOE (cents/kWh)','2052 Emissions (Mton/yr)' ],['Initial People without Power (%)', 'Build-back Time (days)']]

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

#=====================================================
# Begin plotting
#=====================================================


# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

# Create Plots
f, ax = plt.subplots()

count = 0
# Iterate Variables
for i,variable in enumerate(variables):
    ax.bar(df.index,df[variable], label=variable)

ax.set_xticks(df.index)
ax.set_xticklabels(scenarios)

ax.legend()

# Custom

# Legend (only for middle bottom)
# leg = ax[nrows-1,0].legend(bbox_to_anchor=(leg_coord[0], leg_coord[1]), loc='center', ncol=len(series_labels), frameon = False, scatterpoints = 1)

# # Adjust layout
# if len(fig_size)>0:
#     f.set_size_inches(fig_size)
# plt.tight_layout()                         # https://matplotlib.org/users/tight_layout_guide.html
# f.subplots_adjust(wspace = wspace,hspace=hspace) # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
#
# # Save Figure
# savename = figure_name + "_" + context + 'V1.png'
# plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
# # plt.close()
#
# #=================================================
# # Version 2
# #=================================================
# f = plt.figure(figsize=fig_size)
# ax = sns.boxplot(x=x_var,y=y_var,data=df,hue='Scenario',palette=custom_palette)
# ax.set_xlabel(x_label)
# ax.set_ylabel(y_label)
#
# # Save Figure
#
# savename = figure_name + "_" + context + 'V2.png'
# plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
# # plt.close()

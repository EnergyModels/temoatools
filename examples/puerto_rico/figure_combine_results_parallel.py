import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#=====================================================
# User Inputs
#=====================================================
figure_name = "figure_combine_results_parallel" # png extension automatically added later

#-----------------------------------------------------
# Process Data
#-----------------------------------------------------

scenarios = ['Centralized - Natural Gas','Centralized - Hybrid','Distributed - Natural Gas','Distributed - Hybrid']

# Normalized
df = pd.DataFrame({
'scenarios':['Centralized - Natural Gas','Centralized - Hybrid','Distributed - Natural Gas','Distributed - Hybrid'],
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
#
#
#
#
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

#=====================================================
# Set figure parameters based on experience for each context
#=====================================================
if context=='paper':
    fig_size = [8,6]        # (width followed by height, in inches) Note: OK to leave as an empty list
    leg_coord = [0, -0.3] # Legend coordinates (x,y)
    hspace = 0.15           # vertical space between figures
    wspace = 0.15           # horizontal space between figures
elif context=='notebook':
    fig_size = [8,6]
    leg_coord = [0, -0.3]
    hspace = 0.2
    wspace = 0.2
elif context == 'talk':
    fig_size = [12,8]
    leg_coord = [0, -0.4]
    hspace = 0.3
    wspace = 0.35
elif context == 'poster':
    fig_size = [12,8]
    leg_coord = [0, -0.5]
    hspace = 0.3
    wspace = 0.35

#-----------------------------------------------------
# Plotting Inputs
#-----------------------------------------------------
# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

variables = ['LCOE','2052 Emissions' ,'Initial People without Power', 'Build-back Time']
ax = pd.plotting.parallel_coordinates(df, 'scenarios',cols=variables, color=custom_palette)
ax.legend(bbox_to_anchor=(leg_coord[0], leg_coord[1]), ncol=len(df.scenarios)/2, loc='center',frameon = False, scatterpoints = 1)

ax.set_ylabel('Normalized Indices (-)')
# ax.set_xticks()
plt.xticks(rotation=45)
plt.tight_layout()
savename = figure_name + "_" + context + 'V2.png'
plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
#
# #=====================================================
# # Begin plotting
# #=====================================================
#
# # series variables, all lists are expected to the same length
# nrows = len(variables)
# ncols = len(variables[0])
#
#
#
# # Create Plots
# f, ax = plt.subplots(nrows, ncols)
#
# count = 0
# # Iterate Rows (Y variables)
# for i in range(nrows):
#
#     # Iterate Columns (X variables)
#     for j in range(ncols):
#
#
#         variable = variables[i][j]
#
#         series_val = series_vals[count]
#         label = series_labels[count]
#         color = series_colors[count]
#         marker = series_markers[count]
#         size = series_marker_sizes[count]
#         count = count + 1
#
#         # Select entries of interest
#
#
#         ax[i,j].bar(df.index, df[variable], label=variable)
#
#
#         # Plot
#         # x = df2.loc[:, x_var] * x_convert
#         # y = df2.loc[:, y_var] * y_convert
#         # # ax[i,j].scatter(x.values, y.values, c=color, s=size, marker=marker, label=label,edgecolors='none')
#         # sns.boxplot(x=x_var,y=y_var,data=df2,ax=ax[i,j],color=color)
#
#         # X-axis Labels (Only bottom)
#         # if i == nrows-1:
#         #     ax[i,j].set_xlabel(x_label)
#         # else:
#         #     ax[i,j].get_xaxis().set_visible(False)
#
#         # Y-axis labels (Only left side)
#         # if j == 0:
#         ax[i,j].set_ylabel(variable)
#         ax[i,j].yaxis.set_label_coords(-0.25, 0.5)
#         # else:
#         #     ax[i,j].get_yaxis().set_visible(False)
#
#         # Set X and Y Limits
#         # if len(x_lim)== 2:
#         #     ax[i,j].set_xlim(left=x_lim[0], right=x_lim[1])
#         # if len(y_lim) ==2 :
#         #     ax[i,j].set_ylim(bottom=y_lim[0],top=y_lim[1])
#
#         # Set X ticks
#         # if len(x_tick) > 2:
#         #     ax[i,j].xaxis.set_ticks(x_tick)
#         # else:
#         #     n_ticks = 4
#         #     ax[i, j].locator_params(axis='x', nbins=n_ticks)
#
#         # Set Y ticks (either specified values, or limits number of ticks used)
#         # if len(y_tick) > 2:
#         #     ax[i,j].yaxis.set_ticks(y_tick)
#         # else:
#         #     n_ticks = 4
#         #     ax[i, j].locator_params(axis='y', nbins=n_ticks)
#
#         # Column Labels
#         # if i == 0:
#         #     text = col_labels[j]
#         #     ax[i,j].text(0.5, 1.1, text, horizontalalignment='center', verticalalignment='top',
#         #             transform=ax[i,j].transAxes)
#         # Row Labels
#         # if j == ncols-1:
#         #     text = row_labels[i]
#         #     ax[i,j].text(1.05, 0.5, text, horizontalalignment='center', verticalalignment='center',
#         #             rotation=270, transform=ax[i,j].transAxes)
#
#
# # Custom
#
# # Legend (only for middle bottom)
# leg = ax[nrows-1,0].legend(bbox_to_anchor=(leg_coord[0], leg_coord[1]), loc='center', ncol=len(series_labels), frameon = False, scatterpoints = 1)
#
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

# # plt.close()

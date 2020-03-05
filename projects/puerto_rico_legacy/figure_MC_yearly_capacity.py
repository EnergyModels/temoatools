import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#=====================================================
# User Inputs
#=====================================================
figure_name = "figure_MC_yearly_capacity" # png extension automatically added later

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
    # Convert wide to long
    # df2 = pd.wide_to_long(df1, i='caseNum', j='year', stubnames=['cost', 'emis'], sep='_')
    df2 = pd.wide_to_long(df1, i='caseNum', j='year', stubnames=['cost', 'emis','cap_BIO','cap_COAL','cap_DSL','cap_HYDRO','cap_MSW_LF','cap_NATGAS','cap_OIL','cap_SOLAR','cap_WIND','cap_ELC_DIST','cap_ELC_CENTRAL'], sep='-')
    # Add Column for caseName
    df2 = df2.assign(caseName=caseName)
    # Add Column for scenario
    df2 = df2.assign(Scenario=scenario)
    # Flatten indices (remove layers of indexing)
    df2 = df2.reset_index()
    # Coonvert year to numeric
    df2.year = pd.to_numeric(df2.year)
    # Convert emissions from kton/year to Mton/year
    df2.emis = df2.emis / 1000.0
    # Remove null values, use cost as indicator
    df2 = df2.fillna(0.0)
    # Add to df
    df = pd.concat([df, df2],sort=False)
# Return to original directory
os.chdir(workDir)

# Only show certain years
years2show = [2016,2028,2040,2052]
df = df[df['year'].isin(years2show)]

# Convert
convert = 1.0
df.loc[:,'cap_BIO'] = df.loc[:,'cap_BIO'] * convert
df.loc[:,'cap_COAL'] = df.loc[:,'cap_COAL'] * convert
df.loc[:,'cap_DSL'] = df.loc[:,'cap_DSL'] * convert
df.loc[:,'cap_HYDRO'] = df.loc[:,'cap_HYDRO'] * convert
df.loc[:,'cap_MSW_LF'] = df.loc[:,'cap_MSW_LF'] * convert
df.loc[:,'cap_NATGAS'] = df.loc[:,'cap_NATGAS'] * convert
df.loc[:,'cap_OIL'] = df.loc[:,'cap_OIL'] * convert
df.loc[:,'cap_SOLAR'] = df.loc[:,'cap_SOLAR'] * convert
df.loc[:,'cap_WIND'] = df.loc[:,'cap_WIND'] * convert
df.loc[:,'cap_ELC_DIST'] = df.loc[:,'cap_ELC_DIST'] * convert
df.loc[:,'cap_ELC_CENTRAL'] = df.loc[:,'cap_ELC_CENTRAL'] * convert

# Create new categories
df.loc[:,'cap_PETROL'] = df.apply(lambda x: x['cap_OIL'] + x['cap_DSL'], axis=1)
df.loc[:,'cap_RENEW'] = df.apply(lambda x: x['cap_BIO'] + x['cap_HYDRO']+ x['cap_MSW_LF'], axis=1)
df.loc[:,'cap_BATT'] = df.apply(lambda x: x['cap_ELC_DIST'] + x['cap_ELC_CENTRAL'], axis=1)

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
# x variables, all lists are expected to the same length
x_var = "year"                     # Need to be columns in DataFrame
x_label = "Year (-)"     # Note: keep short
x_convert = 1.0                  # Multiplier to convert to display units
x_tick = []                       # Ok to leave empty
x_lim = []                        # Ok to leave empty

# y variables, all lists are expected to the same length
y_vars = ["cap_COAL","cap_PETROL","cap_NATGAS","cap_SOLAR","cap_WIND","cap_BATT"]
y_labels = ["Coal (GW)","Petroleum (GW)","Natural Gas (GW)","Solar (GW)","Wind (GW)","Battery (GW)"]
y_convert = 1.0
y_tick = []
y_lim = []

# series variables, all lists are expected to the same length
nrows = 3
ncols = 2
row_labels = ['','']
col_labels = ['','']
series_var = 'caseName'
series_vals = ['A','B','C','D']
series_labels = ['Case 1','Case 2','Case 3',' Case 4']
series_colors = custom_palette # Use a palette listed above
series_markers = ['x', '+', 'o', '*']
series_marker_sizes = [40,40,40,40]

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
    leg_coord = [1., -0.5]
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

        # # Column Labels
        # if i == 0:
        #     text = col_labels[j]
        #     ax[i,j].text(0.5, 1.1, text, horizontalalignment='center', verticalalignment='top',
        #             transform=ax[i,j].transAxes)
        # # Row Labels
        # if j == ncols-1:
        #     text = row_labels[i]
        #     ax[i,j].text(1.05, 0.5, text, horizontalalignment='center', verticalalignment='center',
        #             rotation=270, transform=ax[i,j].transAxes)


# Custom

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

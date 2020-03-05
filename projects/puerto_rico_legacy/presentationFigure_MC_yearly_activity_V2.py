import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#=====================================================
# User Inputs
#=====================================================
figure_name = "presentationFigure_MC_yearly_activity_V2" # png extension automatically added later

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
    df2 = pd.wide_to_long(df1, i='caseNum', j='year', stubnames=['cost', 'emis','act_BIO','act_COAL','act_DSL','act_HYDRO','act_MSW_LF','act_NATGAS','act_OIL','act_SOLAR','act_WIND','act_ELC_DIST','act_ELC_CENTRAL'], sep='-')
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
convert = 1E-3
df.loc[:,'act_BIO'] = df.loc[:,'act_BIO'] * convert
df.loc[:,'act_COAL'] = df.loc[:,'act_COAL'] * convert
df.loc[:,'act_DSL'] = df.loc[:,'act_DSL'] * convert
df.loc[:,'act_HYDRO'] = df.loc[:,'act_HYDRO'] * convert
df.loc[:,'act_MSW_LF'] = df.loc[:,'act_MSW_LF'] * convert
df.loc[:,'act_NATGAS'] = df.loc[:,'act_NATGAS'] * convert
df.loc[:,'act_OIL'] = df.loc[:,'act_OIL'] * convert
df.loc[:,'act_SOLAR'] = df.loc[:,'act_SOLAR'] * convert
df.loc[:,'act_WIND'] = df.loc[:,'act_WIND'] * convert
df.loc[:,'act_ELC_DIST'] = df.loc[:,'act_ELC_DIST'] * convert
df.loc[:,'act_ELC_CENTRAL'] = df.loc[:,'act_ELC_CENTRAL'] * convert

# Create new categories
df.loc[:,'act_PETROL'] = df.apply(lambda x: x['act_OIL'] + x['act_DSL'], axis=1)
df.loc[:,'act_RENEW'] = df.apply(lambda x: x['act_BIO'] + x['act_HYDRO']+ x['act_MSW_LF'], axis=1)
df.loc[:,'act_BATT'] = df.apply(lambda x: x['act_ELC_DIST'] + x['act_ELC_CENTRAL'], axis=1)

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

all_y_vars = [["act_COAL","act_PETROL","act_NATGAS"],["act_SOLAR","act_WIND","act_BATT"]]
all_y_labels = [["Coal\n(TWh/yr)","Petroleum\n(TWh/yr)","Natural Gas\n(TWh/yr)"],["Solar\n(TWh/yr)","Wind\n(TWh/yr)","Battery\n(TWh/yr)"]]
versions = ['a','b']


for y_vars, y_labels, version in zip(all_y_vars,all_y_labels,versions):

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
    # y_vars = ["act_COAL","act_PETROL","act_NATGAS","act_SOLAR","act_WIND","act_BATT"]
    # y_labels = ["Coal (TWh/yr)","Petroleum (TWh/yr)","Natural Gas (TWh/yr)","Solar (TWh/yr)","Wind (TWh/yr)","Battery (TWh/yr)"]
    y_convert = 1.0
    y_tick = []
    y_lim = []

    # series variables, all lists are expected to the same length
    nrows = 3
    ncols = 1
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
    f, ax = plt.subplots(nrows, ncols, figsize=[10,5])

    count = 0
    # Iterate Rows (Y variables)
    for j in range(nrows):

        # Iterate Columns (X variables)
        for i in range(ncols):

            # Select entries of interest
            y_var = y_vars[count]
            y_label = y_labels[count]
            count = count + 1

            sns.boxplot(x=x_var, y=y_var, data=df, hue='Scenario', palette=custom_palette, ax=ax[j])

            # Remove built-in legend
            ax[j].get_legend().remove()

            # X-axis Labels (Only bottom)
            if j == nrows-1:
                ax[j].set_xlabel(x_label)
            else:
                ax[j].get_xaxis().set_visible(False)

            # Y-axis labels (Only left side)
            ax[j].set_ylabel(y_label)
            ax[j].yaxis.set_label_coords(-0.125, 0.5)

            # Set X and Y Limits
            if len(x_lim)== 2:
                ax[j].set_xlim(left=x_lim[0], right=x_lim[1])
            if len(y_lim) ==2 :
                ax[j].set_ylim(bottom=y_lim[0],top=y_lim[1])

            # Set X ticks
            if len(x_tick) > 2:
                ax[j].xaxis.set_ticks(x_tick)
            else:
                n_ticks = 4
                ax[j].locator_params(axis='x', nbins=n_ticks)

            # Set Y ticks (either specified values, or limits number of ticks used)
            if len(y_tick) > 2:
                ax[i,j].yaxis.set_ticks(y_tick)
            else:
                n_ticks = 4
                ax[j].locator_params(axis='y', nbins=n_ticks)

    # Legend (only for middle bottom)
    leg = ax[1].legend(bbox_to_anchor=(1.3, 0.5), loc='center', ncol=1, frameon = False, scatterpoints = 1)

    # Adjust layout
    if len(fig_size)>0:
        f.set_size_inches(fig_size)
    plt.tight_layout()                         # https://matplotlib.org/users/tight_layout_guide.html
    f.subplots_adjust(wspace = wspace,hspace=hspace) # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html

    # Save Figure
    savename = figure_name + '_' + version + "_" + context + '.png'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
    # plt.close()

import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot(df_, col_order_, x_var_, x_label_, y_var_, y_label_, figure_name_, plot_type='violin', y_scale='linear', ylims=[]):
    # Set style and context using seaborn
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("paper")

    custom_palette = [(0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361), (0.847, 0.000, 0.067),
                      (0.0, 0.0, 0.0)]  # Custom palette

    resolution = 1000

    # Column width guidelines https://www.elsevier.com/authors/author-schemas/artwork-and-media-instructions/artwork-sizing
    # Single column: 90mm = 3.54 in
    # 1.5 column: 140 mm = 5.51 in
    # 2 column: 190 mm = 7.48 i
    width = 7.48  # inches
    height = 4.0  # inches

    # --------------------------
    # Plot
    # --------------------------

    if plot_type == 'violin':
        g = sns.catplot(x=x_var_, y=y_var_, data=df_, hue='Scenario', palette=custom_palette, kind="violin", col="case",
                        col_wrap=2, col_order=col_order_, inner=None, scale="area", cut=0, bw=0.5, linewidth=0.5,
                        legend=False, saturation=1.0, scale_hue=False).set(yscale=y_scale)
    elif plot_type == 'box':
        g = sns.catplot(x=x_var, y=y_var, data=df, hue='Scenario', palette=custom_palette, kind="box", col="case",
                        col_wrap=2, col_order=col_order_, linewidth=0.5, legend=False, saturation=1.0).set(yscale=y_scale)

    if len(ylims)==2:
        g.axes[0].set_ylim(ylims[0],ylims[1])
        g.axes[1].set_ylim(ylims[0],ylims[1])
        g.axes[2].set_ylim(ylims[0],ylims[1])
        g.axes[3].set_ylim(ylims[0],ylims[1])

    # Set size
    f = plt.gcf()
    f.set_size_inches(width, height)

    # Labels
    g.set_axis_labels(x_label_, y_label_)

    # Remove ticks
    g.axes[0].tick_params(top=False, right=False)
    g.axes[1].tick_params(top=False, right=False, left=False)
    g.axes[2].tick_params(top=False, right=False)
    g.axes[3].tick_params(top=False, right=False, left=False)

    # Despine
    sns.despine(ax=g.axes[0], )
    sns.despine(ax=g.axes[1], left=True)
    sns.despine(ax=g.axes[2], )
    sns.despine(ax=g.axes[3], left=True)

    # Additional Labels
    g.set_titles(" ")
    ax = g.axes[0]
    ax.text(0.5, 1.1, 'Current Infrastructure', horizontalalignment='center', verticalalignment='top',
            transform=ax.transAxes)
    ax = g.axes[1]
    ax.text(0.5, 1.1, 'Hardened Infrastructure', horizontalalignment='center', verticalalignment='top',
            transform=ax.transAxes)
    ax.text(1.1, 0.5, 'Historical', horizontalalignment='center', verticalalignment='center', rotation=270,
            transform=ax.transAxes)
    ax = g.axes[3]
    ax.text(1.1, 0.5, 'Climate Change', horizontalalignment='center', verticalalignment='center', rotation=270,
            transform=ax.transAxes)
    # Legend
    ax = g.axes[2]
    plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, ncol=4)  # fontsize=16,

    # Save
    savename = figure_name_ + '.png'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight")
    plt.close()

    # Return plot
    return g


# ======================================================================================================================


# Note: Need to resample results before plotting
# folders = ['2019_10_23', '2019_10_24']
folders = ['2019_10_25']

col_order1 = ['Historical-Current-No Tax', 'Historical-Hardened-No Tax', 'Climate Change-Current-No Tax',
              'Climate Change-Hardened-No Tax']
col_order2 = ['Historical-Current-Tax', 'Historical-Hardened-Tax', 'Climate Change-Current-Tax',
              'Climate Change-Hardened-Tax']

plotCosts = True
plotEmissions = True
plotActivityFuel = False
plotActivityTech = False

# Naming conventions
filename_costs_yearly = "costs_yearly_toPlot.csv"
filename_emissions_yearly = "emissions_yearly_toPlot.csv"
# Iterate through model runs
for folder in folders:

    # Move to results directory
    cwd = os.getcwd()
    path = os.getcwd() + '\\results\\' + folder
    os.chdir(path)

    # =================================================
    # Costs
    # =================================================
    if plotCosts:
        # Load and Process data
        df = pd.read_csv(filename_costs_yearly, index_col=0)

        # Set variables and labels
        x_var = 'Year'
        x_label = "Year (-)"
        y_var = 'Value'
        y_label = "Cost of Electricity\n($/kWh)"


        # Linear limits
        if folder == '2019_10_23':
            ylims = [0,5]
        elif folder =='2019_10_24':
            ylims = [0,100]
        elif folder == '2019_10_25':
            ylims = [0, 2.5]
        else:
            ylims=[]

        # ------------------
        # Violin - linear
        #------------------

        # Violin Plot - Without Tax
        figure_name = "costs_yearly_noTax_violin"
        col_order = col_order1
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear', ylims=ylims)

        # Violin Plot - With Tax
        figure_name = "costs_yearly_tax_violin"
        col_order = col_order2
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear', ylims=ylims)

        # # Log limits
        # if folder == '2019_10_23':
        #     ylims = [0.1, 10]
        # elif folder == '2019_10_24':
        #     ylims = [0.01, 100]
        # else:
        #     ylims = []

        # # ------------------
        # # Violin - log
        # # ------------------
        #
        # # Violin Plot - Without Tax
        # figure_name = "costs_yearly_noTax_violin_log"
        # col_order = col_order1
        # g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='log', ylims=ylims)
        #
        # # Violin Plot - With Tax
        # figure_name = "costs_yearly_tax_violin_log"
        # col_order = col_order2
        # g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='log', ylims=ylims)
        #
        # # ------------------
        # # Box - log
        # # ------------------
        #
        # # Violin Plot - Without Tax
        # figure_name = "costs_yearly_noTax_box"
        # col_order = col_order1
        # g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='box', y_scale='linear', ylims=ylims)
        #
        # # Violin Plot - With Tax
        # figure_name = "costs_yearly_tax_box"
        # col_order = col_order2
        # g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='box', y_scale='linear', ylims=ylims)

    # =================================================
    # Emissions
    figure_name = "emissions_yearly"
    # =================================================
    if plotEmissions:
        # Load and Process data
        df = pd.read_csv(filename_emissions_yearly, index_col=0)

        # Set variables and labels
        x_var = 'Year'
        x_label = "Year (-)"
        y_var = 'Value'
        y_label = "Emissions\n(Mton/yr)"

        ylims = [0,15]

        # ------------------
        # Violin - linear
        #------------------

        # Violin Plot - Without Tax
        figure_name = "emissions_yearly_noTax_violin"
        col_order = col_order1
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear', ylims=ylims)

        # Violin Plot - With Tax
        figure_name = "emissions_yearly_tax_violin"
        col_order = col_order2
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear', ylims=ylims)

        # # ------------------
        # # Box - linear
        # #------------------
        #
        # # Box Plot - Without Tax
        # figure_name = "emissions_yearly_noTax_box"
        # col_order = col_order1
        # g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='box', y_scale='linear', ylims=ylims)
        #
        # # Box Plot - With Tax
        # figure_name = "emissions_yearly_tax_box"
        # col_order = col_order2
        # g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='box', y_scale='linear', ylims=ylims)

    # Return to original directory
    os.chdir(cwd)
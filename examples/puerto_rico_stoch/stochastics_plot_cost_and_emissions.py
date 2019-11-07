import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot(df_, col_order_, x_var_, x_label_, y_var_, y_label_, figure_name_, plot_type='violin', y_scale='linear',
         ylims=[]):
    # Set style and context using seaborn
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("paper")

    custom_palette = [(0.0, 0.0, 0.0), (0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                      (0.847, 0.000, 0.067)]  # Custom palette

    resolution = 1000

    # Column width guidelines https://www.elsevier.com/authors/author-schemas/artwork-and-media-instructions/artwork-sizing
    # Single column: 90mm = 3.54 in
    # 1.5 column: 140 mm = 5.51 in
    # 2 column: 190 mm = 7.48 i
    width = 7.48  # inches
    height = 4.0  # inches

    order = ['Business-as-usual', 'Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas',
             'Distributed - Hybrid']

    # --------------------------
    # Plot
    # --------------------------

    if plot_type == 'violin':
        g = sns.catplot(x=x_var_, y=y_var_, data=df_, hue='Scenario', palette=custom_palette, kind="violin", col="case",
                        col_wrap=2, col_order=col_order_, inner=None, scale="area", cut=0, bw=0.5, linewidth=0.5,
                        legend=False, saturation=1.0, scale_hue=False, hue_order=order).set(yscale=y_scale)
    elif plot_type == 'box':
        g = sns.catplot(x=x_var, y=y_var, data=df, hue='Scenario', palette=custom_palette, kind="box", col="case",
                        col_wrap=2, col_order=col_order_, linewidth=0.5, legend=False, saturation=1.0).set(
            yscale=y_scale)

    if len(ylims) == 2:
        g.axes[0].set_ylim(ylims[0], ylims[1])
        g.axes[1].set_ylim(ylims[0], ylims[1])
        g.axes[2].set_ylim(ylims[0], ylims[1])
        g.axes[3].set_ylim(ylims[0], ylims[1])

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
    plt.legend(loc='center', bbox_to_anchor=(0.0, -0.4), frameon=False, ncol=3)  # fontsize=16,

    # Save
    savename = figure_name_ + '.png'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight")
    plt.close()

    # Return plot
    return g


# ======================================================================================================================


def plot_comb(df_, figure_name_):
    # Set style and context using seaborn
    sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
    sns.set_context("paper")

    custom_palette = [(0.0, 0.0, 0.0), (0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                      (0.847, 0.000, 0.067)]  # Custom palette

    resolution = 1000

    # Column width guidelines https://www.elsevier.com/authors/author-schemas/artwork-and-media-instructions/artwork-sizing
    # Single column: 90mm = 3.54 in
    # 1.5 column: 140 mm = 5.51 in
    # 2 column: 190 mm = 7.48 i
    width = 7.48  # inches
    height = 4.0  # inches

    ylims=[]

    order = ['Business-as-usual', 'Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas',
             'Distributed - Hybrid']

    # --------------------------
    # Plot
    # --------------------------

    g = sns.relplot(x='Emissions', y='Cost', data=df_, hue='Scenario', style='infra', palette=custom_palette,
                    hue_order=order, col='carbon_tax')

    # if len(ylims) == 2:
    #     g.axes[0].set_ylim(ylims[0], ylims[1])
    #     g.axes[1].set_ylim(ylims[0], ylims[1])
    # return g
    # Set size
    f = plt.gcf()
    f.set_size_inches(width, height)

    # Labels
    x_label = 'Emissions (Mton/yr)'
    y_label = 'Cost of Electricity\n ($/kWh)'
    g.set_axis_labels(x_label, y_label)

    # Remove ticks
    g.axes[0][0].tick_params(top=False, right=False)
    g.axes[0][1].tick_params(top=False, right=False, left=False)

    # Despine
    g.despine()
    sns.despine(ax=g.axes[0][0], )
    sns.despine(ax=g.axes[0][1], left=True)

    # Additional Labels
    # g.set_titles(" ")
    # ax = g.axes[0]
    # ax.text(0.5, 1.1, 'Current Infrastructure', horizontalalignment='center', verticalalignment='top',
    #         transform=ax.transAxes)
    # ax = g.axes[1]
    # ax.text(0.5, 1.1, 'Hardened Infrastructure', horizontalalignment='center', verticalalignment='top',
    #         transform=ax.transAxes)
    # ax.text(1.1, 0.5, 'Historical', horizontalalignment='center', verticalalignment='center', rotation=270,
    #         transform=ax.transAxes)
    # ax = g.axes[3]
    # ax.text(1.1, 0.5, 'Climate Change', horizontalalignment='center', verticalalignment='center', rotation=270,
    #         transform=ax.transAxes)
    # Legend
    # ax = g.axes[2]
    # plt.legend(loc='center', bbox_to_anchor=(0.0, -0.4), frameon=False, ncol=3)  # fontsize=16,

    # Save
    savename = figure_name_ + '.png'
    plt.savefig(savename, dpi=resolution, bbox_inches="tight")
    plt.close()

    # Return plot
    return g


# ======================================================================================================================

folders = ['2019_11_07_full']

col_order1 = ['Historical-Current-No Tax', 'Historical-Hardened-No Tax', 'Climate Change-Current-No Tax',
              'Climate Change-Hardened-No Tax']
col_order2 = ['Historical-Current-Tax', 'Historical-Hardened-Tax', 'Climate Change-Current-Tax',
              'Climate Change-Hardened-Tax']

plotCosts = True
plotEmissions = True
plotComb = True

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
            ylims = [0, 5]
        elif folder == '2019_10_24':
            ylims = [0, 100]
        elif folder == '2019_10_25':
            ylims = [0, 2.5]
        else:
            ylims = []

        # ------------------
        # Violin - linear
        # ------------------

        # Violin Plot - Without Tax
        figure_name = "costs_yearly_noTax_violin"
        col_order = col_order1
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear',
                 ylims=ylims)

        # Violin Plot - With Tax
        figure_name = "costs_yearly_tax_violin"
        col_order = col_order2
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear',
                 ylims=ylims)

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

        ylims = [0, 15]

        # ------------------
        # Violin - linear
        # ------------------

        # Violin Plot - Without Tax
        figure_name = "emissions_yearly_noTax_violin"
        col_order = col_order1
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear',
                 ylims=ylims)

        # Violin Plot - With Tax
        figure_name = "emissions_yearly_tax_violin"
        col_order = col_order2
        g = plot(df, col_order, x_var, x_label, y_var, y_label, figure_name, plot_type='violin', y_scale='linear',
                 ylims=ylims)

    # =================================================
    # Emissions
    figure_name = "combined_"
    # =================================================
    if plotComb:
        # Load and Process data
        df_c = pd.read_csv(filename_costs_yearly, index_col=0)
        df_e = pd.read_csv(filename_emissions_yearly, index_col=0)

        # Remove duplicates
        df_c = df_c.drop_duplicates()
        df_e = df_e.drop_duplicates()

        df_c.loc[:, 'Cost'] = df_c.Value
        df_e.loc[:, 'Emissions'] = df_e.Value
        df_c = df_c.drop(columns='Value')
        df_e = df_e.drop(columns='Value')

        # # Only analyze last year
        year = df_c.Year.unique().max()
        df_c2 = df_c[df_c.Year == year]
        df_e2 = df_e[df_c.Year == year]

        # # Merge data together
        df = pd.merge(left=df_c2, right=df_e2)
        df.to_csv('cost_emissions_comb.csv')

        # Plot
        figure_name = 'cost_and_emissions_combined'
        g = plot_comb(df, figure_name)

    # Return to original directory
    os.chdir(cwd)

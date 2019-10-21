import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Note: Need to resample results before plotting

folders = ['2019_10_21']

dbs = ["WA_0.sqlite", "WA_1.sqlite", "WB_0.sqlite", "WB_1.sqlite", "WC_0.sqlite", "WC_1.sqlite", "WD_0.sqlite", "WD_1.sqlite",
       "XA_0.sqlite", "XA_1.sqlite", "XB_0.sqlite", "XB_1.sqlite", "XC_0.sqlite", "XC_1.sqlite", "XD_0.sqlite", "XD_1.sqlite",
       "YA_0.sqlite", "YA_1.sqlite", "YB_0.sqlite", "YB_1.sqlite", "YC_0.sqlite", "YC_1.sqlite", "YD_0.sqlite", "YD_1.sqlite",
       "ZA_0.sqlite", "ZA_1.sqlite", "ZB_0.sqlite", "ZB_1.sqlite", "ZC_0.sqlite", "ZC_1.sqlite", "ZD_0.sqlite", "ZD_1.sqlite"]

# Technology Groups
tech_group = ['Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas', 'Distributed - Hybrid']
tech_group_dict = {"WA_0.sqlite":tech_group[0], "WA_1.sqlite":tech_group[0], "WB_0.sqlite":tech_group[1], "WB_1.sqlite":tech_group[1], "WC_0.sqlite":tech_group[2], "WC_1.sqlite":tech_group[2], "WD_0.sqlite":tech_group[3], "WD_1.sqlite":tech_group[3],
       "XA_0.sqlite":tech_group[0], "XA_1.sqlite":tech_group[0], "XB_0.sqlite":tech_group[1], "XB_1.sqlite":tech_group[1], "XC_0.sqlite":tech_group[2], "XC_1.sqlite":tech_group[2], "XD_0.sqlite":tech_group[3], "XD_1.sqlite":tech_group[3],
       "YA_0.sqlite":tech_group[0], "YA_1.sqlite":tech_group[0], "YB_0.sqlite":tech_group[1], "YB_1.sqlite":tech_group[1], "YC_0.sqlite":tech_group[2], "YC_1.sqlite":tech_group[2], "YD_0.sqlite":tech_group[3], "YD_1.sqlite":tech_group[3],
       "ZA_0.sqlite":tech_group[0], "ZA_1.sqlite":tech_group[0], "ZB_0.sqlite":tech_group[1], "ZB_1.sqlite":tech_group[1], "ZC_0.sqlite":tech_group[2], "ZC_1.sqlite":tech_group[2], "ZD_0.sqlite":tech_group[3], "ZD_1.sqlite":tech_group[3]}

# Historical or Climate Change Probabilities
prob = ["Historical","Climate Change"]
prob_type_dict = {"WA_0.sqlite":prob[0], "WA_1.sqlite":prob[1], "WB_0.sqlite":prob[0], "WB_1.sqlite":prob[1], "WC_0.sqlite":prob[0], "WC_1.sqlite":prob[1], "WD_0.sqlite":prob[0], "WD_1.sqlite":prob[1],
       "XA_0.sqlite":prob[0], "XA_1.sqlite":prob[1], "XB_0.sqlite":prob[0], "XB_1.sqlite":prob[1], "XC_0.sqlite":prob[0], "XC_1.sqlite":prob[1], "XD_0.sqlite":prob[0], "XD_1.sqlite":prob[1],
       "YA_0.sqlite":prob[0], "YA_1.sqlite":prob[1], "YB_0.sqlite":prob[0], "YB_1.sqlite":prob[1], "YC_0.sqlite":prob[0], "YC_1.sqlite":prob[1], "YD_0.sqlite":prob[0], "YD_1.sqlite":prob[1],
       "ZA_0.sqlite":prob[0], "ZA_1.sqlite":prob[1], "ZB_0.sqlite":prob[0], "ZB_1.sqlite":prob[1], "ZC_0.sqlite":prob[0], "ZC_1.sqlite":prob[1], "ZD_0.sqlite":prob[0], "ZD_1.sqlite":prob[1]}

# Infrastructure Type
infra = ["Current","Hardened"]
infra_dict = {"WA_0.sqlite":infra[0], "WA_1.sqlite":infra[0], "WB_0.sqlite":infra[0], "WB_1.sqlite":infra[0], "WC_0.sqlite":infra[0], "WC_1.sqlite":infra[0], "WD_0.sqlite":infra[0], "WD_1.sqlite":infra[0],
       "XA_0.sqlite":infra[1], "XA_1.sqlite":infra[1], "XB_0.sqlite":infra[1], "XB_1.sqlite":infra[1], "XC_0.sqlite":infra[1], "XC_1.sqlite":infra[1], "XD_0.sqlite":infra[1], "XD_1.sqlite":infra[1],
       "YA_0.sqlite":infra[0], "YA_1.sqlite":infra[0], "YB_0.sqlite":infra[0], "YB_1.sqlite":infra[0], "YC_0.sqlite":infra[0], "YC_1.sqlite":infra[0], "YD_0.sqlite":infra[0], "YD_1.sqlite":infra[0],
       "ZA_0.sqlite":infra[1], "ZA_1.sqlite":infra[1], "ZB_0.sqlite":infra[1], "ZB_1.sqlite":infra[1], "ZC_0.sqlite":infra[1], "ZC_1.sqlite":infra[1], "ZD_0.sqlite":infra[1], "ZD_1.sqlite":infra[1]}

# Carbon Tax
carbon_tax = ["No", "Yes"]
carbon_tax_dict = {"WA_0.sqlite":carbon_tax[0], "WA_1.sqlite":carbon_tax[0], "WB_0.sqlite":carbon_tax[0], "WB_1.sqlite":carbon_tax[0], "WC_0.sqlite":carbon_tax[0], "WC_1.sqlite":carbon_tax[0], "WD_0.sqlite":carbon_tax[0], "WD_1.sqlite":carbon_tax[0],
       "XA_0.sqlite":carbon_tax[0], "XA_1.sqlite":carbon_tax[0], "XB_0.sqlite":carbon_tax[0], "XB_1.sqlite":carbon_tax[0], "XC_0.sqlite":carbon_tax[0], "XC_1.sqlite":carbon_tax[0], "XD_0.sqlite":carbon_tax[0], "XD_1.sqlite":carbon_tax[0],
       "YA_0.sqlite":carbon_tax[1], "YA_1.sqlite":carbon_tax[1], "YB_0.sqlite":carbon_tax[1], "YB_1.sqlite":carbon_tax[1], "YC_0.sqlite":carbon_tax[1], "YC_1.sqlite":carbon_tax[1], "YD_0.sqlite":carbon_tax[1], "YD_1.sqlite":carbon_tax[1],
       "ZA_0.sqlite":carbon_tax[1], "ZA_1.sqlite":carbon_tax[1], "ZB_0.sqlite":carbon_tax[1], "ZB_1.sqlite":carbon_tax[1], "ZC_0.sqlite":carbon_tax[1], "ZC_1.sqlite":carbon_tax[1], "ZD_0.sqlite":carbon_tax[1], "ZD_1.sqlite":carbon_tax[1]}

# col_order = [ "Historical + Worst Curves", "Historical + Best Curves",
#               "Climate Change + Worst Curves", "Climate Change + Best Curves",]

aspect = 1.5

plotCosts = True
plotEmissions = False
plotActivityFuel = False
plotActivityTech = False

# Naming conventions
filename_costs_yearly = "costs_yearly_exp_resampled.csv"
filename_emissions_yearly = "emissions_yearly_exp_resampled.csv"
filename_activity_by_fuel = "activity_by_fuel_exp_resampled.csv"
filename_activity_by_tech = "activity_by_tech_exp_resampled.csv"

# Iterate through model runs
for folder in folders:

    # Move to results directory
    cwd = os.getcwd()
    path = os.getcwd() + '\\results\\' + folder
    os.chdir(path)
    # -----------------------------------------------------
    # Aesthetics (style + context)
    # https://seaborn.pydata.org/tutorial/aesthetics.html
    # -----------------------------------------------------
    resolution = 600  # Resolution (DPI - dots per inch)
    style = 'white'  # options: "white", "whitegrid", "dark", "darkgrid", "ticks"
    context = 'talk'  # options "paper", "notebook", "talk", "poster" (smallest -> largest)
    custom_palette = [(0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361), (0.847, 0.000, 0.067),
                      (0.0, 0.0, 0.0)]  # Custom palette

    # =================================================
    # Costs
    figure_name = "costs_yearly"
    # =================================================
    if plotCosts:
        # Load and Process data
        df = pd.read_csv(filename_costs_yearly, index_col=0)
        df = df.drop("prob", axis=1)
        for col in df.columns:
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)
        df2 = pd.melt(df, id_vars=["database", "scenario"], var_name="Year", value_name="Value")
        df2.case = "unknown"
        for db in dbs:
            ind = df2.loc[:, "database"] == db
            df2.loc[ind, "database"] = scenario_dict[db]
            df2.loc[ind, "case"] = case_dict[db]
        df2 = df2.rename(columns={"scenario": "s", "database": "Scenario"})

        # Set style and context using seaborn
        sns.set_style(style)
        sns.set_context(context)

        x_label = "Year (-)"
        y_label = "Cost of Electricity (cents/kWh)"

        # --------------------------
        # Violin Plot
        # --------------------------
        # f = plt.figure(figsize=fig_size)
        g = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                        col="case", col_wrap=2, col_order=col_order, inner=None, scale="area", cut=0, linewidth=1.0,
                        legend=False, aspect=aspect, saturation=1.0)  # , scale_hue=False)
        g.set_axis_labels(x_label, y_label)
        g.set(yscale="log")

        # plt.ylim(0, 200)
        # sns.plt.xlim(0, None)

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
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)

        # Save
        savename = figure_name + "_violin_log_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

        # --------------------------
        # Violin Plot
        # --------------------------
        # f = plt.figure(figsize=fig_size)
        g = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                        col="case", col_wrap=2, col_order=col_order, inner=None, scale="area", cut=0, linewidth=1.0, legend=False, aspect=aspect, saturation=1.0)  # , scale_hue=False)
        g.set_axis_labels(x_label, y_label)

        plt.ylim(0, 200)
        # sns.plt.xlim(0, None)

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
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)

        # Save
        savename = figure_name + "_violin200_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

        # --------------------------
        # Violin Plot
        # --------------------------
        # f = plt.figure(figsize=fig_size)
        g = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                        col="case", col_wrap=2, col_order=col_order, inner=None, scale="area", cut=0, linewidth=1.0, legend=False, aspect=aspect, saturation=1.0)  # , scale_hue=False)
        g.set_axis_labels(x_label, y_label)

        plt.ylim(0, 500)
        # sns.plt.xlim(0, None)

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
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)

        # Save
        savename = figure_name + "_violin500_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()


        # --------------------------
        # Violin Plot
        # --------------------------
        # f = plt.figure(figsize=fig_size)
        g = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                        col="case", col_wrap=2, col_order=col_order, inner=None, scale="area", cut=0, linewidth=1.0, legend=False, aspect=aspect, saturation=1.0)  # , scale_hue=False)
        g.set_axis_labels(x_label, y_label)

        plt.ylim(0, 1000)
        # sns.plt.xlim(0, None)

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
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)

        # Save
        savename = figure_name + "_violin1000_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

    # =================================================
    # Emissions
    figure_name = "emissions_yearly"
    # =================================================
    if plotEmissions:
        # Load and Process data
        df = pd.read_csv(filename_emissions_yearly, index_col=0)
        df = df.drop("prob", axis=1)
        for col in df.columns:
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)
        df2 = pd.melt(df, id_vars=["database", "scenario"], var_name="Year", value_name="Value")
        df2.case = "unknown"
        for db in dbs:
            ind = df2.loc[:, "database"] == db
            df2.loc[ind, "database"] = scenario_dict[db]
            df2.loc[ind, "case"] = case_dict[db]
        df2 = df2.rename(columns={"scenario": "s", "database": "Scenario"})

        # Set style and context using seaborn
        sns.set_style(style)
        sns.set_context(context)

        x_label = "Year (-)"
        y_label = "Emissions (kton/yr)"

        # --------------------------
        # Violin Plot
        # --------------------------
        f = plt.figure(figsize=[8,6])
        g = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                        col="case", col_wrap=2, col_order=col_order, inner=None, cut=0, linewidth=1.0, legend=False, scale="width", aspect=aspect, saturation=1.0)
        g.set_axis_labels(x_label, y_label)

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
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)

        # Save
        savename = figure_name + "_violin_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

    # =====================================================
    # Activity by Fuel
    figure_name = "activity_by_fuel"
    # =====================================================
    if plotActivityFuel:
        fuel_short = ["BIO", "COAL", "DSL", "ELC_CENTRAL", "ELC_DIST", "HYDRO", "MSW_LF", "NATGAS", "OIL", "SOLAR",
                      "WIND"]
        fuel_long = ["Biomass", "Coal", "Diesel", "Battery", "Battery", "Hydro", "Landfill Gas", "Natural Gas", "Oil",
                     "Solar", "Wind"]

        # Load and Process data
        df = pd.read_csv(filename_activity_by_fuel, index_col=0)
        df = df.drop("prob", axis=1)
        for col in df.columns:
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)
        df2 = pd.melt(df, id_vars=["database", "scenario", "fuelOrTech"], var_name="Year", value_name="Value")
        df2.case = "unknown"
        for db in dbs:
            ind = df2.loc[:, "database"] == db
            df2.loc[ind, "database"] = scenario_dict[db]
            df2.loc[ind, "case"] = case_dict[db]
        for short, long in zip(fuel_short, fuel_long):
            ind = df2.loc[:, "fuelOrTech"] == short
            df2.loc[ind, "fuelOrTech"] = long
        df2 = df2.rename(columns={"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"})

        for col in df.columns:
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)

        # Set style and context using seaborn
        sns.set_style(style)
        sns.set_context(context)

        col_order = ["Coal", "Oil", "Diesel", "Natural Gas", "Hydro", "Solar", "Wind", "Battery", "Landfill Gas",
                     "Biomass"]

        # Box Plot
        g = sns.catplot(x="Year", y="Value", hue="Scenario", row="case", col="Type", data=df2, kind="box",
                        col_order=col_order, palette=custom_palette)  # ,height=4, aspect=.7)
        savename = figure_name + "_box_" + context + '.pdf'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

        # Violin Plot
        g = sns.catplot(x="Year", y="Value", hue="Scenario", row="case", col="Type", data=df2, kind="violin",
                        col_order=col_order, palette=custom_palette)  # ,height=4, aspect=.7)
        savename = figure_name + "_violin_" + context + '.pdf'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

    # =====================================================
    # Activity by Tech
    figure_name = "activity_by_tech"
    # =====================================================
    if plotActivityTech:

        tech_short = ['EX_DSL_CC', 'DIST', 'SUB', 'EC_BATT', 'EX_SOLPV', 'ED_BATT', 'EX_COAL', 'EX_HYDRO', 'EX_MSW_LF',
                      'TRANS', 'ED_NG_OC', 'LOCAL', 'EX_DSL_SIMP', 'ED_NG_CC', 'EC_NG_CC', 'EX_OIL_TYPE3',
                      'EX_OIL_TYPE2', 'EC_WIND', 'EC_SOLPV', 'UGND_TRANS', 'EX_WIND', 'EX_NG_CC', 'EC_NG_OC', 'ED_WIND',
                      'UGND_DIST', 'EX_OIL_TYPE1', 'EC_BIO', 'ED_BIO', 'ED_SOLPV']

        cent_fsl = "Centralized Fossil"
        cent_renew = "Centralized Renewable"
        dist_fsl = "Distributed Fossil"
        dist_renew = "Distributed Renewable"

        tech_long = [cent_fsl, 'DIST', 'SUB', 'storage', cent_renew, 'storage', cent_fsl, cent_renew, cent_renew,
                     'TRANS', dist_fsl, 'LOCAL', cent_fsl, dist_fsl, cent_fsl, cent_fsl, cent_fsl, cent_renew,
                     cent_renew, 'UGND_TRANS', cent_renew, cent_fsl, cent_fsl, dist_renew, 'UGND_DIST', cent_fsl,
                     cent_renew, dist_renew, dist_renew]

        # Load and Process data
        df = pd.read_csv(filename_activity_by_tech, index_col=0)
        df = df.drop("prob", axis=1)
        for col in df.columns:
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)
        df2 = pd.melt(df, id_vars=["database", "scenario", "fuelOrTech"], var_name="Year", value_name="Value")
        df2.case = "unknown"
        for db in dbs:
            ind = df2.loc[:, "database"] == db
            df2.loc[ind, "database"] = scenario_dict[db]
            df2.loc[ind, "case"] = case_dict[db]
        for short, long in zip(tech_short, tech_long):
            ind = df2.loc[:, "fuelOrTech"] == short
            df2.loc[ind, "fuelOrTech"] = long
        df2 = df2.rename(columns={"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"})

        for col in df.columns:
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)

        # Set style and context using seaborn
        sns.set_style(style)
        sns.set_context(context)

        # --------------------------------------------------
        # Box Plot - Group 1
        # --------------------------------------------------
        # f = plt.figure(figsize=fig_size)
        col_order = [cent_renew, dist_renew]
        row_order = ["Historical + Worst Curves", "Climate Change + Worst Curves", ]
        g = sns.catplot(x="Year", y="Value", hue="Scenario", row="Type", col="case", data=df2, kind="violin",
                        col_order=col_order, row_order = row_order,palette=custom_palette, legend=False, inner=None,aspect=aspect)
        # Additional Labels
        g.set_titles(" ")
        ax = g.axes[0][0]
        ax.text(0.5, 1.1, 'Underground Transmission', horizontalalignment='center', verticalalignment='top',
                transform=ax.transAxes)
        ax = g.axes[0][1]
        ax.text(0.5, 1.1, 'Underground Distribution', horizontalalignment='center', verticalalignment='top',
                transform=ax.transAxes)
        ax.text(1.1, 0.5, 'Current Infra. + Historical', horizontalalignment='center', verticalalignment='center', rotation=270,
                transform=ax.transAxes)
        ax = g.axes[1][1]
        ax.text(1.1, 0.5, 'Current Infra. + Climate Change', horizontalalignment='center', verticalalignment='center', rotation=270,
                transform=ax.transAxes)
        # Legend
        ax = g.axes[1][0]
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)
        # Save
        savename = figure_name + "group1_violin_" + context + '.pdf'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

        # --------------------------------------------------
        # Box Plot - Group 2
        #--------------------------------------------------
        # col_order = ['TRANS', 'UGND_TRANS', 'DIST', 'UGND_DIST']
        col_order = ['UGND_TRANS', 'UGND_DIST']
        row_order = ["Historical + Worst Curves",  "Climate Change + Worst Curves",]
        g = sns.catplot(x="Year", y="Value", hue="Scenario", row="Type", col="case", data=df2, kind="violin",
                        col_order=col_order, row_order = row_order,palette=custom_palette, legend=False, inner=None,aspect=aspect)  # ,height=4, aspect=.7)

        # Additional Labels
        g.set_titles(" ")
        ax = g.axes[0][0]
        ax.text(0.5, 1.1, 'Underground Transmission', horizontalalignment='center', verticalalignment='top',
                transform=ax.transAxes)
        ax = g.axes[0][1]
        ax.text(0.5, 1.1, 'Underground Distribution', horizontalalignment='center', verticalalignment='top',
                transform=ax.transAxes)
        ax.text(1.1, 0.5, 'Current Infra. + Historical', horizontalalignment='center', verticalalignment='center', rotation=270,
                transform=ax.transAxes)
        ax = g.axes[1][1]
        ax.text(1.1, 0.5, 'Current Infra. + Climate Change', horizontalalignment='center', verticalalignment='center', rotation=270,
                transform=ax.transAxes)
        # Legend
        ax = g.axes[1][0]
        plt.legend(loc='center', bbox_to_anchor=(0.0, -0.3), frameon=False, fontsize=16, ncol=4)
        # Save
        savename = figure_name + "group2_violin_" + context + '.pdf'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

    # =================================================
    # Return to original directory
    os.chdir(cwd)

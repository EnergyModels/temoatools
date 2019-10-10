import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Note: Need to resample results before plotting

folders = ['2019_10_08']

dbs = ["A_0.sqlite", "A_1.sqlite", "A_2.sqlite", "A_3.sqlite", "B_0.sqlite", "B_1.sqlite", "B_2.sqlite", "B_3.sqlite",
       "C_0.sqlite", "C_1.sqlite", "C_2.sqlite", "C_3.sqlite", "D_0.sqlite", "D_1.sqlite", "D_2.sqlite", "D_3.sqlite"]

scenarios = ['Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas', 'Distributed - Hybrid']
scenario_dict = {"A.sqlite": scenarios[0], "A_0.sqlite": scenarios[0], "A_1.sqlite": scenarios[0],
                 "A_2.sqlite": scenarios[0], "A_3.sqlite": scenarios[0], "B.sqlite": scenarios[1],
                 "B_0.sqlite": scenarios[1], "B_1.sqlite": scenarios[1], "B_2.sqlite": scenarios[1],
                 "B_3.sqlite": scenarios[1], "C.sqlite": scenarios[2], "C_0.sqlite": scenarios[2],
                 "C_1.sqlite": scenarios[2], "C_2.sqlite": scenarios[2], "C_3.sqlite": scenarios[2],
                 "D.sqlite": scenarios[3], "D_0.sqlite": scenarios[3], "D_1.sqlite": scenarios[3],
                 "D_2.sqlite": scenarios[3], "D_3.sqlite": scenarios[3]}

case_names = ["Historical + Best Curves", "Historical + Worst Curves", "Climate Change + Best Curves",
              "Climate Change + Worst Curves"]
case_dict = {"A.sqlite": "n/a", "A_0.sqlite": case_names[0], "A_1.sqlite": case_names[1], "A_2.sqlite": case_names[2],
             "A_3.sqlite": case_names[3], "B.sqlite": "n/a", "B_0.sqlite": case_names[0], "B_1.sqlite": case_names[1],
             "B_2.sqlite": case_names[2], "B_3.sqlite": case_names[3], "C.sqlite": "n/a", "C_0.sqlite": case_names[0],
             "C_1.sqlite": case_names[1], "C_2.sqlite": case_names[2], "C_3.sqlite": case_names[3], "D.sqlite": "n/a",
             "D_0.sqlite": case_names[0], "D_1.sqlite": case_names[1], "D_2.sqlite": case_names[2],
             "D_3.sqlite": case_names[3], "s": "Baseline"}

plotCosts = False
plotEmissions = False
plotActivityFuel = False
plotActivityTech = True

# Naming conventions
filename_costs_yearly = "costs_yearly_resampled.csv"
filename_emissions_yearly = "emissions_yearly_resampled.csv"
filename_activity_by_fuel = "activity_by_fuel_resampled.csv"
filename_activity_by_tech = "activity_by_tech_resampled.csv"

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
    context = 'paper'  # options "paper", "notebook", "talk", "poster" (smallest -> largest)
    custom_palette = [(0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361), (0.847, 0.000, 0.067),
                      (0.0, 0.0, 0.0)]  # Custom palette

    # =====================================================
    # Set figure parameters based on experience for each context
    # =====================================================
    if context == 'paper':
        fig_size = [8, 6]  # (width followed by height, in inches) Note: OK to leave as an empty list
        leg_coord = [1.6, -0.3]  # Legend coordinates (x,y)
        hspace = 0.15  # vertical space between figures
        wspace = 0.15  # horizontal space between figures
    elif context == 'notebook':
        fig_size = [8, 6]
        leg_coord = [1.75, -0.3]
        hspace = 0.2
        wspace = 0.2
    elif context == 'talk':
        fig_size = [12, 8]
        leg_coord = [1.75, -0.4]
        hspace = 0.3
        wspace = 0.35
    else:  # context == 'poster':
        fig_size = [12, 8]
        leg_coord = [1.8, -0.5]
        hspace = 0.3
        wspace = 0.35

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

        # Box and Whisker Plot
        # f = plt.figure(figsize=fig_size)
        ax = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="box", col="case",
                         col_wrap=2)
        ax.set_axis_labels(x_label, y_label)
        ax.set(yscale="log")
        savename = figure_name + "_box_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")  # bbox_inches="tight" is used to include the legend
        plt.close()

        # Violin Plot
        # f = plt.figure(figsize=fig_size)
        ax = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                         col="case", col_wrap=2)
        ax.set_axis_labels(x_label, y_label)
        ax.set(yscale="log")
        savename = figure_name + "_violin_" + context + '.pdf'
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

        # Box and Whisker Plot
        # f = plt.figure(figsize=fig_size)
        ax = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="box", col="case",
                         col_wrap=2)
        ax.set_axis_labels(x_label, y_label)
        savename = figure_name + "_box_" + context + '.png'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

        # Violin Plot
        # f = plt.figure(figsize=fig_size)
        ax = sns.catplot(x="Year", y="Value", data=df2, hue='Scenario', palette=custom_palette, kind="violin",
                         col="case", col_wrap=2)
        ax.set_axis_labels(x_label, y_label)
        savename = figure_name + "_violin_" + context + '.pdf'
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
        cent_renew= "Centralized Renewable"
        dist_fsl= "Distributed Fossil"
        dist_renew= "Distributed Renewable"

        tech_long = [cent_fsl, 'DIST', 'SUB', 'storage', cent_renew, 'storage', cent_fsl, cent_renew, cent_renew,
                     'TRANS', dist_fsl, 'LOCAL', cent_fsl, dist_fsl, cent_fsl, cent_fsl,
                     cent_fsl, cent_renew, cent_renew, 'UGND_TRANS', cent_renew, cent_fsl, cent_fsl, dist_renew,
                     'UGND_DIST', cent_fsl, cent_renew, dist_renew, dist_renew]

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



        # Box Plot - Group 1
        col_order = [cent_fsl, cent_renew, dist_fsl, dist_renew]
        g = sns.catplot(x="Year", y="Value", hue="Scenario", row="case", col="Type", data=df2, kind="box",
                       palette=custom_palette)  # ,height=4, aspect=.7)
        savename = figure_name + "group1_box_" + context + '.pdf'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

        # Box Plot - Group 2
        col_order = ['TRANS','UGND_TRANS','DIST','UGND_DIST']
        g = sns.catplot(x="Year", y="Value", hue="Scenario", row="case", col="Type", data=df2, kind="box",
                        palette=custom_palette)  # ,height=4, aspect=.7)
        savename = figure_name + "group2_box_" + context + '.pdf'
        plt.savefig(savename, dpi=resolution, bbox_inches="tight")
        plt.close()

    # =================================================
    # Return to original directory
    os.chdir(cwd)

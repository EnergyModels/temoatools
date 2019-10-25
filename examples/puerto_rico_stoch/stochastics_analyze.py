import os
import pandas as pd
import temoatools as tt
import multiprocessing
from joblib import Parallel, delayed, parallel_backend


# =======================================================
# Function to evaluate simulations by a single metric
# =======================================================

def analyze_results(metric, folder, run_name, dbs, all_dbs, db_shift, node_prob, tech_group_dict, prob_type_dict,
                    infra_dict, carbon_tax_dict):
    # --------------------------------
    # Analyze with temoatools
    # --------------------------------

    create_plots = 'N'  # Create default plots
    save_data = 'Y'  # Do not save data as a csv or xls
    sector_name = 'electric'  # Name of sector to be analyzed

    # Costs
    if metric == 'costs_yearly':
        yearlyCosts, LCOE = tt.getCosts(folder, dbs, save_data=save_data, create_plots=create_plots, run_name=run_name)

    # Emissions
    elif metric == 'emissions_yearly':
        yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs, save_data=save_data, create_plots=create_plots,
                                                        run_name=run_name)
    # Analyze activity by fuel types
    elif metric == 'activity_by_fuel':
        switch = 'fuel'
        ActivityByYearFuel = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                                            create_plots=create_plots, run_name=run_name)

    # Analyze activity by fuel types
    elif metric == 'activity_by_tech':
        switch = 'tech'
        sector_name = 'all'
        ActivityByYearTech = tt.getActivity(folder, dbs, switch=switch, sector_name=sector_name, save_data=save_data,
                                            create_plots=create_plots, run_name=run_name)

    # --------------------------------
    # Move to results directory
    # --------------------------------
    cwd = os.getcwd()
    path = os.getcwd() + '\\results\\' + folder
    os.chdir(path)

    # --------------------------------
    # Expand Results (only costs and emissions)
    # --------------------------------

    if metric == 'costs_yearly' or metric == 'emissions_yearly':

        if metric == 'costs_yearly':
            filename = 'costs_yearly'
        elif metric == 'emissions_yearly':
            filename = 'emissions_yearly'

        tt.stoch_expand(path, filename, db_shift)

    # --------------------------------
    # Resample Results (only costs and emissions)
    # --------------------------------
    if metric == 'costs_yearly' or metric == 'emissions_yearly':

        if metric == 'costs_yearly':
            filename = 'costs_yearly_exp'
        elif metric == 'emissions_yearly':
            filename = 'emissions_yearly_exp'

        tt.stoch_resample(path, filename, node_prob)

    # --------------------------------
    # Prepare for plotting
    # --------------------------------

    # Naming conventions and conversions
    if metric == 'costs_yearly':
        filename = "costs_yearly_exp_resampled.csv"
        conversion = 1.0 / 100.0  # Convert from cents/kWh to $/kWh/yr
        id_vars = ["database", "scenario"]
        col_renames = {"scenario": "s", "database": "Scenario"}
        csv_file = "costs_yearly_toPlot.csv"

    elif metric == 'emissions_yearly':
        filename = "emissions_yearly_exp_resampled.csv"
        conversion = 1.0 / 1000.0  # Convert from kton/yr to Mton/yr
        id_vars = ["database", "scenario"]
        col_renames = {"scenario": "s", "database": "Scenario"}
        csv_file = "emissions_yearly_toPlot.csv"

    elif metric == 'activity_by_fuel':
        filename = "activity_by_fuel.csv"  # Don't expand and resample these results
        conversion = 1.0  # Do not convert
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "activity_by_fuel_toPlot.csv"

    elif metric == 'activity_by_tech':
        filename = "activity_by_tech.csv"  # Don't expand and resample these results
        conversion = 1.0  # Do not convert
        id_vars = ["database", "scenario", "fuelOrTech"]
        col_renames = {"scenario": "s", "database": "Scenario", "fuelOrTech": "Type"}
        csv_file = "activity_by_tech_toPlot.csv"

    # Load and Process data
    df = pd.read_csv(filename, index_col=0)
    df = df.drop("prob", axis=1)
    for col in df.columns:
        if 'Unnamed' in col:
            df = df.drop(col, axis=1)
    df2 = pd.melt(df, id_vars=id_vars, var_name="Year", value_name="Value")
    df2.case = "unknown"
    df2.Value = df2.Value * conversion
    for db in all_dbs:
        ind = df2.loc[:, "database"] == db
        df2.loc[ind, "case"] = prob_type_dict[db] + "-" + infra_dict[db] + "-" + carbon_tax_dict[db]
        df2.loc[ind, "database"] = tech_group_dict[db]
        df2.loc[ind, "prob_type"] = prob_type_dict[db]
        df2.loc[ind, "infra"] = infra_dict[db]
        df2.loc[ind, "carbon_tax"] = carbon_tax_dict[db]
        df2.loc[ind, "infra_and_carbon_tax"] = infra_dict[db]+"-"+carbon_tax_dict[db]
    df2 = df2.rename(columns=col_renames)

    # For activity results, change from temoa names to a more standard naming convention
    if metric == 'activity_by_fuel' or metric == 'activity_by_tech':
        if metric == 'activity_by_fuel':
            type_shorts = ["BIO", "COAL", "DSL", "ELC_CENTRAL", "ELC_DIST", "HYDRO", "MSW_LF", "NATGAS", "OIL", "SOLAR",
                          "WIND"]
            type_longs = ["Biomass", "Coal", "Diesel", "Battery", "Battery", "Hydro", "Landfill Gas", "Natural Gas",
                         "Oil",
                         "Solar", "Wind"]

        elif metric == 'activity_by_tech':
            type_shorts = ['EX_DSL_CC', 'DIST', 'SUB', 'EC_BATT', 'EX_SOLPV', 'ED_BATT', 'EX_COAL', 'EX_HYDRO',
                          'EX_MSW_LF',
                          'TRANS', 'ED_NG_OC', 'LOCAL', 'EX_DSL_SIMP', 'ED_NG_CC', 'EC_NG_CC', 'EX_OIL_TYPE3',
                          'EX_OIL_TYPE2', 'EC_WIND', 'EC_SOLPV', 'UGND_TRANS', 'EX_WIND', 'EX_NG_CC', 'EC_NG_OC',
                          'ED_WIND',
                          'UGND_DIST', 'EX_OIL_TYPE1', 'EC_BIO', 'ED_BIO', 'ED_SOLPV']

            cent_fsl = "Centralized Fossil"
            cent_renew = "Centralized Renewable"
            dist_fsl = "Distributed Fossil"
            dist_renew = "Distributed Renewable"

            type_longs = [cent_fsl, 'DIST', 'SUB', 'storage', cent_renew, 'storage', cent_fsl, cent_renew, cent_renew,
                         'TRANS', dist_fsl, 'LOCAL', cent_fsl, dist_fsl, cent_fsl, cent_fsl, cent_fsl, cent_renew,
                         cent_renew, 'UGND_TRANS', cent_renew, cent_fsl, cent_fsl, dist_renew, 'UGND_DIST', cent_fsl,
                         cent_renew, dist_renew, dist_renew]

        for type_short, type_long in zip(type_shorts, type_longs):
            ind = df2.loc[:, "Type"] == type_short
            df2.loc[ind, "Type"] = type_long

    # Save file
    df2.to_csv(csv_file)

    # --------------------------------
    # Return to original directory
    # --------------------------------
    os.chdir(cwd)


# ================================
# Main body of script
# ================================
if __name__ == '__main__':

    db_folder = os.getcwd() + '\\stochastic_databases'

    run_names = ["2019_10_25", ]

    # Names of databases simulated
    dbs = ["WA_0.sqlite", "WB_0.sqlite", "WC_0.sqlite", "WD_0.sqlite", "WE_0.sqlite",
           "XA_0.sqlite", "XB_0.sqlite", "XC_0.sqlite", "XD_0.sqlite", "XE_0.sqlite",
           "YA_0.sqlite", "YB_0.sqlite", "YC_0.sqlite", "YD_0.sqlite", "YE_0.sqlite",
           "ZA_0.sqlite", "ZB_0.sqlite", "ZC_0.sqlite", "ZD_0.sqlite", "ZE_0.sqlite"]

    # Node probabilities by case (0 is simulated, 1 is calculated)
    node_prob = {"0": [0.52, 0.32, 0.16],  # Historical (sum must equal 1)
                 "1": [0.2, 0.32, 0.48]}  # Climate Change

    # Dictionary relating simulated databases to calculated results using different distributions
    db_shift = {"WA_0": "WA_1", "WB_0": "WB_1",
                "WC_0": "WC_1", "WD_0": "WD_1", "WE_0": "WE_1",
                "XA_0": "XA_1", "XB_0": "XB_1",
                "XC_0": "XC_1", "XD_0": "XD_1", "XE_0": "XE_1",
                "YA_0": "YA_1", "YB_0": "YB_1",
                "YC_0": "YC_1", "YD_0": "YD_1", "YE_0": "YE_1",
                "ZA_0": "ZA_1", "ZB_0": "ZB_1",
                "ZC_0": "ZC_1", "ZD_0": "ZD_1", "ZE_0": "ZE_1"}

    # List of all databases after applying different distributions
    all_dbs = ["WA_0.sqlite", "WA_1.sqlite", "WB_0.sqlite", "WB_1.sqlite", "WC_0.sqlite", "WC_1.sqlite", "WD_0.sqlite",
               "WD_1.sqlite", "WE_0.sqlite", "WE_1.sqlite", "XA_0.sqlite", "XA_1.sqlite", "XB_0.sqlite", "XB_1.sqlite",
               "XC_0.sqlite", "XC_1.sqlite", "XD_0.sqlite", "XD_1.sqlite", "XE_0.sqlite", "XE_1.sqlite", "YA_0.sqlite",
               "YA_1.sqlite", "YB_0.sqlite", "YB_1.sqlite", "YC_0.sqlite", "YC_1.sqlite", "YD_0.sqlite", "YD_1.sqlite",
               "YE_0.sqlite", "YE_1.sqlite", "ZA_0.sqlite", "ZA_1.sqlite", "ZB_0.sqlite", "ZB_1.sqlite", "ZC_0.sqlite",
               "ZC_1.sqlite", "ZD_0.sqlite", "ZD_1.sqlite", "ZE_0.sqlite", "ZE_1.sqlite"]

    # Technology Groups
    tech_group = ['Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas',
                  'Distributed - Hybrid',
                  'Business-as-usual']
    tech_group_dict = {"WA_0.sqlite": tech_group[0], "WA_1.sqlite": tech_group[0], "WB_0.sqlite": tech_group[1],
                       "WB_1.sqlite": tech_group[1], "WC_0.sqlite": tech_group[2], "WC_1.sqlite": tech_group[2],
                       "WD_0.sqlite": tech_group[3], "WD_1.sqlite": tech_group[3], "WE_0.sqlite": tech_group[4],
                       "WE_1.sqlite": tech_group[4], "XA_0.sqlite": tech_group[0], "XA_1.sqlite": tech_group[0],
                       "XB_0.sqlite": tech_group[1], "XB_1.sqlite": tech_group[1], "XC_0.sqlite": tech_group[2],
                       "XC_1.sqlite": tech_group[2], "XD_0.sqlite": tech_group[3], "XD_1.sqlite": tech_group[3],
                       "XE_0.sqlite": tech_group[4], "XE_1.sqlite": tech_group[4], "YA_0.sqlite": tech_group[0],
                       "YA_1.sqlite": tech_group[0], "YB_0.sqlite": tech_group[1], "YB_1.sqlite": tech_group[1],
                       "YC_0.sqlite": tech_group[2], "YC_1.sqlite": tech_group[2], "YD_0.sqlite": tech_group[3],
                       "YD_1.sqlite": tech_group[3], "YE_0.sqlite": tech_group[4], "YE_1.sqlite": tech_group[4],
                       "ZA_0.sqlite": tech_group[0], "ZA_1.sqlite": tech_group[0], "ZB_0.sqlite": tech_group[1],
                       "ZB_1.sqlite": tech_group[1], "ZC_0.sqlite": tech_group[2], "ZC_1.sqlite": tech_group[2],
                       "ZD_0.sqlite": tech_group[3], "ZD_1.sqlite": tech_group[3], "ZE_0.sqlite": tech_group[4],
                       "ZE_1.sqlite": tech_group[4]}

    # Historical or Climate Change Probabilities
    prob = ["Historical", "Climate Change"]
    prob_type_dict = {"WA_0.sqlite": prob[0], "WA_1.sqlite": prob[1], "WB_0.sqlite": prob[0], "WB_1.sqlite": prob[1],
                      "WC_0.sqlite": prob[0], "WC_1.sqlite": prob[1], "WD_0.sqlite": prob[0], "WD_1.sqlite": prob[1],
                      "WE_0.sqlite": prob[0], "WE_1.sqlite": prob[1], "XA_0.sqlite": prob[0], "XA_1.sqlite": prob[1],
                      "XB_0.sqlite": prob[0], "XB_1.sqlite": prob[1], "XC_0.sqlite": prob[0], "XC_1.sqlite": prob[1],
                      "XD_0.sqlite": prob[0], "XD_1.sqlite": prob[1], "XE_0.sqlite": prob[0], "XE_1.sqlite": prob[1],
                      "YA_0.sqlite": prob[0], "YA_1.sqlite": prob[1], "YB_0.sqlite": prob[0], "YB_1.sqlite": prob[1],
                      "YC_0.sqlite": prob[0], "YC_1.sqlite": prob[1], "YD_0.sqlite": prob[0], "YD_1.sqlite": prob[1],
                      "YE_0.sqlite": prob[0], "YE_1.sqlite": prob[1], "ZA_0.sqlite": prob[0], "ZA_1.sqlite": prob[1],
                      "ZB_0.sqlite": prob[0], "ZB_1.sqlite": prob[1], "ZC_0.sqlite": prob[0], "ZC_1.sqlite": prob[1],
                      "ZD_0.sqlite": prob[0], "ZD_1.sqlite": prob[1], "ZE_0.sqlite": prob[0], "ZE_1.sqlite": prob[1]}

    # Infrastructure Type
    infra = ["Current", "Hardened"]
    infra_dict = {"WA_0.sqlite": infra[0], "WA_1.sqlite": infra[0], "WB_0.sqlite": infra[0], "WB_1.sqlite": infra[0],
                  "WC_0.sqlite": infra[0], "WC_1.sqlite": infra[0], "WD_0.sqlite": infra[0], "WD_1.sqlite": infra[0],
                  "WE_0.sqlite": infra[0], "WE_1.sqlite": infra[0], "XA_0.sqlite": infra[1], "XA_1.sqlite": infra[1],
                  "XB_0.sqlite": infra[1], "XB_1.sqlite": infra[1], "XC_0.sqlite": infra[1], "XC_1.sqlite": infra[1],
                  "XD_0.sqlite": infra[1], "XD_1.sqlite": infra[1], "XE_0.sqlite": infra[1], "XE_1.sqlite": infra[1],
                  "YA_0.sqlite": infra[0], "YA_1.sqlite": infra[0], "YB_0.sqlite": infra[0], "YB_1.sqlite": infra[0],
                  "YC_0.sqlite": infra[0], "YC_1.sqlite": infra[0], "YD_0.sqlite": infra[0], "YD_1.sqlite": infra[0],
                  "YE_0.sqlite": infra[0], "YE_1.sqlite": infra[0], "ZA_0.sqlite": infra[1], "ZA_1.sqlite": infra[1],
                  "ZB_0.sqlite": infra[1], "ZB_1.sqlite": infra[1], "ZC_0.sqlite": infra[1], "ZC_1.sqlite": infra[1],
                  "ZD_0.sqlite": infra[1], "ZD_1.sqlite": infra[1], "ZE_0.sqlite": infra[1], "ZE_1.sqlite": infra[1]}

    # Carbon Tax
    carbon_tax = ["No Tax", "Tax"]
    carbon_tax_dict = {"WA_0.sqlite": carbon_tax[0], "WA_1.sqlite": carbon_tax[0], "WB_0.sqlite": carbon_tax[0],
                       "WB_1.sqlite": carbon_tax[0], "WC_0.sqlite": carbon_tax[0], "WC_1.sqlite": carbon_tax[0],
                       "WD_0.sqlite": carbon_tax[0], "WD_1.sqlite": carbon_tax[0], "WE_0.sqlite": carbon_tax[0],
                       "WE_1.sqlite": carbon_tax[0], "XA_0.sqlite": carbon_tax[0], "XA_1.sqlite": carbon_tax[0],
                       "XB_0.sqlite": carbon_tax[0], "XB_1.sqlite": carbon_tax[0], "XC_0.sqlite": carbon_tax[0],
                       "XC_1.sqlite": carbon_tax[0], "XD_0.sqlite": carbon_tax[0], "XD_1.sqlite": carbon_tax[0],
                       "XE_0.sqlite": carbon_tax[0], "XE_1.sqlite": carbon_tax[0], "YA_0.sqlite": carbon_tax[1],
                       "YA_1.sqlite": carbon_tax[1], "YB_0.sqlite": carbon_tax[1], "YB_1.sqlite": carbon_tax[1],
                       "YC_0.sqlite": carbon_tax[1], "YC_1.sqlite": carbon_tax[1], "YD_0.sqlite": carbon_tax[1],
                       "YD_1.sqlite": carbon_tax[1], "YE_0.sqlite": carbon_tax[1], "YE_1.sqlite": carbon_tax[1],
                       "ZA_0.sqlite": carbon_tax[1], "ZA_1.sqlite": carbon_tax[1], "ZB_0.sqlite": carbon_tax[1],
                       "ZB_1.sqlite": carbon_tax[1], "ZC_0.sqlite": carbon_tax[1], "ZC_1.sqlite": carbon_tax[1],
                       "ZD_0.sqlite": carbon_tax[1], "ZD_1.sqlite": carbon_tax[1], "ZE_0.sqlite": carbon_tax[1],
                       "ZE_1.sqlite": carbon_tax[1]}

    # Iterate through each run
    for run_name in run_names:
        folder = db_folder + "\\" + run_name

        metrics = ['costs_yearly', 'emissions_yearly', 'activity_by_fuel', 'activity_by_tech']

        num_cores = multiprocessing.cpu_count() - 1  # Save one core for other processes

        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=num_cores):
            Parallel(n_jobs=num_cores, verbose=5)(
                delayed(analyze_results)(metric, folder, run_name, dbs, all_dbs, db_shift, node_prob, tech_group_dict,
                                         prob_type_dict,
                                         infra_dict, carbon_tax_dict) for metric in metrics)

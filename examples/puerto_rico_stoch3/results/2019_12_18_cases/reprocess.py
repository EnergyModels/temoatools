import pandas as pd

# Common Inputs
run_names = ["2019_12_18_cases", ]

# Names of databases simulated
dbs = ["WA_0.sqlite", "WB_0.sqlite", "WC_0.sqlite", "WD_0.sqlite", "WE_0.sqlite", "WF_0.sqlite", "XA_0.sqlite",
       "XB_0.sqlite", "XC_0.sqlite", "XD_0.sqlite", "XE_0.sqlite", "XF_0.sqlite", "YA_0.sqlite", "YB_0.sqlite",
       "YC_0.sqlite", "YD_0.sqlite", "YE_0.sqlite", "YF_0.sqlite", "ZA_0.sqlite", "ZB_0.sqlite", "ZC_0.sqlite",
       "ZD_0.sqlite", "ZE_0.sqlite", "ZF_0.sqlite", "T_0.sqlite", "U_0.sqlite"]

# Node probabilities by case (0 is simulated, 1 is calculated)
node_prob = {"0": [0.52, 0.32, 0.16],  # Historical (sum must equal 1)
             "1": [0.2, 0.32, 0.48]}  # Climate Change

# Dictionary relating simulated databases to calculated results using different distributions
db_shift = {"WA_0": "WA_1", "WB_0": "WB_1", "WC_0": "WC_1", "WD_0": "WD_1", "WE_0": "WE_1", "WF_0": "WF_1",
            "XA_0": "XA_1", "XB_0": "XB_1", "XC_0": "XC_1", "XD_0": "XD_1", "XE_0": "XE_1", "XF_0": "XF_1",
            "YA_0": "YA_1", "YB_0": "YB_1", "YC_0": "YC_1", "YD_0": "YD_1", "YE_0": "YE_1", "YF_0": "YF_1",
            "ZA_0": "ZA_1", "ZB_0": "ZB_1", "ZC_0": "ZC_1", "ZD_0": "ZD_1", "ZE_0": "ZE_1", "ZF_0": "ZF_1",
            "T_0": "T_1", "U_0": "U_1", }

# List of all databases after applying different distributions
all_dbs = ["WA_0.sqlite", "WA_1.sqlite", "WB_0.sqlite", "WB_1.sqlite", "WC_0.sqlite", "WC_1.sqlite", "WD_0.sqlite",
           "WD_1.sqlite", "WE_0.sqlite", "WE_1.sqlite", "WF_0.sqlite", "WF_1.sqlite", "XA_0.sqlite", "XA_1.sqlite",
           "XB_0.sqlite", "XB_1.sqlite", "XC_0.sqlite", "XC_1.sqlite", "XD_0.sqlite", "XD_1.sqlite", "XE_0.sqlite",
           "XE_1.sqlite", "XF_0.sqlite", "XF_1.sqlite", "YA_0.sqlite", "YA_1.sqlite", "YB_0.sqlite", "YB_1.sqlite",
           "YC_0.sqlite", "YC_1.sqlite", "YD_0.sqlite", "YD_1.sqlite", "YE_0.sqlite", "YE_1.sqlite", "YF_0.sqlite",
           "YF_1.sqlite", "ZA_0.sqlite", "ZA_1.sqlite", "ZB_0.sqlite", "ZB_1.sqlite", "ZC_0.sqlite", "ZC_1.sqlite",
           "ZD_0.sqlite", "ZD_1.sqlite", "ZE_0.sqlite", "ZE_1.sqlite", "ZF_0.sqlite", "ZF_1.sqlite", "T_0.sqlite",
           "T_1.sqlite", "U_0.sqlite", "U_1.sqlite"]

# Technology Groups
tech_group = ['Centralized - Natural Gas', 'Centralized - Hybrid', 'Distributed - Natural Gas', 'Distributed - Hybrid',
              'Business-as-usual', 'Mixed - Hybrid', 'All']
tech_group_dict = {"WA_0.sqlite": tech_group[0], "WA_1.sqlite": tech_group[0], "WB_0.sqlite": tech_group[1],
                   "WB_1.sqlite": tech_group[1], "WC_0.sqlite": tech_group[2], "WC_1.sqlite": tech_group[2],
                   "WD_0.sqlite": tech_group[3], "WD_1.sqlite": tech_group[3], "WE_0.sqlite": tech_group[4],
                   "WE_1.sqlite": tech_group[4], "WF_0.sqlite": tech_group[5], "WF_1.sqlite": tech_group[5],
                   "XA_0.sqlite": tech_group[0], "XA_1.sqlite": tech_group[0], "XB_0.sqlite": tech_group[1],
                   "XB_1.sqlite": tech_group[1], "XC_0.sqlite": tech_group[2], "XC_1.sqlite": tech_group[2],
                   "XD_0.sqlite": tech_group[3], "XD_1.sqlite": tech_group[3], "XE_0.sqlite": tech_group[4],
                   "XE_1.sqlite": tech_group[4], "XF_0.sqlite": tech_group[5], "XF_1.sqlite": tech_group[5],
                   "YA_0.sqlite": tech_group[0], "YA_1.sqlite": tech_group[0], "YB_0.sqlite": tech_group[1],
                   "YB_1.sqlite": tech_group[1], "YC_0.sqlite": tech_group[2], "YC_1.sqlite": tech_group[2],
                   "YD_0.sqlite": tech_group[3], "YD_1.sqlite": tech_group[3], "YE_0.sqlite": tech_group[4],
                   "YE_1.sqlite": tech_group[4], "YF_0.sqlite": tech_group[5], "YF_1.sqlite": tech_group[5],
                   "ZA_0.sqlite": tech_group[0], "ZA_1.sqlite": tech_group[0], "ZB_0.sqlite": tech_group[1],
                   "ZB_1.sqlite": tech_group[1], "ZC_0.sqlite": tech_group[2], "ZC_1.sqlite": tech_group[2],
                   "ZD_0.sqlite": tech_group[3], "ZD_1.sqlite": tech_group[3], "ZE_0.sqlite": tech_group[4],
                   "ZE_1.sqlite": tech_group[4], "ZF_0.sqlite": tech_group[5], "ZF_1.sqlite": tech_group[5],
                   "T_0.sqlite": tech_group[6], "T_1.sqlite": tech_group[6], "U_0.sqlite": tech_group[6],
                   "U_1.sqlite": tech_group[6], }

# Historical or Climate Change Probabilities
prob = ["Historical", "Climate Change"]
prob_type_dict = {"WA_0.sqlite": prob[0], "WA_1.sqlite": prob[1], "WB_0.sqlite": prob[0], "WB_1.sqlite": prob[1],
                  "WC_0.sqlite": prob[0], "WC_1.sqlite": prob[1], "WD_0.sqlite": prob[0], "WD_1.sqlite": prob[1],
                  "WE_0.sqlite": prob[0], "WE_1.sqlite": prob[1], "WF_0.sqlite": prob[0], "WF_1.sqlite": prob[1],
                  "XA_0.sqlite": prob[0], "XA_1.sqlite": prob[1], "XB_0.sqlite": prob[0], "XB_1.sqlite": prob[1],
                  "XC_0.sqlite": prob[0], "XC_1.sqlite": prob[1], "XD_0.sqlite": prob[0], "XD_1.sqlite": prob[1],
                  "XE_0.sqlite": prob[0], "XE_1.sqlite": prob[1], "XF_0.sqlite": prob[0], "XF_1.sqlite": prob[1],
                  "YA_0.sqlite": prob[0], "YA_1.sqlite": prob[1], "YB_0.sqlite": prob[0], "YB_1.sqlite": prob[1],
                  "YC_0.sqlite": prob[0], "YC_1.sqlite": prob[1], "YD_0.sqlite": prob[0], "YD_1.sqlite": prob[1],
                  "YE_0.sqlite": prob[0], "YE_1.sqlite": prob[1], "YF_0.sqlite": prob[0], "YF_1.sqlite": prob[1],
                  "ZA_0.sqlite": prob[0], "ZA_1.sqlite": prob[1], "ZB_0.sqlite": prob[0], "ZB_1.sqlite": prob[1],
                  "ZC_0.sqlite": prob[0], "ZC_1.sqlite": prob[1], "ZD_0.sqlite": prob[0], "ZD_1.sqlite": prob[1],
                  "ZE_0.sqlite": prob[0], "ZE_1.sqlite": prob[1], "ZF_0.sqlite": prob[0], "ZF_1.sqlite": prob[1],
                  "T_0.sqlite": prob[0], "T_1.sqlite": prob[1], "U_0.sqlite": prob[0], "U_1.sqlite": prob[1]}

# Infrastructure Type
infra = ["Current", "Hardened", "All"]
infra_dict = {"WA_0.sqlite": infra[0], "WA_1.sqlite": infra[0], "WB_0.sqlite": infra[0], "WB_1.sqlite": infra[0],
              "WC_0.sqlite": infra[0], "WC_1.sqlite": infra[0], "WD_0.sqlite": infra[0], "WD_1.sqlite": infra[0],
              "WE_0.sqlite": infra[0], "WE_1.sqlite": infra[0], "WF_0.sqlite": infra[0], "WF_1.sqlite": infra[0],
              "XA_0.sqlite": infra[1], "XA_1.sqlite": infra[1], "XB_0.sqlite": infra[1], "XB_1.sqlite": infra[1],
              "XC_0.sqlite": infra[1], "XC_1.sqlite": infra[1], "XD_0.sqlite": infra[1], "XD_1.sqlite": infra[1],
              "XE_0.sqlite": infra[1], "XE_1.sqlite": infra[1], "XF_0.sqlite": infra[1], "XF_1.sqlite": infra[1],
              "YA_0.sqlite": infra[0], "YA_1.sqlite": infra[0], "YB_0.sqlite": infra[0], "YB_1.sqlite": infra[0],
              "YC_0.sqlite": infra[0], "YC_1.sqlite": infra[0], "YD_0.sqlite": infra[0], "YD_1.sqlite": infra[0],
              "YE_0.sqlite": infra[0], "YE_1.sqlite": infra[0], "YF_0.sqlite": infra[0], "YF_1.sqlite": infra[0],
              "ZA_0.sqlite": infra[1], "ZA_1.sqlite": infra[1], "ZB_0.sqlite": infra[1], "ZB_1.sqlite": infra[1],
              "ZC_0.sqlite": infra[1], "ZC_1.sqlite": infra[1], "ZD_0.sqlite": infra[1], "ZD_1.sqlite": infra[1],
              "ZE_0.sqlite": infra[1], "ZE_1.sqlite": infra[1], "ZF_0.sqlite": infra[1], "ZF_1.sqlite": infra[1],
              "T_0.sqlite": infra[2], "T_1.sqlite": infra[2], "U_0.sqlite": infra[2], "U_1.sqlite": infra[2]}

# Carbon Tax
carbon_tax = ["No Tax", "Tax"]
carbon_tax_dict = {"WA_0.sqlite": carbon_tax[0], "WA_1.sqlite": carbon_tax[0], "WB_0.sqlite": carbon_tax[0],
                   "WB_1.sqlite": carbon_tax[0], "WC_0.sqlite": carbon_tax[0], "WC_1.sqlite": carbon_tax[0],
                   "WD_0.sqlite": carbon_tax[0], "WD_1.sqlite": carbon_tax[0], "WE_0.sqlite": carbon_tax[0],
                   "WE_1.sqlite": carbon_tax[0], "WF_0.sqlite": carbon_tax[0], "WF_1.sqlite": carbon_tax[0],
                   "XA_0.sqlite": carbon_tax[0], "XA_1.sqlite": carbon_tax[0], "XB_0.sqlite": carbon_tax[0],
                   "XB_1.sqlite": carbon_tax[0], "XC_0.sqlite": carbon_tax[0], "XC_1.sqlite": carbon_tax[0],
                   "XD_0.sqlite": carbon_tax[0], "XD_1.sqlite": carbon_tax[0], "XE_0.sqlite": carbon_tax[0],
                   "XE_1.sqlite": carbon_tax[0], "XF_0.sqlite": carbon_tax[0], "XF_1.sqlite": carbon_tax[0],
                   "YA_0.sqlite": carbon_tax[1], "YA_1.sqlite": carbon_tax[1], "YB_0.sqlite": carbon_tax[1],
                   "YB_1.sqlite": carbon_tax[1], "YC_0.sqlite": carbon_tax[1], "YC_1.sqlite": carbon_tax[1],
                   "YD_0.sqlite": carbon_tax[1], "YD_1.sqlite": carbon_tax[1], "YE_0.sqlite": carbon_tax[1],
                   "YE_1.sqlite": carbon_tax[1], "YF_0.sqlite": carbon_tax[1], "YF_1.sqlite": carbon_tax[1],
                   "ZA_0.sqlite": carbon_tax[1], "ZA_1.sqlite": carbon_tax[1], "ZB_0.sqlite": carbon_tax[1],
                   "ZB_1.sqlite": carbon_tax[1], "ZC_0.sqlite": carbon_tax[1], "ZC_1.sqlite": carbon_tax[1],
                   "ZD_0.sqlite": carbon_tax[1], "ZD_1.sqlite": carbon_tax[1], "ZE_0.sqlite": carbon_tax[1],
                   "ZE_1.sqlite": carbon_tax[1], "ZF_0.sqlite": carbon_tax[1], "ZF_1.sqlite": carbon_tax[1],
                   "T_0.sqlite": carbon_tax[0], "T_1.sqlite": carbon_tax[0], "U_0.sqlite": carbon_tax[1],
                   "U_1.sqlite": carbon_tax[1]}
#=======================================================

# Inputs
metric = 'costs_yearly'
filename = "costs_yearly_exp_resampled.csv"
conversion = 1.0 / 100.0  # Convert from cents/kWh to $/kWh/yr
id_vars = ["database", "scenario"]
col_renames = {"scenario": "s", "database": "Scenario"}
csv_file = "costs_yearly_toPlot.csv"

# Load and Process data
df = pd.read_csv(filename, index_col=0)
if metric == 'costs_yearly' or metric == 'emissions_yearly':
    df = df.drop(["prob","entry"], axis=1)
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
    df2.loc[ind, "infra_and_carbon_tax"] = infra_dict[db] + "-" + carbon_tax_dict[db]
df2 = df2.rename(columns=col_renames)
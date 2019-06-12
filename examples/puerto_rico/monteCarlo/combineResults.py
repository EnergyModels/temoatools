import pandas as pd


#=======================#
# Inputs
#=======================#
gridRestorationResults = "gridRestorationResults.csv"
# Monte Carlo Results
scenarios = ["Centralized - Natural Gas","Centralized - Hybrid", "Distributed - Natural Gas", "Distributed - Hybrid"]
files = ["MonteCarloResults_A.csv", "MonteCarloResults_B.csv", "MonteCarloResults_C.csv", "MonteCarloResults_D.csv"]
# Variables to read
columns = ["LCOE", "cost-2052","avgEmissions", "emis-2052"]
rawmetrics = ["LCOE (cents/kWh)", "2052 COE (cents/kWh)","Avg. Emissions (Mton/yr)","2052 Emissions (Mton/yr)"]
metrics = ["LCOE (cents/kWh)", "2052 COE (10 cents/kWh)","Avg. Emissions (Gton/yr)","2052 Emissions (Gton/yr)"]
scales = [1.0, 0.1, 1.00E-03, 1.00E-03]

#=======================#
# Process Data
#=======================#
# Read grid restoration results
df = pd.read_csv(gridRestorationResults)

# Iterate through individual monte carlo results files
for scenario,file in zip(scenarios,files):
    df_mc = pd.read_csv(file)

    # Iterate through variables of interest
    for col, rawmetric, metric, scale in zip(columns,rawmetrics, metrics,scales):


        data = pd.DataFrame(columns=["Scenario","RawMetric","Metric","RawValue","Scale","Value"])

        data.RawValue = df_mc[col]
        data.Scale = scale
        data.Value = df_mc[col] * scale
        data.Scenario = scenario
        data.RawMetric = rawmetric
        data.Metric = metric

        # Append Data
        df = df.append(data)



#=======================#
# Save Results
#=======================#
df.to_csv("combinedResults_bar_all.csv")
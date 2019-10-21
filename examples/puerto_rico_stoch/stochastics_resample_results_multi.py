from __future__ import print_function
import pandas as pd
import os
import time

# This script resamples the results based on the calculated probabilities and a Monte Carlo population of 10,000

# Node probabilities
p = {"0": [0.56, 0.24, 0.2],  # Node probabilities (H1, H3, H5) by case (0,1,2,3)
     "1": [0.16, 0.24, 0.6]}

# Model runs to analyze (by folder)
folders = ['2019_10_21', ]

# Result files to resample
# filenames = ["emissions_yearly_exp"]
filenames = ["costs_yearly_exp"]
# filenames = ["activity_by_fuel_exp"]
# filenames = ["activity_by_tech_exp"]

# ====================
# Process files
# ====================
# Start counting time
t0 = time.time()
t_prev = t0

# Iterate through model runs
for folder in folders:

    # Move to results directory
    cwd = os.getcwd()
    path = os.getcwd() + '\\results\\' + folder
    os.chdir(path)

    # Iterate through result files
    for filename in filenames:
        print(filename)

        csv_filename = filename + ".csv"
        # Load and process data
        df = pd.read_csv(csv_filename)
        # Remove scenario==solve
        df.drop(df.loc[df['scenario'] == "solve"].index, inplace=True)

        # Create new column to store probabilities (prob)
        df.loc[:, "prob"] = 0.0

        # Create a new dataframe to store results
        n_population = 10000
        df2 = pd.DataFrame()

        # ------------------
        # Compute Probabilities
        # ------------------
        # Test cases
        # s = "D.S0s0s0s0"
        # s = "D.S1s1s1s1"
        # s = "D.S2s2s2s2"

        for s in df.loc[:, "scenario"].unique():
            # Find each row for this scenario
            indices = df.loc[:, "scenario"] == s
            # Find positions of '_' and 'S' in scenario name to identify case_num and p_case
            ind1 = s.find("_") + 1
            ind2 = s.find("S") + 1
            case_num = s[ind1]
            p_case = p[case_num]
            # Compute probability of this scenario recursively
            prob = p_case[int(s[ind2])]
            while ind2 < len(s) - 1:
                ind2 = ind2 + 2
                prob = prob * p_case[int(s[ind2])]

            # Store prob
            df.loc[indices, "prob"] = prob

            # Copy repeats into a new database
            repeats = int(n_population * prob)
            for i in range(repeats):
                df2 = df2.append(df.loc[indices, :], ignore_index=True)

            # Update user on time elapsed
            t = time.time()
            dt = t - t_prev
            print(s, ": elapsed time (s): ", str(round(dt, 2)))
            t_prev = t

        # Check if successful (total probability per database==1)
        for db in df.database.unique():
            print("db: ", db)
            print("sum = ", df.loc[df.database == db, "prob"].sum(), "(Should be equal to 1 for cost and emissions)")

        # ------------------
        # Save results as csv
        # ------------------
        csv_file = filename + "_resampled.csv"
        df2.to_csv(csv_file)

    # Update total time
    t = time.time()
    print("Total time (s): ", str(round(t - t0, 2)))

    # Return to original folder
    os.chdir(cwd)

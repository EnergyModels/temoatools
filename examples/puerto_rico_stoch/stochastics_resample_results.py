from __future__ import print_function
import pandas as pd
import os

# This script resamples the results based on the calculated probabilities and a Monte Carlo population of 10,000

# Node probabilities
p = [0.52, 0.32, 0.16]  # Node probabilities (H1, H3, H5)
# Model runs to analyze (by folder)
folders = ['2019_09_25_HAZUS_moderate', '2019_09_27_HAZUS_severe']
# Result files to resample
filenames = ["costs_yearly", "emissions_yearly", "activity_by_fuel"]

# ====================
# Process files
# ====================


# Iterate through model runs
for folder in folders:

    # Move to results directory
    cwd = os.getcwd()
    path = os.getcwd() + '\\Results\\' + folder
    os.chdir(path)

    # Iterate through result files
    for filename in filenames:

        csv_filename = filename + ".csv"
        # Load and process data
        df = pd.read_csv(csv_filename)
        # Remove scenario==solve
        df.drop(df.loc[df['scenario'] == "solve"].index, inplace=True)

        # Create new column to store probabilities (prob)
        df.loc[:, "prob"] = 0.0

        # ------------------
        # Compute Probabilities
        # ------------------
        # Test cases
        # s = "D.S0s0s0s0"
        # s = "D.S1s1s1s1"
        # s = "D.S2s2s2s2"

        for index, row in df.iterrows():
            s = row["scenario"]
            ind = s.find("S") + 1
            prob = p[int(s[ind])]
            while ind < len(s) - 1:
                ind = ind + 2
                prob = prob * p[int(s[ind])]

            # Store prob
            df.loc[index, "prob"] = prob

        # Check if successful (total probability per database==1)
        for db in df.database.unique():
            print("db: ", db)
            print("sum = ", df.loc[df.database == db, "prob"].sum(), "(Should be equal to 1)")

        # ------------------
        # Copy samples into new dataframe
        # ------------------
        n_population = 10000

        df2 = pd.DataFrame()
        for index, row in df.iterrows():
            repeats = int(n_population * row["prob"])
            for i in range(repeats):
                df2 = df2.append(row, ignore_index=True)

        # ------------------
        # Save results as csv
        # ------------------
        csv_file = filename + "_resampled.csv"
        df2.to_csv(csv_file)

    # Return to original folder
    os.chdir(cwd)

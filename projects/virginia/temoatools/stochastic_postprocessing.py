import os
import pandas as pd
import time


# ===========================================
# Expand stochastic results
#
# If running the stochastic model with the same hurricane wind speeds
# but different probabilities, then instead of re-running the temoa solution
# the results can be copied and weighted to get new distributions
# ===========================================
def stoch_expand(path, filename, db_shift):
    # Move to results directory
    cwd = os.getcwd()
    os.chdir(path)

    # Read-in existing results
    filein = filename + ".csv"
    f = open(filein, 'r')
    filedata = f.read()
    f.close()

    # Make a replacement on a copy of filedata, to preserve original results
    newdata = filedata
    # Remove first line of newdata, so that when combined we do not have the headings twice
    ind = newdata.find("\n") + 2
    newdata = newdata[ind:]
    # Add a row number for the first line
    newdata = "0" + newdata

    # Replace db names with db_shift
    for key in db_shift.keys():
        newdata = newdata.replace(key, db_shift[key])

    # Combine data
    combdata = filedata + newdata

    # Write out updated results
    fileout = filename + "_exp.csv"
    f = open(fileout, 'w')
    f.write(combdata)
    f.close()

    # Return to original folder
    os.chdir(cwd)


# ===========================================
# Resample stochastic results
#
# The stochastic model solves each node, but does not provide results in a format that weights the results.
# This script resamples the results based on the calculated probabilities and a Monte Carlo population
# of 10,000 so that plotting functions from seaborn can be used to easily visualize the results
# ===========================================
def stoch_resample(path, filename, node_prob):
    # Move to results directory
    cwd = os.getcwd()
    os.chdir(path)

    # ------------------
    # Process files
    # ------------------
    # Start counting time
    t0 = time.time()
    t_prev = t0

    print(filename)

    csv_filename = filename + ".csv"
    # Load and process data
    df = pd.read_csv(csv_filename)
    # Remove scenario==solve
    df.drop(df.loc[df['scenario'] == "solve"].index, inplace=True)

    # Create new columns
    df.loc[:, "prob"] = 0.0  # to store probabilities (prob)
    df.loc[:, "entry"] = 0  # to store entry number
    entry = 0  # Reset entry number
    # Create a new dataframe to store results
    n_population = 10000
    df2 = pd.DataFrame()

    # ------------------
    # Compute Probabilities
    # ------------------
    # Test cases
    # s = "D_#.S0s0s0s0"
    # s = "D_#.S1s1s1s1"
    # s = "D_#.S2s2s2s2"

    for s in df.loc[:, "scenario"].unique():

        # Find each row for this scenario
        indices = df.loc[:, "scenario"] == s
        # Find positions of '_' and 'S' in scenario name to identify case_num and p_case
        ind1 = s.find("_") + 1
        ind2 = s.find("S") + 1
        case_num = s[ind1]
        p_case = node_prob[case_num]
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
            entry = entry + 1
            df.loc[indices, "entry"] = entry
            df2 = df2.append(df.loc[indices, :], ignore_index=True)

        # Update user on time elapsed
        t = time.time()
        dt = t - t_prev
        print(s, ": elapsed time (s): ", str(round(dt, 2)))
        t_prev = t

    # ------------------
    # Check if successful (total probability per database==1)
    # ------------------
    for db in df.database.unique():
        print("db: ", db)
        print(
            "sum = ", df.loc[df.database == db, "prob"].sum(), "(Should be equal to 1 for cost and emissions)")

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

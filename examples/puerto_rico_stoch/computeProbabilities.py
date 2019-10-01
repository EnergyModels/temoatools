from __future__ import print_function
import pandas as pd
import os

# Node probabilities
p = [0.56, 0.24, 0.2] # Node probabilities (H1, H3, H5)


# folder = os.getcwd() + '\\Results'
os.chdir("Results")


filenames = ["Results_Costs","Results_Emissions","Results_yearlyActivity_byFuel"]
sheet_names = ["yearlyCosts","yearlyEmissions","Activity"]


#====================
# Process files
#====================

for filename, sheet_name in zip(filenames,sheet_names):

    xls_filename = filename + ".xls"
    # Load and process data
    df = pd.read_excel(xls_filename,sheet_name=sheet_name)
    # Remove scenario==solve
    df.drop(df.loc[df['scenario']=="solve"].index, inplace=True)

    # Create new column to store probabilities (prob)
    df.loc[:,"prob"]=0.0

    #------------------
    # Compute Probabilities
    #------------------
    # Test cases
    # s = "D.S0s0s0s0"
    # s = "D.S1s1s1s1"
    # s = "D.S2s2s2s2"

    for index, row in df.iterrows():
        s = row["scenario"]
        ind = s.find("S")+1
        prob = p[int(s[ind])]
        while ind < len(s)-1:
            ind = ind + 2
            prob = prob*p[int(s[ind])]

        # Store prob
        df.loc[index,"prob"] = prob

    # Check if successful (total probability per database==1)
    for db in df.database.unique():
        print("db: ", db)
        print("sum = ",df.loc[df.database==db,"prob"].sum(),"(Should be equal to 1)")

    #------------------
    # Copy samples into new dataframe
    #------------------
    n_population = 10000

    df2 = pd.DataFrame()
    for index, row in df.iterrows():
        repeats = int(n_population*row["prob"])
        for i in range(repeats):
            df2 = df2.append(row, ignore_index=True)

    #------------------
    # Save results as csv
    #------------------
    csv_file = filename + "_upsampled.csv"
    df2.to_csv(csv_file)

# Return to original folder
os.chdir("..")
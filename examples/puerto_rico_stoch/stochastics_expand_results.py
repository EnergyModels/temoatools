import os

# Model runs to analyze (by folder)
folders = ['2019_10_25', ]

db_shift = {"WA_0": "WA_1", "WB_0": "WB_1",
            "WC_0": "WC_1", "WD_0": "WD_1", "WE_0": "WE_1",
            "XA_0": "XA_1", "XB_0": "XB_1",
            "XC_0": "XC_1", "XD_0": "XD_1", "XE_0": "XE_1",
            "YA_0": "YA_1", "YB_0": "YB_1",
            "YC_0": "YC_1", "YD_0": "YD_1", "YE_0": "YE_1",
            "ZA_0": "ZA_1", "ZB_0": "ZB_1",
            "ZC_0": "ZC_1", "ZD_0": "ZD_1", "ZE_0": "ZE_1"}

# Filenames to analyze
filenames = ['costs_yearly','emissions_yearly']

for folder in folders:

    # Move to results directory
    cwd = os.getcwd()
    path = os.getcwd() + '\\results\\' + folder
    os.chdir(path)

    for filename in filenames:

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

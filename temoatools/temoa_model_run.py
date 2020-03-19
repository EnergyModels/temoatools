import os
import shutil
import temoatools as tt
from pathlib import Path


# ============================================================================#
# Run Temoa Model using a config File
# ============================================================================#
def run(model_filename, temoa_path=os.path.normcase('C:/temoa/temoa'), saveEXCEL=False, debug=False, solver=''):
    # Keep track of main(working) directory
    workDir = os.getcwd()

    # Model Directory
    model_directory = os.path.join(workDir, "databases")

    # Directory to hold configuration files
    configDir = os.path.join(workDir, "configs")
    try:
        os.stat(configDir)
    except:
        os.mkdir(configDir)
    os.chdir(configDir)

    # Create configuration file
    config_file = CreateConfigFile(model_directory, model_filename, saveEXCEL=saveEXCEL, debug=debug, solver=solver)

    if debug:
        print("config_file: " + config_file)

    # Run temoa
    temoa_path_full = os.path.join(temoa_path, 'temoa_model')
    config_path_full = os.path.join(configDir, config_file)
    command = 'python ' + str(temoa_path_full) + ' --config=' + str(config_path_full)


    # command = 'python ' + str(temoa_path) + '/temoa_model/ --config=' + configDir + '/' + config_file
    error = False
    if debug:
        print(command)
    try:
        os.system(command)
    except:
        print(command)
        error = True

    # # Move saveEXCEL file
    # if saveEXCEL:
    #
    #     xlsDir = Temoa_Dir + '\\db_io\\' + model_filename + '_solve_model'
    #     os.chdir(xlsDir)
    #     shutil.move('solve.xls', model_directory + '\\' + model_filename + '.xls')
    #     os.chdir(workDir)
    #     try:
    #         os.remove(xlsDir)
    #     except:
    #         print("Warning: Unable to delete: " + xlsDir)
    #         #        os.chdir(Temoa_Dir)
    #     os.chdir('db_io\\' + model_filename + '_solve_model')
    #     shutil.move('solve.xls', model_directory + '\\' + model_filename + '.xls')

    # Return to working directory
    os.chdir(workDir)

    return error


# ============================================================================#
# Create Config File
# ============================================================================#
def CreateConfigFile(model_directory, model_filename, saveEXCEL=False, saveTEXTFILE=False, keep_pyomo_lp_file=False,
                     debug=False, solver=''):
    # Locate Database
    full_filename = tt.remove_ext(model_filename) + '.sqlite'
    dBpath = os.path.join(model_directory, full_filename)

    # Write Config File
    config_file = "config_" + tt.remove_ext(model_filename) + ".txt"
    if debug == True:
        print("config_file: " + str(config_file))
    f = open(config_file, "w")
    # ---
    f.write("#-----------------------------------------------------\n")
    f.write("# This is an automatically generated configuration file for Temoa using")
    f.write(" temoatools github.com/EnergyModels/temoatools\n")
    f.write("# It allows you to specify (and document) all run-time model options\n")
    f.write("# Legal chars in path: a-z A-Z 0-9 - _ \' / . :\n")
    f.write("# Comment out non-mandatory options to omit them\n")
    f.write("#-----------------------------------------------------\n")
    f.write("\n")
    f.write("# Input File (Mandatory)\n")
    f.write("# Input can be a .sqlite or .dat file\n")
    f.write("# Both relative path and absolute path are accepted\n")
    f.write("--input=" + dBpath + "\n")
    f.write("\n")
    f.write("# Output File (Mandatory)\n")
    f.write("# The output file must be a existing .sqlite file\n")
    f.write("--output=" + dBpath + "\n")
    f.write("\n")
    f.write("# Scenario Name (Mandatory)\n")
    f.write("# This scenario name is used to store results within the output .sqlite file\n")
    f.write("--scenario=" + "solve" + "\n")
    f.write("\n")
    f.write("# Path to the \"db_io\" folder (Mandatory)\n")
    f.write("# This is the location where database files reside\n")
    f.write("--path_to_db_io=" + model_directory + "\n")
    f.write("\n")
    f.write("# Spreadsheet Output (Optional)\n")
    f.write("# Direct model output to a spreadsheet\n")
    f.write("# Scenario name specified above is used to name the spreadsheet\n")
    # ---
    # Option - saveExcel file, Turn off to save HD space
    # ---
    if saveEXCEL:
        f.write("--saveEXCEL\n")
    else:
        f.write("#--saveEXCEL\n")
    # ---
    f.write("\n")
    f.write("# Save the log file output (Optional)\n")
    f.write("# This is the same output provided to the shell\n")
    # ---
    # Option - saveTEXTFILE file, Turn off to save HD space
    # ---
    if saveTEXTFILE == True:  # Turn off to save HD space
        f.write("--saveTEXTFILE\n")
    else:
        f.write("#--saveTEXTFILE\n")
    # ---
    f.write("\n")
    f.write("# Solver-related arguments (Optional)\n")
    if len(solver) > 0:
        f.write("--solver=" + solver + "                    # Optional, indicate the solver\n")
    else:
        f.write("#--solver=cplex                    # Optional, indicate the solver\n")
    # ---
    # Option - keep_pyomo_lp_file file, Turn off to save HD space       
    # ---
    if keep_pyomo_lp_file:  # Turn off to save HD space
        f.write("--keep_pyomo_lp_file             # Optional, generate Pyomo-compatible LP file\n")
    else:
        f.write("#--keep_pyomo_lp_file             # Optional, generate Pyomo-compatible LP file\n")
    # ---
    f.write("\n")
    f.write("# Modeling-to-Generate Alternatives (Optional)\n")
    f.write("# Run name will be automatically generated by appending '_mga_' and iteration number to scenario name\n")
    f.write("#--mga {\n")
    f.write("#	slack=0.1                     # Objective function slack value in MGA runs\n")
    f.write("#	iteration=4                   # Number of MGA iterations\n")
    f.write("#	weight=integer                # MGA objective function weighting method, currently)")
    f.write("'integer' or 'normalized'\n")
    f.write("#}\n")
    f.write("\n")
    f.close()
    # ---
    return config_file

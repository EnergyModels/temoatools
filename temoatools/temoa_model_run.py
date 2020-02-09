import os
import shutil
import temoatools as tt


# ============================================================================#
# Run Temoa Model using a batch File
# ============================================================================#
def run(model_filename, temoa_path='C:/temoa/temoa', saveEXCEL=False, data_path='data', debug=False):
    # Keep track of main(working) directory
    workDir = os.getcwd()

    # # Unpack temoa_paths
    # os.chdir(data_path)
    # df = pd.read_csv(temoa_paths, delimiter=',')
    # df = df.set_index('name')
    # Conda_Batch = df.loc['Conda_batch', 'path']
    # Temoa_Dir = df.loc['Temoa_Dir', 'path']

    # if debug == True:
    #     print("Conda_Batch: " + Conda_Batch)
    #     print("Temoa_Dir  : " + Temoa_Dir)

    # Model Directory
    model_directory = workDir + "\\databases"

    # Directory to hold configuration files
    configDir = workDir + "\\configs"
    try:
        os.stat(configDir)
    except:
        os.mkdir(configDir)
    os.chdir(configDir)

    # Create configuration file
    config_file = CreateConfigFile(model_directory, model_filename, saveEXCEL=saveEXCEL, debug=debug)

    if debug == True:
        print("config_file: " + config_file)

    # Run temoa
    command = 'python ' + temoa_path + '/temoa_model/ --config=' + configDir + '/' + config_file
    if debug==True:
        print(command)
    try:
        os.system(command)
    except:
        print(command)
    # os.system('python temoa_model/ --config=temoa_model/config_sample')

    # Directory to hold configuration files
    # batchDir = workDir + "\\batch"
    # try:
    #     os.stat(batchDir)
    # except:
    #     os.mkdir(batchDir)
    # os.chdir(batchDir)

    # Create Batch File
    # batchPath = CreateBatchFile(model_filename, configDir, config_file, Conda_Batch, Temoa_Dir, debug=debug)

    # if debug == True:
    #     print("batchPath: " + batchPath)

    # Run Batch File
    # os.system(batchPath)
    #
    # # Move saveEXCEL file
    # if saveEXCEL == True:
    #
    #     xlsDir = Temoa_Dir + '\\db_io\\' + model_filename + '_solve_model'
    #     os.chdir(xlsDir)
    #     shutil.move('solve.xls', model_directory + '\\' + model_filename + '.xls')
    #     os.chdir(workDir)
    #     try:
    #         os.remove(xlsDir)
    #     except:
    #         print("Warning: Unable to delete: " + xlsDir)
    # #        os.chdir(Temoa_Dir)
    #        os.chdir('db_io\\'+model_filename + '_solve_model')
    #        shutil.move('solve.xls',model_directory+'\\'+model_filename+'.xls')

    # Return to working directory
    os.chdir(workDir)


# ============================================================================#
# Create Batch File
# ============================================================================#
def CreateBatchFile(model_filename, configDir, config_file, Conda_Batch, Temoa_Dir, debug=False):
    # Create Batch File
    batchFile = "run_" + tt.remove_ext(model_filename) + ".bat"
    if debug == True:
        print("batchFile: " + batchFile)
    f = open(batchFile, "w")
    f.write(
        "call " + Conda_Batch + " \n")  # Activate Conda2 Environment, example: C:\\Users\\jab6ft\\AppData\\Local\\Continuum\\anaconda2\\Scripts\\activate.bat
    f.write("cd " + Temoa_Dir + "\n")  # Temoa Directory, example:
    f.write("python temoa_model/ --config=" + configDir + "\\" + config_file + "\n")
    if debug == True:
        f.write("pause")
    f.close()

    batchPath = os.getcwd() + '\\' + batchFile

    return batchPath


# ============================================================================#
# Create Config File
# ============================================================================#
def CreateConfigFile(model_directory, model_filename, saveEXCEL=False, saveTEXTFILE=False, keep_pyomo_lp_file=False,
                     debug=False):
    # Locate Database
    dBpath = model_directory + "\\" + tt.remove_ext(model_filename) + '.sqlite'

    # Write Config File
    config_file = "config_" + tt.remove_ext(model_filename) + ".txt"
    if debug == True:
        print("config_file: " + str(config_file))
    f = open(config_file, "w")
    # ---
    f.write(
        "#-----------------------------------------------------                                                          \n")
    f.write(
        "# This is a sample configuration file for Temoa                                                                 \n")
    f.write(
        "# It allows you to specify (and document) all run-time model options                                            \n")
    f.write(
        "# Legal chars in path: a-z A-Z 0-9 - _ \ / . :                                                                  \n")
    f.write(
        "# Comment out non-mandatory options to omit them                                                                \n")
    f.write(
        "#-----------------------------------------------------                                                          \n")
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Input File (Mandatory)                                                                                        \n")
    f.write(
        "# Input can be a .sqlite or .dat file                                                                           \n")
    f.write(
        "# Both relative path and absolute path are accepted                                                             \n")
    f.write("--input=" + dBpath + "\n")
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Output File (Mandatory)                                                                                       \n")
    f.write(
        "# The output file must be a existing .sqlite file                                                               \n")
    f.write("--output=" + dBpath + "\n")
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Scenario Name (Mandatory)                                                                                     \n")
    f.write(
        "# This scenario name is used to store results within the output .sqlite file                                    \n")
    f.write("--scenario=" + "solve" + "\n")
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Path to the “db_io” folder (Mandatory)                                                                        \n")
    f.write(
        "# This is the location where database files reside                                                              \n")
    f.write(
        "--path_to_db_io="+model_directory  +"                                                                                           \n")
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Spreadsheet Output (Optional)                                                                                 \n")
    f.write(
        "# Direct model output to a spreadsheet                                                                          \n")
    f.write(
        "# Scenario name specified above is used to name the spreadsheet                                                 \n")
    # ---
    # Option - saveExcel file, Turn off to save HD space
    # ---
    if saveEXCEL == True:
        f.write(
            "--saveEXCEL                                                                                                    \n")
    else:
        f.write(
            "#--saveEXCEL                                                                                                    \n")
    # ---
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Save the log file output (Optional)                                                                           \n")
    f.write(
        "# This is the same output provided to the shell                                                                 \n")
    # ---
    # Option - saveTEXTFILE file, Turn off to save HD space
    # ---
    if saveTEXTFILE == True:  # Turn off to save HD space
        f.write(
            "--saveTEXTFILE                                                                                                 \n")
    else:
        f.write(
            "#--saveTEXTFILE                                                                                                 \n")
    # ---
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Solver-related arguments (Optional)                                                                           \n")
    f.write(
        "--solver=cplex                    # Optional, indicate the solver                                               \n")
    # ---
    # Option - keep_pyomo_lp_file file, Turn off to save HD space       
    # ---
    if keep_pyomo_lp_file == True:  # Turn off to save HD space
        f.write(
            "--keep_pyomo_lp_file             # Optional, generate Pyomo-compatible LP file                                 \n")
    else:
        f.write(
            "#--keep_pyomo_lp_file             # Optional, generate Pyomo-compatible LP file                                 \n")
    # ---
    f.write(
        "                                                                                                                \n")
    f.write(
        "# Modeling-to-Generate Alternatives (Optional)                                                                  \n")
    f.write(
        "# Run name will be automatically generated by appending '_mga_' and iteration number to scenario name           \n")
    f.write(
        "#--mga {                                                                                                        \n")
    f.write(
        "#	slack=0.1                     # Objective function slack value in MGA runs                                  \n")
    f.write(
        "#	iteration=4                   # Number of MGA iterations                                                    \n")
    f.write(
        "#	weight=integer                # MGA objective function weighting method, currently 'integer' or 'normalized'\n")
    f.write(
        "#}                                                                                                              \n")
    f.write(
        "                                                                                                                \n")
    f.close()
    # ---
    return config_file

# ============================================================================#
# End of TemoaModelRun
# ============================================================================#

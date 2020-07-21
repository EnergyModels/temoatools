# Stochastic optimization
Instructions to run projects/puerto_rico_stoch

While temoatools is now running in python 3, the version of temoa used for puerto_rico_stoch is in python 2.7, using 
version 4.3 of pyomo. Therefore running puerto_rico_stoch has been split into two parts:
1) projects/puerto_rico_stoch - creation of temoa files to run in temoa_stochastic and analysis scripts
2) temoa_stochastic - instance of temoa to use for simulations
projects/puerto_rico_stoch requires no additional set-up required if you follow the above instructions to run 
temoatools using the temoa-py3 environment 

### Set-up of temoa_stochastic:
Temoa_stochastic is written in python 2.7 using a modified version of pyomo 4.3. It is based on Patankar et al. 2019 
https://zenodo.org/record/2551865#.XmEhyahKhPY. 
This version of temoa is computationally intensive, so the example commands below are shown in Linux using Anaconda2 on the Rivanna cluster at the University of Virginia.
1) Install python 2.7 (using anaconda2), https://www.anaconda.com/distribution/#download-section
    - To install python 2.7 using anaconda2: 
    https://www.anaconda.com/distribution/#download-section
    - This is already 1
2) Download temoatools
    - Start terminal
    > git clone https://www.github.com/EnergyModels/temoatools
2) Create temoa-stoch-py2 environment within anaconda 2 (note comment out coincbc requirement if running on windows)
    start anaconda
    > cd temoatools/temoa_stochastic
    > module load anaconda/2019.10-py2.7
    > conda env create
    > source activate temoa-stoch-py2
3) Install modified version of pyomo 4.3.11388 (details on how this was created are in temoa_stochastic/pyomo_instructions.txt)
    > cd pyomo
    > pip install .
4)  Install temoatools
    > cd temoatools
    > pip install .                                                                                                                   
4) Optional: Install a commercial linear solver such as CPLEX or Gurobi, additional information can be found here: https://temoacloud.com/download/
    If running gurobi on Rivanna:
    > export PYTHONPATH=$EBROOTGUROBI/lib/python2.7_utf32
    > module load gurobi/9.0.1

### Running stochastic optimization (all run in temoa-stoch-py2)

1) Update model inputs

1) Enter/update simulation data in projects/puerto_rico_stoch/data folder. Scenarios_overview.ppt/.pdf provides background on cases simulated
    1) data_*.xls - model data
    2) scenarios.xlsx - variations detailed for each case/scenarios
    3) sensitivityVariables.xlsx - used to indicate which temoa variables are considered in a sensitivity study

2) Create input files for temoa
    1) Navigate to temaotools/projects/puerto_rico_stoch
        > cd temoatools/projects/puerto_rico_stoch
    2) Run baseline simluations
        1) Update paths and solver run_baselines.py
            > temoa_path = '/temoatools/temoa_stochastic' # temoa directory (stochastic version of temoa)
            > project_path = '/temoatools/projects/puerto_rico_stoch' # location of run_baselines.py
            > solver = 'gurobi'
         2) Run run_baselines.py
        > python run_baselines.py
    2) Update paths projects/puerto_rico_stoch/stochastics_write_input_files.py to create files for temoa
        > temoa_path = '/home/username/temoatools/temoa_stochastic' # temoa directory (stochastic version of temoa)                                                                                  >
    3) Move input files from projects/puerto_rico_stoch/stoch_inputs/ to temoa_stochastic installation
        1) config_stoch_*.txt files to temoa_stochastic/temoa_model/
            > mv ./stoch_inputs/config_stoch_*.txt temoatools/temoa_stochastic/temoa_model
        2) stoch_*.py files to temoa_stochastic/tools/options/
        > mv ./stoch_inputs/stoch_*.py temoatools/temoa_stochastic/tools/options
        3) *.dat and *.sqlite files to temoa_stochastic/data_files/
        > mv ./stoch_inputs/*.dat temoatools/temoa_stochastic/data_files
        > mv ./stoch_inputs/*.sqlite temoatools/temoa_stochastic/data_files

3) To run a single input file (example shown for the case T_0)
    1) Single run (manual)
        1) Move to temoa_stochastic/tools directory
            > cd temoa_stochastic/tools
        2) Run the following command to generate the scenario tree - This command will create a directory that includes the information related to the stochastic scenario tree
            > python generate_scenario_tree_JB.py options/stoch_T_0.py --debug
        3) Update the scenario tree
            > python rewrite_tree_nodes.py options/stoch_T_0.py --debug
        4) Move to temoa_stochastic directory
            > cd temoa_stochastic
        5) Run the model in temoa
            > python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_T_0.txt
    2) Multiple runs - To run multiple scenarios, parameterize in batch files (examples in temoa_stochastic)
        1) examples for windows: PR_stochastic_createScenarios_all.bat and PR_stochastic_run_all.bat
        2) examples for linux: createScenarios_all.sh, run_cases.sh, run_nocases.sh

4) Analyze results (scripts in projects/puerto_rico_stoch/)
    1) Move results files back to puerto_rico_stoch
        > mv temoatools/stoch_inputs/*.sqlite temoatools/temoa_stochastic/data_files
    2) Analyze results
        > python stochastics_all.py

5) Plot results (performed in R, scripts in projects/puerto_rico_stoch/results/)
                                                 
                                                                                                                                                                                                                                                                  
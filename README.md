# temoatools
The temoatools package is designed to complement the @github/TemoaProject by 
providing methods to help with the creation and analysis of the .sqlite databases used by temoa.
Specifically, users provide inputs in excel, which are then moved into .sqlite databases based 
on several simplifying assumptions (listed below). Methods are provided for creating, running and analyzing
baseline scenarios, sensitivity studies, Monte Carlo studies, and stochastic optimization runs using 
parallelization libraries.

More details:
1) temoatools simplifying assumptions
    - the following costs do not change with time
        - fixed costs
        - variable costs
        - capital costs
    - demand is only for a single sector

2) input files
    1) data - contains all project data (demand, technology, costs, etc.)
    2) scenarios - specify which technologies (from data) are used for each scenario to be run
    3) sensitivityVariables - specify which variables to perturb for a sensitivity analysis
  
3) Suggested project structure
    - project_folder
        - temoa - keep the version of temoa that you use accessible in case you would like to review methods or update
        - temoatools - keep the temoatools directory accessible for example files and for easy updating
        - project_files - keep all project files here
          
# temoatools installation - python 3
Temoatools is meant to be an add-in for Temoa, thus it builds on the current method for installing Temoa. 
These instructions are for a clean installation of Temoa and temoatools.

1) install anaconda3 https://www.anaconda.com/distribution/#download-section

2) install temoa
    1) following instructions on https://temoaproject.org using temoa-py3 environment
    2) record path to temoa

3) download temoatools

4) install temoatools using pip
    1) start anaconda3 prompt
    2) activate environment
    > conda activate temoa-py3
    3) navigate to temoatools directory
    > cd project_folder/temoatools
    4) install using pip
    >pip install .                                                                                                                                                                                                                     >

5) Make modifications to temoa source code for running simulations in parallel from a terminal
    1) comment out lines 548-551 of temoa_run.py
        -     try:  # make compatible with Python 2.7 or 3
	    -            raw_input() # Give the user a chance to confirm input
	    -     except:
        -            input()"

6) to test:

> import temoatools as tt

# Stochastic optimization
Instructions to run projects/puerto_rico_stoch.

While temoatools is now running in python 3, the version of temoa used for puerto_rico_stoch is in python 2.7, using 
version 4.3 of pyomo. Therefore running puerto_rico_stoch has been split into two parts:
1) projects/puerto_rico_stoch - creation of temoa files to run in temoa_stochastic and analysis scripts
2) temoa_stochastic - instance of temoa to use for simulations
projects/puerto_rico_stoch requires no additional set-up required if you follow the above instructions to run 
temoatools using the temoa-py3 environment 

### Set-up of temoa_stochastic:
Temoa_stochastic is written in python 2 using a modified version of pyomo 4.3. It is based on Patankar et al. 2019 
https://zenodo.org/record/2551865#.XmEhyahKhPY
1) Install python 2.7 (using anaconda2), https://www.anaconda.com/distribution/#download-section
2) Create temoa-py2 environment within anaconda 2 (note comment out coincbc requirement if running on windows)
    > module load anaconda/5.2.0-py2.7
    cd temoa_stochastic\
    conda env create\
    source activate temoa-stoch-py2
3) Install modified version of pyomo 4.3.11388 (details on how this was created are in temoa_stochastic/pyomo_instructions.txt)
    > cd temoa_stochastic/pyomo\
    source activate temoa-stoch-py2\
    pip install .
4) Optional: Install a commercial linear solver such as CPLEX or Gurobi, additional information can be found here: https://temoacloud.com/download/

### Running stochastic optimization

1) Enter/update simulation data in examples/puerto_rico_stoch/data folder. Scenarios_overview.ppt/.pdf provides background on cases simulated
    1) data_*.xls - model data
    2) scenarios.xlsx - variations detailed for each case/scenarios
    3) sensitivityVariables.xlsx - used to indicate which temoa variables are considered in a sensitivity study

2) Create input files for temoa
    1) Update paths and run projects/puerto_rico_stoch/run_baselines.py to create baseline simulations
    2) Update pahts and run examples/puerto_rico_stoch/stochastics_write_input_files.py to create files for temoa
    3) Move input files from examples/puerto_rico_stoch/stoch_inputs/ to temoa_stochastic installation
        1) config_stoch_*.txt files to temoa_stochastic/temoa_model/
        2) stoch_*.py files to temoa_stochastic/tools/options/
        3) *.dat and *.sqlite files to temoa_stochastic/data_files/

3) To run a single input file (example shown for the case T_0)
    1) Single run
        1) Run the following command to generate the scenario tree - This command will create a directory that includes the information related to the stochastic scenario tree
            > python generate_scenario_tree_JB.py options/stoch_T_0.py --debug
        2) Update the scenario tree
            > python rewrite_tree_nodes.py options/stoch_T_0.py --debug
        3) Run the model in temoa
            > python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_T_0.txt
    2) Multiple runs - To run multiple scenarios, paramaterize in batch files (examples in temoa_stochastic)
        1) examples for windows: PR_stochastic_createScenarios_all.bat and PR_stochastic_run_all.bat
        2) examples for linux: createScenarios_all.sh, and run_pt1.sh

4) Analyze results (scripts in examples/puerto_rico_stoch/)
    1) Analyze optimized results
        > python stochastics_analyze_nocases.py
    2) Analyze case-based results
        > python stochastics_analyze_cases.py

5) Plot results (performed in R, scripts in examples/puerto_rico_stoch/results/)
                                                 
# Usage notes
As of 2/8/2020, temoa currently does not output results to excel, therefore set saveEXCEL to False in temoatools.run()                                                                                                                                                                                                                                                                  
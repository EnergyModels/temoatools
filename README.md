# temoatools
The temoatools package is designed to complement the @github/TemoaProject by 
providing methods to help with the creation and analysis of the .sqlite databases used by temoa.
Specifically, users provide inputs in excel, which are then moved into .sqlite databases based 
on several simplifying assumptions (listed below). Methods are provided for creating, running and analyzing
single, sensitivity, Monte Carlo, and stochastic runs using parallelization libraries.

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
    >pip install .
                                                                                                                                                                                                                              >
5) Make modifications to temoa source code for running simulations in parallel from a terminal
    1) comment out lines 548-551 of temoa_run.py
        -     try:  # make compatible with Python 2.7 or 3
	    -            raw_input() # Give the user a chance to confirm input
	    -     except:
        -            input()"

6) to test:

> import temoatools as tt

# Usage notes
As of 2/8/2020, temoa currently does not output results to excel, therefore set saveEXCEL to False in temoatools.run()


# Stochastic optimization (uses temoatools v1.0.0)
Instructions to run examples/puerto_rico_stoch.

1) Install python and required packages
    1) Install python 2.7 (using anaconda2), https://www.anaconda.com/distribution/#download-section
    2) Install pyomo version 4.3 (using anaconda2 prompt)
        >pip install pyomo==4.3
    3) Update pyomo using legacy files
        1) Go to the temoa_stochastic/tools/legacy_files folder to find ef_writer_script_old.py. 
        Copy paste this script at: ../anaconda/lib/python2.7/site-packages/pyomo/pysp
        2) Go to the temoa_stochastic/tools/legacy_files folder to find scenariomodels.py.
        Copy paste this script at: ../anaconda/lib/python2.7/site-packages/pyomo/pysp/util 
    4) Install temoatools (instructions above). This will include copying a version of temoa (temoa_stochastic) that has been modified for this analysis
    5) Install a linear solver such as CPLEX, additional information can be found here: https://temoacloud.com/download/

2) Enter/update simulation data in examples/puerto_rico_stoch/data folder. Scenarios_overview.ppt/.pdf provides background on cases simulated
    1) paths.xls - provides paths to anaconda2 and temoa installation
    2) data_*.xls - model data
    2) scenarios.xls - variations detailed for each case/scenarios
    3) sensitivityVariables.xls - used to indicate which temoa variables are considered in a sensitivity study

3) Create input files for temoa
    1) Run examples/puerto_rico_stoch/stochastics_write_input_files.py to create files for temoa
    2) Move input files from examples/puerto_rico_stoch/stoch_inputs/ to temoa installation
        1) config_stoch_*.txt files to temoa_stochastic/temoa_model/
        2) stoch_*.py files to temoa_stochastic/tools/options/
        3) *.dat and *.sqlite files to temoa_stochastic/data_files/

4) To run a single input file (example shown for the case T_0)
    1) Single run
        1) Run the following command to generate the scenario tree - This command will create a directory that includes the information related to the stochastic scenario tree
            >python generate_scenario_tree_JB.py options/stoch_T_0.py --debug
        2) Update the scenario tree
            > python rewrite_tree_nodes.py options/stoch_T_0.py --debug
        3) Run the model in temoa
            > python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_T_0.txt
    2) Multiple runs - To run multiple scenarios, paramaterize in batch files, examples shown in temoa_stochastic/PR_stochastic_createScenarios_all.bat and temoa_stochastic/PR_stochastic_run_all.bat

5) Analyze results (scripts in examples/puerto_rico_stoch/)
    1) Analyze optimized results
        > python stochastics_analyze_nocases.py
    2) Analyze case-based results
        > python stochastics_analyze_cases.py

6) Plot results (performed in R, scripts in examples/puerto_rico_stoch/results/)
                                                                                                                                                                                                                                                                                                                   
# About
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
          
# temoatools installation with python 3
Temoatools is meant to be an add-in for Temoa, thus it builds on the current method for installing Temoa. 
The instructions below are for a new installation of anaconda3, Temoa and temoatools. The example commands are shown in a Windows environment.

1) install python 3 with anaconda3
    - https://www.anaconda.com/distribution/#download-section

2) install temoa
    1) follow instructions on https://temoacloud.com/download/ using the temoa-py3 environment
    2) record path to temoa 
        - Scripts that use temoatools refer to this as the temoa_path variable

3) install temoatools
    1) download temoatools
        > git clone https://www.github.com/EnergyModels/temoatools
    2) install temoatools using pip
        1) start anaconda3 prompt
        2) activate temoa-py3 environment
        > conda activate temoa-py3
        3) navigate to temoatools directory
        > cd project_folder/temoatools
        4) install using pip
        > pip install .                                                                                                                                                                                                                     >

5) to test:
    > import temoatools as tt

6) Optional: Make modifications to temoa source code for running simulations in parallel from a terminal
    1) comment out lines 548-551 of temoa_run.py
        -     try:  # make compatible with Python 2.7 or 3
	    -            raw_input() # Give the user a chance to confirm input
	    -     except:
        -            input()"

# stochastic instructions
For step-by-step instructions to run the stochastic version of temoa refer to stochastic_instructions.md

# Usage notes
As of 2/8/2020, temoa currently does not output results to excel, therefore set saveEXCEL to False in temoatools.run()
## About
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
  
3) Overview of main folders
    - temoatools/examples - sample uses of temoatools to run and analyze temoa models
    - temoatools/projects - sample projects, it is recommended to create a directory here for your project
    - temoatools/temoa-energysystem - an archived version of Temoa is now kept within the temoatools repository. This is the most recent version that works with temoatools
    - temoatools/temoa_stochastic - an archived version of Temoa in Python 2 that  is now kept within the temoatools repository. This is the most recent version that works with temoatools
    - temoatools/temoatools - temoatools source code
          
## temoatools installation with Python 3
Temoatools is meant to be an add-in for Temoa. Temoa is an on-going project, so temoatools uses an archived version of Temoa to ensure compatibility 
The instructions below are for a new installation of anaconda3, Temoa and temoatools. 
The example commands are shown in a Windows environment.

1) prerequisites: git and Anaconda3
    - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    - https://www.anaconda.com/distribution/#download-section
    
2) launch anaconda3 prompt

3) navigate to where you want to install and run temoatools
    > cd harddrive/yourdirectory

4) download temoatools
    > git clone https://www.github.com/EnergyModels/temoatools

3) create temoa-py3 environment
    1) navigate to archived version of temoa
    > cd temoa-energysystem
    2) create and activate environment
    > conda env create
    > conda activate temoa-py3
    
4) install temoatools
    1) navigate to temoatools directory
    > cd ..
    4) install using pip
    > pip install .
                                                                                                                                                                                                                     
5) to test:
    > cd examples/baselines  
    python baselines_run.py

        
## Running on Rivanna, UVA's high performance computing system*:
   ### To install:
          
        module load anaconda/2019.10-py3.7
        git clone https:www.github.com/EnergyModels/temoatools
        cd temoa
        conda env create
        source activate temoa-py3
        cd ..
        cd temoatools
        pip install .
    
   ### To test:
        cd examples/baselines
        sbatch run_baselines.sh
        sacct


## Stochastic Instructions
For step-by-step instructions to run the Puerto Rico Stochastic project, see the README.md file in projects/puerto_rico_stoch. 
This project uses a stochastic implementation of temoa that is archived in temoa_stochastic.

## Notes
As of 2/8/2020, temoa currently does not output results to excel, therefore set saveEXCEL to False in temoatools.run()

*At the time of writing this, Rivanna has python 2.7, Anaconda2 and Gurobi installed.
However, modules on Rivanna are routinely updated. 
Therefore "module load" commands (for anaconda and gurobi) may need to be updated. 
Check https://www.rc.virginia.edu/userinfo/rivanna/software/modules/ for the latest.
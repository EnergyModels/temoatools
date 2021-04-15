## About
The temoatools package is designed to complement the @github/TemoaProject by 
providing methods to help with the creation and analysis of the .sqlite databases used by temoa.
Specifically, users provide inputs in Excel, which are then moved into .sqlite databases based 
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
          
## How to cite
### Temoa
Hunter, K., Sreepathi, S. & DeCarolis, J. F. Modeling for insight using tools for energy model optimization and analysis (Temoa). Energy Econ. 40, 339–349 (2013). https://doi.org/10.1016/j.eneco.2013.07.014

### temoatools (this library)
Bennett, J.A., Trevisan, C.N., DeCarolis, J.F. et al. Extending energy system modelling to include extreme weather risks and application to hurricane events in Puerto Rico. Nat Energy 6, 240–249 (2021). https://doi.org/10.1038/s41560-020-00758-6

## temoatools installation with Python 3
Temoatools is meant to be an extension for Temoa. 
Temoa is an on-going project, so in order to ensure compatibility, temoatools uses an archived version of Temoa.
Temoatools currently uses the June 30, 2020 version of Temoa (commit 9d10c1d), downloadable at:  https://github.com/TemoaProject/temoa/tree/9d10c1da81dc6b4f2b34cadfac9db947251254e2
The instructions below are for a new installation of temoatools. 
The example commands are shown in a Windows environment.

1) prerequisites: git and Anaconda3
    - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    - https://www.anaconda.com/distribution/#download-section
    
2) launch anaconda3 prompt

3) navigate to where you want to install and run temoatools
    > cd harddrive/yourdirectory

4) download temoatools using git
    > git clone https://www.github.com/EnergyModels/temoatools

5) navigate to temoatools directory
    > cd temoatools

3) create temoa-py3 environment (modified from archvied version of Temoa)
    > conda env create
    > conda activate temoa-py3
    
4) install temoatools
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
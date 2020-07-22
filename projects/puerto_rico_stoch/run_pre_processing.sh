#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=6
#SBATCH -t 1:00:00
#SBATCH -p standard

module purge
module load anaconda/2019.10-py2.7

# activate temoa environment
source activate temoa-stoch-py2

# if gurobi is available
export PYTHONPATH=$EBROOTGUROBI/lib/python2.7_utf32
module load gurobi/9.0.1

# set the NUM_PROCS env variable for the Python script
export NUM_PROCS=$SLURM_CPUS_PER_TASK

# run
python stochastics_baselines.py
python stochastics_write_input_files.py

# change run permission of run_all_simulations.sh - enable to run as executable
chmod +x ./run_all_simulations.sh
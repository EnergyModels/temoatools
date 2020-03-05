#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=6
#SBATCH -t 10:00:00
#SBATCH -p standard

module purge
module load anaconda

# if gurobi is available
module load gurobi

# activate temoa environment
source activate temoa-py3

# set the NUM_PROCS env variable for the Python script
export NUM_PROCS=$SLURM_CPUS_PER_TASK

# run
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_YA_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_YB_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_YC_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_YD_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_YE_0.txt
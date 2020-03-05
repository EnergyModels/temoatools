#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=6
#SBATCH -t 10:00:00
#SBATCH -p standard

module purge
module load anaconda/5.2.0-py2.7

# if gurobi is available
module load gurobi

# activate temoa environment
source activate temoa-stoch-py2

# set the NUM_PROCS env variable for the Python script
export NUM_PROCS=$SLURM_CPUS_PER_TASK

# run
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_WA_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_WB_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_WC_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_WD_0.txt
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_WE_0.txt
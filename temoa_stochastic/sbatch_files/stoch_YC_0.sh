#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=8
#SBATCH -t 14:00:00
#SBATCH -p standard

cd ..

module purge
module load anaconda/2019.10-py2.7

# activate temoa environment
source activate temoa-stoch-py2

# if gurobi is available
module load gurobi/9.0.1

# set the NUM_PROCS env variable for the Python script
export NUM_PROCS =$SLURM_CPUS_PER_TASK

# run
cd tools
python generate_scenario_tree_JB.py options/stoch_YC_0.py --debug
python rewrite_tree_nodes.py options/stoch_YC_0.py --debug
cd ..
python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_YC_0.txt

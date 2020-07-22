#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=1
#SBATCH -t 0:10:00
#SBATCH -p standard

module purge
module load anaconda/2019.10-py2.7

# activate temoa environment
source activate temoa-stoch-py2

# if gurobi is available
export PYTHONPATH=$EBROOTGUROBI/lib/python2.7_utf32
module load gurobi/9.0.1

# move to temoa directory (used temoa_stochastic from this repository)

# run
python stochastics_baselines.py
python stochastics_write_input_files.py
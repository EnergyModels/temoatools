#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=6
#SBATCH -t 10:00:00
#SBATCH -p standard

module purge
module load anaconda

# activate temoa environment
source activate temoa-py3

# set the NUM_PROCS env variable for the Python script
export NUM_PROCS=$SLURM_CPUS_PER_TASK

# run
python stochastics_analyze_nocases.py
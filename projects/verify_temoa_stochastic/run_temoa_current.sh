#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=1
#SBATCH -t 0:10:00
#SBATCH -p standard

module purge
module load anaconda/2019.10-py3.7

# activate temoa environment (needs to already be set-up, follow README.md for temoatools)
source activate temoa-py3

# if gurobi is available
module load gurobi/9.0.1

# clone temoa and move to temoa directory (used commit https://github.com/TemoaProject/temoa/commit/9d10c1da81dc6b4f2b34cadfac9db947251254e2)
git clone https://github.com/TemoaProject/temoa
cd temoa-energysystem
git checkout 9d10c1da81dc6b4f2b34cadfac9db947251254e2

# run
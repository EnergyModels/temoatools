#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task=1
#SBATCH -t 10:00:00
#SBATCH -p standard

module purge
module load anaconda/5.2.0-py2.7

# activate temoa environment
source activate temoa-stoch-py2

# set the NUM_PROCS env variable for the Python script
export NUM_PROCS=$SLURM_CPUS_PER_TASK

# change directory
cd tools

# run
python generate_scenario_tree_JB.py options/stoch_T_0.py --debug
python rewrite_tree_nodes.py options/stoch_T_0.py --debug
python generate_scenario_tree_JB.py options/stoch_U_0.py --debug
python rewrite_tree_nodes.py options/stoch_U_0.py --debug

python generate_scenario_tree_JB.py options/stoch_WA_0.py --debug
python rewrite_tree_nodes.py options/stoch_WA_0.py --debug
python generate_scenario_tree_JB.py options/stoch_WB_0.py --debug
python rewrite_tree_nodes.py options/stoch_WB_0.py --debug
python generate_scenario_tree_JB.py options/stoch_WC_0.py --debug
python rewrite_tree_nodes.py options/stoch_WC_0.py --debug
python generate_scenario_tree_JB.py options/stoch_WD_0.py --debug
python rewrite_tree_nodes.py options/stoch_WD_0.py --debug
python generate_scenario_tree_JB.py options/stoch_WE_0.py --debug
python rewrite_tree_nodes.py options/stoch_WE_0.py --debug

python generate_scenario_tree_JB.py options/stoch_XA_0.py --debug
python rewrite_tree_nodes.py options/stoch_XA_0.py --debug
python generate_scenario_tree_JB.py options/stoch_XB_0.py --debug
python rewrite_tree_nodes.py options/stoch_XB_0.py --debug
python generate_scenario_tree_JB.py options/stoch_XC_0.py --debug
python rewrite_tree_nodes.py options/stoch_XC_0.py --debug
python generate_scenario_tree_JB.py options/stoch_XD_0.py --debug
python rewrite_tree_nodes.py options/stoch_XD_0.py --debug
python generate_scenario_tree_JB.py options/stoch_XE_0.py --debug
python rewrite_tree_nodes.py options/stoch_XE_0.py --debug

python generate_scenario_tree_JB.py options/stoch_YA_0.py --debug
python rewrite_tree_nodes.py options/stoch_YA_0.py --debug
python generate_scenario_tree_JB.py options/stoch_YB_0.py --debug
python rewrite_tree_nodes.py options/stoch_YB_0.py --debug
python generate_scenario_tree_JB.py options/stoch_YC_0.py --debug
python rewrite_tree_nodes.py options/stoch_YC_0.py --debug
python generate_scenario_tree_JB.py options/stoch_YD_0.py --debug
python rewrite_tree_nodes.py options/stoch_YD_0.py --debug
python generate_scenario_tree_JB.py options/stoch_YE_0.py --debug
python rewrite_tree_nodes.py options/stoch_YE_0.py --debug

python generate_scenario_tree_JB.py options/stoch_ZA_0.py --debug
python rewrite_tree_nodes.py options/stoch_ZA_0.py --debug
python generate_scenario_tree_JB.py options/stoch_ZB_0.py --debug
python rewrite_tree_nodes.py options/stoch_ZB_0.py --debug
python generate_scenario_tree_JB.py options/stoch_ZC_0.py --debug
python rewrite_tree_nodes.py options/stoch_ZC_0.py --debug
python generate_scenario_tree_JB.py options/stoch_ZD_0.py --debug
python rewrite_tree_nodes.py options/stoch_ZD_0.py --debug
python generate_scenario_tree_JB.py options/stoch_ZE_0.py --debug
python rewrite_tree_nodes.py options/stoch_ZE_0.py --debug
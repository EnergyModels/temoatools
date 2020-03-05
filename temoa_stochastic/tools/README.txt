The intent of this file is to provide general guidance about
running Temoa to analyze South Sudan. This version of code is compatible with python 2.7

#############################
Linear Programming
#############################

(Run Temoa with config_sample file)
python temoa_model/ --config=temoa_model/config_sample 

(Single Temoa run)
python temoa_model/temoa_model.py data_files/utopia15.dat --solver=cplex

------------------------------
Stochastic Optimization README
------------------------------

(Solve a stochastic run and store results into a database using config file)
$ python temoa_model/temoa_stochastic.py --config=temoa_model/config_sample
# Note that to invoke the stochastic run, the "--input" flag must be the path
# to ScenarioStructure.dat in the scenario tree directory, and "--output" flag is the #path to the target database file, where the results will be stored.

(Extensive Formulation or Deterministic Equivalent)
runef -m ../../temoa_model/ -i ./ --solver=cplex --solve >> out.txt 

(Progressive Hedging)
runph -m ../../temoa_model/ -i ./ --solver=ipopt --default-rho=1.0 

(Solve a particular path in the tree as a linear program)
python ../../temoa_model/ R.dat Rs0.dat Rs0s2.dat  

#############################
Stochastic Optimization
#############################

Solve a stochastic run and store results into a database using config file:
$ python ../temoa_model/temoa_stochastic.py --config=temoa_model/config_sample

Note that to invoke the stochastic run, the "--input" flag must be the path
to ScenarioStructure.dat, and "--output" flag is the path to the target 
database file, where the results will be stored.

To solve a particular path in the tree as a linear program:
$ python ../temoa_model/ R.dat Rs0.dat Rs0s2.dat  

#############################
Stochastic Optimization Tools
#############################
                                                        
(EVPI computation)
$ python test_EVPI.py                                     
	Note that the EVPI script also includes the stochastic optimization solve, so 
	it does not need to be conducted separately.

(VSS computation)
$ python VSS.py 
	(Information about how to setup a run of VSS):
	Lines 246 - 249 specify the path to the folders and the solver to be used.
	It is necessary to change these lines in order to properly point to the
	instance that you want to solve. The first one just points to the path of the 
	temoa_stochastic.py file. The second one points to the folder of the instance
	where the scenario tree structure and all the scenarios are represented.
	p_model = '../temoa_model/temoa_stochastic.py'
	p_data  = '../tools/options/stoch_Sudan.py'
	optsolver = 'cplex'

	Deterministic file with average values:
	Inside the stochastic folder where you want to run the VSS script, it is necessary to
	manually create an input file to represent the uncertainty with average values. This
	file will be used to run the deterministic instance where we store information about the
	decisions on the first stage.
	The name of the input file is defined on line 195

	Get info about decisions on the first stage:
	On line 147:
	ef._binding_instance.S0s0s0.V_Capacity[iaux1, iaux2].fix(dV_Capacity[iaux1,iaux2])				
	fixes the first stage capacity variables to the solution from the deterministic case using 
	expected values. To calculate VSS, it is necessary to fix the first stage decisions from the deterministic model 
	(solved with average values) when solving the stochastic program (with fixed values) that will 
	be compared to the true stochastic program (without any fixed values).
	Note that the left portion of the expression is the one that is fixed. The specification of this line 
	depends on the total number of time stages. In the example above, there is a total of four stages: 
	.S0s0s0.V_Capacity.fix. If there were 3 stages, it would become S0s0.V_Capacity.fix

	Additional file for EVPI and VSS usage:
	pyomo version 4.3.11388 requires the addition
	of the file ef_writer_script_old.py within the installation
	of pyomo under anaconda. The correct path to add the
	file is: /anaconda/lib/python2.7/site-packages/pyomo/pysp

(Generate Scenario Tree)
python generate_scenario_tree.py options/stoch_Sudan.py  
	Additional files needed for generate scenario tree script:
	pyomo version 4.3.11388 requires the addition
	of the file scenariomodels.py within the installation
	of pyomo under anaconda. The correct path to add the
	file is: /anaconda/lib/python2.7/site-packages/pyomo/pysp/util


Script for Parallel runs of runph:
$ qsub jobTemoa.pbs


#############################
Flow of the analysis for running the stochastic model for South Sudan
#############################

1. Install python 2.7 and pyomo 4.3. 
You can install a specific version of pyomo using the following command
>>>>pip install pyomo==4.3

2. Go to the temoa_ssudan/legacy_files folder to find ef_writer_script_old.py. Copy paste this script at: /anaconda/lib/python2.7/site-packages/pyomo/pysp

3. Go to the temoa_ssudan/legacy_files folder to find scenariomodels.py. Copy paste this script at: /anaconda/lib/python2.7/site-packages/pyomo/pysp/util
 
4. Go to temoa_ssudan/tools folder using the following command
>>>>cd temoa_ssudan/tools

5. Run the following command to generate scenario tree
>>>>python generate_scenario_tree.py options/stoch_Sudan.py

This command will create a directory called S_Sudan in the tools folder. The directory includes the information related to the stochastic scenario tree

6. Go to the newly created S_Sudan directory
>>>>cd S_Sudan

7. Run the following command to solve the extensive stochastic formulation
>>>>runef -m ../../temoa_model/ -i ./ --solver=cplex --solve >> out.txt 

If you want to compute EVPI or VSS then replace step (3) and (4) with the following command
>>>>python EVPI_new.py
OR
>>>>python VSS.py


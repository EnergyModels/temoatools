from __future__ import print_function
import os
import temoatools as tt

# temoa model technologies and corresponding fragility curve groups
techs = {'LOCAL': "inf_stiff",
         'TRANS': "trans",
         'SUB': "sub",
         'DIST': "dist",
         'EX_SOLPV': "solar",
         'EC_SOLPV': "solar",
         'ED_SOLPV': "solar",
         'EX_WIND': "wind",
         'EC_WIND': "wind",
         'ED_WIND': "wind",
         'EX_COAL': "coal_biomass",
         'EC_BIO': "coal_biomass",
         'ED_BIO': "coal_biomass",
         'EX_NG_CC': "natgas_petrol",
         'EC_NG_CC': "natgas_petrol",
         'EC_NG_OC': "natgas_petrol",
         'ED_NG_CC': "natgas_petrol",
         'ED_NG_OC': "natgas_petrol",
         'EX_DSL_SIMP': "natgas_petrol",
         'EX_DSL_CC': "natgas_petrol",
         'EX_OIL_TYPE1': "natgas_petrol",
         'EX_OIL_TYPE2': "natgas_petrol",
         'EX_OIL_TYPE3': "natgas_petrol",
         'EX_MSW_LF': "natgas_petrol",
         'EX_HYDRO': "hydro",
         'EC_BATT': "battery",
         'ED_BATT': "battery"}

# best and worst cast fragility curves for each group
curves = {"inf_stiff": ["inf_stiff", "inf_stiff"], "trans": ["trans_UK_base", "trans_TX"],
          "sub": ["sub_HAZUS_severe_k1", "sub_HAZUS_severe_k5"],
          "dist": ["dist_TX", "dist_60yr"], "wind": ["wind_yaw", "wind_nonyaw"],
          "solar": ["solar_res", "solar_utility"], "coal_biomass": ["secbh_severe", "inf_stiff"],
          "natgas_petrol": ["secbm_severe", "inf_stiff"], "battery": ["secbl_severe", "inf_stiff"],
          "hydro": ["cecbl_severe", "inf_stiff"], }

# databases to use
dbs = ["A.sqlite", "B.sqlite", "C.sqlite", "D.sqlite"]

# Hurricane scenarios with corresponding probabilities and windspeeds
scenarios = ["H1", "H2", "H3"]
probabilities = [0.56, 0.24, 0.2]  # sum must equal 1
windspeeds = [20.0, 50.0, 150.0]  # mph

# model years
years = [2016, 2021, 2026, 2031, 2036]

# Iterate through
for db in dbs:
    db_name = tt.remove_ext(db)

    # Write File
    filename = "stoch_" + db_name + ".txt"
    # Open File
    f = open(filename, "w")
    f.write("# Automatically generated stochastic input file from temoatools github.com/EnergyModels/temoatools\n\n")
    f.write("verbose = True\n")
    f.write("force = True\n")
    f.write("\n")
    f.write("dirname = 'PR_A'\n")  # Update
    f.write("modelpath = '../temoa_model/temoa_model.py'\n")
    f.write("dotdatpath = '../data_files/'" + db_name + ".dat\n")  # Need to check
    f.write("stochasticset = 'time_optimize'\n")
    f.write("stochastic_points = (")
    for year in years:
        f.write(str(year) + ", ")
    f.write(")\n")
    f.write("stochastic_indices = {'CapReduction': 0}\n")
    f.write("types = (\n\t")
    for scenario in scenarios:
        f.write(scenario + ", ")
    f.write("\n")
    f.write(")\n")
    f.write("conditional_probabiliSty = dict(\n")
    for scenario, prob in zip(scenarios, probabilities):
        f.write("\t" + scenario + "=" + str(prob) + ",\n")
    f.write(")\n")
    f.write("rates = {\n")
    f.write("\t'CapReduction': dict(\n")
    for scenario, prob, windspeed in zip(scenarios, probabilities, windspeeds):
        f.write("\t\t"+scenario + "=(\n")
        for tech in techs.keys():
            tech_cat = techs[tech]
            curve = curves[tech_cat][0]
            fragility = tt.fragility(windspeed, curve=curve)
            capReduction = round(1.0 - fragility,3)
            f.write("\t\t\t('" + tech + "', " + str(capReduction) + "),\n")
        f.write("\t\t),\n\n")
    f.write("\t),\n")
    f.write("}\n")

    # Close File
    f.close()


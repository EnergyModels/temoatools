# Automatically generated stochastic input file from temoatools github.com/EnergyModels/temoatools

verbose = True
force = True

dirname = 'XD_0'
modelpath = '../temoa_model/temoa_model.py'
dotdatpath = '../data_files/XD_0.dat'
stochasticset = 'time_optimize'
stochastic_points = (2016, 2021, 2026, 2031, 2036, )
stochastic_indices = {'CapReduction': 0}
types = (
	'H1', 'H2', 'H3', 
)
conditional_probability = dict(
	H1=0.52,
	H2=0.32,
	H3=0.16,
)
rates = {
	'CapReduction': dict(
		H1=(
			('EX_DSL_CC', 1.0),
			('SUB', 1.0),
			('EC_BATT', 0.998),
			('EX_SOLPV', 1.0),
			('DIST_COND', 1.0),
			('EX_COAL', 1.0),
			('EX_HYDRO', 0.998),
			('EX_MSW_LF', 1.0),
			('TRANS', 1.0),
			('ED_NG_OC', 1.0),
			('LOCAL', 1.0),
			('EX_DSL_SIMP', 1.0),
			('ED_NG_CC', 1.0),
			('ED_BATT', 0.998),
			('EC_NG_CC', 1.0),
			('EX_OIL_TYPE3', 1.0),
			('EX_OIL_TYPE2', 1.0),
			('EC_WIND', 1.0),
			('EC_SOLPV', 1.0),
			('UGND_TRANS', 1.0),
			('EX_WIND', 1.0),
			('EX_NG_CC', 1.0),
			('EC_NG_OC', 1.0),
			('ED_WIND', 1.0),
			('UGND_DIST', 1.0),
			('DIST_TWR', 1.0),
			('EC_BIO', 1.0),
			('ED_BIO', 1.0),
			('ED_SOLPV', 1.0),
			('EX_OIL_TYPE1', 1.0),
		),

		H2=(
			('EX_DSL_CC', 1.0),
			('SUB', 0.999),
			('EC_BATT', 0.989),
			('EX_SOLPV', 1.0),
			('DIST_COND', 0.666),
			('EX_COAL', 1.0),
			('EX_HYDRO', 0.989),
			('EX_MSW_LF', 1.0),
			('TRANS', 0.967),
			('ED_NG_OC', 1.0),
			('LOCAL', 1.0),
			('EX_DSL_SIMP', 1.0),
			('ED_NG_CC', 1.0),
			('ED_BATT', 0.989),
			('EC_NG_CC', 1.0),
			('EX_OIL_TYPE3', 1.0),
			('EX_OIL_TYPE2', 1.0),
			('EC_WIND', 0.985),
			('EC_SOLPV', 1.0),
			('UGND_TRANS', 1.0),
			('EX_WIND', 0.985),
			('EX_NG_CC', 1.0),
			('EC_NG_OC', 1.0),
			('ED_WIND', 0.985),
			('UGND_DIST', 1.0),
			('DIST_TWR', 0.739),
			('EC_BIO', 1.0),
			('ED_BIO', 1.0),
			('ED_SOLPV', 1.0),
			('EX_OIL_TYPE1', 1.0),
		),

		H3=(
			('EX_DSL_CC', 0.913),
			('SUB', 0.785),
			('EC_BATT', 0.554),
			('EX_SOLPV', 0.602),
			('DIST_COND', 0.05),
			('EX_COAL', 0.573),
			('EX_HYDRO', 0.582),
			('EX_MSW_LF', 0.913),
			('TRANS', 0.739),
			('ED_NG_OC', 0.913),
			('LOCAL', 1.0),
			('EX_DSL_SIMP', 0.913),
			('ED_NG_CC', 0.913),
			('ED_BATT', 0.554),
			('EC_NG_CC', 0.913),
			('EX_OIL_TYPE3', 0.913),
			('EX_OIL_TYPE2', 0.913),
			('EC_WIND', 0.201),
			('EC_SOLPV', 0.602),
			('UGND_TRANS', 0.913),
			('EX_WIND', 0.201),
			('EX_NG_CC', 0.913),
			('EC_NG_OC', 0.913),
			('ED_WIND', 0.201),
			('UGND_DIST', 0.913),
			('DIST_TWR', 0.177),
			('EC_BIO', 0.573),
			('ED_BIO', 0.573),
			('ED_SOLPV', 0.602),
			('EX_OIL_TYPE1', 0.913),
		),

	),
}

import temoatools as tt

model_filename = 'data_A.sqlite' # Expected to be in "\\databases"
paths = 'paths.csv' # Expected to be in data_path
data_path = 'data'

tt.run(model_filename, paths, saveEXCEL=True, data_path='data',debug=True)
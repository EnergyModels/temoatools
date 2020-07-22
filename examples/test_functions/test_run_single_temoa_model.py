import temoatools as tt

model_filename = 'data_A.sqlite'  # Expected to be in "\\databases"
temoa_path = 'C:/temoa/temoa'  # path to temoa directory that contains temoa_model/

tt.run(model_filename, temoa_path=temoa_path, saveEXCEL=False, debug=True, solver='cplex')

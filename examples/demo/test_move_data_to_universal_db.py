from __future__ import print_function
import temoatools as tt

# file is expected to be in a sub-directory named 'data'
filename = "data.xlsx"

# build db from filename
db = tt.move_data_to_db(filename,path='data')

print "Successfully moved data to: " + db
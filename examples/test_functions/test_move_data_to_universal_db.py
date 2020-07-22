# ======================================================================================================================
# test_move_data_to_universal_db.py
# Jeff Bennett, jab6ft@virginia.edu
# The purpose of this script is to demonstrate the ability of temoatools to move data to a universal database.
# ======================================================================================================================

import temoatools as tt

# file is expected to be in a sub-directory named 'data'
filename = "data.xlsx"

# build db from filename
db = tt.move_data_to_db(filename, path='data')

print("Successfully moved data to: " + str(db))

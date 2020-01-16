
import os
import sys
from os.path import isfile, join
import pandas as pd

#directory = "C:\\temoa_stochastic2\\tools\\WA_0"
#directory = dirname


from os import getcwd
from os.path import abspath, basename, dirname
from time import clock

if len(sys.argv) < 2:
	usage()
module_name = sys.argv[1][:-3].replace('/', '.')  # remove the '.py'

mbase = basename( module_name )[:-3]
mdir  = abspath( dirname( module_name ))
sys.path.insert(0, mdir)

try:
	__import__(module_name)
	opts = sys.modules[ module_name ]
	sys.path.pop(0)
except ImportError:
	msg = ('Unable to import {}.\n\nRun this script with no arguments for '
		   'more information.\n')
	SE.write( msg.format( sys.argv[1] ) )
	raise
	

# Create dataframe to hold probabilities
cols = []
for types in opts.types:
    cols.append(types)
df_rates = pd.DataFrame(columns=cols)
for key in opts.rates['CapReduction'].keys():
    for pair in opts.rates['CapReduction'][key]:
        df_rates.loc[pair[0],key]=pair[1]

# Move to directory
print(os.getcwd())
wrkdir = os.getcwd()
os.chdir(opts.dirname)
dirname = os.getcwd()

# Iterate through Directory
for fname in os.listdir(dirname):
    # Check if it is a file
    if isfile(join(dirname,fname)):
        #print(fname)

        # Check if it is a node file
        if fname[0:2]=='Rs':

            # Determine previous nodes based on file naming convention
            events = []
            ind1 = fname.find('.dat')
            fname2 = fname[0:ind1]
            ind2 = 2
            events.append(opts.types[int(fname2[ind2])])

            while ind2<len(fname2)-1:
                ind2 = ind2 + 2
                events.append(opts.types[int(fname2[ind2])])
            
			# Read-in file
            df = pd.read_csv(fname, skiprows=3, delim_whitespace=True, names=['p','t','v','val'],skipfooter=1, engine='python')

            # Start by resetting all values to 1.0
            df.val = 1.0

            # Get current year and store all relevant calculation years
            year = df.p[0]
            event_years = []
            for i, event in enumerate(events):
                event_years.append(opts.stochastic_points[i])
            # event_years.append(year)

            # Process by technology
            # tech_rates = pd.DataFrame(cols=event_years)
            for tech in df_rates.index:

                # tech_rates = {year:1.0}
                r = 1.0
                for e, y in zip(reversed(events),reversed(event_years)):
                    r = r * df_rates.loc[tech, e]
                    df.loc[(df.v<=y)&(df.t==tech),'val']= r

            # Apply calculations

            # Write to file
            f = open(fname, 'w')
            f.write('# Decision: ')
            for event in events:
                f.write(event+', ')
            f.write('\n\nparam CapReduction:=\n')
            df.to_csv(f,header=False,index=False,sep='\t')
            f.write('\t;\n')
            f.close()

#os.chdir(cwd)
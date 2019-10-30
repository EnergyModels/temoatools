
import os
from os.path import isfile, join
import pandas as pd

# Automatically generated stochastic input file from temoatools github.com/EnergyModels/temoatools

verbose = True
force = True

dirname = 'WA_0'
modelpath = '../temoa_model/temoa_model.py'
dotdatpath = '../data_files/WA_0.dat'
stochasticset = 'time_optimize'
stochastic_points = (2016, 2021, 2026, 2031, 2036,)
stochastic_indices = {'CapReduction': 0}
types = ('H1', 'H2', 'H3',)
conditional_probability = dict(H1=0.52, H2=0.32, H3=0.16, )
rates = {'CapReduction': dict(H1=(
    ('EX_DSL_CC', 1.0), ('SUB', 1.0), ('EC_BATT', 0.998), ('EX_SOLPV', 1.0), ('DIST_COND', 1.0), ('EX_COAL', 1.0),
    ('EX_HYDRO', 0.998), ('EX_MSW_LF', 1.0), ('TRANS', 1.0), ('ED_NG_OC', 1.0), ('LOCAL', 1.0), ('EX_DSL_SIMP', 1.0),
    ('ED_NG_CC', 1.0), ('ED_BATT', 0.998), ('EC_NG_CC', 1.0), ('EX_OIL_TYPE3', 1.0), ('EX_OIL_TYPE2', 1.0),
    ('EC_WIND', 1.0), ('EC_SOLPV', 1.0), ('UGND_TRANS', 1.0), ('EX_WIND', 1.0), ('EX_NG_CC', 1.0), ('EC_NG_OC', 1.0),
    ('ED_WIND', 1.0), ('UGND_DIST', 1.0), ('DIST_TWR', 1.0), ('EC_BIO', 1.0), ('ED_BIO', 1.0), ('ED_SOLPV', 1.0),
    ('EX_OIL_TYPE1', 1.0),),

    H2=(('EX_DSL_CC', 1.0), ('SUB', 0.999), ('EC_BATT', 0.989), ('EX_SOLPV', 1.0), ('DIST_COND', 0.666),
        ('EX_COAL', 1.0), ('EX_HYDRO', 0.989), ('EX_MSW_LF', 1.0), ('TRANS', 0.967), ('ED_NG_OC', 1.0), ('LOCAL', 1.0),
        ('EX_DSL_SIMP', 1.0), ('ED_NG_CC', 1.0), ('ED_BATT', 0.989), ('EC_NG_CC', 1.0), ('EX_OIL_TYPE3', 1.0),
        ('EX_OIL_TYPE2', 1.0), ('EC_WIND', 0.985), ('EC_SOLPV', 1.0), ('UGND_TRANS', 1.0), ('EX_WIND', 0.985),
        ('EX_NG_CC', 1.0), ('EC_NG_OC', 1.0), ('ED_WIND', 0.985), ('UGND_DIST', 1.0), ('DIST_TWR', 0.739),
        ('EC_BIO', 1.0), ('ED_BIO', 1.0), ('ED_SOLPV', 1.0), ('EX_OIL_TYPE1', 1.0),),

    H3=(('EX_DSL_CC', 0.913), ('SUB', 0.785), ('EC_BATT', 0.554), ('EX_SOLPV', 0.602), ('DIST_COND', 0.05),
        ('EX_COAL', 0.573), ('EX_HYDRO', 0.582), ('EX_MSW_LF', 0.913), ('TRANS', 0.739), ('ED_NG_OC', 0.913),
        ('LOCAL', 1.0), ('EX_DSL_SIMP', 0.913), ('ED_NG_CC', 0.913), ('ED_BATT', 0.554), ('EC_NG_CC', 0.913),
        ('EX_OIL_TYPE3', 0.913), ('EX_OIL_TYPE2', 0.913), ('EC_WIND', 0.201), ('EC_SOLPV', 0.602),
        ('UGND_TRANS', 0.913), ('EX_WIND', 0.201), ('EX_NG_CC', 0.913), ('EC_NG_OC', 0.913), ('ED_WIND', 0.201),
        ('UGND_DIST', 0.913), ('DIST_TWR', 0.177), ('EC_BIO', 0.573), ('ED_BIO', 0.573), ('ED_SOLPV', 0.602),
        ('EX_OIL_TYPE1', 0.913),),

), }







directory = "C:\\temoa_stochastic2\\tools\\WA_0"

# Create dataframe to hold probabilities
cols = []
for types_ in types:
    cols.append(types_)
df_rates = pd.DataFrame(columns=cols)
for key in rates['CapReduction'].keys():
    for pair in rates['CapReduction'][key]:
        df_rates.loc[pair[0],key]=pair[1]

# Move to directory
cwd = os.getcwd()
os.chdir(directory)

# Iterate through Directory
for fname in os.listdir(directory):
    # Check if it is a file
    if isfile(join(directory,fname)):

        # Check if it is a node file
        if fname[0:2]=='Rs':

            # Determine previous nodes based on file naming convention
            events = []
            ind1 = fname.find('.dat')
            fname2 = fname[0:ind1]
            ind2 = 2
            events.append(types[int(fname2[ind2])])

            while ind2<len(fname2)-1:
                ind2 = ind2 + 2
                events.append(types[int(fname2[ind2])])

            # Read-in file
            df = pd.read_csv(fname, skiprows=3, delim_whitespace=True, names=['p','t','v','val'],skipfooter=1, engine='python')

            # Start by resetting all values to 1.0
            df.val = 1.0

            # Get current year and store all relevant calculation years
            year = df.p[0]
            event_years = []
            for i, event in enumerate(events):
                event_years.append(stochastic_points[i])
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

os.chdir(cwd)
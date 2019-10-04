import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Read Data
df = pd.read_csv("hurricaneData.csv")

# Add-in 'None' Category

for year in np.arange(1979,2016,1):
    if sum(df.Year==year)==0:
        s = pd.Series(index=['Name', 'Year', 'Category', 'MaxWind_Kts', 'MaxWind_mph'])
        s['Name'] = 'None'
        s['Year'] = year
        s['Category'] = 'None'
        s['MaxWind_Kts'] = 0.0
        s['MaxWind_mph'] = 0.0
        df = df.append(s,ignore_index=True)
        print year

# Storm Category Analysis

starts = np.arange(1979,1997,1)
step = 5
stop = 2017

cols_prob = ['Start', 'Stop','Interval', 'Years', 'None', 'TD', 'TS', 'H1', 'H2', 'H3', 'H4', 'H5']
probs = pd.DataFrame(columns=cols_prob)

for start in starts:

    # years = stop - start
    bins = np.arange(start,stop+step,step)
    years = bins[-1] - bins[0]
    stop_year = bins[-1]

    cols = ['Low','High','MaxCategory','MaxWind_kts','MaxWind_mph']
    results = pd.DataFrame(columns=cols)

    for i in range(len(bins)-1):
        low = bins[i]
        high = bins[i+1]


        slice = df.loc[(df.Year > low) & (df.Year <= high)]
        if len(slice)> 0:
            sorted = slice.sort_values("MaxWind_Kts", ascending=False)
            MaxCategory = sorted.Category[sorted.index[0]]
            MaxWind_kts = sorted.MaxWind_Kts[sorted.index[0]]
            MaxWind_mph = sorted.MaxWind_mph[sorted.index[0]]
        else:
            MaxCategory = "None"
            MaxWind_kts = 0.0
            MaxWind_mph = 0.0


        # Store Results
        result = pd.Series(index=cols)
        result['Low'] = int(low)
        result['High'] = int(high)
        result['MaxCategory'] = MaxCategory
        result['MaxWind_kts'] = MaxWind_kts
        result['MaxWind_mph'] = MaxWind_mph
        results = results.append(result, ignore_index=True)


    # Calculate Probabilities
    none = sum(results.MaxCategory == "None")
    TD = sum(results.MaxCategory == "TD")
    TS = sum(results.MaxCategory == "TS")
    H1 = sum(results.MaxCategory == "H1")
    H2 = sum(results.MaxCategory == "H2")
    H3 = sum(results.MaxCategory == "H3")
    H4 = sum(results.MaxCategory == "H4")
    H5 = sum(results.MaxCategory == "H5")
    total = none + TD + TS + H1 + H2 + H3 + H4 + H5

    # Store Probabilities
    prob = pd.Series(index=cols_prob)
    prob['Start'] = start
    prob['Stop'] = stop_year
    prob['Interval'] = step
    prob['Years'] = years
    prob['None'] = float(none)/float(total)
    prob['TD'] = float(TD) / float(total)
    prob['TS'] = float(TS) / float(total)
    prob['H1'] = float(H1)/float(total)
    prob['H2'] = float(H2) / float(total)
    prob['H3'] = float(H3)/float(total)
    prob['H4'] = float(H4) / float(total)
    prob['H5'] = float(H5)/float(total)
    probs = probs.append(prob,ignore_index=True)

plt.figure()
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)] # Custom palette
sns.set_style('whitegrid')
sns.set_context('paper')
probs2 = pd.melt(probs,id_vars=["Years"],var_name="Category",value_vars=["None","TD","TS","H1","H2","H3","H4","H5"])
ax = sns.catplot(x="Category",y="value",hue="Years",kind="bar", data=probs2)
ax.set_xlabels('Maximum Storm Category (-)')
ax.set_ylabels('Probability (-)')

# plt.text(0.1, 0.9, 'A', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize='medium',fontweight='bold')
plt.text(0.1, 0.9, 'A', horizontalalignment='center',verticalalignment='center', fontsize='medium',fontweight='bold')

plt.savefig("Hurricane_Probabilities.png",dpi=1000)

# Storm Wind Speed Analysis V2

comb_data = pd.DataFrame()

years = [25,30,35,40]
for year in years:
    start_year = 2017 - year
    slice = df.loc[(df.Year > start_year)]
    slice["Years"] = year
    comb_data = comb_data.append(slice)

ax = sns.catplot(x="Category", y="MaxWind_mph", hue="Years",kind="bar", data=comb_data,order = ["TD", "TS","H1","H2","H3","H4","H5"])
ax.set_xlabels('Storm Category (-)')
ax.set_ylabels('Maximum Windspeed (mph)')
plt.savefig("Hurricane_Windspeeds_Comparison.png", dpi=1000)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Read Data
df = pd.read_csv("hurricaneData.csv")

# Add-in 'None' Category
for year in np.arange(1979, 2016, 1):
    if sum(df.Year == year) == 0:
        s = pd.Series(index=['Name', 'Year', 'Category', 'MaxWind_Kts', 'MaxWind_mph'])
        s['Name'] = 'None'
        s['Year'] = year
        s['Category'] = 'None'
        s['MaxWind_Kts'] = 0.0
        s['MaxWind_mph'] = 0.0
        df = df.append(s, ignore_index=True)

# Categorization
cat = {'None': 'Low', 'TD': 'Low', 'TS': 'Low', 'H1': 'Low', 'H2': 'Medium', 'H3': 'Medium', 'H4': 'High', 'H5': 'High'}

# Storm Category Analysis

starts = np.arange(1979, 1997, 1)
step = 5
stop = 2017

cols_prob = ['Start', 'Stop', 'Interval', 'Years', 'Low', "Medium", "High"]
probs = pd.DataFrame(columns=cols_prob)

for start in starts:

    # years = stop - start
    bins = np.arange(start, stop + step, step)
    years = bins[-1] - bins[0]
    stop_year = bins[-1]

    cols = ['Low', 'High', 'MaxCategory', 'MaxWind_kts', 'MaxWind_mph']
    results = pd.DataFrame(columns=cols)

    for i in range(len(bins) - 1):
        low = bins[i]
        high = bins[i + 1]

        slice = df.loc[(df.Year > low) & (df.Year <= high)]
        if len(slice) > 0:
            sorted = slice.sort_values("MaxWind_Kts", ascending=False)
            MaxCategory = cat[sorted.Category[sorted.index[0]]]
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
    low = sum(results.MaxCategory == "Low")
    med = sum(results.MaxCategory == "Medium")
    high = sum(results.MaxCategory == "High")
    total = low + med + high

    # Store Probabilities
    prob = pd.Series(index=cols_prob)
    prob['Start'] = start
    prob['Stop'] = stop_year
    prob['Interval'] = step
    prob['Years'] = years
    prob['Low'] = float(low) / float(total)
    prob['Medium'] = float(med) / float(total)
    prob['High'] = float(high) / float(total)
    probs = probs.append(prob, ignore_index=True)

custom_palette = [(0.380, 0.380, 0.380), (0.957, 0.451, 0.125), (.047, 0.149, 0.361),
                  (0.847, 0.000, 0.067)]  # Custom palette
sns.set_style('whitegrid')
sns.set_context('talk')



probs2 = pd.melt(probs, id_vars=["Years"], var_name="Category", value_vars=["Low", "Medium", "High"])

rename = {'Low': '1', 'Medium': '2-3', 'High': '4-5'}
for key in rename.keys():
    ind = probs2.loc[:, "Category"] == key
    probs2.loc[ind, "Category"] = rename[key]
ax = sns.catplot(x="Category", y="value", hue="Years", kind="bar", data=probs2)
ax.set_xlabels('Hurricane Category (-)')
ax.set_ylabels('Probability (-)')
plt.savefig("Hurricane_Probabilities_categorized.png", dpi=1000)

# Storm Wind Speed Analysis V2

comb_data = pd.DataFrame()

for index, row in df.iterrows():
    df.loc[index, 'Category'] = cat[row['Category']]

years = [25, 30, 35, 40]
for year in years:
    start_year = 2017 - year
    slice = df.loc[(df.Year > start_year)]
    slice["Years"] = year
    comb_data = comb_data.append(slice)
# Rename for plot
for key in rename.keys():
    ind = comb_data.loc[:, "Category"] == key
    comb_data.loc[ind, "Category"] = rename[key]

ax = sns.catplot(x="Category", y="MaxWind_mph", hue="Years", kind="bar", data=comb_data,
                 order=["1", "2-3", "4-5"])
ax.set_xlabels('Hurricane Category (-)')
ax.set_ylabels('Maximum Windspeed (mph)')
plt.savefig("Hurricane_Windspeeds_Comparison_categorized.png", dpi=1000)

# Write results to terminal
categories = ['Low', 'Medium', 'High']
for cat in categories:
    mph = df.loc[df.loc[:, "Category"] == cat, "MaxWind_mph"].mean()
    prob = probs2.loc[probs2.loc[:, "Category"] == cat, "value"].mean()
    print(cat)
    print('Windspeed (mph): ' + str(round(mph, 0)))
    print('Probability (-): ' + str(round(prob, 2)))

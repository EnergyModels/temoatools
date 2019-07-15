# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import pi

sns.set_style('white')

# Set data
# df = pd.read_csv("combinedResults_bar.csv")
df = pd.read_csv("combinedResults_bar_all.csv")
figsize = (6,5)
#============================
# Version 1
#============================
ax = sns.barplot(y="Scenario",x="Value",hue="Metric",data=df,palette="colorblind",ci="sd")
leg = plt.legend(bbox_to_anchor=(0.35, -0.2), loc='center', ncol=2, frameon = False)
savename = 'combined_results_bar.png'
plt.savefig(savename, dpi=1000, bbox_inches="tight")

#============================
# Version 2
#============================
order = ["LCOE (cents/kWh)", "2052 COE (10 cents/kWh)","Avg. Emissions (Gton/yr)","2052 Emissions (Gton/yr)","Build-back time (100 days)","Initial Outage (million people)"]
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)]

plt.figure(figsize=figsize)
ax = sns.barplot(y="Metric",x="Value",hue="Scenario",data=df,palette=custom_palette,ci="sd",order=order,errcolor="black")#,n_boot=1E4)
leg = plt.legend(bbox_to_anchor=(0.35, -0.2), loc='center', ncol=2, frameon = False)
savename = 'combined_results_bar_V2.png'
plt.savefig(savename, dpi=1000, bbox_inches="tight")


#============================
# Version 3
#============================
order = ["LCOE (cents/kWh)", "2052 COE (10 cents/kWh)","Avg. Emissions (Gton/yr)","2052 Emissions (Gton/yr)","Build-back time (100 days)","Initial Outage (million people)"]
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)]

plt.figure(figsize=figsize)
ax = sns.boxplot(y="Metric",x="Value",hue="Scenario",data=df,palette=custom_palette,order=order)
leg = plt.legend(bbox_to_anchor=(0.35, -0.2), loc='center', ncol=2, frameon = False)
savename = 'combined_results_bar_V3.png'
plt.savefig(savename, dpi=1000, bbox_inches="tight")
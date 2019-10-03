from __future__ import print_function
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import temoatools as tt
# Questions:
# Does wind need correlation from 90m height to ground height?

# =============================================================================#
# Compare Fragility Curves
# =============================================================================#

# Fragility Curves to compare
curves = {"trans": ["trans"], "sub": ["sub"], "dist": ["dist_20yr", "dist_40yr", "dist_60yr"],
    "wind": ["wind_yaw", "wind_nonyaw"], "solar": ["solar_res", "solar_utility"],
    "coal_biomass": ["secbh_moderate", "secbh_severe", "inf_stiff"],
    "natgas_petrol": ["secbm_moderate", "secbm_severe", "inf_stiff"],
    "battery": ["secbl_moderate", "secbl_severe", "inf_stiff"],
    "hydro": ["cecbl_moderate", "cecbl_severe", "inf_stiff"], }

group1 = "T&D"
group2 = "Renew"
group3 = "Other"

groups = {"trans":group1, "sub":group1, "dist": group1,
    "wind":group2 , "solar":group2 ,
    "coal_biomass":group1 ,
    "natgas_petrol":group3 ,
    "battery": group3,
    "hydro":group2, }

# ================================#
# Calculate damage across a range of windspeeds
# ================================#

cols = ["tech","type","group","wind_mph","p_failure"]
df = pd.DataFrame(columns=cols)
wind_mph = np.arange(0, 200, 2)

for tech in curves.keys():
    for type in curves[tech]:
        print(type)
        p_failure = tt.fragility(wind_mph,type=type)

        for w,p in zip(wind_mph,p_failure):
            s = pd.Series()
            s["tech"] = tech
            s["type"] = type
            s["group"] = groups[tech]
            s["wind_mph"] = w
            s["p_failure"] = p
            df = df.append(s,ignore_index=True)


sns.lineplot(x="wind_mph",y="p_failure",hue="tech",data=df)
plt.savefig("compare_all.png",  DPI=1000)

sns.relplot(x="wind_mph",y="p_failure",hue="tech",col="group",col_wrap=3,data=df,kind="line")
plt.savefig("compare_by_group.png",  DPI=1000)

sns.relplot(x="wind_mph",y="p_failure",hue="type",col="tech",col_wrap=3,data=df,kind="line")
plt.savefig("compare_by_tech.png",  DPI=1000)
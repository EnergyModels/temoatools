from __future__ import print_function
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import temoatools as tt

# =============================================================================#
# Compare Fragility Curves
# =============================================================================#

# Fragility Curves to compare
curves = {"trans": ["trans_UK_base", "trans_TX"], "sub": ["sub_HAZUS_severe_k1", "sub_HAZUS_severe_k5"],
          "dist": ["dist_TX", "dist_60yr"], "wind": ["wind_yaw", "wind_nonyaw"],
          "solar": ["solar_res", "solar_utility"], "coal_biomass": ["secbh_severe", "inf_stiff"],
          "natgas_petrol": ["secbm_severe", "inf_stiff"], "battery": ["secbl_severe", "inf_stiff"],
          "hydro": ["cecbl_severe", "inf_stiff"], }

group1 = "T&D"
group2 = "Renew"
group3 = "Other"

groups = {"trans": group1, "sub": group1, "dist": group1, "wind": group2, "solar": group2, "coal_biomass": group3,
          "natgas_petrol": group3, "battery": group3, "hydro": group2, }

# ================================#
# Calculate damage across a range of windspeeds
# ================================#

cols = ["tech", "type", "group", "wind_mph", "p_failure"]
df = pd.DataFrame(columns=cols)
wind_mph = np.arange(0, 200, 2)

for tech in curves.keys():
    for curve in curves[tech]:
        p_failure = tt.fragility(wind_mph, curve=curve)

        for w, p in zip(wind_mph, p_failure):
            s = pd.Series()
            s["tech"] = tech
            s["curve"] = curve
            s["group"] = groups[tech]
            s["wind_mph"] = w
            s["p_failure"] = p
            df = df.append(s, ignore_index=True)

sns.lineplot(x="wind_mph", y="p_failure", hue="tech", data=df)
plt.savefig("fragility_curves_all.png", DPI=1000)

sns.relplot(x="wind_mph", y="p_failure", hue="tech", col="group", col_wrap=3, data=df, kind="line")
plt.savefig("fragility_curves_by_group.png", DPI=1000)

sns.relplot(x="wind_mph", y="p_failure", hue="curve", col="tech", col_wrap=3, data=df, kind="line")
plt.savefig("fragility_curves_by_tech.png", DPI=1000)

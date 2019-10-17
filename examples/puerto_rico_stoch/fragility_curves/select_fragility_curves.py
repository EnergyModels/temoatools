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
curves = {"trans": ["trans_UK_base",], "sub": ["sub_HAZUS_severe_k3", ],
        "dist_cond": ["dist_cond_TX"],
          "dist_twr": ["dist_60yr"], "wind": [ "wind_nonyaw"],
          "solar": ["solar_utility"], "coal_biomass": ["secbh_moderate",],
          "natgas_petrol": ["secbm_moderate", ], "battery": ["secbl_moderate",] ,
          "hydro": ["cecbl_moderate",], "UGND":["secbl_destr"]}

group1 = "T&D"
group2 = "Renew"
group3 = "Other"

groups = {"trans": group1, "sub": group1, "dist_twr": group1, "dist_cond": group1, "wind": group2, "solar": group2, "coal_biomass": group3,
          "natgas_petrol": group3, "battery": group3, "hydro": group2, "UGND": group1}

# ================================#
# Calculate damage across a range of windspeeds
# ================================#

cols = ["tech", "curve", "group", "wind_mph", "p_failure"]
df = pd.DataFrame(columns=cols)
wind_mph = np.arange(0, 160, 2)

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

# ================================#
# Compare best and worst case scenarios
# ================================#

# best and worst case fragility curves for each group
# curves_best = {"trans": "trans_TX", "sub": "sub_HAZUS_severe_k5", "dist_cond": "dist_cond_TX",
#                "dist_twr": "dist_TX", "wind": "wind_yaw", "solar": "solar_utility",
#                "coal_biomass": "secbh_severe",
#                "natgas_petrol": "secbm_severe",
#                "battery": "secbl_severe",
#                "hydro": "cecbl_severe", "UGND":"secbl_severe"}

# curves = {"trans": "trans_UK_base",
#                 "sub": "sub_HAZUS_severe_k3", "dist_cond": "dist_cond_TX", "dist_twr": "dist_60yr", "wind": "wind_nonyaw",
#                 "solar": "solar_utility",
#                 "coal_biomass": "secbh_moderate",
#                 "natgas_petrol": "secbm_moderate",
#                 "battery": "secbl_moderate",
#                 "hydro": "cecbl_moderate",
#                 "UGND":"secbl_severe"}

curves = {"trans": "trans_UK_base",
                "sub": "sub_HAZUS_severe_k3", "dist_cond": "dist_cond_TX", "dist_twr": "dist_60yr", "wind": "wind_nonyaw",
                "solar": "solar_utility",
                "coal_biomass": "secbh_severe",
                "natgas_petrol": "secbm_severe",
                "battery": "secbl_severe",
                "hydro": "cecbl_severe",
                "UGND":"secbl_severe"}


cols = ["tech", "curve", "group", "wind_mph", "p_failure"]
df_best = pd.DataFrame(columns=cols)
# df_worst = pd.DataFrame(columns=cols)
wind_mph = np.arange(0, 160, 2)

# for curve_best_key,curve_worst_key in zip(curves_best, curves_worst):
#     p_failure_best = tt.fragility(wind_mph, curve=curves_best[curve_best_key])
#     p_failure_worst = tt.fragility(wind_mph, curve=curves_worst[curve_worst_key])
#
#     for w, p_best, p_worst in zip(wind_mph, p_failure_best, p_failure_worst):
#         s = pd.Series()
#         s["tech"] = tech
#
#         s["group"] = groups[tech]
#         s["wind_mph"] = w
#
#         s["curve"] = curve_best_key
#         s["p_failure"] = p_best
#         df_best = df_best.append(s, ignore_index=True)
#
#         s["curve"] = curve_worst_key
#         s["p_failure"] = p_worst
#         df_worst = df_worst.append(s, ignore_index=True)

# curves = curves_best
for curve_key in curves:
    p_failure = tt.fragility(wind_mph, curve=curves[curve_key])

    for w, p in zip(wind_mph, p_failure):
        s = pd.Series()
        s["tech"] = curve_key
        s["group"] = groups[curve_key]
        s["wind_mph"] = w
        s["curve"] = curves[curve_key]
        s["p_failure"] = p
        df_best = df_best.append(s, ignore_index=True)

# curves = curves_worst
# for curve_key in curves:
#     p_failure = tt.fragility(wind_mph, curve=curves[curve_key])
#
#     for w, p in zip(wind_mph, p_failure):
#         s = pd.Series()
#         s["tech"] = curve_key
#         s["group"] = groups[curve_key]
#         s["wind_mph"] = w
#         s["curve"] = curves[curve_key]
#         s["p_failure"] = p
#         df_worst = df_worst.append(s, ignore_index=True)

sns.relplot(x="wind_mph", y="p_failure", hue="tech", col="group", col_wrap=3, data=df_best, kind="line")
plt.savefig("fragility_curves_by_group_best.png", DPI=1000)


# sns.relplot(x="wind_mph", y="p_failure", hue="tech", col="group", col_wrap=3, data=df_worst, kind="line")
# plt.savefig("fragility_curves_by_group_worst.png", DPI=1000)

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import temoatools as tt
import pandas as pd

# =============================================================================#
# Select Fragility Curves
# =============================================================================#
curves = {"trans": "trans_UK_base",
          "sub": "sub_HAZUS_severe_k3",
          "dist_cond": "dist_cond_TX",
          "dist_twr": "dist_60yr",
          "wind": "wind_nonyaw",
          "solar": "solar_utility",
          "coal_biomass": "secbh_severe",
          "natgas_petrol": "secbm_severe",
          "battery": "secbl_severe",
          "hydro": "cecbl_severe",
          "UGND": "secbm_severe"}

# ================================#
# Calculate damage across a range of windspeeds
# ================================#

mph = np.arange(0.1, 178, 1)  # 80 m/s
# mph = np.arange(0.1, 223, 1) # 100 m/s
ms = mph * 0.44704
trans = tt.fragility(mph, curve=curves['trans'])
sub = tt.fragility(mph, curve=curves['sub'])
dist_cond = tt.fragility(mph, curve=curves['dist_cond'])
dist_twr = tt.fragility(mph, curve=curves['dist_twr'])
UGND = tt.fragility(mph, curve=curves['UGND'])

coal_biomass = tt.fragility(mph, curve=curves['coal_biomass'])
natgas_petrol = tt.fragility(mph, curve=curves['natgas_petrol'])

wind = tt.fragility(mph, curve=curves['wind'])
solar = tt.fragility(mph, curve=curves['solar'])
hydro = tt.fragility(mph, curve=curves['hydro'])
battery = tt.fragility(mph, curve=curves['battery'])

# ================================#
# Plot - Compare Used Damage Functions
# ================================#
plt.figure(1)
# plt.subplots(constrained_layout=True)
f = plt.gcf()
width = 3.58  # inches
height = 3.58  # inches
f.set_size_inches(height, width)  # s
# sns.set_style("white")
sns.set_style("white", {"font.family": "serif", "font.serif": ["Times", "Palatino", "serif"]})
sns.set_context("paper")
sns.set_palette("colorblind")
colors = sns.color_palette('colorblind')

plt.plot(ms, dist_cond, label="Distribution lines", color=colors[0])
plt.plot(ms, wind, label="Wind turbines", color=colors[2])
plt.plot(ms, dist_twr, label="Distribution towers", color=colors[5])

plt.plot(ms, solar, label="Solar panels", color=colors[8])
plt.plot(ms, coal_biomass, '--', label="Coal & biomass power plants", color=colors[7])
plt.plot(ms, battery, label="Battery storage plants", color=colors[3])
plt.plot(ms, hydro, '--', label="Hydroelectric power plants", color=colors[9])

plt.plot(ms, sub, '--', label="Substations", color=colors[6])

plt.plot(ms, trans, label="Transmission lines", color=colors[4])
plt.plot(ms, natgas_petrol, label="Natural gas, oil, diesel \n& landfill gas power plants", color=colors[1])
plt.plot(ms, UGND, ':', label="Buried lines", color=colors[0])

# Legend and Labels
# plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', ncol=1, frameon=False)
# plt.legend(bbox_to_anchor=(0.1, 0.6), loc='center left', ncol=1, frameon=True)
plt.ylabel("Probability of damage (-)")
plt.xlabel("Wind speed ($ms^{-1}$)")

# Add vertical lines for category cases
y = [0, 1.02]
low = 22. * 0.44704  # mph to m/s
med = 113.0 * 0.44704
high = 154.0 * 0.44704

plt.plot([low, low], y, color="gray")
plt.plot([med, med], y, color="gray")
plt.plot([high, high], y, color="gray")

y_txt = 1.03
plt.text(low, y_txt, "1", ha="center")
plt.text(med, y_txt, "2-3", ha="center")
plt.text(high, y_txt, "4-5", ha="center")
plt.text((low + high) / 2.0, y_txt + 0.07, "Hurricane category", ha="center")

sns.despine()

# Save and show
plt.savefig("Figure4_fragility_curves_selected_ms.png", dpi=1000, bbox_inches="tight")

# --------------------------
# write out results to csv
# --------------------------
low = low / 0.44704  # m/s back to mph
med = med / 0.44704
high = high / 0.44704

entries = ['technology', 'curve', 'low', 'med', 'high']

curve_order = ["dist_cond", "wind", "dist_twr", "solar", "coal_biomass",
               "battery", "hydro", "sub", "trans", "natgas_petrol", "UGND"]
df = pd.DataFrame(columns=entries)
for curve in curve_order:
    s = pd.Series(index=entries)
    s['technology'] = curve
    s['curve'] = curves[curve]
    s['low'] = 1.0 - tt.fragility(low, curve=curves[curve])
    s['med'] = 1.0 - tt.fragility(med, curve=curves[curve])
    s['high'] = 1.0 - tt.fragility(high, curve=curves[curve])
    df = df.append(s, ignore_index=True)
df.to_csv('fragility_curve_summary.csv')

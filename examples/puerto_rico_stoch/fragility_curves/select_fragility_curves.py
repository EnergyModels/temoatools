from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import temoatools as tt

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

mph = np.arange(0, 200, 1)
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

plt.plot(mph, dist_cond, label="Distribution Line", color=colors[0])
plt.plot(mph, dist_twr, label="Distribution Tower", color=colors[5])
plt.plot(mph, trans, label="Transmission", color=colors[4])

plt.plot(mph, wind, label="Wind", color=colors[2])
plt.plot(mph, battery,  label="Battery", color=colors[3])
plt.plot(mph, hydro, '--', label="Hydro", color=colors[9])

plt.plot(mph, coal_biomass, '--', label="Coal & Biomass", color=colors[7])
plt.plot(mph, solar, label="Solar", color=colors[8])
plt.plot(mph, sub, '--', label="Substation", color=colors[6])
plt.plot(mph, natgas_petrol, label="Natural Gas, Oil, \nDiesel & Landfill Gas", color=colors[1])
plt.plot(mph, UGND, ':', label="Buried Lines", color=colors[0])

# Legend and Labels
# plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', ncol=1, frameon=False)
# plt.legend(bbox_to_anchor=(0.1, 0.6), loc='center left', ncol=1, frameon=True)
plt.ylabel("Probability of Damage (-)")
plt.xlabel("Windspeed (mph)")

# Add vertical lines for category cases
y = [0, 1.0]
low = 22.
med = 113.0
high = 154.0

plt.plot([low, low], y, color="black")
plt.plot([med, med], y, color="black")
plt.plot([high, high], y, color="black")

y_txt = 1.05
plt.text(low, y_txt, "Low", ha="center")
plt.text(med, y_txt, "Medium", ha="center")
plt.text(high, y_txt, "High", ha="center")

sns.despine()

# Save and show
plt.savefig("fragility_curves_selected.png", dpi=1000, bbox_inches="tight")


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

mph = np.arange(0.1, 178, 1) # 80 m/s
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

plt.plot(ms, dist_cond, label="Distribution line", color=colors[0])
plt.plot(ms, wind, label="Wind", color=colors[2])
plt.plot(ms, dist_twr, label="Distribution tower", color=colors[5])

plt.plot(ms, solar, label="Solar", color=colors[8])
plt.plot(ms, coal_biomass, '--', label="Coal & biomass", color=colors[7])
plt.plot(ms, battery,  label="Battery", color=colors[3])
plt.plot(ms, hydro, '--', label="Hydro", color=colors[9])

plt.plot(ms, sub, '--', label="Substation", color=colors[6])

plt.plot(ms, trans, label="Transmission", color=colors[4])
plt.plot(ms, natgas_petrol, label="Natural gas, oil, \ndiesel & landfill gas", color=colors[1])
plt.plot(ms, UGND, ':', label="Buried lines", color=colors[0])

# Legend and Labels
# plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', ncol=1, frameon=False)
# plt.legend(bbox_to_anchor=(0.1, 0.6), loc='center left', ncol=1, frameon=True)
plt.ylabel("Probability of damage (-)")
plt.xlabel("Windspeed (m/s)")

# Add vertical lines for category cases
y = [0, 1.02]
low = 22.*0.44704 # mph to m/s
med = 113.0*0.44704
high = 154.0*0.44704

plt.plot([low, low], y, color="gray")
plt.plot([med, med], y, color="gray")
plt.plot([high, high], y, color="gray")

y_txt = 1.03
plt.text(low, y_txt, "1", ha="center")
plt.text(med, y_txt, "2-3", ha="center")
plt.text(high, y_txt, "4-5", ha="center")
plt.text((low+high)/2.0, y_txt+0.07, "Hurricane category", ha="center")

sns.despine()

# Save and show
plt.savefig("Figure4_fragility_curves_selected_ms.png", dpi=1000, bbox_inches="tight")


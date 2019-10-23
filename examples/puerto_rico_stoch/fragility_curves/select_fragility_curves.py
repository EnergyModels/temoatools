from __future__ import print_function
import numpy as np
import pandas as pd
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
          "UGND": "secbl_severe"}

# ================================#
# Calculate damage across a range of windspeeds
# ================================#

mph = np.arange(0, 180, 2)
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
sns.set_style("white")
sns.set_context("talk")
plt.plot(mph, trans, label="Transmission")
plt.plot(mph, sub, label="Substation")
plt.plot(mph, dist_cond, label="Distribution Lines")
plt.plot(mph, dist_twr, label="Distribution Tower")
plt.plot(mph, UGND, label="Buried Lines")

plt.plot(mph, coal_biomass, '--', label="Coal + Biomass")
plt.plot(mph, natgas_petrol, '--', label="NG, Oil, Diesel, Landfill Gas")

plt.plot(mph, wind, label="Wind")
plt.plot(mph, solar, label="Solar")
plt.plot(mph, hydro, '--', label="Hydro")
plt.plot(mph, battery, '--', label="Battery")

# Legend and Labels
plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
plt.ylabel("Probability of Damage (-)")
plt.xlabel("Windspeed (mph)")

# Add vertical lines for category cases
y = [0, 1.0]
low = 20
med = 50
high = 150

plt.plot([low, low], y, color="black", label="Low")
plt.plot([med, med], y, color="black", label="Medium")
plt.plot([high, high], y, color="black", label="High")

y_txt = 1.05
plt.text(low, y_txt, "Category 1", ha="center")
plt.text(med, y_txt, "Category 2-3", ha="center")
plt.text(high, y_txt, "Category 4-5", ha="center")

# Save and show
plt.savefig("fragility_curves_selected.png", dpi=1000, bbox_inches="tight")

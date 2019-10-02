# =============================================================================#
# Fragility Curves
# Written by Claire Trevisan and Jeff Bennett
# =============================================================================#

import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
import temoatools as tt


from damageFunctions import trans_damage, sub_damage, dist_damage, wind_damage, solar_damage, \
    SECBL_moderate, SECBM_moderate, SECBH_moderate, CECBL_moderate, CECBM_moderate, CECBH_moderate, \
    SECBL_severe, SECBM_severe, SECBH_severe, CECBL_severe, CECBM_severe, CECBH_severe

# ================================#
# Calculate damage across a range of windspeeds
# ================================#

mph = np.arange(0, 160, 2)
dist = dist_damage(mph)
sub = sub_damage(mph)
trans = trans_damage(mph)
solar = solar_damage(mph)
wind = wind_damage(mph)
CECBL = CECBL_moderate(mph)
CECBM = CECBM_moderate(mph)
CECBH = CECBH_moderate(mph)
SECBL = SECBL_moderate(mph)
SECBM = SECBM_moderate(mph)
SECBH = SECBH_moderate(mph)

# Add substations to Temoa? And number of miles of dist, trans?

# ================================#
# Plot 1 - Compare Used Damage Functions
# ================================#
plt.figure(1)
sns.set_style("darkgrid")
plt.plot(mph, dist, label="dist")
plt.plot(mph, sub, label="sub")
plt.plot(mph, trans, label="trans")
plt.plot(mph, solar, label="solar")
plt.plot(mph, wind, label="wind")
plt.plot(mph, CECBM, '--', label="CECBM - Hydro?")
plt.plot(mph, SECBM, '--', label="SECBM - NG")
plt.plot(mph, SECBH, '--', label="SECBH - Coal")
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=4)
plt.ylabel("Probability of Damage (-)")

# Add vertical lines for category cases
y = [0, 0.8]
TD = 32
TS = 57
H1 = 67
H3 = 120
H5 = 155
plt.plot([TD, TD], y, color="black", label="TD")
plt.plot([TS, TS], y, color="black", label="TS")
plt.plot([H1, H1], y, color="black", label="H1")
plt.plot([H3, H3], y, color="black", label="H3")
plt.plot([H5, H5], y, color="black", label="H5")

y_txt = 0.8
plt.text(TD, y_txt, "TD")
plt.text(TS, y_txt, "TS")
plt.text(H1, y_txt, "H1")
plt.text(H3, y_txt, "H3")
plt.text(H5, y_txt, "H5")

# Save
plt.savefig("DamageFunctionComparison_Original.png", dpi=1000, bbox_inches="tight")

# ================================#
# Plot 2 - Compare HAZUS Damage Functions Available - Moderate
# ================================#
plt.figure(2)
sns.set_style("darkgrid")
plt.plot(mph, CECBL, color = "green", label="CECBL - Concrete, Eng. Comm. Bldg 1 to 2 stories")
plt.plot(mph, CECBM, color = "blue", label="CECBM - Concrete, Eng. Comm. Bldg 3 to 5 stories")
plt.plot(mph, CECBH, color = "orange", label="CECBH - Concrete, Eng. Comm. Bldg 6+ stories")
plt.plot(mph, SECBL, color = "green", linestyle='--', label="SECBL - Steel, Eng. Comm. Bldg 1 to 2 stories")
plt.plot(mph, SECBM, color = "blue", linestyle='--', label="SECBM - Steel, Eng. Comm. Bldg 3 to 5 stories")
plt.plot(mph, SECBH, color = "orange", linestyle='--', label="SECBH - Steel, Eng. Comm. Bldg 6+ stories")
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
plt.xlabel("Windspeed (mph)")
plt.ylabel("Probability of Damage (-)")

# Add vertical lines for category cases
y = [0, 1.0]
TD = 32
TS = 57
H1 = 67
H3 = 120
H5 = 155
plt.plot([TD, TD], y, color="black", label="TD")
plt.plot([TS, TS], y, color="black", label="TS")
plt.plot([H1, H1], y, color="black", label="H1")
plt.plot([H3, H3], y, color="black", label="H3")
plt.plot([H5, H5], y, color="black", label="H5")

y_txt = 0.8
plt.text(TD, y_txt, "TD")
plt.text(TS, y_txt, "TS")
plt.text(H1, y_txt, "H1")
plt.text(H3, y_txt, "H3")
plt.text(H5, y_txt, "H5")

# Save
plt.savefig("DamageFunctionComparison_HAZUS_moderate.png", dpi=1000, bbox_inches="tight")


# ================================#
# Plot 3 - Compare HAZUS Damage Functions Available - Severe
# ================================#
CECBL = CECBL_severe(mph)
CECBM = CECBM_severe(mph)
CECBH = CECBH_severe(mph)
SECBL = SECBL_severe(mph)
SECBM = SECBM_severe(mph)
SECBH = SECBH_severe(mph)

plt.figure(3)
sns.set_style("darkgrid")
plt.plot(mph, CECBL, color = "green", label="CECBL - Concrete, Eng. Comm. Bldg 1 to 2 stories")
plt.plot(mph, CECBM, color = "blue", label="CECBM - Concrete, Eng. Comm. Bldg 3 to 5 stories")
plt.plot(mph, CECBH, color = "orange", label="CECBH - Concrete, Eng. Comm. Bldg 6+ stories")
plt.plot(mph, SECBL, color = "green", linestyle='--', label="SECBL - Steel, Eng. Comm. Bldg 1 to 2 stories")
plt.plot(mph, SECBM, color = "blue", linestyle='--', label="SECBM - Steel, Eng. Comm. Bldg 3 to 5 stories")
plt.plot(mph, SECBH, color = "orange", linestyle='--', label="SECBH - Steel, Eng. Comm. Bldg 6+ stories")
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
plt.xlabel("Windspeed (mph)")
plt.ylabel("Probability of Damage (-)")

# Add vertical lines for category cases
y = [0, 1.0]
TD = 32
TS = 57
H1 = 67
H3 = 120
H5 = 155
plt.plot([TD, TD], y, color="black", label="TD")
plt.plot([TS, TS], y, color="black", label="TS")
plt.plot([H1, H1], y, color="black", label="H1")
plt.plot([H3, H3], y, color="black", label="H3")
plt.plot([H5, H5], y, color="black", label="H5")

y_txt = 0.8
plt.text(TD, y_txt, "TD")
plt.text(TS, y_txt, "TS")
plt.text(H1, y_txt, "H1")
plt.text(H3, y_txt, "H3")
plt.text(H5, y_txt, "H5")

# Save
plt.savefig("DamageFunctionComparison_HAZUS_severe.png", dpi=1000, bbox_inches="tight")

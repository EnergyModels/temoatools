import pandas as pd
import matplotlib.pyplot as plt

# Import data
filename = "combined_results.csv"
df = pd.read_csv(filename)

# Indicate columns of interest
cols = ['LCOE (cents/kWh)','Emissions 2052 (Mton/yr)','Build-back time (days)', 'Build-back cost (B$)']

# Color palette
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)]

# Create Plot
plt.figure()
pd.plotting.parallel_coordinates(df, 'Scenario', cols=cols)#, colormap=custom_palette)

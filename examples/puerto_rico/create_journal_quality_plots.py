import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import temoatools as tt
from   custom_analysis_groups  import getCustomGroup

#=============================================================================#
# Common Inputs
#=============================================================================#
analyzeSingle = False
folder = os.getcwd() + '\\Databases'
dbs = ["A.sqlite","B.sqlite","C.sqlite","D.sqlite"]
labels = ["Centralized","Regionalized","Small-scale","No Policy"]
colors = ['black','blue','green','red']
resolution = 600 # DPI
#==============================================================================
# Remove filetype from filename
def name(db):
    return db[:db.find('.')]

#%%=============================================================================#
# 1) Cost by year
savename = 'Fig_CostByYear.png'
#=============================================================================#
# Analyze and get results
yearlyCosts, LCOE = tt.getCosts(folder, dbs)

# Create plot
plt.figure()
sns.set(style="darkgrid")
for db,label,color in zip(dbs,labels,colors):
    plt.plot(yearlyCosts.index,yearlyCosts.loc[:,name(db)],label=label,color=color)

plt.legend(loc = 'upper center',bbox_to_anchor=(0.5, -0.1),ncol=len(dbs))
plt.xlabel("Year (-)")
plt.ylabel("Cost of Electricity (cents/kWh)")

# Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")

#%%=============================================================================#
# 2) Emissions by year
savename = 'Fig_EmissionsByYear.png'
#=============================================================================#
# Analyze and get results
#yearlyEmissions, avgEmissions = Emissions.SingleDB(folder, dbs[0])
yearlyEmissions, avgEmissions = tt.getEmissions(folder, dbs)

# Create plot
plt.figure()
sns.set(style="darkgrid")
for db,label,color in zip(dbs,labels,colors):
    plt.plot(yearlyEmissions.index,yearlyEmissions.loc[:,name(db)],label=label,color=color)

plt.legend(loc = 'upper center',bbox_to_anchor=(0.5, -0.1),ncol=len(dbs))
plt.xlabel("Year (-)")
plt.ylabel("CO$_2$ Emissions (Mton/year)")

# Adjust layout
plt.tight_layout()

# Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")

#%%=============================================================================#
switch     = 'techgroup'
group      = getCustomGroup(groupNum=1)
sectorName = 'electric'  # Name of sector to be analyzed
activity,capacity,df = tt.getActCap(folder, dbs, switch=switch,group=group,sectorName=sectorName)
#sns.relplot(x='Year',y='Capacity',col='Group',hue='Scenario',col_wrap=4,kind='line',data=df)
#sns.relplot(x='Year',y='Activity',col='Group',hue='Scenario',col_wrap=4,kind='line',data=df)

n_x = 2
n_y = 3
plotGroups = np.unique(group.values())
plotGroups = ['Battery','Coal', 'Natural Gas', 'Petrol.','Solar', 'Wind']
actual_year = 2015
cap_year    = 2015
cap_actual  = [0.0,0.454,0.507,4.7695,0.0521,0.102] # GW
act_year    = 2016
act_actual  = [-1,3.63,4.13,15.09,0.1,0.38] #

# 3) Capacity by year and fuel
savename = 'Fig_CapacityByYearAndFuel.png'
#=============================================================================#
# Categories and corresponding labels

# Create plot
f,ax = plt.subplots(n_y,n_x,sharex=True, sharey=True)
count = 0

for i in range(n_y):
    for j in range(n_x):
        # Plot Simulation
        plotGroup = plotGroups[count]
        for db,label,color in zip(dbs,labels,colors):
            x = capacity[name(db)].index
            y = capacity[name(db)].loc[:,plotGroup]
            ax[i,j].plot(x,y,label=label,color=color)
        
        # Plot Actual
        if cap_actual[count]>-1:
            x = cap_year
            y = cap_actual[count]
            ax[i,j].plot(x,y,label='Actual',marker='o',linestyle='',color='gray')
        
        ax[i,j].set_ylabel(plotGroup + '\n(GW)')
        count = count + 1
        
        if i==n_y-1:
            ax[i,j].set_xlabel("Year (-)")    


plt.legend(loc = 'upper center',bbox_to_anchor=(-0.3, -0.6),ncol=3)

# Adjust layout
plt.tight_layout()

# Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")

#%%=============================================================================#
# 4) Activity by year and fuel
savename = 'Fig_ActivityByYearAndFuel.png'
#=============================================================================#

# Create plot
f,ax = plt.subplots(n_y,n_x,sharex=True, sharey=True)
count = 0
for i in range(n_y):
    for j in range(n_x):
        # Plot simulation
        plotGroup = plotGroups[count]
        for db,label,color in zip(dbs,labels,colors):
            x = activity[name(db)].index
            y = activity[name(db)].loc[:,plotGroup]*1E-3 # Convert to TWh
            ax[i,j].plot(x,y,label=label,color=color)
            
        # Plot Actual
        if act_actual[count]>-1:
            x = act_year
            y = act_actual[count]
            ax[i,j].plot(x,y,label='Actual',marker='o',linestyle='',color='gray')
            
        ax[i,j].set_ylabel(plotGroup + '\n(TWh/year)')
        count = count + 1
        
        if i==n_y-1:
            ax[i,j].set_xlabel("Year (-)")    

ax[i,j].set_ylim([0,20])
plt.legend(loc = 'upper center',bbox_to_anchor=(-0.3, -0.6),ncol=3)

# Adjust layout
plt.tight_layout()

# Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")
#%%=============================================================================#
# 5) Activity + Capacity by year and group
savename = 'Fig_ActivityCapacityByYearAndFuel.png'
#=============================================================================#

# Create plot
f,ax = plt.subplots(2*n_y,n_x,sharex=True, sharey='col')
count = 0
for i in range(2*n_y):
    plotGroup = plotGroups[count]
    count = count + 1
    for j in range(n_x):    
        # Capacity
        if j==0:
            for db,label,color in zip(dbs,labels,colors):
                x = capacity[name(db)].index
                y = capacity[name(db)].loc[:,plotGroup]
                ax[i,j].plot(x,y,label=label,color=color)
            ax[i,j].set_ylabel(plotGroup + '\n(GW)')
        # Activity
        if j==1:
            for db,label,color in zip(dbs,labels,colors):
                x = activity[name(db)].index
                y = activity[name(db)].loc[:,plotGroup]*1E-3 # Convert to TWh
                ax[i,j].plot(x,y,label=label,color=color)
            ax[i,j].set_ylabel(plotGroup + '\n(TWh/year)')
        
        
        
        if i==2*n_y-1:
            ax[i,j].set_xlabel("Year (-)")    

ax[i,j].set_ylim([0,20])
plt.legend(loc = 'upper center',bbox_to_anchor=(-0.3, -0.6),ncol=3)

# Adjust layout
plt.tight_layout()

# Save
plt.savefig(savename,dpi=resolution,bbox_inches="tight")


#%%=============================================================================#
## 5) Combine Capacity and Activity by year and fuel
#savename = 'Fig_CapacityAndActivityByYearAndFuel.png'
##=============================================================================#
## Analyze and get results
#switch     = 'fuel'
#sectorName = 'electric'  # Name of sector to be analyzed
#capacity = Capacity.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName)
#activity = ActivityYear.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName)
#
## Categories and corresponding labels
#fuels      = ['COAL','DSL','HYDRO','MSW_LF','NATGAS','OIL','SOLAR','WIND']
#fuelLabels = ['Coal','Diesel','Hydro','Landfill Gas','Natural Gas','Oil','Solar','Wind']
#
## Create plot
#f,ax = plt.subplots(4,2,sharex=True, sharey=True)
#count = 0
#for i in range(4):
#    for j in range(2):
#        fuel = fuels[count]
#        fuelLabel = fuelLabels[count]
#        ax2 = ax[i,j].twinx()
#        for db,label,color in zip(dbs,labels,colors):
#            # Capacity
#            x1 = capacity[name(db)].index
#            y1 = capacity[name(db)].loc[:,fuel]
#            ax[i,j].plot(x,y,label=label,color=color,linestyle='-')
#            
#            # Activity
#            x2 = activity[name(db)].index
#            y2 = activity[name(db)].loc[:,fuel]*1E-3 # Convert to TWh
#            ax2.plot(x2,y2,label=label,color=color,linestyle='--')
#        
#        if j ==0:
#            # Capacity
#            ax[i,j].set_ylabel(fuelLabel + '\n(GWh)')
#        elif j==1:
#            # Activity
#            ax2.set_ylabel(fuelLabel + '\n(TWh/year)')
#        count = count + 1
#        
#        if i==3:
#            ax[i,j].set_xlabel("Year (-)")    
#
#plt.legend(loc = 'upper center',bbox_to_anchor=(-0.3, -0.4),ncol=len(dbs))
#
## Adjust layout
#plt.tight_layout()
#
## Save
#plt.savefig(savename,dpi=resolution,bbox_inches="tight")

#%%=============================================================================#
## 4) Activity by year and fuel
#savename = 'Fig_ActivityCapacityByYearAndFuel.png'
##=============================================================================#
## Analyze and get results
#switch     = 'fuel'
#sectorName = 'electric'  # Name of sector to be analyzed
#activityTOD = ActivityTOD.MultipleDB(folder, dbs, switch=switch,sectorName=sectorName,)
#
## Save
#plt.savefig(savename,dpi=resolution,bbox_inches="tight")
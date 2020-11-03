import os
import shutil
import sqlite3
import pandas as pd
import copy
import numpy as np
import temoatools as tt
from pathlib import Path

debug = False
# =============================================================================
# Table structures used for inputs, local variables and temoa(outputs)
# =============================================================================

# Format for inputs, format is name and number of associated entries
inputTables = [("representativeDays", 2), ("timesOfDay", 2), ("Connections", 11), ("ConnectionsExisting", 4),
               ("Demand", 4), ("DiscountRate", 2), ("Fuels", 12), ("FuelsExisting", 4), ("PowerPlants", 7),
               ("PowerPlantsPerformance", 9), ("PowerPlantsCosts", 7), ("PowerPlantsConstraints", 7),
               ("PowerPlantsExisting", 4), ("ReserveMargin", 2), ("capacityFactorTOD", 5), ("ref", 6)]

# Format for local, names only
localTables = ['plants_to_include', 'fuels_to_include', 'connections_to_include', 'include_baseload',
               'include_reserve_margin', 'include_ramping', 'include_growth_limit', 'delay_newBuilds',
               'future_periods', 'active_future_periods', 'allTimePeriods', 'commodities', 'MaxLoan_yrs']

# Format for outputs, format is name and number of associated entries
temoaTables = [('commodities', 3), ('technologies', 5), ('tech_baseload', 1),
               ('tech_reserve', 1), ('tech_ramping', 1), ('time_of_day', 1),
               ('time_periods', 2), ('time_season', 1), ('CapacityFactorTech', 5),
               ('CapacityToActivity', 3), ('CostFixed', 6), ('CostInvest', 5),
               ('CostVariable', 6), ('Demand', 5), ('DemandSpecificDistribution', 5),
               ('Efficiency', 6), ('EmissionActivity', 8),
               ('ExistingCapacity', 5), ('LifetimeLoanTech', 3), ('LifetimeTech', 3),
               ('MaxCapacity', 5), ('MaxActivity', 5),
               ('GlobalDiscountRate', 1), ('GrowthRateMax', 3), ('GrowthRateSeed', 4),
               ('RampUp', 2), ('RampDown', 2), ('ReserveMargin', 2), ('SegFrac', 4),
               ('MinGenGroupOfTechnologies_Data', 3), ('MinGenGroupOfTechnologies', 4), ('CapacityCredit', 2)]

# =============================================================================
# Hard coded inputs
# =============================================================================

# emission_type
emission_type = 'CO2'

# demand_commodity
demand_commodity = 'ELC_DMD'


# =============================================================================
# Function to build a temoa model
# =============================================================================
def build(modelInputs, scenarioXLSX, scenarioName, outFilename, sensitivity={}, MCinputs={}, path=os.path.normcase('.')):
    data_path = os.path.join(path, 'data')
    # Get empty dictionary of local variables
    local = getEmptyLocalDict()

    # Process scenarios
    local = processScenarios(scenarioXLSX, scenarioName, local, data_path)

    # Read-in inputs as dictionary
    inputs = inputs2Dict(modelInputs, data_path)

    # Apply Sensitivity to inputs
    if debug:
        print(sensitivity)
    if not len(
            sensitivity) == 0:  # if dictionary is empty, it will evaluae to false, and no senstivity will be performed
        inputs, local = applySensitivity(inputs, sensitivity, local)

    # Apply Monte Carlo to inputs
    if debug:
        print(MCinputs)
    if not len(MCinputs) == 0:  # if dictionary is empty, it will evaluae to false, and no monte carlo will be performed
        for i in range(len(MCinputs)):
            inputs, local = applySensitivity(inputs, MCinputs.loc[i, :], local)

    # Create empty dictionary of temoa outputs
    outputs = getEmptyTemoaDict()

    # System parameters
    local, outputs = processSystem(inputs, local, outputs)

    # PowerPlants
    local, outputs = processPowerPlants(inputs, local, outputs)

    # Fuels
    local, outputs = processFuels(inputs, local, outputs)

    # Connections
    local, outputs = processConnections(inputs, local, outputs)

    # Copy temoa_schema_mod.db and write(commit) outputs to it
    Write2Temoa(outputs, outFilename)

    return inputs


# =============================================================================
# Move modelInputs to a dictionary using pandas
# =============================================================================
def inputs2Dict(modelInputs, path):
    # Keep track of working directory
    workDir = os.getcwd()
    os.chdir(path)

    # Set-up sqlite connection
    conn = sqlite3.connect(modelInputs)

    # tables to read-in from SQL
    tables = ["representativeDays", "timesOfDay", "Connections", "ConnectionsExisting",
              "Demand", "DiscountRate", "Fuels", "FuelsExisting", "PowerPlants",
              "PowerPlantsPerformance", "PowerPlantsCosts", "PowerPlantsConstraints",
              "PowerPlantsExisting", "ReserveMargin", "capacityFactorTOD", "ref"]

    # Connect and store tables in dictionary inputs
    inputs = {}
    for table in tables:
        inputs[table] = pd.read_sql_query("SELECT * FROM " + table, conn)

    # Close connection
    conn.close()

    # Set index using powerplant for easier access
    inputs['PowerPlants'] = inputs['PowerPlants'].set_index('powerplant')
    inputs['PowerPlantsConstraints'] = inputs['PowerPlantsConstraints'].set_index('powerplant')
    inputs['PowerPlantsCosts'] = inputs['PowerPlantsCosts'].set_index('powerplant')
    inputs['PowerPlantsPerformance'] = inputs['PowerPlantsPerformance'].set_index('powerplant')
    # Set index using fuel for easier access
    inputs['Fuels'] = inputs['Fuels'].set_index('fuel')
    # Set index using connection for easier access
    inputs['Connections'] = inputs['Connections'].set_index('connection')

    # Return to original directory
    os.chdir(workDir)

    # Return dictionary of inputs
    return inputs


# =============================================================================
# Get empty dictionary of temoa tables
# =============================================================================
def getEmptyTemoaDict():
    outputs = {}

    for table, numEntries in temoaTables:
        outputs[table] = []

    return outputs


# =============================================================================
# Write outputs to an empty temoa database
# =============================================================================
def Write2Temoa(outputs, outFilename):
    # Keep track of working directory
    workDir = os.getcwd()

    # Directory to hold empty (unrun) database files
    databaseDir = os.path.join(workDir, "databases")
    try:
        os.stat(databaseDir)
    except:
        os.mkdir(databaseDir)

    # Create New SQL File
    # Set Filenames
    emptydB = os.path.join(tt.resource_path, "db_schema_temoa_mod.sqlite")
    outfilename_w_ext = outFilename + '.sqlite'
    outputdB = os.path.join(databaseDir, outfilename_w_ext)

    # Delete old *.sqlite file (if it already exists) and copy/rename copy of temoa_schema.sqlite
    if os.path.isfile(outputdB):
        os.remove(outputdB)
    shutil.copyfile(emptydB, outputdB)

    # Set-up sqlite connection
    conn = sqlite3.connect(outputdB)
    c = conn.cursor()

    for table, numEntries in temoaTables:

        # Create SQL command based on number of entries
        command = 'INSERT INTO ' + table + ' VALUES (?'
        for i in range(numEntries - 1):
            command = command + ',?'
        command = command + ')'

        # Execute SQL Command
        try:
            if len(outputs[table]) == 1 and numEntries == 1:
                c.execute(command, outputs[table])
            else:
                c.executemany(command, outputs[table])
        except:
            print('Error inputting ' + table)

    # Close Connection
    conn.commit()
    conn.close()

    # Return to working directory
    os.chdir(workDir)


# =============================================================================
# Get empty dictionary to hold local variables
# =============================================================================
def getEmptyLocalDict():
    # Create dictionary
    local = {}

    # Populate table with empty lists
    for table in localTables:
        local[table] = []

    # return local
    return local


# =============================================================================
# Process Scenarios
# =============================================================================
def processScenarios(scenarioXLSX, scenarioName, local, path):
    # Keep track of working directory
    workDir = os.getcwd()
    os.chdir(path)

    # Unpack PowerPlants
    print(os.getcwd())
    df = pd.read_excel(scenarioXLSX, sheet_name='PowerPlants')
    ind = df.loc[:, scenarioName] == 'Y'
    local['plants_to_include'] = df.Scenario[ind]

    # Unpack Fuels
    df = pd.read_excel(scenarioXLSX, sheet_name='Fuels')
    ind = df.loc[:, scenarioName] == 'Y'
    local['fuels_to_include'] = df.Scenario[ind]

    # Unpack Connections
    df = pd.read_excel(scenarioXLSX, sheet_name='Connections')
    ind = df.loc[:, scenarioName] == 'Y'
    local['connections_to_include'] = df.Scenario[ind]

    # Unpack SolverSettings (all or Y/N)
    df = pd.read_excel(scenarioXLSX, sheet_name='SolverSettings')
    df = df.set_index('Scenario')
    # Option to include baseload constraint (Does not work with LCOE script)
    local['include_baseload'] = df.loc['include_baseload', scenarioName]
    # Option to include reserve margin constraint (Does not work on TEMOA cloud)
    local['include_reserve_margin'] = df.loc['include_reserve_margin', scenarioName]
    # Option to include ramping constraint
    local['include_ramping'] = df.loc['include_ramping', scenarioName]
    # Prevents new builds of any technology during the first period
    local['delay_newBuilds'] = df.loc['delay_newBuilds', scenarioName]
    # Option to include growth_rate and growth_seed
    local['include_growth_limit'] = df.loc['include_growth_limit', scenarioName]

    # Growth Limits
    # Maximum growth rate
    local['MaxGrowthRate'] = df.loc['MaxGrowthRate', scenarioName]
    # Minimum initial growth
    local['MinGrowthSeed'] = df.loc['MinGrowthSeed', scenarioName]
    # Minimum initial growth
    local['MaxLoan_yrs'] = df.loc['MaxLoan_yrs', scenarioName]

    # Minimum initial growth
    local['include_RPS'] = df.loc['include_RPS', scenarioName]

    # Return to working directory
    os.chdir(workDir)

    # return local
    return local


# =============================================================================
# Process System parameters
# =============================================================================
def processSystem(inputs, local, outputs):
    # time_periods
    for period in inputs['Demand'].Year:
        outputs['time_periods'].append((str(period), "f"), )
        local['future_periods'].append(period)

    # Store local variables of future_periods and allTimePeriods
    local['active_future_periods'] = local['future_periods'][:-1]
    local['allTimePeriods'] = copy.copy(local['future_periods'])

    # time_season
    for season in inputs['representativeDays'].representativeDay:
        outputs['time_season'].append((season,))

    # time_of_day        
    for timeOfDay in inputs['timesOfDay'].timeOfDay:
        outputs['time_of_day'].append((timeOfDay,))

    # SegFrac
    for season, season_frac in zip(inputs['representativeDays'].representativeDay,
                                   inputs['representativeDays'].timeFrac):
        for timeOfDay, timeOfDay_frac in zip(inputs['timesOfDay'].timeOfDay, inputs['timesOfDay'].timeFrac):
            value = season_frac * timeOfDay_frac
            outputs['SegFrac'].append([season, timeOfDay, value, " "])

    # Demand(Yearly Demand)
    for period, demand in zip(local['active_future_periods'], inputs['Demand'].Demand):
        outputs['Demand'].append((str(period), demand_commodity, demand, "PJ", " "))

    # DemandSpecificDistribution
    for season, season_frac in zip(inputs['representativeDays'].representativeDay,
                                   inputs['representativeDays'].dmdFrac):
        for timeOfDay, timeOfDay_frac in zip(inputs['timesOfDay'].timeOfDay, inputs['timesOfDay'].dmdFrac):
            value = season_frac * timeOfDay_frac
            outputs['DemandSpecificDistribution'].append([season, timeOfDay, demand_commodity, value, " "])

    # Add system level commodities
    # Add dummy fuel
    outputs['commodities'].append(("ethos", "p", "dummy variable"))
    local['commodities'].append("ethos")

    # Add demand variable
    outputs['commodities'].append((demand_commodity, "d", "demand variable"))
    local['commodities'].append(demand_commodity)

    # Add emissions
    outputs['commodities'].append((emission_type, "e", "emission"))
    local['commodities'].append(emission_type)

    # Discount Rate
    outputs['GlobalDiscountRate'].append(str(inputs['DiscountRate'].DiscountRate[0]))

    # ReserveMargin
    if local['include_reserve_margin'] == 'Y':
        outputs['ReserveMargin'].append((demand_commodity, str(inputs['ReserveMargin'].ReserveMargin[0])))

    # Renewable Portfolio Standard
    if local['include_RPS'] == 'Y':
      for period, RPS in zip(local['active_future_periods'], inputs['Demand'].RPS):
        outputs['MinGenGroupOfTechnologies_Data'].append((str(period), "RPS", RPS))

    return local, outputs


# =============================================================================
# Process PowerPlants
# =============================================================================
def processPowerPlants(inputs, local, outputs):
    #    # Set index using powerplant for easier access
    #    inputs['PowerPlants']               = inputs['PowerPlants'].set_index('powerplant')
    #    inputs['PowerPlantsConstraints']    = inputs['PowerPlantsConstraints'].set_index('powerplant')
    #    inputs['PowerPlantsCosts']          = inputs['PowerPlantsCosts'].set_index('powerplant')
    #    inputs['PowerPlantsPerformance']    = inputs['PowerPlantsPerformance'].set_index('powerplant')
    #    # Set index using fuel for easier access
    #    inputs['Fuels']  = inputs['Fuels'].set_index('fuel')
    #    # Set index using connection for easier access
    #    inputs['Connections']               = inputs['Connections'].set_index('connection')

    for techType in local['plants_to_include']:
        tech = {}

        # General
        tech['name'] = techType
        tech['fuel'] = inputs['PowerPlants'].loc[techType, 'fuel']
        tech['output'] = inputs['PowerPlants'].loc[techType, 'output']

        tech['baseload'] = str(inputs['PowerPlants'].loc[techType, 'baseload'])
        tech['reserve'] = inputs['PowerPlants'].loc[techType, 'reserve']
        tech['newBuilds'] = str(inputs['PowerPlants'].loc[techType, 'newBuilds'])
        tech['renewable'] = inputs['PowerPlants'].loc[techType, 'renewable']
        tech['storage'] = inputs['PowerPlants'].loc[techType, 'storage']
        tech['sector'] = 'electric'
        tech['CapacityCredit'] = inputs['PowerPlants'].loc[techType, 'CapacityCredit']

        tech['c2a'] = 'Y'  # Indicator whether to include a capacity to activity input, only needed for powerplants

        # Performance
        # Efficiency takes precedence over heatRate value
        if goodValue(inputs['PowerPlantsPerformance'].loc[techType, 'Efficiency']):
            tech['efficiency'] = inputs['PowerPlantsPerformance'].loc[techType, 'Efficiency'] / 100.0
        else:
            tech['efficiency'] = 3412.0 / float(inputs['PowerPlantsPerformance'].loc[techType, 'HeatRate'])
        tech['lifetime'] = inputs['PowerPlantsPerformance'].loc[techType, 'ExpectedLifetime']
        tech['emission_activity'] = None
        tech['capacity_factor'] = inputs['PowerPlantsPerformance'].loc[techType, 'CapacityFactor'] / 100.0

        # Costs
        tech['cost_fixed'] = inputs['PowerPlantsCosts'].loc[techType, 'CostFixed']
        tech['cost_invest'] = inputs['PowerPlantsCosts'].loc[techType, 'CostInvest']
        tech['cost_variable'] = inputs['PowerPlantsCosts'].loc[techType, 'CostVariable']
        tech['costVariableIncr'] = 0.0  # # Yearly increase (%) - Constant

        # Constraints
        tech['max_capacity'] = inputs['PowerPlantsConstraints'].loc[
                                   techType, 'MaxCapacity'] / 1000.0  # Convert from MW to GW
        tech['max_activity'] = inputs['PowerPlantsConstraints'].loc[techType, 'MaxActivity']
        tech['ramp_rate'] = inputs['PowerPlantsConstraints'].loc[techType, 'RampRate']
        tech['Retirement'] = None

        # Existing
        tech['existing_capacity_year'] = []
        tech['existing_capacity_rating'] = []
        for index, row in inputs['PowerPlantsExisting'].iterrows():
            if row['powerplant'] == techType:
                tech['existing_capacity_year'].append(row['YearInstalled'])
                tech['existing_capacity_rating'].append(row['Capacity'] / 1000.0)  # Convert from MW to GW

        # Update outputs for this technology
        local, outputs = processTech(inputs, local, outputs, tech)

    # Do something    
    return local, outputs


# =============================================================================
# Process Fuels
# =============================================================================
def processFuels(inputs, local, outputs):
    # Set index using fuel for easier access
    #    inputs['Fuels']  = inputs['Fuels'].set_index('fuel')
    # Set index using connection for easier access
    #    inputs['Connections']               = inputs['Connections'].set_index('connection')
    # Set index using fuel for easier access
    #    inputs['Fuels']  = inputs['Fuels'].set_index('fuel')

    for techType in local['fuels_to_include']:
        tech = {}

        # General
        tech['name'] = 'IMP' + techType
        tech['fuel'] = 'ethos'
        tech['output'] = techType

        tech['baseload'] = 'N'
        tech['reserve'] = 'N'
        tech['newBuilds'] = 'Y'
        tech['renewable'] = 'N'
        tech['storage'] = 'N'
        tech['sector'] = 'supply'
        tech['CapacityCredit'] = None

        tech['c2a'] = 'Y'  # Indicator whether to include a capacity to activity input, only needed for powerplants

        # Performance
        tech['efficiency'] = 1.0
        tech['lifetime'] = inputs['Fuels'].loc[techType, 'Lifetime']
        tech['emission_activity'] = inputs['Fuels'].loc[techType, 'EmissionActivity']
        tech['capacity_factor'] = None

        # Costs
        tech['cost_fixed'] = None
        tech['cost_invest'] = inputs['Fuels'].loc[techType, 'CostInvest']
        tech['cost_variable'] = inputs['Fuels'].loc[techType, 'CostVariable']
        tech['costVariableIncr'] = inputs['Fuels'].loc[techType, 'CostVariableIncr']  # Yearly increase (%)

        # Constraints
        tech['max_capacity'] = None
        tech['max_activity'] = None
        tech['ramp_rate'] = None
        tech['Retirement'] = inputs['Fuels'].loc[techType, 'Retirement']

        # Existing
        tech['existing_capacity_year'] = []
        tech['existing_capacity_rating'] = []
        for index, row in inputs['FuelsExisting'].iterrows():
            if row['fuel'] == techType:
                tech['existing_capacity_year'].append(row['YearInstalled'])
                tech['existing_capacity_rating'].append(row['Capacity'] / 1000.0)  # Convert from MW to GW

        # Update outputs for this technology
        local, outputs = processTech(inputs, local, outputs, tech)

        # Fuel Specific Tasks
        # Add fuel as a commodity
        outputs['commodities'].append((techType, "p", techType))
        local['commodities'].append(techType)

    return local, outputs


# =============================================================================
# Process Connections
# =============================================================================
def processConnections(inputs, local, outputs):
    # Set index using connection for easier access
    #    inputs['Connections']               = inputs['Connections'].set_index('connection')

    for techType in local['connections_to_include']:
        tech = {}

        # General
        tech['name'] = techType
        tech['fuel'] = inputs['Connections'].loc[techType, 'input']
        tech['output'] = inputs['Connections'].loc[techType, 'output']

        tech['baseload'] = 'N'
        tech['reserve'] = 'N'
        tech['newBuilds'] = 'Y'
        tech['renewable'] = 'N'
        tech['storage'] = 'N'
        tech['sector'] = 'transport'
        tech['CapacityCredit'] = None

        tech['c2a'] = 'Y'  # Indicator whether to include a capacity to activity input, only needed for powerplants

        # Performance
        tech['efficiency'] = 1.0 - inputs['Connections'].loc[techType, 'Loss'] / 100.0
        tech['lifetime'] = inputs['Connections'].loc[techType, 'Lifetime']
        tech['emission_activity'] = None
        tech['capacity_factor'] = None

        # Costs
        tech['cost_fixed'] = None
        tech['cost_invest'] = inputs['Connections'].loc[techType, 'CostInvest']
        tech['cost_variable'] = inputs['Connections'].loc[techType, 'CostVariable']
        tech['costVariableIncr'] = 0.0  # # Yearly increase (%) - Constant

        # Constraints
        tech['max_capacity'] = None
        tech['max_activity'] = None
        tech['ramp_rate'] = None
        tech['Retirement'] = None

        # Existing
        tech['existing_capacity_year'] = []
        tech['existing_capacity_rating'] = []
        for index, row in inputs['ConnectionsExisting'].iterrows():
            if row['connection'] == techType:
                tech['existing_capacity_year'].append(row['YearInstalled'])
                tech['existing_capacity_rating'].append(row['Capacity'] / 1000.0)  # Convert from MW to GW

        # Update outputs for this technology
        local, outputs = processTech(inputs, local, outputs, tech)

        # Connection Specific Tasks
        # Add fuel as a commodity
        if not tech['fuel'] in local['commodities']:
            outputs['commodities'].append((tech['fuel'], "p", tech['fuel']))
            local['commodities'].append(tech['fuel'])

        if not tech['output'] in local['commodities']:
            outputs['commodities'].append((tech['output'], "p", tech['output']))
            local['commodities'].append(tech['output'])

    return local, outputs


# =============================================================================
# Check database for good value (not null or NaN)
# =============================================================================
def goodValue(value):
    return (not value is None) and (not str(value) == 'nan')


# =============================================================================
# Process Technologies
# =============================================================================
def processTech(inputs, local, outputs, tech):
    # Do something    

    # --------    
    # Find years the technology is active
    # --------

    # No New Builds Allowed
    if not tech['newBuilds'] == 'Y':
        buildYears = []
        futureBuildYears = []
    # New Builds Allowed
    else:
        # No Builds First Year (only applies to electric sector)
        if local['delay_newBuilds'] == "Y" and tech['sector'] == 'electric':
            buildYears = copy.copy(local['active_future_periods'][1:])
            futureBuildYears = copy.copy(local['active_future_periods'][1:])
        # Builds Any Year
        else:
            buildYears = copy.copy(local['active_future_periods'])
            futureBuildYears = copy.copy(local['active_future_periods'])
    for year in tech['existing_capacity_year']:
        if min(local['active_future_periods']) - year < tech['lifetime']:  # Prevent including already retired capacity
            # For this technology only
            if not year in buildYears:
                buildYears.append(year)
            # For entire model
            if not year in local['allTimePeriods']:
                local['allTimePeriods'].append(year)
                outputs['time_periods'].append((str(year), "e"), )
    # Sort into ascending order
    buildYears.sort()
    futureBuildYears.sort()

    # --------
    # Record powerplant information
    # --------
    # CapacityCredit
    if goodValue(tech['CapacityCredit']):
        outputs['CapacityCredit'].append((tech['name'], tech['CapacityCredit']))

    # CapacityToActivity
    if tech['c2a'] == 'Y':
        outputs['CapacityToActivity'].append((tech['name'], 31.54, "GW to PJ"))

    # CapacityFactorTech
    if tech['sector'] == 'electric':  # Only apply to powerplant technologies

        # Constant capacity factor
        if not tech['fuel'] in list(inputs['capacityFactorTOD'].fuel):
            for representativeDay in inputs['representativeDays'].representativeDay:
                for timeOfDay in inputs['timesOfDay'].timeOfDay:
                    outputs['CapacityFactorTech'].append(
                        (representativeDay, timeOfDay, tech['name'], tech['capacity_factor'], " "))
        # Capacity factor that varies with timeOfday and representativeDay
        else:
            for index, row in inputs['capacityFactorTOD'].iterrows():
                if row['fuel'] == tech['fuel']:
                    outputs['CapacityFactorTech'].append((row['representativeDay'], row['timeOfDay'], tech['name'],
                                                          row['capacityFactor'] * tech['capacity_factor'], " "))

    # CostFixed
    if goodValue(tech['cost_fixed']):
        for period in local['active_future_periods']:
            for vintage in buildYears:
                if (vintage <= period) and ((period - vintage) < tech['lifetime']):
                    outputs['CostFixed'].append(
                        (str(period), tech['name'], str(vintage), tech['cost_fixed'], "M$/GW", " "))

    # CostInvest
    if goodValue(tech['cost_invest']):
        for year in futureBuildYears:
            outputs['CostInvest'].append((tech['name'], str(year), tech['cost_invest'], "M$/GW", " "))

    # CostVariable
    if goodValue(tech['cost_variable']):
        start_year = local['active_future_periods'][0]
        for period in local['active_future_periods']:
            for vintage in buildYears:
                if (vintage <= period) and ((period - vintage) < tech['lifetime']):
                    if goodValue(tech['costVariableIncr']):
                        N = float(period - start_year)
                        costVar = tech['cost_variable'] * (1.0 + tech['costVariableIncr'] / 100.0) ** (N)
                    else:
                        costVar = tech['cost_variable']
                    outputs['CostVariable'].append((str(period), tech['name'], str(vintage), costVar, "M$/PJ", " "))

    # Efficiency
    if goodValue(tech['efficiency']):
        for vintage in buildYears:
            outputs['Efficiency'].append(
                (tech['fuel'], tech['name'], str(vintage), tech['output'], tech['efficiency'], " "))

    # EmissionActivity
    if goodValue(tech['emission_activity']):
        for vintage in buildYears:
            outputs['EmissionActivity'].append((emission_type, tech['fuel'], tech['name'], str(vintage), tech['output'],
                                                tech['emission_activity'], "kt/PJout", " "))

    # ExistingCapacity
    exist_cap = 0  # Keep track of current capacity, growthrate_seed must be equal to or greater than this
    for vintage, capacity in zip(tech['existing_capacity_year'], tech['existing_capacity_rating']):
        if min(local['active_future_periods']) - vintage < tech['lifetime']: # Prevent including if already retired
            outputs['ExistingCapacity'].append((tech['name'], vintage, capacity, "GW", " "))
            exist_cap = exist_cap + capacity

    # LifetimeTech and LifetimeLoanTech
    if goodValue(tech['lifetime']):
        outputs['LifetimeTech'].append((tech['name'], float(tech['lifetime']), " "))

        loan_yrs = min(local['MaxLoan_yrs'], float(tech['lifetime']))
        outputs['LifetimeLoanTech'].append((tech['name'], loan_yrs, " "))

    # -----
    # technologies
    # -----
    # Fuels
    if tech['sector'] == 'supply':
        outputs['technologies'].append((tech['name'], "r", tech['sector'], "fuels", " "))

        # Connections
    elif tech['sector'] == 'transport':
        outputs['technologies'].append((tech['name'], "p", tech['sector'], "connections", " "))

        # PowerPlants
    elif tech['sector'] == 'electric':
        if local['include_baseload'] == "Y" and tech['baseload'] == "Y":
            outputs['tech_baseload'].append((tech['name'],))
            outputs['technologies'].append((tech['name'], "pb", tech['sector'], "baseload", " "))
        elif tech['storage'] == "Y":
            outputs['technologies'].append((tech['name'], "ps", tech['sector'], "storage", " "))
        else:
            outputs['technologies'].append((tech['name'], "p", tech['sector'], "powerplant", " "))

    # tech_reserve
    if local['include_reserve_margin'] == "Y" and tech['reserve'] == "Y":
        outputs['tech_reserve'].append((tech['name'],))

    # renewable
    if local['include_RPS'] == 'Y' and tech['renewable'] == "Y":
       outputs['MinGenGroupOfTechnologies'].append((tech['name'], 'RPS', 1.0, ''))

    # -----
    # Constraints
    # -----
    # Check delayBuild
    if local['delay_newBuilds'] == 'Y' and exist_cap == 0.0:
        active_future_periods_con = local['active_future_periods'][1:]
    else:
        active_future_periods_con = local['active_future_periods']

    # MaxCapacity
    if goodValue(tech['max_capacity']):
        for period in active_future_periods_con:
            outputs['MaxCapacity'].append((str(period), tech['name'], tech['max_capacity'], "GW", " "))

    # MaxActivity (also used to enforce retirement)
    # Dual constraint
    if goodValue(tech['max_activity']) and goodValue(tech['Retirement']):
        for period in active_future_periods_con:
            if period >= tech['Retirement']:
                outputs['MaxActivity'].append((str(period), tech['name'], 0.0, "PJ", " "))
            else:
                outputs['MaxActivity'].append((str(period), tech['name'], tech['max_activity'], "PJ", " "))
            # Only activitiy constraint
    elif goodValue(tech['max_activity']):
        for period in active_future_periods_con:
            outputs['MaxActivity'].append((str(period), tech['name'], tech['max_activity'], "PJ", " "))
            # Only retirement constraint
    elif goodValue(tech['Retirement']):
        for period in active_future_periods_con:
            if period >= tech['Retirement']:
                outputs['MaxActivity'].append((str(period), tech['name'], 0.0, "PJ", " "))

    # Global growth limits - only apply to power plant technologies
    if tech['newBuilds'] == 'Y' and tech['sector'] == 'electric' and local['include_growth_limit'] == "Y":
        # GrowthRateMax
        if goodValue(local['MaxGrowthRate']):
            outputs['GrowthRateMax'].append(
                (tech['name'], str(local['MaxGrowthRate'] / 100.0), 'Global Growth Limit - Fraction'))

        # GrowthRateSeed
        if goodValue(local['MinGrowthSeed']) == 1:
            if local['MinGrowthSeed'] / 1000.0 > exist_cap:
                growthrate_seed = local['MinGrowthSeed'] / 1000.0
            else:
                growthrate_seed = exist_cap
            outputs['GrowthRateSeed'].append((tech['name'], str(growthrate_seed), 'GW', 'Global Growth Limit'))

    # RampUp and RampDown (Temoa code uses the same value for RampUp and RampDown, despite having two separate variables)
    if local['include_ramping'] == "Y" and goodValue(tech['ramp_rate']):
        outputs['tech_ramping'].append((tech['name'],))
        outputs['RampUp'].append((tech['name'], str(tech['ramp_rate'])))
        outputs['RampDown'].append((tech['name'], str(tech['ramp_rate'])))

    return local, outputs


# =============================================================================
# Create Sensitivity Inputs
# =============================================================================
def createSensitivityCases(scenarioXLSX, scenarioName, sensitivityInputs, multiplier, path=os.path.normcase('.')):
    data_path = os.path.join(path, 'data')
    params = {}

    # ----------
    # Process scenarioXLSX
    # ----------
    # Get empty dictionary of local variables
    local = getEmptyLocalDict()

    # Process scenarios
    local = processScenarios(scenarioXLSX, scenarioName, local, path=data_path)
    # Extract quantities of interest
    params['plants'] = local['plants_to_include']
    params['fuels'] = local['fuels_to_include']
    params['connections'] = local['connections_to_include']

    # ----------
    # Process sensitivityInputs
    # ----------

    # Move to directory with inputs
    os.chdir(data_path)
    # Globals
    df = pd.read_excel(sensitivityInputs, sheet_name='Globals')
    ind = df.loc[:, 'include'] == 'Y'
    params['global_vars'] = df.variable[ind]

    # PowerPlants
    df = pd.read_excel(sensitivityInputs, sheet_name='PowerPlants')
    ind = df.loc[:, 'include'] == 'Y'
    params['plant_vars'] = df.variable[ind]

    # Fuels
    df = pd.read_excel(sensitivityInputs, sheet_name='Fuels')
    ind = df.loc[:, 'include'] == 'Y'
    params['fuel_vars'] = df.variable[ind]

    # Connections
    df = pd.read_excel(sensitivityInputs, sheet_name='Connections')
    ind = df.loc[:, 'include'] == 'Y'
    params['conn_vars'] = df.variable[ind]

    # Return to original directory
    os.chdir('..')
    # ----------
    # Create sensitivity cases
    # ----------
    # Create Empty DataFrame
    cols = ['type', 'variable', 'tech', 'multiplier']
    df = pd.DataFrame(columns=cols)
    count = 0

    # Baseline
    df.loc[count] = ['Baseline', 'Baseline', 'Baseline', 1.0]  # no change
    count = count + 1

    # Globals
    for var in params['global_vars']:
        # Negative multiplier
        df.loc[count] = ['Globals', var, 'global', -1.0 * multiplier]
        count = count + 1
        # Positive multiplier
        df.loc[count] = ['Globals', var, 'global', 1.0 * multiplier]
        count = count + 1

    # PowerPlants
    for var in params['plant_vars']:
        for tech in params['plants']:
            # Negative multiplier
            df.loc[count] = ['PowerPlants', var, tech, -1.0 * multiplier]
            count = count + 1
            # Positive multiplier
            df.loc[count] = ['PowerPlants', var, tech, 1.0 * multiplier]
            count = count + 1

    # Fuels
    for var in params['fuel_vars']:
        for tech in params['fuels']:
            # Negative multiplier
            df.loc[count] = ['Fuels', var, tech, -1.0 * multiplier]
            count = count + 1
            # Positive multiplier
            df.loc[count] = ['Fuels', var, tech, 1.0 * multiplier]
            count = count + 1

    # Connections
    for var in params['conn_vars']:
        for tech in params['connections']:
            # Negative multiplier
            df.loc[count] = ['Connections', var, tech, -1.0 * multiplier]
            count = count + 1
            # Positive multiplier
            df.loc[count] = ['Connections', var, tech, 1.0 * multiplier]
            count = count + 1

    return df


# =============================================================================
# Create Sensitivity Inputs
# =============================================================================
def createMonteCarloCases(scenarioXLSX, scenarioName, sensitivityInputs, multiplier, n_cases=100, path=os.path.normcase('.')):
    params = {}
    data_path = os.path.join(path, 'data')

    # ----------
    # Process scenarioXLSX
    # ----------
    # Get empty dictionary of local variables
    local = getEmptyLocalDict()

    # Process scenarios
    local = processScenarios(scenarioXLSX, scenarioName, local, path=data_path)

    # Extract quantities of interest
    params['plants'] = local['plants_to_include']
    params['fuels'] = local['fuels_to_include']
    params['connections'] = local['connections_to_include']

    # ----------
    # Process sensitivityInputs
    # ----------
    # Move to directory with inputs
    os.chdir(data_path)

    # Globals
    df = pd.read_excel(sensitivityInputs, sheet_name='Globals')
    ind = df.loc[:, 'include'] == 'Y'
    params['global_vars'] = df.variable[ind]

    # PowerPlants
    df = pd.read_excel(sensitivityInputs, sheet_name='PowerPlants')
    ind = df.loc[:, 'include'] == 'Y'
    params['plant_vars'] = df.variable[ind]

    # Fuels
    df = pd.read_excel(sensitivityInputs, sheet_name='Fuels')
    ind = df.loc[:, 'include'] == 'Y'
    params['fuel_vars'] = df.variable[ind]

    # Connections
    df = pd.read_excel(sensitivityInputs, sheet_name='Connections')
    ind = df.loc[:, 'include'] == 'Y'
    params['conn_vars'] = df.variable[ind]

    # Return to original directory
    os.chdir('..')
    # ----------
    # Create sensitivity cases
    # ----------
    # Create Empty DataFrame
    cols = ['type', 'variable', 'tech'] + list(range(n_cases))
    df = pd.DataFrame(columns=cols)
    count = 0

    # Globals
    for var in params['global_vars']:
        df.loc[count] = ['Globals', var, 'global'] + np.random.triangular(-1. * multiplier, 0, multiplier,
                                                                          size=n_cases).tolist()
        count = count + 1

    # PowerPlants
    for var in params['plant_vars']:
        for tech in params['plants']:
            df.loc[count] = ['PowerPlants', var, tech] + np.random.triangular(-1. * multiplier, 0, multiplier,
                                                                              size=n_cases).tolist()
            count = count + 1

    # Fuels
    for var in params['fuel_vars']:
        for tech in params['fuels']:
            df.loc[count] = ['Fuels', var, tech] + np.random.triangular(-1. * multiplier, 0, multiplier,
                                                                        size=n_cases).tolist()
            count = count + 1

    # Connections
    for var in params['conn_vars']:
        for tech in params['connections']:
            df.loc[count] = ['Connections', var, tech] + np.random.triangular(-1. * multiplier, 0, multiplier,
                                                                              size=n_cases).tolist()
            count = count + 1

    return df


# =============================================================================
# Apply Model Sensitivity
# ============================================================================
def applySensitivity(inputs, sensitivity, local):
    # Treat global parameters differently - only need to modify one value
    if sensitivity['type'] == 'Globals':

        multiplier = 1.0 + sensitivity['multiplier'] / 100.0

        if sensitivity['variable'] == 'DiscountRate':
            entryName = 'DiscountRate'
            entry = inputs[entryName]
            if goodValue(entry.loc[0, 'DiscountRate']):
                entry.at[0, 'DiscountRate'] = entry.loc[0, 'DiscountRate'] * multiplier
                inputs[entryName] = entry

        elif sensitivity['variable'] == 'ReserveMargin':
            entryName = 'ReserveMargin'
            entry = inputs[entryName]
            if goodValue(entry.loc[0, 'ReserveMargin']):
                entry.at[0, 'ReserveMargin'] = entry.loc[0, 'ReserveMargin'] * multiplier
                inputs[entryName] = entry

        elif sensitivity['variable'] == 'MaxGrowthRate':
            if goodValue(local['MaxGrowthRate']):
                local['MaxGrowthRate'] = local['MaxGrowthRate'] * multiplier

        elif sensitivity['variable'] == 'MinGrowthSeed':
            if goodValue(local['MinGrowthSeed']):
                local['MinGrowthSeed'] = local['MinGrowthSeed'] * multiplier


    elif sensitivity['type'] in ['PowerPlants', 'Fuels', 'Connections']:  # Baseline is excluded (no modifications made)
        # -------------------
        # Determine which inputs dictionary entry to modify
        # -------------------
        # PowerPlants
        if sensitivity['type'] == 'PowerPlants':
            index = 'powerplant'

            # PowerPlantsPerformance
            if sensitivity['variable'] in ['Efficiency', 'ExpectedLifetime', 'CapacityFactor']:
                entryName = 'PowerPlantsPerformance'

            # PowerPlantsCosts
            elif sensitivity['variable'] in ['CostInvest', 'CostFixed', 'CostVariable']:
                entryName = 'PowerPlantsCosts'

            # PowerPlantsConstraints
            elif sensitivity['variable'] in ['RampRate', 'MaxCapacity', 'MaxActivity']:
                entryName = 'PowerPlantsConstraints'

                # Fuels
        elif sensitivity['type'] == 'Fuels':
            index = 'fuel'
            entryName = 'Fuels'

        # Connections
        elif sensitivity['type'] == 'Connections':
            index = 'connection'
            entryName = 'Connections'

        # -------------------
        # Apply Multiplier
        # -------------------
        # Extract original entry
        entry = inputs[entryName]
        if not entry.index.name == index:
            entry = entry.set_index(index)

        if debug == True:
            print(entry)

        # Modify specified value
        multiplier = 1.0 + sensitivity['multiplier'] / 100.0
        if goodValue(entry.loc[sensitivity['tech'], sensitivity['variable']]):  # Ensure that entry can be changed
            # Calculate updated value
            newValue = entry.loc[sensitivity['tech'], sensitivity['variable']] * multiplier

            # Check values are reasonable
            if newValue > 100.0 and sensitivity['variable'] == 'Efficiency':
                newValue = 100.0
            elif newValue > 100.0 and sensitivity['variable'] == 'CapacityFactor':
                newValue = 100.0
            elif newValue < 0.0 and sensitivity['variable'] == 'Loss':
                newValue = 0.0

            if sensitivity['variable'] == 'ExpectedLifetime': # Must be an integer
                newValue = int(newValue)

            # Set new value
            entry.at[sensitivity['tech'], sensitivity['variable']] = newValue

        # Special case: if PowerPlant efficiency, also apply to heat rate (heat rate is inverse of efficiency, so a -1.0 multiplier is applied)
        if sensitivity['type'] == 'PowerPlants' and sensitivity['variable'] == 'Efficiency':
            multiplier = 1.0 + -1.0 * sensitivity['multiplier'] / 100.0
            if goodValue(entry.loc[sensitivity['tech'], 'HeatRate']):  # Ensure that entry can be changed
                # Calcualte updated value
                newValue = entry.loc[sensitivity['tech'], 'HeatRate'] * multiplier

                # Check values are reasonable
                if newValue < 3412.0:  # Heat rate corresponding to 100% efficiency
                    newValue = 3412.0

                # Set new value
                entry.at[sensitivity['tech'], 'HeatRate'] = newValue

        # Push updated entry back to inputs dictionary
        inputs[entryName] = entry

    # -------------------
    # Return modified dictionary of inputs
    # -------------------
    return inputs, local

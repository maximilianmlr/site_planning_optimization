import numpy as np
import pandas as pd
import csv
from geopy.distance import vincenty
import random

plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)
distances = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/distances.csv', encoding='unicode_escape', index_col=0)
distances = pd.DataFrame(distances)

locations = pd.DataFrame(plz_nrw['plz'])
customers = pd.DataFrame(plz_nrw['plz'])

locations['open'] = 0
locations['fixed_costs'] = 0
customers['demand'] = 0

rng_cost_fx_low = range(10000, 20000)
rng_cost_fx_high = range(10, 100)
locations['fixed_costs'] = [random.choice(rng_cost_fx_low) for x in locations['fixed_costs']]

rng_demand_low = range(1, 10)
rng_demand_high = range(10, 100)
customers['demand'] = [random.choice(rng_demand_low) for x in customers['demand']]

# Add/Drop Heuristik

# Start Add-Heuristik
I = pd.DataFrame()
z_old = 1000000000000000
z_new = z_old-1
z_list = []
var_list = []
z_fx = 0

while z_new < z_old:
    z_old = z_new
    for index, row in locations.iterrows():
        if row['open'] == 0:
                z_fix = row['fixed_costs'] + z_fx
                z = z_fix + sum([a * b for a, b in zip(list(pd.concat([I, pd.DataFrame(distances.iloc[len(range(index)),:]).T]).min()), list(customers.demand))])
                if z < z_new:
                    z_new = z
                    z_fx_store = z_fix
                    i_low = index
    if z_new < z_old:
        z_fx = z_fx_store
        locations['open'].iloc[i_low] = 1
        I = I.append(pd.DataFrame(distances.iloc[i_low,:]).T, sort=False)

print(locations[locations['open'] == 1])
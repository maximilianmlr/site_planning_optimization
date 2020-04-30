import numpy as np
import pandas as pd
import csv
from geopy.distance import vincenty
import random

class metaheuristics:
    def __init__(self, z_old, locations, distances, customers):
        self.I = pd.DataFrame()
        self.z_old = z_old
        self.z_new = z_old-1
        self.z_fx = 0
        self.locations = locations
        self.distances = distances
        self.customers = customers
    
    def add_heuristic(self):
        while self.z_new < self.z_old:
            self.z_old = self.z_new
            for index, row in self.locations.iterrows():
                if row['open'] == 0:
                        z_fix = row['fixed_costs'] + self.z_fx
                        z = z_fix + sum([a * b for a, b in zip(list(pd.concat([self.I, pd.DataFrame(self.distances.iloc[len(range(index)),:]).T]).min()), list(self.customers.demand))])
                        if z < self.z_new:
                            self.z_new = z
                            z_fx_store = z_fix
                            i_low = index
            if self.z_new < self.z_old:
                self.z_fx = z_fx_store
                self.locations['open'].iloc[i_low] = 1
                self.I = self.I.append(pd.DataFrame(self.distances.iloc[i_low,:]).T, sort=False)
        self.add_z_total = self.z_old
        self.add_open_locations = self.locations[self.locations['open'] == 1]
        return [self.add_z_total, self.add_open_locations]




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
rng_cost_fx_high = range(100000, 200000)
locations['fixed_costs'] = [random.choice(rng_cost_fx_low) for x in locations['fixed_costs']]

rng_demand_low = range(10, 20)
rng_demand_high = range(100, 300)
customers['demand'] = [random.choice(rng_demand_low) for x in customers['demand']]

# Add/Drop Heuristik

# Start Add-Heuristik
I = pd.DataFrame()
z_old = 1000000000000000
z_new = z_old-1
z_fx = 0


    

heuristics = metaheuristics(10000000, locations, distances, customers)
print("Folgende Standorte wurden eröffnet: \n", heuristics.add_heuristic())
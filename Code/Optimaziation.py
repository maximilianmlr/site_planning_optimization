import numpy as np
import pandas as pd
import csv
from geopy.distance import vincenty
import random

class loc:
    def __init__(self, name, data, rng_l):
        self.name = name
        self.locations = data
        self.rng = rng_l
        self.locations['open'] = 0
        self.locations['fixed_costs'] = 0
        self.locations['fixed_costs'] = [random.choice(self.rng) for x in self.locations['fixed_costs']]

class cust:
    def __init__(self, name, data, rng_c):
        self.name = name
        self.customers = data
        self.rng = rng_c
        self.customers['demand'] = 0
        self.customers['demand'] = [random.choice(self.rng) for x in self.customers['demand']]

class metaheuristics:
    def __init__(self, z_old, locations, distances, customers):
        self.I = pd.DataFrame()
        self.z_old = z_old
        self.z_new = z_old-1
        self.z_fx = 0
        self.counter = 0
        self.locations = locations
        self.distances = distances
        self.customers = customers
    
    def add_heuristic(self):
        while self.z_new < self.z_old:
            self.counter = self.counter + 1
            print("Number of iterations: ", self.counter)
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
                self.locations.loc[self.locations.index[i_low], 'open'] = 1
                self.I = self.I.append(pd.DataFrame(self.distances.iloc[i_low,:]).T, sort=False)
        return self.z_old, self.locations[self.locations['open'] == 1]

    def drop_heuristic(self):
        self.locations['open'] = 1
        self.I = self.locations
        self.z_new = sum(self.I['fixed_costs'])
        while self.z_new < self.z_old:
            self.counter = self.counter + 1
            print("Number of iterations: ", self.counter)
            self.z_old = self.z_new
            for index, row in self.locations.iterrows():
                if row['open'] == 1:
                        z_fix = row['fixed_costs'] - self.z_fx
                        z = z_fix + sum([a * b for a, b in zip(list(pd.concat([self.I, pd.DataFrame(self.distances.iloc[len(range(index)),:]).T]).min()), list(self.customers.demand))])
                        if z < self.z_new:
                            self.z_new = z
                            z_fx_store = z_fix
                            i_low = index
            if self.z_new < self.z_old:
                self.z_fx = z_fx_store
                self.locations.loc[self.locations.index[i_low], 'open'] = 0
                self.I = self.I.drop(pd.DataFrame(self.distances.iloc[i_low,:]).T)
        return self.z_old, self.locations[self.locations['open'] == 1]


print("Reading data...")
# Read in Datasets
plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/plz_nrw.csv', encoding='unicode_escape')
#plz_nrw = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)
#distances = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/distances.csv', encoding='unicode_escape', index_col=0)
distances = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/distances.csv', encoding='unicode_escape', index_col=0)
distances = pd.DataFrame(distances)

# Cost and Demand
rng_cost_fx_low = range(10000, 20000)
rng_cost_fx_high = range(100000, 200000)

rng_demand_low = range(10, 20)
rng_demand_high = range(100, 300)

# Add/Drop Heuristik
# Start Add-Heuristik
df_loc = plz_nrw.copy()
loc = loc('low', df_loc, rng_cost_fx_high)
locations_df = loc.locations

df_cust = plz_nrw.copy()
cust = cust('low', df_cust, rng_demand_high)
customers_df = cust.customers

heuristics = metaheuristics(100000000000, locations_df, distances, customers_df)

#print("Starting add heuristic calculation...")
#z, open = heuristics.add_heuristic()
#print('Gesamtkosten: ', z, '\nEröffnete Standorte: \n', open)

print("Starting drop heuristic calculation...")
z, open = heuristics.drop_heuristic()
print('Gesamtkosten: ', z, "\nGeöffnete Standorte: \n", open)
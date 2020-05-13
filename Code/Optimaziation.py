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
        self.locations['fixed_costs'] = (2, 4, 6) # was 0
        #self.locations['fixed_costs'] = [random.choice(self.rng) for x in self.locations['fixed_costs']]

class cust:
    def __init__(self, name, data, rng_c):
        self.name = name
        self.customers = data
        self.rng = rng_c
        self.customers['demand'] = (5, 6, 4) # was 0
        #self.customers['demand'] = [random.choice(self.rng) for x in self.customers['demand']]

class metaheuristics:
    def __init__(self, z_old, locations, distances, customers):
        self.I = pd.DataFrame()
        self.z_old = z_old
        self.z_new = z_old-1
        self.counter = 0
        self.locations = locations
        self.distances = distances
        self.customers = customers
    
    def add_heuristic(self):
        while self.z_new < self.z_old:
            self.counter = self.counter + 1
            print("Number of iterations: ", self.counter)
            self.z_old = self.z_new
            for self.index, self.row in self.locations.iterrows():
                if self.row['open'] == 0:
                        self.z_fix = self.row['fixed_costs'] + self.locations.loc[self.locations['open'] == 1, 'fixed_costs'].sum()
                        self.z = self.z_fix + sum([a * b for a, b in zip(list(pd.concat([self.I, pd.DataFrame(self.distances.iloc[len(range(self.index)),:]).T]).min()), list(self.customers.demand))])
                        if self.z < self.z_new:
                            self.z_new = self.z
                            self.i_low = self.index
            if self.z_new < self.z_old:
                self.locations.loc[self.locations.index[self.i_low], 'open'] = 1
                self.I = self.I.append(pd.DataFrame(self.distances.iloc[self.i_low,:]).T, sort=False)
        return self.z_old, self.locations[self.locations['open'] == 1]

    def drop_heuristic(self):
        self.locations['open'] = 1
        self.I = self.distances
        self.z_new = self.locations['fixed_costs'].sum() + sum([a * b for a, b in zip(list(self.distances.min()), list(self.customers.demand))])
        while self.z_new < self.z_old:
            self.counter = self.counter + 1
            print("Number of iterations: ", self.counter)
            self.z_old = self.z_new
            for self.index, self.row in self.locations.iterrows():
                if self.row['open'] == 1:
                        self.z_fix = self.locations.loc[self.locations['open'] == 1, 'fixed_costs'].sum() - self.row['fixed_costs'] 
                        self.z = self.z_fix + sum([a * b for a, b in zip(list(self.I.drop([self.row['plz']]).min()), list(self.customers.demand))])
                        if self.z < self.z_new:
                            self.z_new = z
                            self.i_low = self.row['plz']
            if self.z_new < self.z_old:
                self.locations.loc[self.locations['plz'] == self.i_low, 'open'] = 0
                self.I = self.I.drop([self.i_low], axis = 0)
        return self.z_old, self.locations[self.locations['open'] == 1]


print("Reading data...")
# Read in Datasets

plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/plz_nrw.csv', encoding='unicode_escape')
#plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/Bugfixing/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)

distances = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/distances.csv', encoding='unicode_escape', index_col=0)
#distances = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/Bugfixing/distances.csv', encoding='unicode_escape', index_col=0)
distances = pd.DataFrame(distances)

# Cost and Demand
rng_cost_fx_low = range(10000, 20000)
rng_cost_fx_high = (range(100000, 200000))
#rng_cost_fx_high = (2, 4, 6)

rng_demand_low = range(10, 20)
rng_demand_high = range(100, 300)
#rng_demand_high = (5, 6, 4)

# Add/Drop Heuristik
# Start Add-Heuristik
df_loc = plz_nrw.copy()
loc = loc('low', df_loc, rng_cost_fx_high)
locations_df = loc.locations

df_cust = plz_nrw.copy()
cust = cust('low', df_cust, rng_demand_high)
customers_df = cust.customers

heuristics = metaheuristics(100000000000, locations_df, distances, customers_df)
print("Starting add heuristic calculation...")
z, open = heuristics.add_heuristic()
print('Gesamtkosten: ', z, '\nEröffnete Standorte: \n', open)

heuristics = metaheuristics(100000000000, locations_df, distances, customers_df)
print("Starting drop heuristic calculation...")
z, open = heuristics.drop_heuristic()
print('Gesamtkosten: ', z, "\nGeöffnete Standorte: \n", open)
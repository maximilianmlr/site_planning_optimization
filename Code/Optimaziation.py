import numpy as np
import pandas as pd
import csv
from geopy.distance import vincenty
import random
from math import exp

class loc:
    def __init__(self, name, data, rng_l):
        self.name = name
        self.locations = data
        self.rng = rng_l
        self.locations['open'] = 0
        if bugfixing == 0:
            self.locations['fixed_costs'] = 0 # was 0
            self.locations['fixed_costs'] = [random.choice(self.rng) for x in self.locations['fixed_costs']]
        else:
            self.locations['fixed_costs'] = rng_l # was 0

class cust:
    def __init__(self, name, data, rng_c):
        self.name = name
        self.customers = data
        self.rng = rng_c
        if bugfixing == 0:
            self.customers['demand'] = 0
            self.customers['demand'] = [random.choice(self.rng) for x in self.customers['demand']]
        else:
            self.customers['demand'] = rng_c # was 0



class adddrop:
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
            self.counter += 1
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
            self.counter += + 1
            print("Number of iterations: ", self.counter)
            self.z_old = self.z_new
            for self.index, self.row in self.locations.iterrows():
                if self.row['open'] == 1:
                        self.z_fix = self.locations.loc[self.locations['open'] == 1, 'fixed_costs'].sum() - self.row['fixed_costs'] 
                        self.z = self.z_fix + sum([a * b for a, b in zip(list(self.I.drop([self.row['plz']]).min()), list(self.customers.demand))])
                        if self.z < self.z_new:
                            self.z_new = self.z
                            self.i_low = self.row['plz']
            if self.z_new < self.z_old:
                self.locations.loc[self.locations['plz'] == self.i_low, 'open'] = 0
                self.I = self.I.drop([self.i_low], axis = 0)
        return self.z_old, self.locations[self.locations['open'] == 1]


class simulated_annealing:
    def __init__(self, locations, distances, customers, alpha, t_end, multiplyer):
        self.loc_full = locations
        self.start = locations
        self.best = self.start
        self.distances = distances
        self.customers = customers
        self.alpha = alpha
        self.multiplyer = multiplyer
        self.T_end = t_end
    
    def create_neighbor(self, locations):
        i = random.choice(locations.loc[locations['open']==1].index)
        k = random.choice(locations.loc[locations['open']==0].index)
        self.neighbor = locations.copy()
        self.neighbor.loc[i, 'open'] = 0
        self.neighbor.loc[k, 'open'] = 1
        return self.neighbor

    def cal_costs(self, locations, distances, customers):
        open_loc = locations.loc[locations['open'] == 1]
        open_loc_list = list(open_loc['plz'])
        open_dist = distances.loc[open_loc_list]

        self.fixcosts = open_loc['fixed_costs'].sum()
        self.varcosts = sum([a * b for a, b in zip(list(open_dist.min()), list(self.customers.demand))])
        self.costs = self.fixcosts + self.varcosts
        return self.costs

    def calculate(self):
        self.best_costs = self.cal_costs(self.best, self.distances, self.customers)
        self.T = self.best_costs * self.multiplyer
        self.initial_costs = self.best_costs
        self.solution = self.best
        while self.T > self.T_end:
            self.xe = self.create_neighbor(self.solution)
            self.costs = self.cal_costs(self.xe, self.distances, self.customers)
            if self.costs <= self.initial_costs:
                self.initial_costs = self.costs
                self.solution = self.xe.copy()
                if self.costs < self.best_costs:
                    self.best_costs = self.costs
                    self.best = self.xe.copy()
                    print(self.best_costs)
            else:
                expo = exp((-(self.costs-self.initial_costs))/self.T)
                if random.random() <= expo:
                    self.initial_costs = self.costs
                    self.solution = self.xe.copy()
            self.T = self.alpha * self.T
            print(self.T, end="\r", flush=True)
        return self.best_costs, self.solution.loc[self.solution['open'] == 1]



print("Reading data...")
# Read in Datasets

bugfixing = 0

if bugfixing == 0:
    plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/plz_nrw.csv', encoding='unicode_escape')
else:
    plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/Bugfixing/plz_nrw.csv', encoding='unicode_escape')

plz_nrw = pd.DataFrame(plz_nrw)

if bugfixing == 0:
    distances = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/distances.csv', encoding='unicode_escape', index_col=0)
else:
    distances = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/Bugfixing/distances.csv', encoding='unicode_escape', index_col=0)
distances = pd.DataFrame(distances)

# Cost and Demand
rng_cost_fx_low = range(10000, 50000)
if bugfixing == 0:
    rng_cost_fx_high = range(100000, 200000)
else:
    rng_cost_fx_high = (2, 4, 6)

rng_demand_low = range(100, 200)
if bugfixing == 0:
    rng_demand_high = range(100, 300)
else:
    rng_demand_high = (5, 6, 4)

# Add/Drop Heuristik
# Start Add-Heuristik
df_loc = plz_nrw.copy()
loc = loc('low', df_loc, rng_cost_fx_low)
locations_df = loc.locations

df_cust = plz_nrw.copy()
cust = cust('low', df_cust, rng_demand_low)
customers_df = cust.customers

heuristics = adddrop(100000000000, locations_df, distances, customers_df)
print("Starting add heuristic calculation...")
z, open = heuristics.add_heuristic()
print('Gesamtkosten: ', z, '\nEröffnete Standorte: \n', open)

# heuristics = adddrop(100000000000, locations_df, distances, customers_df)
# print("Starting drop heuristic calculation...")
# z, open = heuristics.drop_heuristic()
# print('Gesamtkosten: ', z, "\nGeöffnete Standorte: \n", open)

input_sa = locations_df
simann = simulated_annealing(input_sa, distances, customers_df, 0.999, 1, 5)
z, open = simann.calculate()
print('Gesamtkosten: ', z, '\nEröffnete Standorte: \n', open)

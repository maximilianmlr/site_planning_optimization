import numpy as np
import pandas as pd
import csv
import time as time
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
            self.locations['fixed_costs'] = self.rng # was 0

class cust:
    def __init__(self, name, data, rng_c):
        self.name = name
        self.customers = data
        self.rng = rng_c
        if bugfixing == 0:
            self.customers['demand'] = 0
            self.customers['demand'] = [random.choice(self.rng) for x in self.customers['demand']]
        else:
            self.customers['demand'] = self.rng # was 0

class adddrop:
    def __init__(self, z_old, locations, distances, customers):
        self.I = pd.DataFrame()
        self.z_old = z_old
        self.z_new = z_old-1
        self.counter = 0
        self.locations = locations.copy()
        self.distances = distances.copy()
        self.customers = customers.copy()

    def add_heuristic(self):
        min = 9999999999
        while self.z_new < self.z_old:
            self.counter += 1
            print("\rNumber of iterations: ", self.counter, end="")
            self.z_old = self.z_new
            for self.index, self.row in self.locations.loc[self.locations['open']==0].iterrows():
                self.z_fix = self.row['fixed_costs'] + self.locations.loc[self.locations['open'] == 1, 'fixed_costs'].sum()
                tempmin = np.minimum(min, self.distances.iloc[len(range(self.index)),:])
                self.z = self.z_fix + sum([a * b for a, b in zip(list(tempmin), list(self.customers.demand))])
                if self.z < self.z_new:
                    self.z_new = self.z
                    self.i_low = self.index
            if self.z_new < self.z_old:
                self.locations.loc[self.locations.index[self.i_low], 'open'] = 1
                self.I = self.I.append(pd.DataFrame(self.distances.iloc[self.i_low,:]).T, sort=False)
                min = self.I.min().values

        return self.z_old, self.locations

    def drop_heuristic(self):
        self.locations['open'] = 1
        self.I = self.distances
        self.z_new = self.locations['fixed_costs'].sum() + sum([a * b for a, b in zip(list(self.distances.min()), list(self.customers.demand))])
        while self.z_new < self.z_old:
            self.counter += + 1
            print("\rNumber of iterations: ", self.counter, end="")
            self.z_old = self.z_new
            for self.index, self.row in self.locations.loc[self.locations['open']==1].iterrows():
                self.z_fix = self.locations.loc[self.locations['open'] == 1, 'fixed_costs'].sum() - self.row['fixed_costs'] 
                tempmin = self.I.loc[self.I.index != self.row['plz']]
                tempmin = np.min(tempmin, axis=0)
                self.z = self.z_fix + sum([a * b for a, b in zip(list(tempmin), list(self.customers.demand))])
                if self.z < self.z_new:
                    self.z_new = self.z
                    self.i_low = self.row['plz']
            if self.z_new < self.z_old:
                self.locations.loc[self.locations['plz'] == self.i_low, 'open'] = 0
                self.I = self.I.drop([self.i_low], axis = 0)
                min = self.I.values
        return self.z_old, self.locations

class simulated_annealing:
    def __init__(self, locations, distances, customers, alpha, t_end, multiplyer):
        self.loc_full = locations.copy()
        self.start = locations.copy()
        self.best = self.start.copy()
        self.distances = distances.copy()
        self.customers = customers.copy()
        self.alpha = alpha
        self.multiplyer = multiplyer
        self.T_end = t_end
    
    def create_neighbor(self, locations):
        i = random.sample(list(locations.loc[locations['open']==1].index), k = 5)
        i = random.choice(i)
        k = random.sample(list(locations.loc[locations['open']==0].index), k = 5)
        k = random.choice(k)
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
                    print("\rNew best costs found: ", "{:.2f}".format(self.best_costs), end='')
            else:
                expo = exp((-(self.costs-self.initial_costs))/self.T)
                if random.random() <= expo:
                    self.initial_costs = self.costs
                    self.solution = self.xe.copy()
            self.T = self.alpha * self.T
            print("\rTemperature: ", self.T, end="")
        return self.best_costs, self.solution.loc[self.solution['open'] == 1]

class late_acceptance:
    def __init__(self, locations, distances, customers, l, max_iter):
        self.start = locations.copy()
        self.best = self.start.copy()
        self.max_iter = max_iter
        self.distances = distances.copy()
        self.customers = customers.copy()
        self.list = list()
        self.l = l

    def cal_costs(self, locations, distances, customers):
        open_loc = locations.loc[locations['open'] == 1]
        open_loc_list = list(open_loc['plz'])
        open_dist = distances.loc[open_loc_list]

        self.fixcosts = open_loc['fixed_costs'].sum()
        self.varcosts = sum([a * b for a, b in zip(list(open_dist.min()), list(self.customers.demand))])
        self.costs = self.fixcosts + self.varcosts
        return self.costs

    def create_neighbor(self, locations):
        i = random.sample(list(locations.loc[locations['open']==1].index), k = 5)
        i = random.choice(i)
        k = random.sample(list(locations.loc[locations['open']==0].index), k = 5)
        k = random.choice(k)
        self.neighbor = locations.copy()
        self.neighbor.loc[i, 'open'] = 0
        self.neighbor.loc[k, 'open'] = 1
        return self.neighbor

    def calculate(self):
        self.list = [self.cal_costs(self.best, self.distances, self.customers)] * self.l
        self.initial_costs = self.cal_costs(self.start, self.distances, self.customers)
        self.best_costs = self.cal_costs(self.best, self.distances, self.customers)
        i = 0
        k = 0
        self.xe = self.best
        while i <= 10 and k <= self.max_iter:
            #print(self.list, end = '\r', flush = True)
            self.xe = self.create_neighbor(self.start)
            self.costs = self.cal_costs(self.xe, self.distances, self.customers)
            #print(self.costs, self.best_costs, end = '\r', flush = True)
            v = i
            self.index = v % self.l
            k += 1
            print("\r", k, self.best_costs, end = '')
            if self.costs <= self.list[self.index]:
                self.start = self.xe
                self.list[self.index] = self.costs
                if self.costs < self.best_costs:
                    self.best = self.xe
                    self.best_costs = self.costs
                    i += 1
                    #print(i, self.best_costs, end = '\r', flush = True)
        return self.best_costs, self.best.loc[self.best['open'] == 1]


print("Reading data...")
# Read in Datasets

bugfixing = 1

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
rng_cost_fx_low = range(150000, 500000)
if bugfixing == 0:
    rng_cost_fx_high = range(1000000, 3000000)
else:
    rng_cost_fx_high = (2, 4, 6)

rng_demand_low = range(150, 300)
if bugfixing == 0:
    rng_demand_high = range(1000, 3000)
else:
    rng_demand_high = (5, 6, 4)

# Add/Drop Heuristik
# Start Add-Heuristik
df_loc = plz_nrw.copy()
loc = loc('low', df_loc, rng_cost_fx_high)
locations_df = loc.locations

df_cust = plz_nrw.copy()
cust = cust('low', df_cust, rng_demand_high)
customers_df = cust.customers

# heuristics = adddrop(100000000000, locations_df, distances, customers_df)
# start_time = time.time()
# print("\nStarting add heuristic calculation...")
# z, df = heuristics.add_heuristic()
# open = df.loc[df['open'] == 1]
# print('\nGesamtkosten: ', z, '\nEröffnete Standorte: \n', open)
# print("Computation time add heuristic: ", round(time.time() - start_time, 2), "seconds.")


heuristics = adddrop(100000000000, locations_df, distances, customers_df)
start_time = time.time()
print("\nStarting drop heuristic calculation...")
z, df = heuristics.drop_heuristic()
open = df.loc[df['open'] == 1]
print('\nGesamtkosten: ', z, "\nGeöffnete Standorte: \n", open)
print("Computation time drop heuristic: ", round(time.time() - start_time, 2), "seconds.")


input_sa = df
start_time = time.time()
print("\nStarting simulated annealing optimaziation...")
simann = simulated_annealing(input_sa, distances, customers_df, 0.999, 1, 1.5)
z, open = simann.calculate()
print('\nGesamtkosten: ', z, '\nEröffnete Standorte: \n', open)
print("Computation time simulated annealing optimaziation: ", round(time.time() - start_time, 2), "seconds.")


input_la = df
start_time = time.time()
print("\nStarting late acceptance optimaziation...")
lateacc = late_acceptance(input_la, distances, customers_df, 20, 10000)
z, open = lateacc.calculate()
print('\nGesamtkosten: ', z, '\nEröffnete Standorte: \n', open)
print("Computation time late acceptance optimaziation: ", round(time.time() - start_time, 2), "seconds.")




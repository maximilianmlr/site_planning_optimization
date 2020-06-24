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


bugfixing = 0

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

plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/plz_nrw.csv', encoding='unicode_escape')

df_loc_high = plz_nrw.copy()
loc_high = loc('low', df_loc_high, rng_cost_fx_high)
locations_df_high = loc_high.locations

df_loc_low = plz_nrw.copy()
loc_low = loc('low', df_loc_low, rng_cost_fx_low)
locations_df_low = loc_low.locations

df_cust_high = plz_nrw.copy()
cust_high = cust('low', df_cust_high, rng_demand_high)
customers_df_high = cust_high.customers

df_cust_low = plz_nrw.copy()
cust_low = cust('low', df_cust_low, rng_demand_low)
customers_df_low = cust_low.customers

locations_df_high.to_csv('/Users/maximilianmuller/Documents/GitHub/location_optimization/Datasets/locations_df_high.csv')
locations_df_low.to_csv('/Users/maximilianmuller/Documents/GitHub/location_optimization/Datasets/locations_df_low.csv')

customers_df_high.to_csv('/Users/maximilianmuller/Documents/GitHub/location_optimization/Datasets/customers_df_high.csv')
customers_df_low.to_csv('/Users/maximilianmuller/Documents/GitHub/location_optimization/Datasets/customers_df_low.csv')

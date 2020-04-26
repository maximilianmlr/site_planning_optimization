import numpy as np
import pandas as pd
import csv
import geopy.distance

# Variablendekleration

plz_nrw = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)
distances = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
customers = pd.DataFrame(customers)

plz_nrw['open'] = 0
plz_nrw['cost_fix'] = 0
plz_nrw['cost_var'] = 0

customers['demand'] = 0

c = pd.DataFrame()




print(plz_nrw)
print(customers)




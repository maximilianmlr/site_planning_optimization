import numpy as np
import pandas as pd
import csv
import geopy.distance

plz_nrw = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)
customers = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
customers = pd.DataFrame(customers)


c = [(geopy.distance.distance((plz_nrw.loc[i, 'latitude'], plz_nrw.loc[i, 'longitude']), (customers.loc[k, 'latitude'], customers.loc[k, 'longitude'])).m) for i in range(5) for k in range(5)]
print(c)


import numpy as np
import pandas as pd
import csv
import geopy.distance

plz_nrw = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)
customers = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
customers = pd.DataFrame(customers)

c = pd.DataFrame(columns=plz_nrw['plz'], index=plz_nrw['plz'])

for(i in range(len(c.columns)))
    for(k in range(len(c.rows)))
        

print(c)


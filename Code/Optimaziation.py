import numpy as np
import pandas as pd
import csv
import geopy.distance

# Variablendekleration


I = ['Duisburg', 'Wuppertal', 'Essen'] #Standort
J = ['Kunde 1', 'Kunde 2', 'Kunde 3'] #Kunden
d = int #Nachfrage
i = [0, 0, 0]
f = [10, 20, 10]
c = [2, 3 , 2]

plz_nrw = pd.read_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/plz_nrw.csv', encoding='unicode_escape')
plz_nrw = pd.DataFrame(plz_nrw)
plz_nrw['open'] = 0
plz_nrw['cost_fix'] = 0
plz_nrw['cost_var'] = 0


print(plz_nrw)
df = pd.DataFrame({'Name':I,'Eröffnet':i, 'Fixkosten':f, 'Variable Kosten':c})

print(df)



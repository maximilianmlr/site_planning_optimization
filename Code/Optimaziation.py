import numpy as np
import pandas as pd
import csv

# Variablendekleration


I = ['Duisburg', 'Wuppertal', 'Essen'] #Standort
J = ['Kunde 1', 'Kunde 2', 'Kunde 3'] #Kunden
d = int #Nachfrage
i = [0, 0, 0]
f = [10, 20, 10]
c = [2, 3 , 2]

plz_nrw = pd.read_csv("C:/Users/maxim/iCloudDrive/Uni/WiWiMaster\4. Semester\Seminar Optimierung\plz_nrw.csv")
plz_nrw = pd.DataFrame(plz_nrw)
print(plz_nrw.head)
df = pd.DataFrame({'Name':I,'Eröffnet':i, 'Fixkosten':f, 'Variable Kosten':c})

print(df)



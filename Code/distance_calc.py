import pandas as pd
import numpy as np
from geopy.distance import vincenty
from tqdm import tqdm
import geopy.distance

tqdm.pandas()

plz_nrw = pd.read_csv('https://raw.githubusercontent.com/mexemt/location_optimization/master/Datasets/plz_nrw.csv', encoding='unicode_escape')

plz_nrw['coord'] = list(zip(plz_nrw.latitude, plz_nrw.longitude))
square = pd.DataFrame(
    np.zeros(len(plz_nrw) ** 2).reshape(len(plz_nrw), len(plz_nrw)),
    index=plz_nrw.index, columns=plz_nrw.index)

def get_distance(col):
    end = plz_nrw.ix[col.name]['coord']
    return plz_nrw['coord'].apply(vincenty, args=(end,), ellipsoid='WGS-84')

distances = square.progress_apply(get_distance, axis=1).T

def units(input_df):
    return input_df.km

distances = distances.applymap(units)

distances.index = plz_nrw['plz']
distances.columns = plz_nrw['plz']

distances.to_csv('C:/Users/maxim/Documents/GitHub/location_optimization/Datasets/distances.csv')


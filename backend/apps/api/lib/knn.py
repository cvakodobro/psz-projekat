import os
import pandas as pd
from math import sqrt
import numpy as np


def knn(df, new_point, k=None):
    df['rooms'] = df['rooms'].fillna(df['rooms'].median())
    df['class'] = df.apply(lambda x: 1 if x.price < 50000 else 2 if x.price <
                           100000 else 3 if x.price < 150000 else 4 if x.price < 200000 else 5, axis=1)

    X = df.drop(["price", 'class'], axis=1)
    X = X.values
    y = df["class"]
    y = y.values

    distances_e = np.linalg.norm(X - new_point, axis=1)
    distances_m = np.linalg.norm(X - new_point, ord=1, axis=1)

    if k == None:
        k = int(sqrt(len(df.index)+1))
        k = k if k % 2 == 0 else k-1
    else: 
        k=int(k)

    nearest_neighbor_ids = distances_e.argsort()[:k]
    nearest_neighbor_price = y[nearest_neighbor_ids]
    price_e = np.bincount(nearest_neighbor_price).argmax()

    nearest_neighbor_ids = distances_m.argsort()[:k]
    nearest_neighbor_price = y[nearest_neighbor_ids]
    price_m = np.bincount(nearest_neighbor_price).argmax()
    return [price_e, price_m]


# dir_path = os.path.dirname(os.path.realpath(__file__))
# file = os.path.join(dir_path, 'linear_regression/bgd10.csv')
# df = pd.read_csv(
#     'C:/Users/vule0/Desktop/psz-moje/psz-projekat/models/data/bgd1010.csv')

# new_point = np.array([40, 1, 2, -1])

# print(knn(df, new_point))

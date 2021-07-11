import os
import pandas as pd
from math import sqrt
import numpy as np

def knn(df, new_point):
    df['rooms'] = df['rooms'].fillna(df['rooms'].median())

    X = df.drop("price", axis=1)
    X = X.values
    y = df["price"]
    y = y.values
    print(X)
    print(new_point)
    distances = np.linalg.norm(X - new_point, axis=1)

    k = int(sqrt(len(df.index)+1))
    k=k if k % 2==0 else k-1
    
    nearest_neighbor_ids = distances.argsort()[:k]
    nearest_neighbor_price = y[nearest_neighbor_ids]
    return nearest_neighbor_price.mean()

# dir_path = os.path.dirname(os.path.realpath(__file__))
# file = os.path.join(dir_path, 'linear_regression/bgd10.csv')
# df = pd.read_csv(file)

# new_point = np.array([40, 1, 2, -1])

# print(knn(df, new_point))
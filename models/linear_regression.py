from math import sqrt
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# Rescale dataset columns to the range 0-1


def normalize_dataset(dataset, minmax=True):
    if minmax:
        return (dataset-dataset.min())/(dataset.max()-dataset.min())
    else:
        return (dataset-dataset.mean()) / dataset.std()

# Split a dataset into 10 folds


def cross_validation_split(dataset):
    dataset_split = list()
    dataset_copy = dataset.copy()
    fold_size = int(len(dataset_copy.index)/5)
    for i in range(5):
        fold = dataset_copy.sample(n=fold_size)
        dataset_copy = dataset_copy[~dataset_copy.index.isin(fold.index)]
        dataset_split.append(fold)
    return dataset_split

def train_test_split(dataset):
    dataset_copy = dataset.copy()
    train_set = dataset_copy.sample(frac=0.8)
    test_set = dataset_copy[~dataset_copy.index.isin(train_set.index)]
    return train_set, test_set

# Calculate root mean squared error


def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)

def predict(row, coefficients):
    yhat = coefficients[0]
    yhat += coefficients[1] * row['size']
    yhat += coefficients[2] * row['distance_from_center']
    yhat += coefficients[3] * row['rooms']
    yhat += coefficients[4] * row['new']
    yhat += coefficients[5] * row['old']
    yhat += coefficients[6] * row['no_data']

    return yhat

def train_model(train,test, l_rate, reg_rate, n_epoch):
    coef=[0.0 for i in range(7)]
    for epoch in range(n_epoch):
        for index, row in train.iterrows():
            yhat = predict(row, coef)
            error = yhat - row['price']
            coef[0] = coef[0] - l_rate * error / len(train.index) 
            coef[1] = coef[1] - l_rate * error * row['size'] / len(train.index) + reg_rate * coef[1] / len(train.index)
            coef[2] = coef[2] - l_rate * error * row['distance_from_center'] / len(train.index) + reg_rate * coef[2] / len(train.index)
            coef[3] = coef[3] - l_rate * error * row['rooms'] / len(train.index) + reg_rate * coef[3] / len(train.index)
            coef[4] = coef[4] - l_rate * error * row['new'] / len(train.index) + reg_rate * coef[4] / len(train.index)
            coef[5] = coef[5] - l_rate * error * row['old'] / len(train.index) + reg_rate * coef[5] / len(train.index)
            coef[6] = coef[6] - l_rate * error * row['no_data'] / len(train.index) + reg_rate * coef[6] / len(train.index)

    predicted = []
    for index, row in test.iterrows():
        prediction = predict(row, coef)
        predicted.append(prediction)

    actual = test['price'].to_list()
    rmse = rmse_metric(actual, predicted)
    return coef, rmse


def hyperparameters_selection(train,validation, l_rates, reg_rates, n_epoch):
    coefs=list()
    errors=list()
    hyperparameters=list()
    for l_rate in l_rates:
        for reg_rate in reg_rates:
            coef, error = train_model(train,validation,l_rate,reg_rate, n_epoch)
            coefs.append(coef)
            errors.append(error)
            hyperparameters.append([l_rate, reg_rate])
    return coefs, errors, hyperparameters

# Evaluate an algorithm using a cross validation split


def evaluate_algorithm(dataset, l_rates, reg_rates, n_epoch):
    train_set, test_set = train_test_split(dataset)
    validation_folds = cross_validation_split(train_set)

    best_coefs=list()
    best_hypers=list()
    best_errors=list()
    for fold in validation_folds:
        print('train fold')
        validation_set = fold.copy()
        train_set_validation = pd.concat(validation_folds)
        train_set_validation = train_set_validation[~train_set_validation.index.isin(validation_set.index)]
        coefs, errors, hyperparameters = hyperparameters_selection(train_set_validation,validation_set, l_rates, reg_rates, n_epoch)

        best_index = np.argmin(errors)
        best_error=errors[best_index]
        best_coef = coefs[best_index]
        best_hyper = hyperparameters[best_index]

        best_coefs.append(best_coef)
        best_hypers.append(best_hyper)
        best_errors.append(best_error)
    
    best_index = np.argmin(best_errors)
    best_coef = best_coefs[best_index]
    best_hyper = best_hypers[best_index]
    
    predicted=list()
    for index, row in test_set.iterrows():
        prediction = predict(row, best_coef)
        predicted.append(prediction)

    actual = test_set['price'].to_list()
    rmse = rmse_metric(actual, predicted)

    return rmse, best_coef

dir_path = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(dir_path, 'linear_regression/bgd1010.csv')
df = pd.read_csv(file)
df['rooms'] = df['rooms'].fillna(df['rooms'].median())
df['new']=df.apply(lambda x: 1 if x.year==1 else 0, axis=1)
df['old']=df.apply(lambda x: 1 if x.year==-1 else 0, axis=1)
df['no_data']=df.apply(lambda x: 1 if x.year==0 else 0, axis=1)


min = [df["size"].min(), df.distance_from_center.min(), df.rooms.min(), df.price.min()]
max = [df["size"].max(), df.distance_from_center.max(), df.rooms.max(), df.price.max()]
print(min)
print(max)

df_normalizer = normalize_dataset(df, minmax=True)

l_rates = [0.001, 0.01, 0.1, 0.5]
reg_rates = [0.001, 0.01, 0.1, 0.5]
n_epoch = 50

score, coefs = evaluate_algorithm(df_normalizer, l_rates,reg_rates, n_epoch)

print('Score: %s' % score)
print('Coefs:', coefs)
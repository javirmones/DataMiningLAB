#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy
import datetime as dt
import Paths as route_of
import matplotlib.pyplot as plt

import sklearn.neighbors

from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

from pylab import pcolor, xticks, yticks
from sklearn import preprocessing

def plot_courses(data_target):
    data_to_plot = data_target.sort_values('dropout_percentage')
    plt.plot(data_to_plot['dropout_percentage'])

def normalize_filtered_data(file):

    exclude         = ['course_id','from','to']
    df_ex           = file.loc[:, file.columns.difference(exclude)]

    min_max_scaler  = preprocessing.MinMaxScaler()
    df_norm         = min_max_scaler.fit_transform(df_ex)

    return df_norm

def test_corr(df_ex):
    
    R   = corrcoef(transpose(df_ex))
    pcolor(R)
    plt.colorbar()
    yticks(arange(0,14),range(0,14))
    xticks(arange(0,14),range(0,14))
    plt.savefig("plots/correlation.png")

    
    sns.set(style="white")
    mask = numpy.zeros_like(R, dtype=numpy.bool)
    mask[numpy.triu_indices_from(mask)] = True
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(200, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(R, mask=mask, cmap=cmap, vmax=.8,
                square=True, xticklabels=2, yticklabels=2,
                linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
    
    plt.savefig("plots/heat_map.png")
    


def calculatePCA(dataframe):
    #file = pd.read_csv(path, low_memory=False)
    estimator = PCA (n_components = 2)
    X_pca = estimator.fit_transform(dataframe)

    #Print
    print(estimator.explained_variance_ratio_)
    pd.DataFrame(numpy.matrix.transpose(estimator.components_),
    columns=['PC-1', 'PC-2'], index=dataframe.columns)

    #Print
    fig, ax = plt.subplots()

    for i in range(len(X_pca)):
        plt.text(X_pca[i][0], X_pca[i][1], ".")

    plt.xlim(-1, 1.5)
    plt.ylim(-1, 1.5)
    ax.grid(True)
    fig.tight_layout()
    return X_pca

    
def read_dataset(path):
    return pd.read_csv(path)

if __name__ == '__main__':
    data_target = read_dataset(route_of.target_data)
    
    data_target_treated = data_target.drop(data_target.columns[[0]], axis=1) 
    data_norm = normalize_filtered_data(data_target_treated)
    
    calculatePCA(data_norm)
    plot_courses(data_target)
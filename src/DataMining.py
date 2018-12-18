#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy
from numpy import corrcoef, transpose, arange
import datetime as dt
import Paths as route_of
import matplotlib.pyplot as plt

import sklearn.neighbors
import seaborn as sns

from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

from pylab import pcolor, xticks, yticks
from sklearn import preprocessing

exclude         = ['course_id','from','to','course','course_info','combinedopened',
                   'n_navigates','n_discussions','n_wikis','n_page_close',
                   'duration_in_days','dropout_percentage', 'n_drops', 
                   'n_finished']

def plot_courses(data_target):
    data_to_plot = data_target.sort_values('dropout_percentage')
    data_to_plot['dropout_percentage'].hist(histtype = 'bar', bins = 3, label="C")
    
    plt.title("Actual dropout percentage in MOOC dataset")
    plt.xlabel("dropout percentage")
    plt.ylabel("number of courses")
    plt.savefig(route_of.plots.format("histogram_courses_dropouts"))

def cleaning_fields_unnecesaries(dataframe):
    
    dataframe       = dataframe.drop(exclude, axis=1)
    return dataframe

def normalize_filtered_data(dataframe):

    df_ex           = dataframe.loc[:, dataframe.columns.difference(exclude)]

    min_max_scaler  = preprocessing.MinMaxScaler()
    df_norm         = min_max_scaler.fit_transform(df_ex)

    return df_norm

def test_corr(df_ex):
    
    R   = corrcoef(transpose(df_ex))
    pcolor(R)
    plt.colorbar()
    yticks(arange(0,18),range(0,18))
    xticks(arange(0,18),range(0,18))
    plt.show()
    
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
    
    plt.show()
    


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

def plot_pca(X_pca, labels, type_clus):

    colors      = numpy.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
    colors      = numpy.hstack([colors] * 20)
    fig, ax     = plt.subplots()

    for i in range(len(X_pca)):
        plt.text(X_pca[i][0], X_pca[i][1], '.', color=colors[labels[i]])

    plt.xlim(-1, 1)
    plt.ylim(-0.5, 0.8)
    ax.grid(True)
    fig.tight_layout()
    
    
def read_dataset(path):
    return pd.read_csv(path)

if __name__ == '__main__':
    data_target = read_dataset(route_of.target_data)
    
    data_target_treated = data_target.drop(data_target.columns[[0]], axis=1)
    data_target_treated['group'] = pd.cut(data_target_treated['dropout_percentage'], 3, labels=['quality_course','regular_course','low_quality_course'])
    plot_courses(data_target_treated)
    data_target_treated = cleaning_fields_unnecesaries(data_target_treated)

#    data_norm = normalize_filtered_data(data_target_treated)
#    data_norm = pd.DataFrame(data_norm)
    
    calculatePCA(data_norm)
    test_corr(data_norm)
    # Da rangos, hay que cambiarlos a etiqueta
#    data_target_treated['group'] = pd.cut(data_target_treated['dropout_percentage'], 3, labels=['quality_course','regular_course','low_quality_course'])

    
    
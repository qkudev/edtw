import numpy as np
import csv
from datetime import date
from sklearn.metrics import mutual_info_score as MI
from numpy import zeros, mean
from fastdtw import fastdtw as FDTW
from matplotlib import pyplot as plt
from matplotlib import cm
from numpy.random import normal
from scipy.spatial.distance import euclidean
from functions import origin, bins, EMC, nozero_mean, MI_lag, subsets, normalize
import fractions
import pandas as pd
from scipy.stats import entropy
from scipy import stats
import scipy as sp

filename = 'datasets/weather/CF-moscow-20120101-20141231.csv'
input = open(filename, 'r')
reader = csv.reader(input)
data = []

for year in range(2012, 2015):
    reader = csv.reader(input)
    X = []
    date1 = date(year, 1, 1)
    date2 = date(year, 12, 31)

    for row in reader:
        [ DATE, AVRG_C ] = [ row[0], float(row[1]) ]
        DATE = date(int(DATE[0:4]), int(DATE[5:7]), int(DATE[8:10]))
        if date2 < DATE: break
        if date1 <= DATE <= date2:  X.append(AVRG_C)
    data.append(X)
input.close()
X = data[0]
Y = []; Y.extend(data[1]); Y.extend(data[2])

resolution = 5

###############################################

lag = 0
A =

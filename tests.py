import numpy as np
import csv
from datetime import date
from sklearn.metrics import mutual_info_score as MI
from numpy import zeros, mean
from fastdtw import fastdtw as FDTW
from matplotlib import pyplot as plt
from matplotlib import cm
from numpy.random import normal
from functions import origin, bins, EMC, nozero_mean, MI_lag

X = [0,0,0,1,2,3,2,1,0,0]
Y = [0,0,1,2,3,2,1,0,0,0]

print(MI(X,Y))
print(MI(X[1:],Y[:len(Y)-1]))

plt.plot(X)
plt.plot(Y)
plt.show()
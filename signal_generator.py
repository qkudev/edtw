import csv
import numpy as np
from fastdtw import fastdtw as FDTW
from scipy.spatial.distance import euclidean
import random
from sklearn.metrics import mutual_info_score as I
from functions import Hdtw, bins, lag_by_path, bins
from functions import D

import csv
import numpy as np
from scipy import stats
import random
from matplotlib import pyplot as plt


def series_by_path(X,Y, path):

    A = []
    B = []

    for p in path:
        A.append(X[p[0]])
        B.append(Y[p[1]])

    return [A,B]

###
### Reading input peak form
###

input_file = open('input_signal_peak.csv', 'r')
reader = csv.reader(input_file)
for row in reader:
    input_peak = [float(k) for k in row]

input_file.close()


N = 20                                  ## Volume of series
signal_len = len(input_peak)            ## Volume of signal
K = 100                                 ## Number of generated series

###
### Generating no-lag time series with one peak from input_signal_peak.csv
###

nolag_series = np.zeros(N)
for j in range(signal_len):
    nolag_series[j] = input_peak[j]

###
### Generating K time series with random lags and random noise with Gauss's destribution function
###

RELS = []
VARS = []
Iss = 0.
Q = 0.
for i in range(K):

    lag = random.randint(1, N - signal_len - 1)
    #lag = random.randint(1, N //2)

    random_series = np.zeros(N)
    for j in range(signal_len): random_series[lag + j] = input_peak[j]
    r = stats.norm.rvs(size = N)
    for j in range(N): random_series[j] += r[j]/100

    [s, path] = FDTW(nolag_series, random_series, dist=euclidean)
    diffs = [p[1] - p[0] for p in path]
    var = np.var(diffs)
    VARS.append(var)

    I1 = I(nolag_series, random_series)

    L = np.abs(lag_by_path(path))
    L = np.abs(lag_by_path(path[int(L) : len(path) - int(L)]))
    L = np.abs(lag_by_path(path[int(L) : len(path) - int(L)]))

    [A, B] = series_by_path(nolag_series, random_series, path)
    I2 = I(nolag_series[:len(nolag_series) - int(L)],
           random_series[int(L):])

    rel = np.abs(L - lag)/(lag)
    dI = (I2 - I1)/I2
    print("L = {:.2f},\t lag = {}, \t RE= {:.3f} \t I's: {:.2f}".format(L,lag, rel, dI))
    Iss += dI
    Q += rel
    RELS.append(rel)

print("Accuracy ~ "+ str(int(100 - Q/K*100)) + "%")
print("dI  ~ "+ str(int(Iss/K*100)) + "%")
plt.hist(RELS)
fig = plt.figure()
plt.scatter(VARS,RELS)
plt.show()

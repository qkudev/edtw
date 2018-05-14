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

input_file = open('input_signal_peak.csv', 'r')
reader = csv.reader(input_file)
for row in reader:
    input_peak = [float(k) for k in row]

input_file.close()


N = 20                                  ## Volume of series
signal_len = len(input_peak)            ## Volume of signal
K = 100                                 ## Number of generated series

res = 5

###
### Generating no-lag time series with one peak from input_signal_peak.csv
###

#nolag_series= stats.norm.rvs(size = N)
nolag_series= np.zeros(N)
for i in range(1, signal_len):
    nolag_series[i] += input_peak[i]

VARS = []
RELS = []
Q = 0.

for i in range(K):

    lag = random.randint(1, N - signal_len - 1)

    random_series = np.zeros(N)
    for j in range(signal_len): random_series[lag + j] = input_peak[j]
    r = stats.norm.rvs(size = N)
    #for j in range(N): random_series[j] += r[j]/1

    X = bins(nolag_series, res)
    Y = bins(random_series, res)

    [path, Map] = Hdtw(Y,X, res)
    diffs = [p[1] - p[0] for p in path]
    var = np.var(diffs)


    # plt.plot(nolag_series)
    # plt.plot(random_series)
    # fig = plt.figure()

    L = np.abs(res*lag_by_path(path))
    # L = np.abs(lag_by_path(path[int(L): len(path) - int(L)]))
    # L = np.abs(lag_by_path(path[int(L): len(path) - int(L)]))

    rel = np.abs(L - lag)/(lag)

    #print("L = {:.2f},\t lag = {}, \t RE= {:.3f}".format(L,lag, rel))

    if var != 0:
        RELS.append(rel)
        VARS.append(var)
        print("Relative Error:\t{}%,\t\t Variance:\t{:.2f}".format(int(rel * 100), var))

print("\nMean accuracy:\t"+ str(int(100 - np.mean(RELS)*100)) + "%")
plt.hist(RELS)
fig = plt.figure()
plt.scatter(VARS,RELS)
plt.show()
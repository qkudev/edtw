import random
import csv
import numpy as np
import random
from matplotlib import pyplot as plt
from functions import Hdtw, lag_by_path, bins


input_file = open('input_signal_peak.csv', 'r')
reader = csv.reader(input_file)
for row in reader:
    input_peak = [float(k) for k in row]
input_file.close()


N = 50                                  ## Volume of series
signal_len = len(input_peak)            ## Volume of signal
K = 100                                 ## Number of generated series

res = 10

###
### Generating no-lag time series with one peak from input_signal_peak.csv
###

#nolag_series= stats.norm.rvs(size = N)
nolag_series= np.zeros(N)
for i in range(1, signal_len):
    nolag_series[i] += input_peak[i]

VARS = []
LAGS = []
RELS = []

zero_vars = []
norm_vars = []

for i in range(K):

    Lag = random.randint(1, (N - signal_len) // 2)
    random_series = np.zeros(N)
    for j in range(signal_len):
        random_series[Lag + j] = input_peak[j]

    # r = stats.norm.rvs(size = N)
    #for j in range(N): random_series[j] += r[j]/1

    X = bins(nolag_series, res)
    Y = bins(random_series, res)

    [Path, Map] = Hdtw(X, Y, res)

    diffs = [p[1] - p[0] for p in Path]
    Variance = np.var(diffs)
    L = np.abs(res * lag_by_path(Path))

    if Variance == 0:

        X = bins(nolag_series, res//2)
        Y = bins(random_series, res//2)

        [Path, Map] = Hdtw(X, Y, res // 2)
        diffs = [p[1] - p[0] for p in Path]
        Variance = np.var(diffs)
        L = np.abs(res // 2 * lag_by_path(Path))

    RelError = np.abs(1. - L / Lag)

    fig = plt.figure()
    plt.plot(nolag_series)
    plt.plot(random_series)

    fig = plt.figure()
    plt.imshow(Map, cmap='viridis', interpolation='nearest')

    if Variance != 0:
        RELS.append(RelError)
        VARS.append(Variance)
        LAGS.append(Lag)
        print("Relative Error:\t{:.0%},\t\t"
              "Variance:\t{:.2f}\t\tlag: {}".format(RelError, Variance, Lag))
        norm_vars.append(Lag)
    else:
        zero_vars.append(Lag)


### OUTPUT ALL
################################################################################################

print("\n\nMean accuracy:\t{:.0%} of\t{}".format(1. - np.mean(RELS), len(RELS)))
print("Wrong:\t{:.0%}".format(float(len(zero_vars))/K))

plt.hist(zero_vars, color='r')
plt.hist(norm_vars, color='g')

fig = plt.figure()
plt.hist(RELS)

fig = plt.figure()
plt.scatter(LAGS, RELS)

plt.show()
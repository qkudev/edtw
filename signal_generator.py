import csv
import numpy as np
from scipy import stats
from DTWalgorithm import DTW
import random

###
### Reading input peak form
###

input_file = open('input_signal_peak.csv', 'r')
reader = csv.reader(input_file)
for row in reader:
    input_peak = [float(k) for k in row]
input_file.close()

N = 10                                  ## Volume of series
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

Q = 0
for i in range(K):
    lag = random.randint(0, N - signal_len - 1)
    random_series = np.zeros(N)
    for j in range(signal_len):
        random_series[lag + j] = input_peak[j]
    r = stats.norm.rvs(size = N)
    for j in range(N):
        random_series[j] = random_series[j] + r[j]/10
    [A, B, result, diff] = DTW(nolag_series, random_series, "abs")
    E = np.abs(np.average(diff))
    #print("Average: " + str(E) + "    Real generated lag: " + str(lag))
    estimated_lag = (np.floor(E)) * 2
    if np.abs(estimated_lag - lag) < 2:
        Q += 1
print(Q)
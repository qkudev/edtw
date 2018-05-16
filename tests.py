import random
import csv
from scipy import stats
import numpy as np
import random
from matplotlib import pyplot as plt
from functions import Hdtw, lag_by_path, bins, EMC



input_file = open('input_signal_peak.csv', 'r')
reader = csv.reader(input_file)
for row in reader:
    input_peak = [float(k) for k in row]
input_file.close()


N = 30                                  ## Volume of series
res = 3
signal_len = len(input_peak)            ## Volume of signal
K = 50                                 ## Number of generated series



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
micRELS = []

zero_vars = []
norm_vars = []

for i in range(K):

    Lag = random.randint(2, N - signal_len -1)
    random_series = np.zeros(N)
    for j in range(signal_len):
        random_series[Lag + j] = input_peak[j]

    # random_series += stats.norm.rvs(size = N) /100
    # nolag_series += stats.norm.rvs(size = N) /100
    #
    # random_series = random_series / np.linalg.norm(random_series)
    # nolag_series = nolag_series / np.linalg.norm(nolag_series)


    [maxI, micLag] = EMC(random_series, nolag_series,  (N - signal_len) // 2)
    RelMIC = np.abs(Lag - micLag)/Lag
    micRELS.append(RelMIC)
    X = bins(nolag_series, res)
    Y = bins(random_series, res)

    [Path, Map] = Hdtw(X, Y)

    diffs = [p[1] - p[0] for p in Path]
    Variance = np.var(diffs)


    L = 2*np.abs(res*np.mean(diffs))

    # if Variance == 0:
    #     X = bins(nolag_series, res//2)
    #     Y = bins(random_series, res//2)
    #
    #     [Path, Map] = Hdtw(X, Y, res // 2)
    #     diffs = [p[1] - p[0] for p in Path]
    #     Variance = np.var(diffs)
    #     L = np.abs(res // 2 * lag_by_path(Path))

    RelError = np.abs(1. - L / Lag)

    # fig = plt.figure()
    # plt.plot(nolag_series)
    # plt.plot(random_series)
    #
    # # fig = plt.figure()
    # # plt.imshow(Map, cmap='viridis', interpolation='nearest')

    if Variance == 0:
        zero_vars.append(Lag)
    RELS.append(RelError)
    VARS.append(Variance)
    LAGS.append(Lag)
    print("Relative Error:\t{:.0%},\t\t"
          "Relative MIC:\t{:.2f}\t\tlag: {}\t L: {:.2f}\t micLag: {}".format(RelError, RelMIC, Lag, L, micLag))


### OUTPUT ALL
################################################################################################

print("Mean RELS:\t{0:.2f}".format(np.mean(RELS)))
print("\n\nMy accuracy:\t{:.0%} of\t{}".format(1. - np.mean(RELS), len(RELS)))
print("\n\nMIC accuracy:\t{:.0%} of\t{}".format(1. - np.mean(micRELS), len(micRELS)))
print("Wrong:\t{:.0%}".format(float(len(zero_vars))/K))

# plt.hist(norm_vars, color='g')

fig = plt.figure(figsize=(12,8), dpi=80)
plt.xlabel('Relative Error')
plt.ylabel('Count')
ax = plt.gca()
ax.yaxis.set_ticklabels([])
plt.hist(RELS)

fig = plt.figure()
plt.plot(random_series)
plt.plot(nolag_series)
#plt.scatter(LAGS, RELS)

plt.show()
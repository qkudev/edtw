import numpy as np
from sklearn.metrics import mutual_info_score as MI
from numpy import zeros

def normalize(X):
    return np.exp(X)/(np.exp(X) + 1)

def subsets(X):
    res = []
    for i in range(len(X)):
        for j in range(len(X) - i):
            subset = []
            for k in range(i + 1):
                subset.append(X[j + k])
            res.append(subset)
    return res


def origin(X,Y, lagmax):
    Imax = 0
    lag = 0
    N = len(Y)
    result = []
    for i in range(lagmax):

        I = MI(X[lag:], Y[:N - lag])
        result.append((i, I))
        if Imax < I:
            lag = i
            Imax = I
    return [result, Imax, lag]

def bins(series, res= 30):
    n  = len(series)
    while n % res != 0: res -= 1
    binned = []
    for i in range(n // res):
        bin = []
        for j in range(res):
            bin.append(series[i * res + j])

        binned.append(bin)

    return binned

def EMC(X, Y):
    return np.exp(-MI(X,Y))

def nozero_mean(X):
    sum = 0; count = 1
    for x in X:
        sum += x
        if x != 0: count += 1
    return sum/count

def MI_lag(X, Y, max, T=False):
    MAX = MI(X, Y)
    lag = 0
    ALL = [MAX]

    for i in range(1, max):
        I_lagged = MI(X[i:], Y[:len(Y) - i])
        ALL.append(I_lagged)
        if I_lagged > MAX:
            MAX = I_lagged
            lag = i
    return [ALL, MAX, lag]
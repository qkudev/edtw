import numpy as np
from sklearn.metrics import mutual_info_score as I
from scipy import stats
from numpy import zeros



def H(X):
    probs = [np.mean(X == c) for c in set(X)]
    return np.sum(-p * np.log2(p) for p in probs)


def H(X, Y):
    probs = []
    for c1 in set(X):
        for c2 in set(Y):
            probs.append(np.mean(np.logical_and(X == c1, Y == c2)))

    return np.sum(-p * np.log2(p) for p in probs)


def bins(series, resolution = 30):
    n  = len(series)
    binned = []
    for i in range(n // resolution):
        bin = []
        for j in range(resolution): bin.append( series[i * resolution + j] )
        binned.append(bin)

    return binned


def d(X,Y):
    return H(X,Y) - I(X,Y)


def D(X,Y):
    return d(X,Y)/H(X,Y)


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


# def origin(X,Y, lagmax):
#     Imax = 0
#     lag = 0
#     N = len(Y)
#     result = []
#     for i in range(lagmax):
#
#         I = I(X[lag:], Y[:N - lag])
#         result.append((i, I))
#         if Imax < I:
#             lag = i
#             Imax = I
#     return [result, Imax, lag]


def EMC(X, Y):
    return np.exp(-I(X, Y))

def nozero_mean(X):
    sum = 0; count = 1
    for x in X:
        sum += x
        if x != 0: count += 1
    return sum/count

def MI_lag(X, Y, max, T=False):
    MAX = I(X, Y)
    lag = 0
    ALL = [MAX]

    for i in range(1, max):
        I_lagged = I(X[i:], Y[:len(Y) - i])
        ALL.append(I_lagged)
        if I_lagged > MAX:
            MAX = I_lagged
            lag = i
    return [ALL, MAX, lag]
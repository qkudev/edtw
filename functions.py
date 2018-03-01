from numpy import sum, log2, mean, logical_and, exp
import numpy as np
from sklearn.metrics import mutual_info_score as MI
from time import time





def entropy(X, Y):
    probs = []
    for c1 in set(X):
        for c2 in set(Y): probs.append(mean(logical_and(X == c1, Y == c2)))

    return sum(-p * log2(p) for p in probs)


def MI_lag(X, Y, max, T=False):
    ctime = time()
    MAX = MI(X, Y)
    lag = 0

    ALL = []

    for i in range(1, max):
        dist_lag = MI(X[i:], Y[:len(Y) - i])
        #ALL.append(dist_lag)
        if dist_lag > MAX:
            MAX = dist_lag
            lag = i

    if T: return [lag, time() - ctime]
    #return [ALL, lag]
    return lag


def path_lag(path):
    lag = 0
    sum = 0.;
    k = 0

    for p in path:
        difference = abs(p[0] - p[1])
        if difference == 0: k += 1
        sum += difference
        lag = sum/(len(path) - k)

    sum = 0.;
    k = 0

    for i in range(int(lag/2), len(path) - int(lag/2)):
        difference = abs(path[i][0] - path[i][1])
        if difference == 0: k += 1
        sum += difference
        lag = sum / (len(path) -int(lag) -k)

    return lag

    # for p in path:
    #     sum += p[0] - p[1]
    # return sum/len(path)

# def DTW(X,Y, distance, lag=False, T=False):
#     ctime = time()
#     D = zeros((len(X), len(Y)), dtype=float64)
#     p = array([len(X) - 1, len(Y) - 1])
#     result = []
#
#     for i in range(len(X)):
#         for j in range(len(Y)):
#             D[i,j] = power(abs(X[i] - Y[j]), distance)
#             D[i,j] += (i==0 and j!=0)*D[0,j-1]
#             D[i,j] += (i!=0 and j==0)*D[i-1,0]
#             D[i,j] += (i!=0 and j!=0)*min([ D[i - 1][j], D[i - 1][j - 1], D[i][j - 1] ] )
#
#
#     while p[0] != 0 and p[1] != 0:
#         result.append([p[0], p[1]])
#         if abs(p[0] - p[1]) > 12:
#             p -= array([1,1])
#             continue
#         if p[0] == 0 or p[1] == 0: break
#         p -= step(D[p[0] - 1, p[1]], D[p[0] - 1, p[1] - 1], D[p[0], p[1] - 1])
#
#
#     while p[0] != 0 or p[1] != 0:
#         result.append([p[0], p[1]])
#         if p[0] != 0: p[0] -= 1
#         else: p[1] -= 1
#
#
#     result.append([0, 0])
#     result.reverse()
#
#     if lag:
#         diffs = []
#         for r in result:    diffs.append(r[0] - r[1])
#         if T: return [E(diffs), time() - ctime]
#         return E(diffs)
#
#     if T: return [result, time() - ctime]
#     return result
#
# def step(left, left_up, up):
#     if left_up <= left and left_up <= up: return array([1,1])
#     elif left <= left_up and left <= up: return array([1,0])
#
#     return array([0,1])
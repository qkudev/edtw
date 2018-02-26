from numpy import abs, power, min, zeros, float64, array, sum, log2, mean, logical_and, exp
from sklearn.metrics import mutual_info_score as I
from time import time
from numpy import average as E


def average_nozero(X):
    n = 1
    sum = 0.

    for x in X:
        sum += x
        if x != 0 : n += 1

    return sum/n


def entropy(X, Y):
    probs = []
    for c1 in set(X):
        for c2 in set(Y): probs.append(mean(logical_and(X == c1, Y == c2)))

    return sum(-p * log2(p) for p in probs)


def divine(X):
    result_nonnegative = []
    result_nonpositive = []
    for x in X:
        if x >= 0:  result_nonnegative.append(x)
        if x <= 0:  result_nonpositive.append(x)
    return [result_nonnegative, result_nonpositive]


def step(left, left_up, up):
    if left_up <= left and left_up <= up: return array([1,1])
    elif left <= left_up and left <= up: return array([1,0])

    return array([0,1])


def MI_lag(X, Y, max, T=False):
    ctime = time()
    min_dist = exp(-I(X, Y))
    lag = 0

    for i in range(1, max):
        dist_lag = exp(-I(X[i:], Y[:len(Y) - i]))
        if dist_lag < min_dist:
            min_dist = dist_lag
            lag = i

    if T: return [lag, time() - ctime]
    return lag


def DTW(X,Y, distance, lag=False, T=False):
    ctime = time()
    D = zeros((len(X), len(Y)), dtype=float64)
    p = array([len(X) - 1, len(Y) - 1])
    result = []

    for i in range(len(X)):
        for j in range(len(Y)):
            D[i,j] = power(abs(X[i] - Y[j]), distance)
            D[i,j] += (i==0 and j!=0)*D[0,j-1]
            D[i,j] += (i!=0 and j==0)*D[i-1,0]
            D[i,j] += (i!=0 and j!=0)*min([ D[i - 1][j], D[i - 1][j - 1], D[i][j - 1] ] )


    while p[0] != 0 and p[1] != 0:
        result.append([p[0], p[1]])
        if abs(p[0] - p[1]) > 12:
            p -= array([1,1])
            continue
        if p[0] == 0 or p[1] == 0: break
        p -= step(D[p[0] - 1, p[1]], D[p[0] - 1, p[1] - 1], D[p[0], p[1] - 1])


    while p[0] != 0 or p[1] != 0:
        result.append([p[0], p[1]])
        if p[0] != 0: p[0] -= 1
        else: p[1] -= 1


    result.append([0, 0])
    result.reverse()

    if lag:
        diffs = []
        for r in result:    diffs.append(r[0] - r[1])
        if T: return [average_nozero(diffs), time() - ctime]
        return average_nozero(diffs)

    if T: return [result, time() - ctime]
    return result
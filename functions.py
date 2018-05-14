import numpy as np
from sklearn.metrics import mutual_info_score as I

def d(X,Y): return I(X,X) + I(Y,Y) - 2*I(X,Y)

def D(X,Y):
    Ix = I(X,X)
    Iy = I(Y,Y)
    Ixy = I(X,Y)

    return 1. - Ixy/(Ix + Iy - Ixy)

def lag_by_path(path):
    lag = 0.
    k = 0

    for pair in path:
        difference = pair[0] - pair[1]
        lag += difference
        if difference != 0: k += 1
    if k == 0: return 0
    return lag / k

def bins(series, resolution = 30):
    n  = len(series)
    binned = []
    for i in range(n // resolution):
        bin = []
        for j in range(resolution): bin.append( series[i * resolution + j] )
        binned.append(bin)

    return binned

def Hdtw(X, Y, resolution = 10):

    n = len(X)
    m = len(Y)

    ### 1. Building distance matrix

    DistanceMatrix = np.zeros((n, m))
    Map = np.zeros((n, m))
    max_i = 0; max_j = 0; Max = 1000000.
    for i in range(n):
        for j in range(m):
            Distance = d(X[i], Y[j])
            DistanceMatrix[i, j] = Distance
            if Distance < Max:
                max_i = i; max_j = j; Max = Distance

            Map[i, j] = DistanceMatrix[i, j]
            if i == 0 and j > 0: Map[i, j] += Map[i, j - 1]
            if j == 0 and i > 0: Map[i, j] += Map[i - 1, j]

    ### 2. Building Map

    for i in range(1, n):
        for j in range(1, m):
            Map[i, j] += np.min([Map[i - 1, j], Map[i - 1, j - 1], Map[i, j - 1]])

    ### 3. Searching path

    i = n - 1
    j = m - 1
    path = [(i, j)]
    score = Map[i, j]

    while i != 0 and j != 0:
        Min = np.min([Map[i - 1, j], Map[i - 1, j - 1], Map[i, j - 1]])
        if Min == Map[i - 1, j - 1]:
            i -= 1
            j -= 1
        else:
            if Min == Map[i - 1, j]: i -= 1
            else: j -= 1
        score += Map[i, j]
        path.append((i, j))

    while i != 0 or j != 0:
        if i != 0: i -= 1
        else: j -= 1
        score += Map[i, j]
        path.append((i, j))

    path.reverse()

    return [path, DistanceMatrix]

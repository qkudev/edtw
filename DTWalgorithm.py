import numpy as np

def minimum(a, b, c):
    if (a <= b and a <= c):
        return a
    if (b <=a and b <= c):
        return b
    return c

def DTW(X,Y):
    Distance_map = np.zeros((len(X), len(Y)), np.double)

    for i in range(len(X)):
        for j in range(len(Y)):
            Distance_map[i,j] = np.abs(X[i] - Y[j])

    Moves_map = np.zeros((len(X), len(Y)), np.double)

    for i in range(1, len(X)):
        Moves_map[i][0] = Distance_map[i][0] + Moves_map[i - 1][0]

    for j in range(1, len(Y)):
        Moves_map[0][j] = Distance_map[0][j] + Moves_map[0][j -1]

    for i in range(1, len(X)):
        for j in range(1, len(Y)):
            Moves_map[i][j] = Distance_map[i][j] + minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])

    result = []
    l = len(X)

    i = len(X) - 1
    j = len(Y) - 1

    while [i,j] != [0,0]:
        result.append([i,j])
        min = minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])
        if min == Moves_map[i - 1][j - 1]:
            i -= 1
            j -= 1
            continue
        if min == Moves_map[i - 1][j]:
            i -= 1
            continue
        j -= 1

    result.append([0, 0])

    result.reverse()

    return result

def DDTW(X, Y):
    Distance_map = np.zeros((len(X), len(Y)), np.double)

    for i in range(len(X)):
        for j in range(len(Y)):
            Distance_map[i, j] = np.abs(X[i] - Y[j])
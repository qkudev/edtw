from numpy import abs, power, min, zeros, float64, array, sum, log2, mean, logical_and
from sklearn.metrics import mutual_info_score

def entropy(X, Y):
    probs = []
    for c1 in set(X):
        for c2 in set(Y):
            probs.append(mean(logical_and(X == c1, Y == c2)))

    return sum(-p * log2(p) for p in probs)

def lag_by_I(X,Y, max):
    MIN = mutual_info_score(X,Y); lag = 0
    for i in range(1,max):
        if mutual_info_score(X[i:], Y[:len(Y) - i - 1]) < MIN: lag = i

    return lag

def step(left, left_up, up):

    if left_up <= left and left_up <= up: return array([1,1])
    elif left <= left_up and left <= up: return array([1,0])
    return array([0,1])


def DTW(X,Y, distance):

    D = zeros((len(X), len(Y)), dtype=float64)
    p = array([len(X) - 1, len(Y) - 1])
    result = []

    for i in range(len(X)):
        for j in range(len(Y)):
            D[i,j] = power(abs(X[i] - Y[j]), distance) + \
                     (i==0 and j!=0)*D[0,j-1] + (j==0 and i!=0)*D[i-1,0] + \
                     (i!=0 and j!=0)*min([ D[i - 1][j], D[i - 1][j - 1], D[i][j - 1] ] )


    while p[0] != 0 and p[1] != 0:

        result.append([p[0], p[1]])

        if abs(p[0] - p[1]) > 12:
            p -= array([1,1])
            continue

        if p[0] == 0 or p[1] == 0:
            break

        p -= step(D[p[0] - 1, p[1]], D[p[0] - 1, p[1] - 1], D[p[0], p[1] - 1])


    while p[0] != 0 or p[1] != 0:

        result.append([p[0], p[1]])

        if p[0] != 0:
            p[0] -= 1

        else: p[1] -= 1


    result.append([p[0], p[1]])
    result.reverse()

    return result
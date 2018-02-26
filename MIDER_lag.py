import numpy as np
from sklearn.metrics import mutual_info_score

def entropy(X, Y):
    probs = []
    for c1 in set(X):
        for c2 in set(Y):
            probs.append(np.mean(np.logical_and(X == c1, Y == c2)))

    return np.sum(-p * np.log2(p) for p in probs)

def lag_by_I(X,Y, max):

    MIN = mutual_info_score(X,Y); lag = 0

    for i in range(1,max):
        if mutual_info_score(X[i:], Y[:len(Y) - i - 1]) < MIN: lag = i

    return lag




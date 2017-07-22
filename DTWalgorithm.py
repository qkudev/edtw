import numpy as np

def divine(X):
    result_nonnegative = []
    result_nonpositive = []

    for x in X:
        if x >= 0:
            result_nonnegative.append(x)
        if x <= 0:
            result_nonpositive.append(x)
    return [result_nonnegative, result_nonpositive]

def minimum(a, b, c):
    if (a <= b and a <= c):
        return -1
    if (b <=a and b <= c):
        return 0
    return 1

def min3(a, b, c):
    if (a <= b and a <= c):
        return a
    if (b <=a and b <= c):
        return b
    return c

def average_nozero(X):
    n = len(X)
    k = 0
    sum = 0
    for i in range(n):
        sum += X[i]
        if X[i] == 0:
            k += 1
    return sum/(n - k + 1)
def d(X):
    n = len(X)
    result = []
    for i in range(n - 1):
        result.append(X[i + 1] - X[i])
    return result

def normilize(X):
    minX = min(X)
    maxX = max(X)
    d = maxX - minX
    result = []
    for i in range(len(X)):
        result.append((X[i] - minX)/d)
    return result


def DTW(X,Y, distance):

    ###
    ###Variable       | description
    ###
    ### X, Y         - input time series of varibles X and Y
    ### Distance_map - matrix of distances between Xi and Yj
    ### Moves_map    - matrix of moves
    ### moves        - 2*m matrix that contains all moves
    ###                move = -1 is equal to move though Y only
    ###                move = 0 is equal to move throug X and Y simultanioysly
    ###                move - 1 is equal to move through X only
    ###
    ### result       - resulting 2*m matrix, where  min(length(X) = k, length(Y) = n) <= m <= n + k
    ### E(X)         - Expected value estimating function
    ### D(X)         - Despersion estimating function


    ###
    ###Generating distance matrix
    ###ABSmetric of x and y is |x - y|
    ###SQRmetric of x and y is |x - y| in the power of k
    ###

    Distance_map = np.zeros((len(X), len(Y)), np.double)
    if distance == "abs":
        for i in range(len(X)):
            for j in range(len(Y)):
                    Distance_map[i,j] = np.abs(X[i] - Y[j])
    else:
        if distance == "sqr":
            for i in range(len(X)):
                for j in range(len(Y)):
                        Distance_map[i,j] = np.square(X[i] - Y[j])
        else:
            for i in range(len(X)):
                for j in range(len(Y)):
                    Distance_map[i,j] = np.power(np.abs(X[i] - Y[i]), distance)
    ###
    ###Generating moves matrix
    ###

    Moves_map = np.zeros((len(X), len(Y)), np.double)
    Moves_map[0][0] = Distance_map[0][0]
    for i in range(1, len(X)):
        Moves_map[i][0] = Distance_map[i][0] + Moves_map[i - 1][0]

    for j in range(1, len(Y)):
        Moves_map[0][j] = Distance_map[0][j] + Moves_map[0][j -1]

    for i in range(1, len(X)):
        for j in range(1, len(Y)):
            Moves_map[i][j] = Distance_map[i][j] + min3(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])

    ####
    ###Generating result matrix
    ###

    result = []

    i = len(X) - 1
    j = len(Y) - 1

    k = 0
    lag = 0
    lags = []

    diff = []

    while i != 0 and j != 0:
        diff.append(i - j)
        if abs(i - j) > 12:
            i = i - 1
            j = j - 1
            continue
        if i == 0 or j == 0:
            break
        result.append([i, j])
        min = minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])
        if min == 0:
            i -= 1
            j -= 1
            if lag != 0:
                lags.append(k * lag)
                lag = 0
            continue
        if min == -1:
            i -= 1
            if lag == -1:
                k += 1
            else:
                if lag == 1:
                    lags.append(k * lag)
                k = 1
                lag = -1
            continue
        if lag == 1:
            k += 1
        else:
            if lag == -1:
                lags.append(k * lag)
            k = 1
            lag = 1
        j -= 1


    if lag != 0:
        lags.append(k * lag)


    if i == 0 and j != 0:
        if lag == -1:
            lags.append(k * lag)
            k = 1
        while j != 0:
            diff.append(i - j)
            result.append([0, j])
            k += 1
            j -= 1
        lags.append(k)

    if j == 0 and i != 0:
        if lag == 1:
            lags.append(k * lag)
            k = 1
        while i != 0:
            diff.append(i - j)
            result.append([i, 0])
            k += 1
            i -= 1
        lags.append(-k)


    result.append([0, 0])

    result.reverse()

    A = []
    B = []

    for i in range(len(result)):
        A.append(result[i][0])
        B.append(result[i][1])

    return A, B, result, diff
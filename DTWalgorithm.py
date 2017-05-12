import numpy as np
import functions





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

    for i in range(len(X)):
        for j in range(len(Y)):
            if distance == "abs":
                Distance_map[i,j] = functions.ABSdistance(X[i], Y[j])
                continue
            if distance == "sqr":
                Distance_map[i,j] = functions.SQRdistance(X[i], Y[j])

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
            Moves_map[i][j] = Distance_map[i][j] + functions.minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])

    ####
    ###Generating result matrix
    ###

    result = []

    DerivativesX = [0]
    DerivativesY = [0]

    for i in range(1,len(X)):
        DerivativesX.append(float(X[i] - X[i - 1])/2)
    for j in range(1, len(Y)):
        DerivativesY.append(float(Y[j] - Y[j - 1])/2)



    i = len(X) - 1
    j = len(Y) - 1

    k = 0
    lag = 0
    lags = []

    while i != 0 and j != 0:
        if i == 0 or j == 0:
            break
        result.append([i, j])
        #min = minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])
        min = functions.minimum(Moves_map[i - 1][j] + np.abs(DerivativesX[i - 1] - DerivativesY[j]) , Moves_map[i - 1][j - 1] + np.abs(DerivativesX[i - 1] - DerivativesY[j - 1]), Moves_map[i][j - 1] + np.abs(DerivativesX[i] - DerivativesY[j - 1]))
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
            result.append([0, j])
            k += 1
            j -= 1
        lags.append(k)

    if j == 0 and i != 0:
        if lag == 1:
            lags.append(k * lag)
            k = 1
        while j != 0:
            result.append([i, 0])
            k += 1
            i -= 1
        lags.append(-k)


    result.append([0, 0])

    result.reverse()

    return result, lags

def DTWsimple(X, Y, metric):

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

    for i in range(len(X)):
        for j in range(len(Y)):
            if metric == "abs":
                Distance_map[i,j] = functions.ABSdistance(X[i], Y[j])
                continue
            if metric == "sqr":
                Distance_map[i,j] = functions.SQRdistance(X[i], Y[j])

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
            Moves_map[i][j] = Distance_map[i][j] + functions.minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])

    ####
    ###Generating result matrix
    ###

    result = []

    i = len(X) - 1
    j = len(Y) - 1

    while i != 0 and j != 0:
        if i == 0 or j == 0:
            break
        result.append([i, j])

        min = functions.minimum(Moves_map[i - 1][j], Moves_map[i - 1][j - 1], Moves_map[i][j - 1])
        if min == 0:
            i -= 1
            j -= 1
            continue
        if min == -1:
            i -= 1
            continue
        j -= 1

    if i == 0 and j != 0:
        while j != 0:
            j -= 1
            result.append([0, j])


    if j == 0 and i != 0:
        while j != 0:
            i -= 1
            result.append([i, 0])



    result.append([0, 0])

    result.reverse()

    return result
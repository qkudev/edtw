import numpy as np

def minimum(a, b, c):
    if (a <= b and a <= c):
        return -1
    if (b <=a and b <= c):
        return 0
    return 1

def min(a, b, c):
    if (a <= b and a <= c):
        return a
    if (b <=a and b <= c):
        return b
    return c

def SQRdistance(x,y):
    return np.power(np.abs(x - y), 1/2)
def ABSdistance(x,y):
    return np.abs(x - y)

def E(X):

    S = 0
    for x in X:
        S += x
    return float(S)/len(X)

def D(X):
    #Despersion estimating function
    S = 0
    expected_value = E(X)
    for x in X:
        S += np.square(x - expected_value)
    return float(S)/len(X)

def Correlation(X, Y):
    XY = []

    for x in X:
        for y in Y:
            xy = x*y
            if xy not in XY:
                XY.append(xy)


    return (E(XY) - E(X)*E(Y))/np.sqrt(D(X)*D(Y))

def MutualInformation(X, Y):
    pX = []
    pY = []
    print("HELLO")
    if 1 in X:
        print("YES")
    else:
        print("NO")
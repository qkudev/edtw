import numpy as np
import csv
from datetime import date
from matplotlib import pyplot as plt
from matplotlib import cm
from functions import Hdtw, bins, lag_by_path


filename = 'datasets/weather/CF-moscow-20120101-20141231.csv'
input = open(filename, 'r')
reader = csv.reader(input)
data = []

for year in range(2012, 2015):
    reader = csv.reader(input)
    X = []
    date1 = date(year, 1, 1)
    date2 = date(year, 12, 31)

    for row in reader:
        [ DATE, AVRG_C ] = [ row[0], float(row[1]) ]
        DATE = date(int(DATE[0:4]), int(DATE[5:7]), int(DATE[8:10]))
        if date2 < DATE: break
        if date1 <= DATE <= date2:  X.append(AVRG_C)
    data.append(X)
input.close()

A = data[0][:360]
B = []; B.extend(data[1]); B.extend(data[2])

resolution = 10
lag = 11
N = 0
M = 0
REL = 0
RELS = []
VARS = []
while lag < 51:

    X = bins(A, resolution=resolution)
    Y = bins(B[lag:360+lag], resolution=resolution)
    W = Hdtw(X, Y, resolution=resolution)
    L1 = resolution*np.abs(lag_by_path(W))
    relerr1 = np.abs(lag - L1) / (lag + 1)
    print("lag = {}, L = {:.2f}, relerr = {:.3}".format(lag, L1, relerr1))

    # if relerr1 < 0.2: color = 'g'
    # else: color = 'b'
    RELS.append(relerr1); N+=1
    # fig = plt.figure()
    # X_mean = [np.mean(x) for x in X]
    # Y_mean = [np.mean(y) for y in Y]

    # plt.hist(LAGS, color=color)
    # plt.title("{}, {:.2f}, {:.3f}".format(lag, L1, relerr1))

    # fig = plt.figure()
    # plt.plot(X_mean)
    # plt.plot(Y_mean)
    # for w in W:
    #     plt.plot([w[0], w[1]], [X_mean[w[0]], Y_mean[w[1]]], color='r', linewidth=0.5)
    lag += 1


plt.hist(RELS)
plt.show()
print(REL/N)




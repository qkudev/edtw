import numpy as np
import csv
from datetime import date
from sklearn.metrics import mutual_info_score as MI
from numpy import zeros, mean
from fastdtw import fastdtw as FDTW
from matplotlib import pyplot as plt
from matplotlib import cm
from numpy.random import normal
from scipy.spatial.distance import euclidean
from functions import origin, bins, EMC, nozero_mean, MI_lag, subsets, normalize
import fractions
import pandas as pd
from scipy.stats import entropy
from scipy import stats
import scipy as sp

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
X = data[0]
Y = []; Y.extend(data[1]); Y.extend(data[2])

resolution = 5

###############################################

lag = 0
while lag <125:
    fig = plt.figure()
    A = normal(X[:360]);    B = normalize(Y[lag:360 + lag])
    [ALL, MAX, MIlag] = MI_lag(A,B,150)
    [dist, path] = FDTW(A,B,dist=euclidean)
    A_aligned = []; B_aligned = []
    for p in path:
        A_aligned.append(A[p[0]])
        B_aligned.append(B[p[1]])
    [ALL_aligned, MAX_aligned, MIlag_aligned] = MI_lag(A_aligned, B_aligned, 150)

    ALL = normalize(ALL)
    ALL_aligned = normalize(ALL_aligned)
    plt.plot(ALL)
    plt.plot(ALL_aligned)
    plt.legend(["original", "aligned"])
    plt.title("lag = "+str(lag)+"\n" + "MIlag = "+str(MIlag) + "MIlag aligned = "+ str(MIlag_aligned))
    plt.xlabel("Cropped by")
    plt.ylabel("Information")

    fig.savefig("ALIGN_lag="+str(lag))
    lag+= 20
    print(lag)


plt.show()











# while lag <155:
#     A = normalize(X[:360]);    B = normalize(Y[lag:360 + lag])
#     #A = bins(A,resolution); B = bins(B, resolution)
#     [dist, path] = FDTW(A,B,dist=euclidean)
#
#     diffs = [(p[0] - p[1]) for p in path]
#     fig = plt.figure()
#     s = pd.Series(diffs)
#     s.plot.kde()
#     plt.xlim([-200, 200])
#     plt.axvline(mean(diffs))
#     fig.savefig("lags/lag"+str(lag))
#
#
#     lag+=5
# plt.show()



# while lag <185:
#     fig = plt.figure()
#     A = normalize(X[:360]);    B = normalize(Y[lag:360 + lag])
#
#     A = bins(A,resolution); B = bins(B, resolution)
#
#     D = zeros((len(A),len(B)))
#
#     for i in range(len(A)):
#         for j in range(len(B)):
#             D[i,j] = MI(A[i],B[j])
#
#     plt.title("lag = "+str(lag))
#     plt.imshow(D, interpolation='nearest', cmap='inferno')
#     lag+=20
#     fig.savefig("lag = "+str(lag))
#
# plt.show()




#
# MIs = []
# for a in subsets(A):
#     for b in subsets(B):
#         n = len(a)
#         m = len(b)
#         gcd = fractions._gcd(n,m)
#         lcm = int(n*m/gcd)
#         left = a*int(lcm/n)
#         right = b*int(lcm/m)
#         P = []; Q=[]
#         for i in range(len(left)): P.extend(left[i])
#         for i in range(len(left)): Q.extend(right[i])
#         MIs.append((MI(P,Q),a,b))
#
# Max = MIs[0]
#
# for i in range(len(MIs)):
#     if MIs[i][0] > Max[0]:
#         Max = MIs[i]
# print(Max)
# P = []; Q = []
# for i in range(len(Max[1])): P.extend(Max[1][i])
# for i in range(len(Max[2])): Q.extend(Max[2][i])
# plt.plot(P)
# plt.plot(Q)
# plt.show()
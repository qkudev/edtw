import csv
from datetime import date
from functions import MI_lag, path_lag
from numpy import zeros, array
from numpy.linalg import norm
from fastdtw import fastdtw as FDTW
from scipy.spatial.distance import euclidean
from time import time
from sklearn.metrics import mutual_info_score as MI
import numpy as np

def normilize(X):
    X = np.array(X)
    MAX = np.max([ np.max(X), abs(np.min(X)) ])
    MEAN = np.mean(X)
    res = []
    for x in X: res.append((x - MEAN)/MAX)
    return res


### format: YYYY-MM-DD, average C, average F for 2012-2014 years
filename = 'datasets/weather/CF-moscow-20120101-20141231.csv'
input = open(filename, 'r')
reader = csv.reader(input)

data = []
L1 = zeros((3, 3))
L2 = zeros((3, 3))
original = zeros((3,3))

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
##### DATA INPUT END #######


output = open("out.csv", 'w')
writer = csv.writer(output)
X = data[0]
Y = []; Y.extend(data[1]); Y.extend(data[2])
X = normilize(X); Y = normilize(Y)

k = 10

while k < 125:
    row = [k]

    A = X[:365]; B = Y[k:365+k]
    ctime = time()

    L1 = MI_lag(A,B, 2*k)
    t1 = time() - ctime
    err1 = abs(k - L1) / k

    #print("MI lag: {:.2f} \nMI time:{:.2f}s \n".format(L1, time() - ctime))

    ctime = time()
    [dist, path] = FDTW(A,B, dist=euclidean)

    L2 = path_lag(path)
    t2 = time() - ctime
    err2 = abs(k - L2) / k
    #print("DTW lag: {:.2f} \nDTW time: {:.2f}s \n".format(L2, time() - ctime))
    row = [k,err1,err2, L1, L2,t1,t2]
    writer.writerow(row)
    k += 10





# #######################################
# ### MI   ↓
#
# ctime = time()
#
# for i in range(3):
#     for j in range(3):
#         L1[i, j] = MI_lag(data[i][:240], data[j][100:340], 120)
#         original[i,j] = 100.
#
# T1 = time() - ctime
#
# ### MI   ↑
# #######################################
# ### FDTW ↓
#
# ctime = time()
#
# for i in range(3):
#     for j in range(3):
#         L2[ i, j ] = path_lag(FDTW(data[i][:240], data[j][100:340], dist=euclidean)[1])
#
# T2 = time() - ctime
#
# ### FDTW ↑
# #######################################
#
# rel_error1 = norm(L1 - original)/norm(original)
# rel_error2 = norm(L2 - original)/norm(original)
#
# print("Lag matrix by Mutual Information")
# print(L1)
# print("elapsed time: {:.2f}s \n".format(T1))
# print("relative error MI: {}".format(rel_error1))
#
# print("-"*50)
#
# print("Lag matrix by FDTW")
# print(L2)
# print("elapsed time: {:.2f}s".format(T2))
# print("relative error FDTW: {}".format(rel_error2))


#
# cycle = []
# for x in data[0]:
#     cycle.append(x)
# for y in data[1]:
#     cycle.append(y)
#
# k = 100
# r = 150
#
# X = data[0];
#
# Y = cycle[k:k+366]
#
# [All, lag] = MI_lag(X,Y, r)
#
# [dist, path] = FDTW(X,Y,dist=euclidean)
#
# Xaligned = []; Yaligned = []
# for p in path:
#     Xaligned.append(X[p[0]])
#     Yaligned.append(Y[p[1]])
#
# [All_aligned, lag_aligned] = MI_lag(Xaligned, Yaligned, r )
#
# #print(lag)
# #print(lag_aligned)
#
# for el in All_aligned:
#     print(el)
# print(len(All_aligned))
#

# data[i][:180], data[j][60:240] relErr1 = 0.62, relErr2 = 0.39
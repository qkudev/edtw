import csv
from datetime import date
from functions import MI_lag, path_lag, path_lag2
from numpy import zeros
from fastdtw import fastdtw as FDTW
from scipy.spatial.distance import euclidean
from time import time
import numpy as np
from numpy.random import normal
from matplotlib import pyplot as plt

def normilize(X):
    X = np.array(X)
    MAX = 2* np.max([ np.max(X), abs(np.min(X)) ])
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



X = data[0]
Y = []; Y.extend(data[1]); Y.extend(data[2])
Z = []


X = normilize(X); Y = normilize(Y);

MEAN = np.mean(X)
zoom = 2
for i in range(int(len(X)//zoom)):
    Z.append(X[int(zoom)*i])


k = 50

X.extend(normal(X[-1], 0.05, k ))
Z.extend(normal(X[-1], 0.05, len(X) - len(Z)))
print(len(X), len(Z))

output = open("out.csv", 'w')
writer = csv.writer(output)
MEAN = np.mean(X)
row = [k]


# A = X[:365]; B = Y[:365]
X.reverse(); Z.reverse()
A = X; B = Z
A.extend(normal(A[-1],0.05, k))
B.reverse()
B.extend(normal(B[-1],0.05, k))
B.reverse()

ctime = time()

L1 = MI_lag(A,B, 2*k)
t1 = time() - ctime
err1 = abs(k - L1) / k

print("MI lag: {:.2f} \nMI time:{:.2f}s \n".format(L1, time() - ctime))

ctime = time()
[dist, path] = FDTW(A,B, dist=euclidean)

# [L2, L3] = path_lag(path)
[L2, L3] = path_lag(path)
t2 = time() - ctime
err2 = abs(k - L2) / k
print("DTW lag: {:.2f} \n"
      "DTW max: {:.2f} \n"
      "DTW time: {:.2f}s \n".format(L2,L3, time() - ctime))
row = [k,err1,err2, L1, L2,t1,t2]
writer.writerow(row)



L1 = MI_lag(B,A, 2*k)
t1 = time() - ctime
err1 = abs(k - L1) / k

print("MI lag: {:.2f} \nMI time:{:.2f}s \n".format(L1, time() - ctime))

ctime = time()
[dist, path] = FDTW(B,A, dist=euclidean)


[L2, L3] = path_lag(path)
t2 = time() - ctime
err2 = abs(k - L2) / k
print("DTW lag: {:.2f} \n"
      "DTW max: {:.2f} \n"
      "DTW time: {:.2f}s \n".format(L2,L3, time() - ctime))




ctime = time()

L1 = MI_lag(A,B, 2*k)
t1 = time() - ctime
err1 = abs(k - L1) / k

print("MI lag: {:.2f} \nMI time:{:.2f}s \n".format(L1, time() - ctime))

ctime = time()
[dist, path] = FDTW(A,B, dist=euclidean)


[L2, L3] = path_lag2(path)

print(L2)
L2 = np.mean(L2)
t2 = time() - ctime
err2 = abs(k - L2) / k
print("DTW lag: {:.2f} \n"
      "DTW max: {:.2f} \n"
      "DTW time: {:.2f}s \n".format(L2,L3, time() - ctime))
row = [k,err1,err2, L1, L2,t1,t2]
writer.writerow(row)



L1 = MI_lag(B,A, 2*k)
t1 = time() - ctime
err1 = abs(k - L1) / k

print("MI lag: {:.2f} \nMI time:{:.2f}s \n".format(L1, time() - ctime))

ctime = time()
[dist, path] = FDTW(B,A, dist=euclidean)


[L2, L3] = path_lag2(path)

print(L2)

L2 = np.mean(L2)
t2 = time() - ctime
err2 = abs(k - L2) / k
print("DTW lag: {:.2f} \n"
      "DTW max: {:.2f} \n"
      "DTW time: {:.2f}s \n".format(L2,L3, time() - ctime))





plt.plot(X)
plt.plot(Z)
print(len(X),len(Z))
plt.show()
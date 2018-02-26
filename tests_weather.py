import csv
from datetime import date
from functions import MI_lag, path_lag
from numpy import zeros
from fastdtw import fastdtw as FDTW
from scipy.spatial.distance import euclidean
from time import time


### format: YYYY-MM-DD, average C, average F for 2012-2014 years
filename = 'datasets/weather/CF-moscow-20120101-20141231.csv'
input = open(filename, 'r')
reader = csv.reader(input)

data = []
L1 = zeros((3, 3))
L2 = zeros((3, 3))

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

##### DATA INPUT END #######
#######################################
### MI   ↓

ctime = time()

for i in range(3):
    for j in range(3):
        L1[i, j] = MI_lag(data[i][:320], data[j][20:340], 40)

T1 = time() - ctime

### MI   ↑
#######################################
### FDTW ↓

ctime = time()

for i in range(3):
    for j in range(3):
        L2[ i, j ] = path_lag(FDTW(data[i][:320], data[j][20:340], dist=euclidean)[1])

T2 = time() - ctime

### FDTW ↑
#######################################


print("Lag matrix by Mutual Information")
print(L1)
print("elapsed time: {:.2f}s \n".format(T1))
print("Lag matrix by FDTW")
print(L2)
print("elapsed time: {:.2f}s".format(T2))

input.close()
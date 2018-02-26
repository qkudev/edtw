import csv
from functions import DTW, MI_lag
from datetime import date
from numpy import zeros

filename = 'datasets/weather/CF-moscow-20120101-20141231.csv'
### format: YYYY-MM-DD, average C, average F for 2012-2014 years


input = open(filename, 'r')
reader = csv.reader(input)
year = 2012; data = []
L1= zeros((3, 3))
L2 = zeros((3,3))

for year in range(2012, 2015):
    reader = csv.reader(input); X = []
    date1 = date(year, 1, 1); date2 = date(year, 12, 31)

    for row in reader:
        [ DATE, AVRG_C ] = [ row[0], float(row[1]) ]
        DATE = date(int(DATE[0:4]), int(DATE[5:7]), int(DATE[8:10]))
        if date2 < DATE: break
        if date1 <= DATE <= date2:  X.append(AVRG_C)

    data.append(X)


##### DATA INPUT END #######

T1 = 0.; T2 = 0.
for i in range(3):
    for j in range(3):

        [ L1[i, j], t1 ] = MI_lag(data[i][:200], data[j][8:208], 40, T=True)
        [ L2[i, j], t2 ] = DTW( data[i][:200], data[j][8:208],distance=5, lag=True, T=True)

        T1 += t1
        T2 += t2


print("Lag matrix by Mutual Information")
print(L1)
print("elapsed time: {:.2f}s \n".format(T1))
print("Lag matrix by DTW")
print(L2)
print("elapsed time: {:.2f}s".format(T2))

input.close()
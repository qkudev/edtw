import csv
from functions import DTW, lag_by_I
from datetime import date
from numpy import zeros


filename = 'datasets/weather/CF-moscow-20120101-20141231.csv'
### format: YYYY-MM-DD, average C, average F, (C calculated from F to 2 digits after dot)

input = open(filename, 'r')
reader = csv.reader(input)

year = 2012
data = []

for year in range(2012, 2015):
    reader = csv.reader(input)

    XDATE1 = date(year,  1,  1 )
    XDATE2 = date(year, 12, 31 )
    X = []
    for row in reader:
        [DATE, AVRG_C] = [ row[0], row[1] ]
        DATE = date(int(DATE[0:4]), int(DATE[5:7]), int(DATE[8:10]))
        if XDATE2 < DATE: break
        if XDATE1 <= DATE <= XDATE2:  X.append(AVRG_C)
    data.append(X)

Lags= zeros((3,3))
for i in range(3):
    for j in range(3):
        if i ==j: Lags[i,i] = 0; continue
        Lags[i,j] = lag_by_I(data[i][:300],data[j][40:340], 40)

print(Lags)





input.close()
# for i in range(N):
#     for j in range(N):
#         X = VARS[i]
#         Y = VARS[j]
#         result = DTW(X, Y, 1)
#         if i ==1 and j ==0: print(result)
#         for pair in result: diff.append(pair[0] - pair[1])
#         diff.sort()
#
#         [Eplus, Eminus] = divine(diff)
#         Eplus = average(Eplus)
#         Eminus = average(Eminus)
#         E = average(diff)
#         d = 50
#
#         while d > 0.1:
#             last = E
#             q = int(abs(E))
#             Q = len(diff) - q - 1
#             if E >= 0:  Iter = diff[:Q]
#             else:       Iter = diff[q:]
#             E = average(Iter)
#             d = abs(last - E)
#
#
#         if Eplus <= 1 or Eminus > -1 or abs(Eplus + Eminus) > 8: E = 0
#         d = abs(TAU[i][j] - 1 - abs(E))
#         for q in range(5):
#             if d < q + 1: K[q] += 1
#
#         LAGS[i][j] = around(E)
#
#
# DATE	TAVG, F°	TAVG, C°	STATION: RSM00027612	NAME: MOSCOW, RS
#

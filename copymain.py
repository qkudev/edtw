from DTWalgorithm import DTW
from DTWalgorithm import normilize
import scipy
from matplotlib import pyplot as plt
import numpy as np
import csv
import networkx as nx


file = open('datasets/glycolysis.csv', 'r')
reader = csv.reader(file)
data = []

VARS = []

for i in range(10):
    VARS.append([])

LAGS = np.zeros((10,10))
MI = np.zeros((10,10))




data1 = []
data2 = []

#for row in reader:
#    data.append([row[2], row[3]])
#
#for i in range(1,len(data)):
#    [date, temp] = data[i]functions.E(lagsABS)
#    if int(date) < 20160401:
#        data1.append(float(temp))
#    else:
#        data2.append(float(temp))

#for row in reader:
#    data.append([row[2], row[3]])
#
#for i in range(1, len(data)):
#    [date, temp] = data[i]
#    if int(date) > 20150401 and int(date) < 20160401:
#        data1.append(float(temp))
#    if int(date) > 20150101 and int(date) < 20160101:
#        data2.append(float(temp))

for row in reader:
    for i in range(10):
        VARS[i].append(float(row[i]))


X = [0, 0, 3, 2, 2]
Y = [10, 14, 7, 11]
Y = VARS[0]
X = VARS[1]



X = normilize(X)
Y = normilize(Y)


dtwABS, lagsABS, movesABS = DTW(X, Y, "abs")
dtwSQR, lagsSQR, movesSQR = DTW(X, Y, "sqr")

k = int(np.abs(np.average(movesABS)))
ABSmoves = movesABS
print np.average(ABSmoves)

#dtwABS = DTWsimple(X, Y, "abs")
#dtwSQR = DTWsimple(X, Y, "sqr")




fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

plt.plot(X,linewidth=2.0, label = u'first series')
plt.plot(Y,linewidth=2.0, label = u'second series')

ax1.set_color_cycle(['red'])

for i in range(len(dtwABS)):
    plt.plot([dtwABS[i][0], dtwABS[i][1]], [X[dtwABS[i][0]], Y[dtwABS[i][1]]], linewidth=0.5)

#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)

#plt.plot(X, linewidth=2.0)
#plt.plot(Y, linewidth=2.0)

#ax2.set_color_cycle(['red'])


#for i in range(len(dtwSQR)):
#    plt.plot([dtwSQR[i][0], dtwSQR[i][1]], [X[dtwSQR[i][0]], Y[dtwSQR[i][1]]], linewidth=0.5)
#
#ax1.set_title(u'absolute metrics')
#ax2.set_title(u'square metrics')
plt.show()





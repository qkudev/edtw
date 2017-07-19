from DTWalgorithm import DTW
from DTWalgorithm import normilize
from DTWalgorithm import d
import math
from sklearn import metrics
from scipy import stats
from matplotlib import pyplot as plt
import numpy as np
import csv
from csv import writer
import networkx as nx


file = open('datasets/glycolysis.csv', 'r')
reader = csv.reader(file)
data = []

VARS = []

for i in range(10):
    VARS.append([])

LAGS = np.zeros((10,10))
LAGSnormal = np.zeros((10,10))
MI = np.zeros((10,10,10))




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


#for i in range(10):
#    for j in range(10):
#        X = VARS[i]
#        Y = VARS[j]
#        Xnormal = normilize(X)
#        Ynormal = normilize(Y)
#        [A, B, result, diff] = DTW(X,Y, "abs")
#        [A, B, result, normaldiff] = DTW(Xnormal,Ynormal, "abs")
#        lag = np.average(diff)
#        normallag = np.average(normaldiff)
#        k = math.floor(lag)
#        normalk = math.floor(normallag)
#        LAGS[i][j] = abs(k)
#        LAGSnormal[i][j] = abs(normalk)
#
#        MI[i][j] = np.exp(-2*metrics.mutual_info_score(A,B))

MIscore = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        X = VARS[i]
        Y = VARS[j]
        length = len(X)
        [A, B, result, diff] = DTW(X,Y,'abs')
        lag = math.floor(np.average(diff))
        MIscore[i][j] = np.exp(-metrics.mutual_info_score(A, B))
        LAGS[i][j] = abs(lag)






G = nx.DiGraph()

G.add_node(1, label='Citr-M')
G.add_node(2, label= 'AMP-M')
G.add_node(3, label = 'Pi')
G.add_node(4, label = 'F26BP')
G.add_node(5, label = 'F16BP')
G.add_node(6, label = 'DHAP')
G.add_node(7, label = 'F6P')
G.add_node(8, label = 'G6P')
G.add_node(9, label = 'Citr-I')
G.add_node(10, label = 'AMP-I')

for i in range(1,11):
    for j in range(1,11):
        if LAGS[i - 1][j - 1] > 0:
            G.add_edge(i,j, weight = MI[i - 1][j - 1] * 100, lag = LAGS[i - 1][j - 1])


pos = nx.circular_layout(G)
edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]
labels = {}
labels[0] = 'Citr-M'
labels[1] = 'AMP-M'
labels[2] = 'Pi'
labels[3] = 'F26BP'
labels[4] = 'F16BP'
labels[5] = 'DHAP'
labels[6] = 'F6P'
labels[7] = 'G6P'
labels[8] = 'Citr-I'
labels[9] = 'AMP-I'
#nx.draw(G,pos, with_labels=True, width=weights)


lags = open("lags.csv", 'w')

Writer = writer(lags)

for i in range(10):
    row = LAGS[i]
    Writer.writerow(row)
lags.close()

lagsnormal = open('lagsnormal.csv', 'w')

Writer = writer(lagsnormal)

for i in range(10):
    row = LAGSnormal[i]
    Writer.writerow(row)
lagsnormal.close()


lagsout1 = open("lagsout1.csv", 'w')
X = VARS[0]
Y = VARS[9]

[A, B, result, diff] = DTW(X,Y,'abs')
lagswriter = writer(lagsout1)
lagswriter.writerow(diff)
lagsout1.close()


MIout = open('MIout.csv', 'w')
Writer = writer(MIout)

for row in MIscore:
    Writer.writerow(row)
MIout.close()
X = d(VARS[0])
Y = d(VARS[9])
[A, B, dtwABS, movesABS ] = DTW(normilize(X), normilize(Y), "abs")

k = int(np.abs(np.average(movesABS)))
print k
ABSmoves = movesABS


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





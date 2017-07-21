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

tau_file = open("datasets/taumin.csv", 'r')
reader = csv.reader(tau_file)

TAU = []
for row in reader:
    X = [int(k) for k in row]
    TAU.append(X)
print(TAU[1][3])

file = open('datasets/glycolysis.csv', 'r')
reader = csv.reader(file)
data = []

VARS = []
names = ['Citr-M','AMP-M','Pi','F26BP','F16BP','DHAP','F6P','G6P','Citr-I','AMP-I']

for i in range(10):
    VARS.append([])

LAGS = np.zeros((10,10))
LAGSnormal = np.zeros((10,10))
MI = np.zeros((10,10,10))


N = 0

data1 = []
data2 = []


for row in reader:
    for i in range(10):
        VARS[i].append(float(row[i]))


MIscore = np.zeros((10,10), )
LAGS_MATRIX = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        X = VARS[i]
        Y = VARS[j]
        length = len(X)
        [A, B, result, diff] = DTW(X,Y,'abs')
        diff.sort()
        diff_plus = []
        diff_minus = []
        for m in range(len(diff)):
            if diff[m] >= 0:
                diff_plus.append(diff[m])
            if diff[m] <= 0:
                diff_minus.append(diff[m])
        Eplus = np.average(diff_plus)
        Eminus = np.average(diff_minus)
        E = np.average(diff)
        if Eplus <= 1 or Eminus > -1 or abs(abs(Eminus) - Eplus) > 8:
            E = 0
        if abs(TAU[i][j] - 1 - abs(E)) < 5:
            N += 1
            print("Var: " + str(np.var(diff)) + ", +E: " + str(Eplus) + ", -E :" + str(Eminus))
        else:
            fg = plt.figure()
            ax1 = fg.add_subplot(111)
            ax1.text(0.95, 0.9,
                     names[i] + r'$\rightarrow$' + names[j] + "\n" +
                     #str(i) + r'$\rightarrow$' + str(j) + "\n" +
                     "+E(" + r'$\eta$ )=' + str(Eplus) + "\n" +
                     "-E(" + r'$\eta$ )=' + str(Eminus) + "\n" +
                     "E(" + r'$\eta$ )=' + str(E) + "\n" +
                     "D(" + r'$\eta$ )=' + str(np.var(diff)) + "\n" +
                     r'$\tau_{min} = $' + str(TAU[i][j] - 1)
                     ,
                     verticalalignment='top', horizontalalignment='right',
                     transform=ax1.transAxes,
                     color='black', fontsize=15)
            plt.hist(diff, bins=30)

            ax2 = fg.add_subplot(121)
            plt.plot(X, linewidth=2.0, label=u'first series')
            plt.plot(Y, linewidth=2.0, label=u'second series')
            ax2.set_color_cycle(['red'])
            for k in range(len(result)):
                plt.plot([result[k][0], result[k][1]], [X[result[k][0]], Y[result[k][1]]], linewidth=0.5)

        lag = math.floor(np.average(diff))
        LAGS[i][j] = abs(lag)



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
print(N)
ABSmoves = movesABS


#dtwABS = DTWsimple(X, Y, "abs")
#dtwSQR = DTWsimple(X, Y, "sqr")






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





from DTWalgorithm import DTW
from DTWalgorithm import E
from DTWalgorithm import D
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import csv


file = open('weather2.csv', 'r')
reader = csv.reader(file)
data = []

data1 = []
data2 = []

for row in reader:
    data.append([row[2], row[3]])

for i in range(1,len(data)):
    [date, temp] = data[i]
    if int(date) < 20160401:
        data1.append(float(temp) + 50)
    else:
        data2.append(float(temp))





X = [0,0,0,0,0] +  np.cos(np.arange(3*np.pi/2, 2*np.pi, 0.2))
Y = np.sin(np.arange(0, np.pi/2, 0.2))
#Y = data1
#X = data2


dtwABS, lagsABS = DTW(X, Y, "abs")
dtwSQR, lagsSQR = DTW(X, Y, "sqr")






fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

plt.plot(X,linewidth=2.0, label = u'first series')
plt.plot(Y,linewidth=2.0, label = u'second series')

ax1.set_color_cycle(['red'])

for i in range(len(dtwABS)):
    plt.plot([dtwABS[i][0], dtwABS[i][1]], [X[dtwABS[i][0]], Y[dtwABS[i][1]]], linewidth=0.5)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

plt.plot(X, linewidth=2.0)
plt.plot(Y, linewidth=2.0)

ax2.set_color_cycle(['red'])

for i in range(len(dtwSQR)):
    plt.plot([dtwSQR[i][0], dtwSQR[i][1]], [X[dtwSQR[i][0]], Y[dtwSQR[i][1]]], linewidth=0.5)

ax1.set_title(u'absolute metrics')
ax2.set_title(u'square metrics')
plt.show()





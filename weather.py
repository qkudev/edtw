import numpy as np
from DTWalgorithm import DTW
from scipy import stats
import csv
from matplotlib import pyplot as plt



dataset = open("datasets/weather2.csv", 'r')
reader = csv.reader(dataset)

data = []
data1 = []
data2 = []

for row in reader:
    data.append([row[2], row[3]])

for i in range(1, len(data)):
    [date, temp] = data[i]
    if int(date) > 20150501 and int(date) < 20160501:
        data1.append(float(temp))
    if int(date) > 20150401 and int(date) < 20160401:
        data2.append(float(temp))

print(len(data1))
print(len(data2))

output = open("Output/weather_lags.csv", 'w')
Writer = csv.writer(output)

[A, B, dtwABS, lags ] = DTW(data1,data2,'abs')
Writer.writerow(lags)
output.close()

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

plt.plot(data1,linewidth=2.0, label = u'first series')
plt.plot(data2,linewidth=2.0, label = u'second series')

ax1.set_color_cycle(['red'])

for i in range(len(dtwABS)):
    plt.plot([dtwABS[i][0], dtwABS[i][1]], [data1[dtwABS[i][0]], data2[dtwABS[i][1]]], linewidth=0.5)



fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

lags.sort()
for i in range(len(lags)):
    lags[i] = lags[i] + 31
print("EX: ", np.average(lags))
print("1/EX: ",1/np.average(lags))
plt.hist(lags)

plt.show()
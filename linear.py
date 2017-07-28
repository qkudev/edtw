import csv
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from DTWalgorithm import DTW

input_file = open('linear_in.csv', 'r')
reader = csv.reader(input_file)

for row in reader:
    input_series = [float(k) for k in row]

plt.subplot(111)
plt.plot(input_series)

input_file.close()

N = len(input_series)
K = 10

for i in range(K):
    r = stats.norm.rvs(size = N)
    transformed_series = np.zeros(N)
    for j in range(N):
        transformed_series[j] = input_series[j] + r[j]/10
    plt.plot(transformed_series)
    [A, B, result, diff] = DTW(input_series, transformed_series, "abs")
    print(np.average(diff))


plt.show()
from DTWalgorithm import DTW
from matplotlib import pyplot as plt

Y = [2,4, 3,2.5 ,  1, 1]
X = [6, 7, 7,  9, 8,  6, 8]

fig, ax = plt.subplots()

dtw = DTW(X, Y)
plt.plot(X)
plt.plot(Y)


ax.set_color_cycle(['red'])
for i in range(len(dtw)):
    plt.plot([dtw[i][0], dtw[i][1]], [X[dtw[i][0]], Y[dtw[i][1]]])

plt.show()

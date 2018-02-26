from functions import DTW
import csv
from matplotlib import pyplot as plt
from numpy import zeros, average, abs, floor, around

def divine(X):
    result_nonnegative = []
    result_nonpositive = []

    for x in X:
        if x >= 0:
            result_nonnegative.append(x)
        if x <= 0:
            result_nonpositive.append(x)
    return [result_nonnegative, result_nonpositive]


diff = []; TAU = []; VARS = []
name = "glycolysis"
file = open('datasets/'+ name+'.csv', 'r')
reader = csv.reader(file)
for row in reader:
    N = len(row)
    break
file.close()

LAGS = zeros((N,N))
for i in range(N): VARS.append([])

tau_file = open("datasets/taumin_" + name + ".csv", 'r')
file = open('datasets/'+ name+'.csv', 'r')
reader = csv.reader(tau_file)

for row in reader:
    X = [int(k) for k in row]
    TAU.append(X)

reader = csv.reader(file)

K = zeros(5)

for row in reader:
    for i in range(N):
        VARS[i].append(float(row[i]))

for i in range(N):
    for j in range(N):
        X = VARS[i]
        Y = VARS[j]
        result = DTW(X, Y, 1)
        for pair in result: diff.append(pair[0] - pair[1])
        diff.sort()

        [Eplus, Eminus] = divine(diff)
        Eplus = average(Eplus)
        Eminus = average(Eminus)
        E = average(diff)
        d = 50

        while d > 0.1:
            last = E
            q = int(abs(E))
            Q = len(diff) - q - 1
            if E >= 0:  Iter = diff[:Q]
            else:       Iter = diff[q:]
            E = average(Iter)
            d = abs(last - E)


        if Eplus <= 1 or Eminus > -1 or abs(Eplus + Eminus) > 8: E = 0
        d = abs(TAU[i][j] - 1 - abs(E))
        for q in range(5):
            if d < q + 1: K[q] += 1

        LAGS[i][j] = around(E)

        # #if np.abs(E - TAU[i][j]) < 5 and TAU[i][j] != 1:
        # #if i == 0 and j == 1:
        # fg = plt.figure()
        #
        # plt.subplot(211)
        # plt.title("Среднее:" + str(average(diff)) + ", Тау: " + str(TAU[i][j] - 1))
        # #ax1 = fg.add_subplot(111)
        # #ax1.text(0.95, 0.9,
        # #         'G'+str(i) + r'$\rightarrow$' + 'G'+str(j) + "\n" +
        # #         #str(i) + r'$\rightarrow$' + str(j) + "\n" +
        # #         #"+E(" + r'$\eta$ )=' + str(Eplus) + "\n" +
        # #         #"-E(" + r'$\eta$ )=' + str(Eminus) + "\n" +
        # #         "E(" + r'$\eta$ )=' + str(E) + "\n" +
        # #         #"D(" + r'$\eta$ )=' + str(np.var(diff)) + "\n" +
        # #         r'$\tau_{min} = $' + str(TAU[i][j] - 1)
        # #         ,
        # #         verticalalignment='top', horizontalalignment='right',
        # #         transform=ax1.transAxes,
        # #         color='black', fontsize=15)
        # plt.hist(diff, bins=30)
        #
        # #ax2 = fg.add_subplot(121)
        # plt.subplot(212)
        # plt.plot(X, linewidth=2.0, label=u'first series')
        # plt.plot(Y, linewidth=2.0, label=u'second series')
        #
        # #ax2.set_color_cycle(['red'])
        # for k in range(len(result)):
        #     plt.plot([result[k][0], result[k][1]], [X[result[k][0]], Y[result[k][1]]],color='r', linewidth=0.5)

for i in range(5): print(str(int(floor(K[i]*100/(N*N)))) + '%,\t')



#plt.show()

#lagsout = open("Output/lagsout_" + name + ".csv", 'w')
#Writer = csv.writer(lagsout)
#
#for row in LAGS:
#    Writer.writerow(row)
#lagsout.close()




#Accuracy for small_chain:      75%,    81%,    87%,    100%,   100%
#if not zeroing:                62%,    93%,    100%,   100%,   100%

#Accuracy for mapk:             79%,    88%,    91%,    94%,    97%
#if not zeroing:                17%,    22%,    22%,    24%,    25%

#Accuracy for irma_on_off:      60%,    68%,    76%,    76%,    76%
#if not zeroing:                44%,    52%,    60%,    60%,    60%

#Accuracy for glycolysis:       76%,    80%,    82%,    85%,    89%
#if not zeroing:                59%,    66%,    67%,    73%,    76%

#Accuracy for enzyme_cat_chain: 82%,    96%,    96%,    96%,    96%
#if not zeroing:                54%,    67%,    70%,    75%,    75%

#Accuracy for dream4_100:       34%,    44%,    53%,    60%,    66%
#if not zeroing:                9%,     16%,	22%,	28%,	34%

#Accuracy for dream4_10:        44%,    57%,    66%,    69%,    74%
#if not zeroing:                16%,    27%,    33%,    34%,    40%

####
####For taumax == 30:
####

#Accuracy for small_chain:      75%,    81%,    87%,    100%,   100%
#if not zeroing:                62%,    93%,    100%,   100%,   100%

#Accuracy for mapk:             72%,    81%,    82%,    85%,    88%
#if not zeroing:                17%,    22%,    22%,    24%,    25%

#Accuracy for irma_on_off:      60%,    68%,    76%,    76%,    76%
#if not zeroing:                44%,    52%,    60%,    60%,    60%

#Accuracy for glycolysis:       65%,    66%,    68%,    70%,    74%
#if not zeroing:                59%,    66%,    67%,    73%,    76%

#Accuracy for enzyme_cat_chain: 82%,    96%,    96%,    96%,    100%
#if not zeroing:                54%,    67%,    70%,    75%,    75%

#Accuracy for dream4_100:       13%,    18%,    22%,    25%,    28%
#if not zeroing:                9%,     16%,	22%,	28%,	34%

#Accuracy for dream4_10:        26%,    32%,    37%,    40%,    40%
#if not zeroing:                16%,    27%,    33%,    34%,    40%
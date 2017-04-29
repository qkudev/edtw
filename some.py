m = 0
for i in range(10):
    for j in range(10):
        for k in range(10):
            for n in range(10):
                if i + j == k + n:
                    m += 1
                    print(str(i) + str(j) + str(k) + str(n))

print(m)
a = [-5,-6,2,6,-5,-7,5]
b = []
b.append(a[0])
for i in a:
    if i not in b:
        b.append(i)

occurences = []
for j in b:
    k = a.count(j)
    occurences.append(k)
print(occurences)

for i in occurences:
    c = occurences.count(i)
    print(c)

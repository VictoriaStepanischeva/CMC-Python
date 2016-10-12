import Task_2

L = [1,2,3,4,5]
l2 = [6,5,4,3,2,1]
L3 = [999,98,97,87,679]
itrtr = Task_2.generator(L, l2, L3, N = 5)
print("RESULT")
for i in itrtr(100):
    print(i)

import math
from sys import setrecursionlimit,  getrecursionlimit
x = input("Input X: ")
N = input("Input N: ")
default = getrecursionlimit()
setrecursionlimit(4*(int(math.log(float(N)))+1))
result = Task_2.my_pow(int(x), int(N))
print(result)
setrecursionlimit(default)

Task_2.print_digits(result)


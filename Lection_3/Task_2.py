import sys
sys.path += ['../Lection_2']

import Task_1

def generator(*args, N):
    All = []
    for i in args:
        All = Task_1.N_max(N, All, i)
    def iteratormana(minimumana):
        for i in All:
            if not i < minimumana: yield i
    return iteratormana
L = [1,2,3,4,5]
l2 = [6,5,4,3,2,1]
L3 = [999,98,97,87,679]
mana = generator(L, l2, L3, N = 5)
print("RESULT")
for i in mana(100):
    print(i)


import math
from sys import setrecursionlimit,  getrecursionlimit
def my_pow(x, N):
    if N == 0:
        return 1
    elif N == 1:
        return x
    else:
        return my_pow(x, N//2)*my_pow(x, (N+1)//2)

x = input("Input X: ")
N = input("Input N: ")
default = getrecursionlimit()
setrecursionlimit(4*(int(math.log(float(N)))+1))
result = my_pow(int(x), int(N))
print(result)
setrecursionlimit(default)

def print_digits(K):
    if K//10:
        print_digits(K//10)
    print("{}".format(K%10), end ='')
print_digits(result)

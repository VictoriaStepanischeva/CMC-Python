import sys
sys.path += ['../Lection_2']

import Task_1

def generator(*args, N):
    All = []
    for i in args:
        All = Task_1.N_max(N, All, i)
    def iterator(minimum):
        for i in All:
            if not i < minimum: yield i
    return iterator

def my_pow(x, N):
    if N == 0:
        return 1
    elif N == 1:
        return x
    else:
        return my_pow(x, N//2)*my_pow(x, (N+1)//2)

def print_digits(K):
    if K//10:
        print_digits(K//10)
    print("{}".format(K%10), end ='')

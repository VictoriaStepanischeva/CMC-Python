import time
import random
import time
def iterative_merge_sort(S_loc):
    step = 1
    while step <= len(S_loc):
        k = 0
        while k <= len(S_loc):
            S_loc[k:k+2*step] = merge(S_loc[k:k+step],\
                    S_loc[k+step:k+2*step])
            k = k+2*step
        step = 2*step
    return S_loc

def merge(S1_loc, S2_loc):
    S_loc = []
    while len(S1_loc)>0 and len(S2_loc)>0:
        if S1_loc[0] >= S2_loc[0]:
            S_loc.append(S1_loc.pop(0))
        else:
            S_loc.append(S2_loc.pop(0))
    return S_loc + (S1_loc if len(S1_loc)>0 else S2_loc)

N = input()

def N_max(N_loc, S1_loc, S2_loc):
    S = S1_loc+S2_loc
    S =  iterative_merge_sort(S)
    return S[:N_loc]

o = time.time()
M = 1000000;
S1 = [random.random() for elem in range(M)]
S2 = [random.random() for elem in range(M)]
# S1 = [4, 1, 5, 7, 8]
# S2 = [3, 6, 2, 9, 0]
# print (iterative(S1+S2))
print(N_max(int(N), S1, S2))
oo = time.time()
print(oo-o)

import random
import time
import functools
def iterative_merge_sort(All):
    step = 1
    while step < len(All):
        for k in range(0, len(All), 2 * step):
            Left = All[k:k+step]
            Right = All[k+step:k+2*step]
            l = r = 0
            while l < len(Left) and r < len(Right):
                if Left[l] > Right[r]:
                    All[k+l+r] = Left[l]
                    l += 1
                else:
                    All[k+l+r] = Right[r]
                    r += 1
            else:
                All[k+l+r:k+2*step] = Left[l:] if l < len(Left) else Right[r:]
        step = 2*step
    return All

def N_max(N, List1, List2):
#     List1 = [i for i in set(List1)]
#     List2 = [i for i in set(List2)]
    List1 = iterative_merge_sort(List1)
    List2 = iterative_merge_sort(List2)
    All = []
    while len(List1) > 0 and len(List2) > 0 and len(All) < N:
        elem = List1.pop(0) if List1[0] > List2[0] else List2.pop(0)
#         print("{} {}".format(("List1:" if List1[0] > List2[0] else "List2:"), elem))
        if not len(All) or elem < All[-1]: All.append(elem)
    else:
        if len(All) < N:
            if len(List1) > 0:
                All += List1[:N - len(List1)]
            if len(List2) > 0:
                All += List2[:N - len(List2)]
    return All

def main(N, M, K):
    full_time = 0
    for k in range(K):
        S1 = [random.randint(0,2*M) for elem in range(M)]
        S2 = [random.randint(0,2*M) for elem in range(M)]
        o = time.time()
        print(N_max(int(N), S1, S2))
        oo = time.time()
        full_time += oo - o
    return full_time / K

if __name__=="__main__":
    K = 10
    magic_hash = { 10: [1, 2, 5], 100: [2, 5, 10], 1000: [5, 50, 100], 1000000: [5, 100, 1000] }
    with open("results_stepanischeva:{2}-{1}-{0}:{3}:{4}:{5}".format(*time.localtime()), "w") as f:
        for M in sorted(magic_hash.keys()):
            for N in magic_hash[M]:
                s = "N = {}, M = {}".format(N, M)
                print(s)
#                 summ = 0
#                 for i in range(K):
#                     summ += main(N,M)
#                 summ /= K
                s += " time {}\n".format(main(N, M, K))
                f.write(s)

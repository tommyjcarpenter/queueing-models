from __future__ import division
from scipy.misc import comb
from math import pow

_tol = .00001

def _elm_recursive(rho, N, m, cache = {}):
    if m == 0:
        return 1
    else:
        k = (rho, N, m)
        if k in cache:
            term = cache[k]
        else:
            term = _elm_recursive(rho, N, m-1)
            cache[k] = term
            
        return (rho*(N - m + 1)*term ) / (m + rho*(N - m + 1)*term) 

def elm_recursive(rho, N, m):
    #iverson page 146, eq 5.45
    E = _elm_recursive(rho, N, m)
    return ( (N - m)*E*(1 + rho) ) / (N + (N - m)*E*rho)


def elm_comb(rho, N, m):
    offered_traffic = rho / (1 + rho)
    numerator = comb(N-1, m, exact=True)*pow(offered_traffic, m)*pow(1-offered_traffic, N-m)
    denominator = 0
    for i in range(0, m+1):
        denominator += comb(N-1, i, exact=True)*pow(offered_traffic,  i)*pow(1-offered_traffic, N-i)
    
    return numerator / denominator

########################################################################    
    
def test():
    r = 0.1
    rho_range = []
    for i in range(0, 10): #python does not support floating ranges like range(0, .99, .01)
        rho_range.append(r)
        r += 0.1
    for rho in rho_range:
        for N in range(1, 100):
            for m in range(1, N):
                print(rho, N, m, elm_recursive(rho, N, m))
                assert abs(elm_comb(rho, N, m) - elm_recursive(rho, N, m)) < _tol

test()

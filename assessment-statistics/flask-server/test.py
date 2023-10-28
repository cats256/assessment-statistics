import numpy as np
from scipy.stats import lognorm
from scipy.special import gammaln

def order_statistics(N, M, q, X, cdf, parameters):
    U = np.array([cdf(x, *parameters) for x in X])

    lpdf = 0
    lpdf += gammaln(N+1) - gammaln(N*q[0]) - gammaln(N-N*q[M-1]+1)
    lpdf += (N*q[0]-1) * np.log(U[0])
    lpdf += (N-N*q[M-1]) * np.log(1-U[M-1])

    for m in range(1, M):
        lpdf += -gammaln(N*q[m]-N*q[m-1])
        lpdf += (N*q[m]-N*q[m-1]-1) * np.log(U[m] - U[m-1])
        lpdf += 
    return lpdf
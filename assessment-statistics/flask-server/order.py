import numpy as np
from scipy.special import gammaln
import math


def neg_log_likelihood2(N):
    u, v = 0.21, 0.71
    logu, logv = np.log(u), np.log(v)
    i = 21
    j = 71
    log_likelihood = 0
    log_likelihood += (i - 1) * logu
    log_likelihood += (j - i - 1) * (logv + np.log(1 - np.exp(logu - logv)))
    log_likelihood += (N - j) * np.log(1 - v)
    log_likelihood -= gammaln(i)
    log_likelihood -= gammaln(j - i)
    log_likelihood -= gammaln(N - j + 1)
    return log_likelihood


def likelihood(N):
    u, v = 0.21, 0.71
    i, j = 21, 71
    log_likelihood = math.factorial(N) * (u ** (i - 1)) * (v - u) ** (j - i - 1) * (1 - v) ** (N - j) / (math.factorial(i - 1) * math.factorial(j - i - 1) * math.factorial(N - j))
    return log_likelihood


# print(math.factorial(101))
# print(neg_log_likelihood2(101))
print(np.exp(neg_log_likelihood2(100) + gammaln(100 + 1)))
print(likelihood(100))

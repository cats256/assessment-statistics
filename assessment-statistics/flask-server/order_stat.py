from scipy.stats import norm
import numpy as np
from math import factorial
import math


def log_likelihood_order_statistics(x_i, x_j, n, i, j):
    # Ensure that i < j
    if i >= j:
        return "Indices i and j must satisfy i < j"

    # Calculate the pdf and cdf for the standard normal distribution
    f_x_i = norm.pdf(x_i)
    F_x_i = norm.cdf(x_i)
    f_x_j = norm.pdf(x_j)
    F_x_j = norm.cdf(x_j)

    log_likelihood = (i - 1) * np.log(F_x_i) + np.log(f_x_i) + (j - i - 1) * np.log(F_x_j - F_x_i) + np.log(f_x_j) + (n - j) * np.log(1 - F_x_j)

    return log_likelihood


# Example usage
print(log_likelihood_order_statistics(-1, 2, 5, 2, 4))


def neg_log_likelihood3(theta, xs, n):
    mean, std = theta
    x, y = xs
    j = 2
    k = 4
    Fx_x = norm.cdf(x, mean, std)
    Fx_y = norm.cdf(y, mean, std)
    logFx_x = norm.logcdf(x, mean, std)
    logFx_y = norm.logcdf(y, mean, std)
    logfx_x = norm.logpdf(x, mean, std)
    logfx_y = norm.logpdf(y, mean, std)

    log_joint_pdf = 0
    # log_joint_pdf = gammaln(n + 1) - gammaln(j) - gammaln(k - j) - gammaln(n - k + 1)
    log_joint_pdf -= logFx_x * (j - 1)
    log_joint_pdf -= np.log(Fx_y - Fx_x) * (k - 1 - j)
    log_joint_pdf -= np.log(1 - Fx_y) * (n - k)
    log_joint_pdf -= logfx_x + logfx_y

    return log_joint_pdf


print(neg_log_likelihood3((0, 1), (-1, 2), 5))
# from scipy.stats import norm
# import numpy as np
# from math import factorial


# def likelihood_order_statistics(x_i, x_j, n, i, j):
#     # Ensure that i < j
#     if i >= j:
#         return "Indices i and j must satisfy i < j"

#     # Calculate the pdf and cdf for the standard normal distribution
#     f_x_i = norm.pdf(x_i)
#     F_x_i = norm.cdf(x_i)
#     f_x_j = norm.pdf(x_j)
#     F_x_j = norm.cdf(x_j)

#     # Apply the formula for the joint distribution of two order statistics
#     likelihood = (
#         (factorial(n) / (factorial(i - 1) * factorial(j - i - 1) * factorial(n - j))) * (F_x_i) ** (i - 1) * f_x_i * (F_x_j - F_x_i) ** (j - i - 1) * f_x_j * (1 - F_x_j) ** (n - j)
#     )

#     return likelihood


# # Example usage
# data = np.sort(norm.rvs(1.5, 0.5, size=1001))
# print(likelihood_order_statistics(-1, 1, 5, 2, 4))

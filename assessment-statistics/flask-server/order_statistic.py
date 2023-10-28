import numpy as np
from scipy.stats import norm, norm
from scipy.optimize import minimize
from scipy.special import gammaln
from sklearn.linear_model import LinearRegression
import math
from scipy.optimize import differential_evolution
from scipy.optimize import dual_annealing

rng = np.random.default_rng()


def neg_log_likelihood(theta, x, q, N):
    mean, std = theta
    M = len(q)
    x = norm.cdf(x, s=std, loc=mean, scale=1)
    u, v = x
    epsilon = 1e-16
    # print(mean, std, x)
    # print()

    u = max(u, epsilon)
    if np.isnan(u):
        u = epsilon
    v = max(v, epsilon)
    if np.isnan(v):
        v = epsilon
    v_minus_u = max(v - u, epsilon)
    one_minus_v = max(1 - v, epsilon)

    i = 21
    j = 71
    log_likelihood = 0
    log_likelihood += (i - 1) * np.log(u)
    log_likelihood += (j - i - 1) * np.log(v_minus_u)
    log_likelihood += (N - j) * np.log(one_minus_v)
    log_likelihood -= gammaln(i)
    log_likelihood -= gammaln(j - i)
    log_likelihood -= gammaln(N - j + 1)
    return -log_likelihood


# def neg_log_likelihood3(theta, x, q, N):
#     mean, std = theta
#     M = len(q)
#     x = norm.cdf(x, s=std, loc=mean, scale=1)
#     u, v = x
#     epsilon = 1e-10
#     # print(mean, std, x)
#     # print()

#     u = max(u, epsilon)
#     if np.isnan(u):
#         u = epsilon
#     v = max(v, epsilon)
#     if np.isnan(v):
#         v = epsilon
#     v_minus_u = max(v - u, epsilon)
#     one_minus_v = max(1 - v, epsilon)

#     i = 26
#     j = 76
#     log_likelihood = 0
#     log_likelihood += (i - 1) * np.log(u)
#     log_likelihood += (j - i - 1) * np.log(v_minus_u)
#     log_likelihood += (N - j) * np.log(one_minus_v)
#     log_likelihood -= gammaln(i)
#     log_likelihood -= gammaln(j - i)
#     log_likelihood -= gammaln(N - j + 1)
#     return -log_likelihood


def neg_log_likelihood2(theta, x, q, N):
    mean, std = theta
    u, v = norm.cdf(x, s=std, loc=mean, scale=1)
    logu, logv = norm.logcdf(x, s=std, loc=mean, scale=1)
    logupdf, logvpdf = norm.logpdf(x, s=std, loc=mean, scale=1)
    i = 26
    j = 51
    try:
        log_likelihood = 0
        log_likelihood += (i - 1) * logu
        log_likelihood += (j - i - 1) * (logv + np.log(1 - np.exp(logu - logv)))
        # log_likelihood += (j - i - 1) * np.log(v - u)
        # # print(logu, logv)
        # # print(np.exp(logu - logv))
        # print()
        log_likelihood += (N - j) * np.log(1 - v)
        log_likelihood -= gammaln(i)
        log_likelihood -= gammaln(j - i)
        log_likelihood -= gammaln(N - j + 1)
        log_likelihood += logupdf
        log_likelihood += logvpdf
        # if math.isinf(log_likelihood):
        #     print((i - 1) * logu)
        #     print((j - i - 1) * (logv + np.log(1 - np.exp(logu - logv))))
        #     print(log_likelihood)
    except:
        print((j - i - 1) * (logv + np.log(1 - np.exp(logu - logv))))
    # print(log_likelihood)
    return -log_likelihood


def neg_log_likelihood3(theta, xs, q, n):
    mean, std = theta
    x, y = xs
    j = 26
    k = 51
    Fx_x = norm.cdf(x, mean, std)
    Fx_y = norm.cdf(y, mean, std)
    logFx_x = norm.logcdf(x, mean, std)
    logFx_y = norm.logcdf(y, mean, std)
    logfx_x = norm.logpdf(x, mean, std)
    logfx_y = norm.logpdf(y, mean, std)

    log_joint_pdf = 0
    # log_joint_pdf = gammaln(n + 1) - gammaln(j) - gammaln(k - j) - gammaln(n - k + 1)
    log_joint_pdf += logFx_x * (j - 1)
    log_joint_pdf += np.log(Fx_y - Fx_x) * (k - 1 - j)
    log_joint_pdf += np.log(1 - Fx_y) * (n - k)
    log_joint_pdf += logfx_x + logfx_y

    return -log_joint_pdf
    # mean, std = theta
    # Fx_x, Fx_y = norm.cdf(xs, s=std, loc=mean, scale=1)
    # logFx_x, logFx_y = norm.logcdf(xs, s=std, loc=mean, scale=1)
    # logfx_x, logfx_y = norm.logpdf(xs, s=std, loc=mean, scale=1)
    # j = 26
    # k = 51
    # neg_log_ll = 0
    # neg_log_ll += gammaln(j)
    # neg_log_ll += gammaln(k - j)
    # neg_log_ll += gammaln(n - k)
    # neg_log_ll -= logFx_x * (j - 1)
    # neg_log_ll -= np.log(Fx_y - Fx_x) * (k - 1 - j)
    # neg_log_ll -= np.log(1 - Fx_y) * (n - k)
    # neg_log_ll -= logfx_x
    # neg_log_ll -= logfx_y
    # return neg_log_ll


def norm_loss2(params, q, observations):
    mean, std = params
    expected_values = norm.ppf(q, mean, std)

    squared_differences = (observations - expected_values) ** 2
    raw_variance = q * (1 - q) / norm.pdf(norm.ppf(q)) ** 2
    sample_weight = 1 / raw_variance

    return np.sum(squared_differences * sample_weight)


# import numpy as np
# from scipy.stats import gamma
# from scipy.special import gammaln

# def order_statistics(N, M, q, X, cdf, parameters):
#     U = np.array([cdf(x, *parameters) for x in X])

#     lpdf = 0
#     lpdf += gammaln(N+1) - gammaln(N*q[0]) - gammaln(N-N*q[M-1]+1)
#     lpdf += (N*q[0]-1) * np.log(U[0])
#     lpdf += (N-N*q[M-1]) * np.log(1-U[M-1])

#     for m in range(1, M):
#         lpdf += -gammaln(N*q[m]-N*q[m-1])
#         lpdf += (N*q[m]-N*q[m-1]-1) * np.log(U[m] - U[m-1])

#     return lpdf


estimation_total = np.zeros(2)
loss = np.zeros(2)

estimation_total2 = np.zeros(2)
loss2 = np.zeros(2)

# data = np.arange(1001)
# print(np.quantile(data, 0.75))
true_params = np.array([1.5, 0.5])
for i in range(1001):
    data = np.sort(norm.rvs(1.5, 0.5, size=1001))
    # print(data)
    q = np.array([0.025, 0.050])
    x = np.quantile(data, q)
    # print(x)
    # print(norm.cdf(x, s=1.4, loc=0.4, scale=1))
    N = 1001
    initial_guess = np.array([0.4, 1.6])

    # result = minimize(neg_log_likelihood, initial_guess, bounds=[(0.2, 3.0), (0.15, 2.5)], args=(x, q, N), method="L-BFGS-B")
    # optimal_theta = result.x
    # estimation_total += optimal_theta
    # loss += abs(true_params - optimal_theta) ** 1

    # result = minimize(neg_log_likelihood2, initial_guess, bounds=[(0.2, 3.0), (0.15, 2.5)], args=(np.array([data[20], data[70]]), q, N), method="Nelder-Mead")
    # result = differential_evolution(
    #     neg_log_likelihood3,  # The objective function to be minimized
    #     bounds=[(0.2, 3.0), (0.15, 2.5)],  # Bounds for variables
    #     args=(np.array([data[25], data[50]]), q, N),  # Additional arguments to pass to the objective function
    #     # You can adjust the following parameters as needed
    # )
    # print(data[0])
    result = dual_annealing(
        neg_log_likelihood3,  # The objective function to be minimized
        bounds=[(-1.0, 4.0), (0.1, 3)],  # Bounds for variables
        # args=(np.array([data[25], data[50]]), q, N),  # Additional arguments to pass to the objective function
        args=(np.array([data[25], data[50]]), q, N),
        # You can adjust the following parameters as needed
        maxiter=1000,  # Maximum number of global search iterations
    )
    # print(result)
    optimal_theta = result.x
    estimation_total += optimal_theta
    loss += abs(true_params - optimal_theta) ** 1

    # standard_norm_quantiles = norm.ppf(q)
    # raw_variance = q * (1 - q) / norm.pdf(norm.ppf(q)) ** 1
    # sample_weight = 1 / raw_variance

    # q = q.reshape(-1, 1)
    # standard_norm_quantiles = standard_norm_quantiles.reshape(-1, 1)

    # model = LinearRegression().fit(standard_norm_quantiles, x, sample_weight=sample_weight)
    # optimal_theta = np.array([float(model.intercept_), float(model.coef_[0])])
    # # optimal_theta = minimize(
    # #     norm_loss2,
    # #     initial_guess,
    # #     # args=(np.array([0.25, 0.50]), np.array([data[25], data[50]])),
    # #     args=(np.array([0.25, 0.50]), x),
    # #     method="L-BFGS-B",
    # #     bounds=[(0.1, 3.0), (0.15, 2.5)],
    # # )
    # # # print(optimal_theta)
    # estimation_total2 += optimal_theta
    # loss2 += abs(true_params - optimal_theta) ** 1
    # # print(neg_log_likelihood3(optimal_theta, norm.ppf(np.array([0.25, 0.50]), 0.5, 1.5), q, N))
    # # print(neg_log_likelihood3(result.x, norm.ppf(np.array([0.25, 0.50]), 0.5, 1.5), q, N))

    if i % 10 == 0:
        print(i)
        print(estimation_total / (i + 1))
        print(estimation_total2 / (i + 1))
        print(loss)
        print(loss2)

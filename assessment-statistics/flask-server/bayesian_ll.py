import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.special import gammaln
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng()


import numpy as np
from scipy.stats import norm
from scipy.special import gammaln


def neg_log_likelihood(theta, x, q, N):
    mean, std = theta
    M = len(q)
    x = norm.cdf(x, loc=mean, scale=std)
    u, v = x
    epsilon = 1e-16  # small constant to avoid log(0)

    u = max(u, epsilon)
    if np.isnan(u):
        u = epsilon
    v = max(v, epsilon)
    if np.isnan(v):
        v = epsilon
    v_minus_u = max(v - u, epsilon)
    one_minus_v = max(1 - v, epsilon)

    i = 26
    j = 76
    log_likelihood = 0
    log_likelihood += (i - 1) * np.log(u)
    log_likelihood += (j - i - 1) * np.log(v_minus_u)
    log_likelihood += (N - j) * np.log(one_minus_v)
    log_likelihood -= gammaln(i)
    log_likelihood -= gammaln(j - i)
    log_likelihood -= gammaln(N - j + 1)
    return -log_likelihood


def neg_log_likelihood2(theta, x, q, N):
    mean, std = theta
    x = norm.cdf(x, loc=mean, scale=std)
    u, v = x
    i = 26
    j = 76
    log_likelihood = 0
    log_likelihood += (i - 1) * np.log(u)
    log_likelihood += (j - i - 1) * np.log(v - u)
    log_likelihood += (N - j) * np.log(1 - v)
    log_likelihood -= gammaln(i)
    log_likelihood -= gammaln(j - i)
    log_likelihood -= gammaln(N - j + 1)
    return -log_likelihood


# def neg_log_likelihood(theta, x, q, N):
#     mean, std = theta
#     M = len(q)
#     x = norm.cdf(x, loc=mean, scale=std)
#     u, v = x
#     i = 26
#     j = 76
#     log_likelihood = 0
#     # log_likelihood += np.log(u ** (i - 1))
#     # log_likelihood += np.log((v - u) ** (j - i - 1))
#     # log_likelihood += np.log((1 - v) ** (N - j))
#     print("u = ", u)
#     print(np.log(u))
#     log_likelihood += (i - 1) * np.log(u)
#     # print((i - 1) * np.log(u))
#     # print(log_likelihood)
#     log_likelihood += (j - i - 1) * np.log(v - u)
#     # print(log_likelihood)
#     log_likelihood += (N - j) * np.log(1 - v)
#     # print(log_likelihood)
#     log_likelihood -= gammaln(i)
#     # print(log_likelihood)
#     log_likelihood -= gammaln(j - i)
#     # print(log_likelihood)
#     log_likelihood -= gammaln(N - j + 1)
#     # print(log_likelihood)
#     # print()
#     # log_likelihood -= np.log(factorial(i - 1))
#     # log_likelihood -= np.log(factorial(j - i - 1))
#     # log_likelihood -= np.log(factorial(N - j))
#     return -log_likelihood  # negative log likelihood


# def neg_log_likelihood(theta, x, q, N):
#     M = len(q)
#     F_theta = norm.cdf(x, loc=theta[0], scale=theta[1])
#     f_theta = norm.pdf(F_theta, loc=theta[0], scale=theta[1])

#     term1 = (q[0] * N - 1) * np.log(F_theta[0])
#     term2 = (N - q[-1] * N) * np.log1p(-F_theta[-1])
#     term3 = np.sum([(q[m] * N - q[m - 1] * N - 1) * np.log(F_theta[m] - F_theta[m - 1]) for m in range(1, M)])
#     term4 = np.sum(np.log(f_theta))

#     log_likelihood = term1 + term2 + term3 + term4
#     return -log_likelihood  # negative log likelihood


estimation_total = np.zeros(2)
loss = np.zeros(2)
estimation_total2 = np.zeros(2)
loss2 = np.zeros(2)

true_params = np.array([1.45, 0.45])
for i in range(10000):
    data = np.sort(rng.normal(1.45, 0.45, size=101))

    # Example usage:
    q = np.array([0.25, 0.75])
    x = np.quantile(data, q)
    N = 101
    initial_guess = np.array([2.0, 0.75])

    result = minimize(neg_log_likelihood, initial_guess, args=(x, q, N))
    # print(result)
    optimal_theta = result.x
    estimation_total += optimal_theta
    loss += abs(true_params - optimal_theta) ** 1

    result = minimize(neg_log_likelihood2, initial_guess, bounds=[(0.8, 3.0), (0.2, 2.5)], args=(x, q, N))
    optimal_theta = result.x
    estimation_total2 += optimal_theta
    loss2 += abs(true_params - optimal_theta) ** 1

    # standard_norm_quantiles = norm.ppf(q)

    # raw_variance = q * (1 - q) / norm.pdf(norm.ppf(q)) ** 2
    # sample_weight = 1 / raw_variance

    # model = LinearRegression().fit(standard_norm_quantiles, x, sample_weight)
    # optimal_theta = np.array([float(model.intercept_[0]), float(model.coef_[0][0])])

    if i % 100 == 0 and i != 0:
        print(estimation_total / i)
        print(estimation_total2 / i)
        print(loss)
        print(loss2)

print(estimation_total)
# from bqme.distributions import Normal, Gamma
# from bqme.models import NormalQM

# N, q, X = 100, [0.25, 0.5, 0.75], [-0.1, 0.3, 0.8]

# # define priors
# mu = Normal(0, 1, name="mu")
# sigma = Gamma(1, 1, name="sigma")

# # define likelihood
# model = NormalQM(mu, sigma)

# # sample the posterior
# fit = model.sampling(N, q, X)

# # extract posterior samples
# mu_posterior = fit.mu
# sigma_posterior = fit.sigma

# # get stan sample object
# stan_samples = fit.stan_obj

# # get pdf and cdf of x_new
# x_new = 1.0
# pdf_x = fit.pdf(x_new)
# cdf_x = fit.cdf(x_new)

# # get percent point function of q_new (inverse of cdf)
# # default return values are samples from posterior predictive p(x|q)
# q_new = 0.2
# ppf_q = fit.ppf(q_new)

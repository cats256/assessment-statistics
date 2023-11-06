import scipy.stats as stats
import numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize
from scipy.stats import norm


def log_likelihood_order_stats(sorted_sample, ranks, mu, sigma):
    n = len(sorted_sample)
    k = len(ranks)

    order_statistics = sorted_sample[np.array(ranks) - 1]

    cdf_values = stats.norm.cdf(order_statistics, loc=mu, scale=sigma)
    log_pdf_values = stats.norm.logpdf(order_statistics, loc=mu, scale=sigma)
    log_cdf_values = stats.norm.logcdf(order_statistics, loc=mu, scale=sigma)

    # technically calculating gammaln, which is log(factorial(n - 1)) is not needed for
    # MLE but i included it in for the sake of correctness

    log_likelihood = gammaln(n + 1)
    for i in range(k):
        if i == 0:
            log_likelihood += log_pdf_values[i] + (ranks[i] - 1) * log_cdf_values[i]
        elif i == k - 1:
            log_likelihood += log_pdf_values[i] + (n - ranks[i]) * np.log(1 - cdf_values[i - 1])
        else:
            log_likelihood += log_pdf_values[i] + (ranks[i] - ranks[i - 1] - 1) * np.log(cdf_values[i] - cdf_values[i - 1])

        if i > 0:
            log_likelihood -= gammaln(ranks[i] - ranks[i - 1])

    log_likelihood -= gammaln(ranks[0]) + gammaln(n - ranks[-1] + 1)

    return log_likelihood


def negative_ll_order_stats(params, *args):
    mu, sigma = params
    sample, ranks = args

    if sigma <= 0:
        return np.inf
    return -log_likelihood_order_stats(sample, ranks, mu, sigma)


def norm_loss(params, quantiles, observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, mean, std)

    squared_differences = (observations - expected_values) ** 2
    raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)
    weight = 1 / raw_variance

    return np.sum(squared_differences * weight)


def neg_log_likelihood(theta, xs, n):
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


total_os = np.zeros(2)
loss_os = np.zeros(2)

total_wls = np.zeros(2)
loss_wls = np.zeros(2)

true_params = np.array([4, 2])

for i in range(1000000 + 2):
    initial_guess = true_params
    sample = np.sort(stats.norm.rvs(true_params[0], true_params[1], size=101))
    # ranks = [251, 501, 751]

    # result = minimize(negative_ll_order_stats, initial_guess, args=(sample, ranks), method="Nelder-Mead")
    # i don't think negative_ll_order_stats work as it's supposed to, prob recheck the code later
    result = minimize(neg_log_likelihood, initial_guess, args=(np.array([sample[25], sample[50]]), 101), method="Nelder-Mead")

    total_os += result.x
    loss_os += abs(true_params - result.x) ** 1

    param_bounds = [(-1.5, 6.0), (0.01, 4.0)]
    result = minimize(
        norm_loss,
        initial_guess,
        args=(np.array([0.25, 0.5]), np.array([sample[25], sample[50]])),
        method="L-BFGS-B",
        bounds=param_bounds,
    )
    total_wls += result.x
    loss_wls += abs(true_params - result.x) ** 1

    if i % 100 == 1:
        print(total_os / (i + 1))
        print(total_wls / (i + 1))
        print(loss_os / (i + 1))
        print(loss_wls / (i + 1))
        print()

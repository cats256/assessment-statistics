import scipy.stats as stats
import numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize


def log_likelihood_order_statistics(sorted_sample, ranks, mu, sigma):
    n = len(sorted_sample)
    k = len(ranks)

    order_statistics = sorted_sample[np.array(ranks) - 1]

    cdf_values = stats.norm.cdf(order_statistics, loc=mu, scale=sigma)
    log_pdf_values = stats.norm.logpdf(order_statistics, loc=mu, scale=sigma)
    log_cdf_values = stats.norm.logcdf(order_statistics, loc=mu, scale=sigma)

    log_likelihood = 0
    # log_likelihood = gammaln(n + 1)
    for i in range(k):
        if i == 0:
            log_likelihood += log_pdf_values[i] + (ranks[i] - 1) * log_cdf_values[i]
        elif i == k - 1:
            log_likelihood += log_pdf_values[i] + (n - ranks[i]) * np.log(1 - cdf_values[i - 1])
        else:
            log_likelihood += log_pdf_values[i] + (ranks[i] - ranks[i - 1] - 1) * np.log(cdf_values[i] - cdf_values[i - 1])

        # if i > 0:
        #     log_likelihood -= gammaln(ranks[i] - ranks[i - 1])

    # log_likelihood -= gammaln(ranks[0]) + gammaln(n - ranks[-1] + 1)

    return log_likelihood


def negative_log_likelihood(params, *args):
    mu = params
    sigma = 2
    sample, ranks = args

    if sigma <= 0:
        return np.inf
    return -log_likelihood_order_statistics(sample, ranks, mu, sigma)


def normal_ll(params, samples):
    log_likelihood = 0
    for sample in samples:
        log_likelihood += stats.norm.logpdf(sample, params[0], 2)
    return -log_likelihood


total = np.zeros(1)
loss = np.zeros(1)

total_two = np.zeros(1)
loss_two = np.zeros(1)

for i in range(10000):
    initial_guess = [1.3]
    sample = np.sort(stats.norm.rvs(2, 2, size=7))
    ranks = [2, 3, 4, 5, 6]

    result = minimize(negative_log_likelihood, initial_guess, args=(sample, ranks), method="Nelder-Mead")
    total += result.x
    loss += abs(2 - result.x) ** 1
    print(-log_likelihood_order_statistics(sample, ranks, result.x[0], 2))
    sample = np.delete(sample, 3)
    result = minimize(normal_ll, initial_guess, args=(sample), method="Nelder-Mead")
    total_two += result.x
    loss_two += abs(2 - result.x) ** 1

    if i % 100 == 1:
        print(total / i)
        print(total_two / i)
        print(loss)
        print(loss_two)
        print()
    # print(result)
    # print(result.x)
    # print(-log_likelihood_order_statistics(sample, ranks, 1.3, 2))
    # print(-log_likelihood_order_statistics(sample, ranks, result.x[0], 2))

print(total)
print(total_two)

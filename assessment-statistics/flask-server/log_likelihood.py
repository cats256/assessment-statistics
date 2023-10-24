import numpy as np
from scipy.optimize import differential_evolution
from scipy.stats import gamma, norm


def max_likelihood(params, observed_quantiles, quantiles):
    shape, scale = params
    log_likelihood = 0

    for i, quantile in enumerate(quantiles):
        quantile_mean = gamma.ppf(quantile, shape, scale=scale)
        quantile_std = np.sqrt(quantile * (1 - quantile) / (10 * norm.pdf(norm.ppf(quantile)) ** 2))

        log_likelihood += norm.logpdf(observed_quantiles[i], quantile_mean, quantile_std)

    return -log_likelihood


def least_square_loss(params, observations, quantiles):
    shape, scale = params
    expected_values = gamma.ppf(quantiles, shape, scale=scale)

    squared_differences = (observations - expected_values) ** 2
    raw_variance = (quantiles * (1 - quantiles)) / norm.pdf(norm.ppf(quantiles) ** 2)
    weight = 1 / raw_variance

    return np.sum(squared_differences * weight)


quantiles = np.array([0.25, 0.5, 0.75])
num_loop = 10000

estimation_total = np.zeros(2)
estimation_loss = np.zeros(2)

estimation_total_2 = np.zeros(2)
estimation_loss_2 = np.zeros(2)

rng = np.random.default_rng()
true_params = np.array([1.21, 1.38])
size = 10000

for i in range(num_loop):
    data = np.sort(rng.gamma(shape=true_params[0], scale=true_params[1], size=size + 1))
    observed_quantiles = np.quantile(data, quantiles)

    result = differential_evolution(max_likelihood, bounds=[(1.0, 100.0), (1.0, 100.0)], args=(observed_quantiles, quantiles))

    estimation_total += result.x[:2]
    estimation_loss += abs(true_params - result.x[:2]) ** 2

    result = differential_evolution(least_square_loss, bounds=[(1.0, 100.0), (1.0, 100.0)], args=(observed_quantiles, quantiles))

    estimation_total_2 += result.x
    estimation_loss_2 += abs(true_params - result.x) ** 2

    if i % 10 == 0 and i != 0:
        print(i)

        print(estimation_total / i)
        print(estimation_total_2 / i)

        print(estimation_loss)
        print(estimation_loss_2)

        print((abs((estimation_total_2[0] / i) - true_params[0])) / (abs((estimation_total[0] / i) - true_params[0])))
        print()


print("Estimation Total")
print(estimation_total / num_loop)
print(estimation_total_2 / num_loop)

print("Estimation Loss")
print(estimation_loss)
print(estimation_loss_2)

print("Error ratio")
print((abs((estimation_total_2[0] / num_loop) - true_params[0])) / (abs((estimation_total[0] / num_loop) - true_params[0])))

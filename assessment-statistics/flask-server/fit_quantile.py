import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize


def norm_loss(params, quantiles, observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, mean, std)

    squared_differences = (observations - expected_values) ** 2
    raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)

    return np.sum(squared_differences / raw_variance)


def uw_norm_loss(params, quantiles, observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, mean, std)

    squared_differences = (observations - expected_values) ** 2

    return np.sum(squared_differences)


# note could use long double for more precision but np.random.normal internally uses double-float
# also could combine norm.pdf(norm.ppf(value)) into one which may produce better result (too lazy + maybe lower)
quantiles = np.array([0.25, 0.5, 0.75])
num_loop = 1

estimation_total = np.zeros(2)
uw_estimation_total = np.zeros(2)

initial_guess = np.array([2.5, 0.84])
param_bounds = np.array([(-1.5, 3.0), (-1.5, 3.0)])

for i in range(num_loop):
    observations = np.sort(np.random.normal(size=101, loc=1.54, scale=0.85))

    optimization_result = minimize(
        norm_loss,
        initial_guess,
        args=(quantiles, np.array([observations[25], observations[50], observations[75]])),
        method="L-BFGS-B",
        bounds=param_bounds,
    )

    estimation_total += optimization_result.x

    optimization_result = minimize(
        uw_norm_loss,
        initial_guess,
        args=(quantiles, np.array([observations[25], observations[50], observations[75]])),
        method="L-BFGS-B",
        bounds=param_bounds,
    )

    uw_estimation_total += optimization_result.x

    if i % 1000 == 0:
        print(i)

print(estimation_total / num_loop)
print(uw_estimation_total / num_loop)

print((abs((uw_estimation_total[0] / num_loop) - 1.54)) / (abs((estimation_total[0] / num_loop) - 1.54)))
print((abs((uw_estimation_total[1] / num_loop) - 0.85)) / (abs((estimation_total[1] / num_loop) - 0.85)))

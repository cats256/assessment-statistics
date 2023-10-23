import numpy as np
from scipy.optimize import differential_evolution
from scipy.stats import expon, norm
from scipy.optimize import dual_annealing


def max_likelihood(params, observed_quantiles, quantiles):
    try:
        scale = params
        log_likelihood = 0

        for i, quantile in enumerate(quantiles):
            quantile_mean = expon.ppf(quantile, scale=scale)
            quantile_std = np.sqrt(quantile * (1 - quantile) / (10000 * norm.pdf(norm.ppf(quantile)) ** 2))

            quantile_likelihood = norm.pdf(observed_quantiles[i], quantile_mean, quantile_std)

            if np.isnan(quantile_likelihood) or np.isinf(quantile_likelihood) or quantile_likelihood == 0:
                return np.inf

            log_q_prob = np.log(quantile_likelihood)

            if np.isnan(log_q_prob) or np.isinf(log_q_prob):
                return np.inf

            log_likelihood += log_q_prob

        return -log_likelihood
    except:
        return np.inf


def least_square_loss(params, observations, quantiles):
    try:
        scale = params[0]
        expected_values = expon.ppf(quantiles, scale=scale)

        squared_differences = (observations - expected_values) ** 2
        raw_variance = (quantiles * (1 - quantiles)) / norm.pdf(norm.ppf(quantiles) ** 2)
        weight = 1 / raw_variance

        return np.sum(squared_differences * weight)
    except:
        return np.inf


quantiles = np.array([0.01, 0.5, 0.99])
num_loop = 100

estimation_total = np.zeros(1)
estimation_loss = np.zeros(1)

estimation_total_2 = np.zeros(1)
estimation_loss_2 = np.zeros(1)

rng = np.random.default_rng()
true_params = np.array([1.98])
size = 10000


for i in range(num_loop):
    data = np.sort(rng.exponential(scale=1.38, size=size + 1))
    observed_quantiles = np.quantile(data, quantiles)

    result = dual_annealing(
        max_likelihood,
        bounds=np.array([(1.0, 100.0)]),
        args=(
            observed_quantiles,
            quantiles,
        ),
    )
    estimation_total += result.x[:1]
    estimation_loss += abs(true_params - result.x[:1]) ** 2

    result = dual_annealing(
        least_square_loss,
        bounds=np.array([(1.0, 100.0)]),
        args=(
            observed_quantiles,
            quantiles,
        ),
    )

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

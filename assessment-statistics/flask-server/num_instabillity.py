import numpy as np
from scipy.special import erfinv
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

quantiles = np.array([0.01, 0.50, 0.99])
num_loop = 1000000

estimation_total = np.zeros(2)
estimation_loss = np.zeros(2)

estimation_total_2 = np.zeros(2)
estimation_loss_2 = np.zeros(2)

estimation_total_3 = np.zeros(2)
estimation_loss_3 = np.zeros(2)

rng = np.random.default_rng()
true_params = np.array([0, 1])
size = 100

model = LinearRegression()

for i in range(num_loop):
    # ordinary least square
    data = np.sort(rng.normal(loc=true_params[0], scale=true_params[1], size=size + 1))

    # observed_quantiles = np.quantile(data, quantiles, method="normal_unbiased")
    observed_quantiles = np.quantile(data, quantiles)
    expected_quantiles = erfinv(2 * quantiles - 1)

    expected_quantiles = expected_quantiles.reshape(-1, 1)
    observed_quantiles = observed_quantiles.reshape(-1, 1)

    raw_variance = quantiles * (1 - quantiles) / (norm.pdf(norm.ppf(quantiles)) ** 2)
    # raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2)
    weight = 1 / raw_variance

    model.fit(norm.ppf(quantiles).reshape(-1, 1), observed_quantiles, sample_weight=weight)
    coefficients = np.array([float(model.intercept_[0]), float(model.coef_[0][0])])

    estimation_total += coefficients
    estimation_loss += abs(true_params - coefficients) ** 2

    raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2)
    weight = 1 / raw_variance

    model.fit(expected_quantiles * np.sqrt(2), observed_quantiles, sample_weight=weight)
    coefficients = np.array([float(model.intercept_[0]), float(model.coef_[0][0])])

    estimation_total_2 += coefficients
    estimation_loss_2 += abs(true_params - coefficients) ** 2

    if i % 1000 == 0 and i != 0:
        print(i)

        print((estimation_total / i).astype(str))
        print((estimation_total_2 / i).astype(str))

        print((estimation_loss).astype(str))
        print((estimation_loss_2).astype(str))

        print((abs((estimation_total_2[0] / i) - true_params[0])) / (abs((estimation_total[0] / i) - true_params[0])))
        print((abs((estimation_total_2[1] / i) - true_params[1])) / (abs((estimation_total[1] / i) - true_params[1])))

        print()

print("Estimation Total")
print(estimation_total / num_loop)
print(estimation_total_2 / num_loop)

print("Estimation Loss")
print(estimation_loss)
print(estimation_loss_2)

print("Error ratio")
print((abs((estimation_total_2[0] / num_loop) - true_params[0])) / (abs((estimation_total[0] / num_loop) - true_params[0])))
print((abs((estimation_total_2[1] / num_loop) - true_params[1])) / (abs((estimation_total[1] / num_loop) - true_params[1])))

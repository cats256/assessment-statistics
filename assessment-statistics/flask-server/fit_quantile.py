import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.special import erfinv


# weighted least squares
def norm_loss(params, quantiles, observations):
    try:
        mean, std = params
        expected_values = norm.ppf(quantiles, mean, std)
        squared_differences = (observations - expected_values) ** 2

        # raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)
        # below is pretty much same thing just more explicit and optimized
        # theoretically could take out std term and 2 * pi since they are constants and would not affect
        # estimated parameters but since we're estimating numerically, taking them out
        # increases error in estimated variance and decreases error in estimated mean
        # this is probably due to taking out std term leads to a decrease in how much change in std affects
        # change in sum squared error
        raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2) * (std**2) * 2 * np.pi
        # print(raw_variance)
        return np.sum(squared_differences / raw_variance)
    except:
        return np.inf


def norm_loss_2(params, quantiles, observations):
    try:
        mean, std = params
        expected_values = norm.ppf(quantiles, mean, std)
        squared_differences = (observations - expected_values) ** 2

        # raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)
        # below is pretty much same thing just more explicit and optimized
        # theoretically could take out std term and 2 * pi since they are constants and would not affect
        # estimated parameters but since we're estimating numerically, taking them out
        # increases error in estimated variance and decreases error in estimated mean
        # this is probably due to taking out std term leads to a decrease in how much change in std affects
        # change in sum squared error
        raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2)
        # print(raw_variance)
        return np.sum(squared_differences / raw_variance)
    except:
        print("Exception occured: ", mean, std)
        return np.inf


# note could use long double for more precision but np.random.normal internally uses double-float
# also could combine norm.pdf(norm.ppf(value)) into one which may produce better result (too lazy + maybe lower)
quantiles = np.array([0.01, 0.5, 0.99])
num_loop = 100000

estimation_total = np.zeros(2)
estimation_loss = np.zeros(2)

estimation_total_2 = np.zeros(2)
estimation_loss_2 = np.zeros(2)

true_params = np.array([1.38, 1.06])

initial_guess = true_params
param_bounds = np.array([(-np.inf, np.inf), (0.0, np.inf)])

machine_eps = np.finfo(float).eps
for i in range(num_loop):
    observations = np.sort(np.random.normal(size=100001, loc=true_params[0], scale=true_params[1]))

    optimization_result = minimize(
        norm_loss,
        initial_guess,
        args=(quantiles, np.array([observations[1000], observations[50000], observations[99000]])),
        method="L-BFGS-B",
        bounds=[(None, None), (0.1, None)],
    )

    estimation_total += optimization_result.x
    estimation_loss += (true_params - optimization_result.x) ** 2
    # print(optimization_result)
    if not optimization_result.success:
        print("Optimization did not converge.")
        print("Message:", optimization_result.message)

    optimization_result = minimize(
        norm_loss_2,
        initial_guess,
        args=(quantiles, np.array([observations[1000], observations[50000], observations[99000]])),
        method="L-BFGS-B",
        bounds=[(None, None), (0.1, None)],
    )

    estimation_total_2 += optimization_result.x
    estimation_loss_2 += (true_params - optimization_result.x) ** 2
    # print(optimization_result)
    if not optimization_result.success:
        print("Optimization did not converge.")
        print("Message:", optimization_result.message)

    if i % 1000 == 0:
        print(i)

        print(estimation_total / num_loop)
        print(estimation_total_2 / num_loop)

        print(estimation_loss)
        print(estimation_loss_2)

        print((abs((estimation_total_2[0] / num_loop) - true_params[0])) / (abs((estimation_total[0] / num_loop) - true_params[0])))
        print((abs((estimation_total_2[1] / num_loop) - true_params[1])) / (abs((estimation_total[1] / num_loop) - true_params[1])))

        print()


print(estimation_total / num_loop)
print(estimation_total_2 / num_loop)

print(estimation_loss)
print(estimation_loss_2)

print((abs((estimation_total_2[0] / num_loop) - true_params[0])) / (abs((estimation_total[0] / num_loop) - true_params[0])))
print((abs((estimation_total_2[1] / num_loop) - true_params[1])) / (abs((estimation_total[1] / num_loop) - true_params[1])))
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize, differential_evolution


def max_likelihood(params, values):
    mean, std = params
    quantiles = [0.25, 0.5, 0.75]

    log_likelihood = 0

    for q in quantiles:
        q_mean = norm.ppf(q, mean, std)
        q_std = np.sqrt((q) * (1 - q) / ((101) * norm.pdf(norm.ppf(q)) ** 2))
        # print("q_mean = ", q_mean)
        # print("q_std = ", q_std)
        # print("quantile = ", values[int(q * 1000)])
        # print("cdf ", q, " ", norm.cdf(values[int(q * 1000)], q_mean, q_std))
        # print("")
        q_prob = norm.pdf(values[int(q * 100)], q_mean, q_std)
        if np.isnan(q_prob) or np.isinf(q_prob) or q_prob == 0:
            return np.inf
        log_q_prob = np.log(q_prob)
        if np.isnan(log_q_prob) or np.isinf(log_q_prob):
            return np.inf
        log_likelihood += log_q_prob

    # print(mean, std, -1 * log_likelihood)
    return -1 * log_likelihood


def max_likelihood2(params, values):
    mean, std = params
    quantiles = np.array([0.25, 0.5, 0.75])

    log_likelihood = 0

    for q in quantiles:
        q_mean = norm.ppf(q, mean, std)
        q_std = np.sqrt((q) * (1 - q) / ((101) * norm.pdf(norm.ppf(q, mean, std), mean, std) ** 2))
        # print("q_mean = ", q_mean)
        # print("q_std = ", q_std)
        # print("quantile = ", values[int(q * 1000)])
        # print("cdf ", q, " ", norm.cdf(values[int(q * 1000)], q_mean, q_std))
        # print("")
        q_prob = norm.pdf(values[int(q * 100)], q_mean, q_std)
        if np.isnan(q_prob) or np.isinf(q_prob) or q_prob == 0:
            return np.inf
        log_q_prob = np.log(q_prob)
        if np.isnan(log_q_prob) or np.isinf(log_q_prob):
            return np.inf
        log_likelihood += log_q_prob

    # print(mean, std, -1 * log_likelihood)
    return -1 * log_likelihood


def norm_loss(params, quantiles, observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, mean, std)

    squared_differences = (observations - expected_values) ** 2
    raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)
    weight = 1 / raw_variance

    return np.sum(squared_differences * weight)


def norm_loss2(params, quantiles, observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, mean, std)

    squared_differences = (observations - expected_values) ** 2
    weight = 1

    return np.sum(squared_differences * weight)


correct_param = np.array([1.54, 0.85])
params = 0
loss1 = np.array([0.0, 0.0])
params2 = 0
loss2 = np.array([0.0, 0.0])
params3 = 0
loss3 = np.array([0.0, 0.0])
params4 = 0
loss4 = np.array([0.0, 0.0])

for i in range(10):
    data_chunk = np.random.normal(size=(1, 101), loc=1.54, scale=0.85)

    sorted_data = sorted(data_chunk[0])
    lower_quartile = np.percentile(data_chunk, 25, axis=1)
    median = np.percentile(data_chunk, 50, axis=1)
    upper_quartile = np.percentile(data_chunk, 75, axis=1)

    initial_guess = [2.5, 0.84]
    param_bounds = [(-1.5, 3.0), (0.01, 3.0)]

    # result = minimize(max_likelihood, initial_guess, args=(sorted_data), bounds=param_bounds, method="Powell")
    result = differential_evolution(max_likelihood, bounds=param_bounds, args=(sorted_data,))
    params += result.x
    loss1 += abs(correct_param - result.x) ** 2

    # result = differential_evolution(max_likelihood2, bounds=param_bounds, args=(sorted_data,))
    # params2 += result.x
    # loss2 += abs(correct_param - result.x) ** 2
    # # print("Results = ", result.x)
    # # print("Objective function", result.fun)
    # # if not result.success:
    # #     print("Optimization did not converge.")
    # #     print("Message:", result.message)

    # # # print(lower_quartile)
    # # # print(median)
    # # # print(upper_quartile)
    # # print(max_likelihood((2.5, 1.84), sorted(data_chunk[0])))

    # optimization_result = minimize(
    #     norm_loss,
    #     initial_guess,
    #     args=(np.array([0.25, 0.5, 0.75]), np.array([sorted_data[25], sorted_data[50], sorted_data[75]])),
    #     method="L-BFGS-B",
    #     bounds=param_bounds,
    # )

    # params3 += optimization_result.x
    # loss3 += abs(correct_param - optimization_result.x) ** 2

    # optimization_result = minimize(
    #     norm_loss2,
    #     initial_guess,
    #     args=(np.array([0.25, 0.5, 0.75]), np.array([sorted_data[25], sorted_data[50], sorted_data[75]])),
    #     method="L-BFGS-B",
    #     bounds=param_bounds,
    # )

    # params4 += optimization_result.x
    # loss4 += abs(correct_param - optimization_result.x) ** 2

    if i % 100 == 0:
        print(i)

print(params / 10)
print(loss1)
# print("")
# print(params2 / 10)
# print(loss2)
# print("")
# print(params3 / 100)
# print(loss3)
# print("")
# print(params4 / 10)
# print(loss4)

# for i in range(1000)
# [25.07711158 17.21942186]
# [156.03758436 190.55993706]

# [25.07711157 17.23675105]
# [156.03757889 189.92040163]

# [25.07711447 18.21296627]
# [156.0376179  173.29882088]

# [25.08180738 18.09126603]
# [155.92862063 173.24774285]

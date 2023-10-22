import timeit
import numpy as np
from scipy.special import erfinv
from sklearn.linear_model import LinearRegression

quantiles = np.array([0.01, 0.5, 0.99])
num_loop = 1

estimation_total = np.zeros(2)
estimation_loss = np.zeros(2)

estimation_total_2 = np.zeros(2)
estimation_loss_2 = np.zeros(2)

model = LinearRegression()
size = 10000
true_params = np.array([1.38, 1.06])

for i in range(num_loop):
    # ordinary least square
    data = np.sort(np.random.normal(size=size + 1, loc=true_params[0], scale=true_params[1]))

    observed_quantiles = np.percentile(data, quantiles * 100)
    expected_quantiles = np.sqrt(2) * erfinv(2 * quantiles - 1)

    expected_quantiles = expected_quantiles.reshape(-1, 1)
    observed_quantiles = observed_quantiles.reshape(-1, 1)

    def ols():
        model.fit(expected_quantiles, observed_quantiles)
        coefficients = np.array([float(model.intercept_[0]), float(model.coef_[0][0])])

        # estimation_total += coefficients
        # estimation_loss += abs(true_params - coefficients) ** 2

    # weighted least square

    def wls():
        raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2)
        weight = 1 / raw_variance

        model.fit(expected_quantiles, observed_quantiles, sample_weight=weight)
        coefficients = np.array([float(model.intercept_[0]), float(model.coef_[0][0])])

        # estimation_total_2 += coefficients
        # estimation_loss_2 += abs(true_params - coefficients) ** 2

    ols_time = timeit.timeit(ols, number=10)
    wls_time = timeit.timeit(wls, number=10)

    print(f"Ordinary Linear Regression Time: {ols_time} seconds")
    print(f"Weighted Linear Regression Time: {wls_time} seconds")

    # if i % 1000 == 0 and i != 0:
    #     print(i)

    #     print(estimation_total / i)
    #     print(estimation_total_2 / i)

    #     print(estimation_loss)
    #     print(estimation_loss_2)

    #     print((abs((estimation_total_2[0] / i) - true_params[0])) / (abs((estimation_total[0] / i) - true_params[0])))
    #     print((abs((estimation_total_2[1] / i) - true_params[1])) / (abs((estimation_total[1] / i) - true_params[1])))

    #     print()

print("Estimation Total")
print(estimation_total / num_loop)
print(estimation_total_2 / num_loop)

print("Estimation Loss")
print(estimation_loss)
print(estimation_loss_2)

print("Error ratio")
print((abs((estimation_total_2[0] / num_loop) - true_params[0])) / (abs((estimation_total[0] / num_loop) - true_params[0])))
print((abs((estimation_total_2[1] / num_loop) - true_params[1])) / (abs((estimation_total[1] / num_loop) - true_params[1])))


# # weighted least squares
# def norm_loss(params, quantiles, observations):
#     try:
#         mean, std = params
#         expected_values = norm.ppf(quantiles, mean, std)
#         squared_differences = (observations - expected_values) ** 2

#         # raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)
#         # below is pretty much same thing just more explicit and optimized
#         # theoretically could take out std term and 2 * pi since they are constants and would not affect
#         # estimated parameters but since we're estimating numerically, taking them out
#         # increases error in estimated variance and decreases error in estimated mean
#         # this is probably due to taking out std term leads to a decrease in how much change in std affects
#         # change in sum squared error
#         # raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2) * (std**2) * 2 * np.pi
#         # print(raw_variance)
#         return np.sum(squared_differences / 1)
#     except:
#         return np.inf


# # note could use long double for more precision but np.random.normal internally uses double-float
# # also could combine norm.pdf(norm.ppf(value)) into one which may produce better result (too lazy + maybe lower)
# quantiles = np.array([0.01, 0.5, 0.99])
# num_loop = 1

# estimation_total = np.zeros(2)
# estimation_loss = np.zeros(2)

# estimation_total_2 = np.zeros(2)
# estimation_loss_2 = np.zeros(2)

# # true_params = np.array([1.38, 1.06])
# true_params = np.array([0, 1])

# initial_guess = true_params
# param_bounds = np.array([(-np.inf, np.inf), (0.0, np.inf)])


# for i in range(num_loop):
#     observations = np.sort(np.random.normal(size=100001, loc=true_params[0], scale=true_params[1]))

#     def parameter_estimation():
#         optimization_result = minimize(
#             norm_loss,
#             initial_guess,
#             args=(quantiles, np.array([observations[1000], observations[50000], observations[99000]])),
#             method="L-BFGS-B",
#             bounds=[(None, None), (0.1, None)],
#         )

#         # estimation_total += optimization_result.x
#         # estimation_loss += abs(true_params - optimization_result.x)

#         # if not optimization_result.success:
#         #     print("Optimization did not converge.")
#         #     print("Message:", optimization_result.message)

#     def linear_regression():
#         x_arr = np.sqrt(2) * erfinv(2 * quantiles - 1)
#         coefficients = np.polyfit(x_arr, np.array([observations[1000], observations[50000], observations[99000]]), 1)
#         coefficients = np.array([coefficients[1], coefficients[0]])

#         # estimation_total_2 += coefficients
#         # estimation_loss_2 += abs(true_params - coefficients)

#     parameter_estimation_time = timeit.timeit(parameter_estimation, number=1000)
#     linear_regression_time = timeit.timeit(linear_regression, number=1000)

#     print(f"Linear Regression Time: {linear_regression_time} seconds")
#     print(f"Parameter Estimation Time: {parameter_estimation_time} seconds")

#     # if i % 1000 == 0 and i != 0:
#     #     print(i)

#     #     print(estimation_total / i)
#     #     print(estimation_total_2 / i)

#     #     print(estimation_loss)
#     #     print(estimation_loss_2)

#     #     print((abs((estimation_total_2[0] / i) - true_params[0])) / (abs((estimation_total[0] / i) - true_params[0])))
#     #     print((abs((estimation_total_2[1] / i) - true_params[1])) / (abs((estimation_total[1] / i) - true_params[1])))

#     #     print()


# # print(estimation_total / num_loop)
# # print(estimation_total_2 / num_loop)

# # print(estimation_loss)
# # print(estimation_loss_2)

# # print((abs((estimation_total_2[0] / num_loop) - true_params[0])) / (abs((estimation_total[0] / num_loop) - true_params[0])))
# # print((abs((estimation_total_2[1] / num_loop) - true_params[1])) / (abs((estimation_total[1] / num_loop) - true_params[1])))

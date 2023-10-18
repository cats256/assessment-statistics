# import numpy as np
# from scipy.stats import norm
# from multiprocessing import Pool


# def generate_medians(chunk_size, n):
#     data_chunk = np.random.normal(size=(chunk_size, n))
#     return np.median(data_chunk, axis=1)


# if __name__ == "__main__":
#     n = 101
#     n_rep = 500000 * 10
#     chunk_size = 500000
#     num_chunks = n_rep // chunk_size

#     # Use multiprocessing to generate medians in parallel
#     with Pool() as pool:
#         medians = pool.starmap(generate_medians, [(chunk_size, n)] * num_chunks)
#     medians = np.concatenate(medians)

#     median_sd = np.var(medians)  # Calculate the final median_sd

#     print(median_sd)
#     print(abs(1 / (4 * n * norm.pdf(0) ** 2)))
#     print(abs(1 / (4 * (n + 2) * norm.pdf(0) ** 2)))
#     print(abs(1 / (4 * n * norm.pdf(0) ** 2) - median_sd))
#     print(abs(1 / (4 * (n + 2) * norm.pdf(0) ** 2) - median_sd))

import numpy as np
from scipy.stats import norm

n = 101
n_rep = 500000
chunk_size = 500000
medians = []

for i in range(0, n_rep, chunk_size):
    data_chunk = np.random.normal(size=(chunk_size, n))
    median_chunk = np.median(data_chunk, axis=1)
    medians.extend(median_chunk)

median_sd = np.var(medians)  # Calculate the final median_sd

print(median_sd)
print(abs((1 / (4 * (n) * norm.pdf(0) ** 2))))
print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2))))
print(abs((1 / (4 * (n) * norm.pdf(0) ** 2)) - median_sd))
print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2)) - median_sd))

# import numpy as np
# from scipy.stats import norm

# n = 101
# n_rep = 10000000

# x = np.random.normal(size=(n_rep, n))
# medians = np.median(x, axis=1)
# median_sd = np.var(medians)

# print(median_sd)
# print(abs((1 / (4 * (n) * norm.pdf(0) ** 2))))
# print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2))))
# print(abs((1 / (4 * (n) * norm.pdf(0) ** 2)) - median_sd))
# print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2)) - median_sd))

# import numpy as np
# from scipy.stats import norm
# import timeit

# n = 1000
# n_rep = 1000


# def original_code():
#     x = np.random.normal(size=(n_rep, n))
#     median_sd = np.std(np.apply_along_axis(np.median, axis=1, arr=x)) ** 2


# def optimized_code():
#     x = np.random.normal(size=(n_rep, n))
#     medians = np.median(x, axis=1)
#     median_sd = np.var(medians)


# # Time the original code
# original_time = timeit.timeit(original_code, number=100)
# print("Original code execution time (average of 100 runs):", original_time)

# # Time the optimized code
# optimized_time = timeit.timeit(optimized_code, number=100)
# print("Optimized code execution time (average of 100 runs):", optimized_time)

# import numpy as np
# from scipy.stats import norm

# n = 1000
# n_rep = 10000

# x = np.random.normal(size=(n_rep, n))
# median_sd = np.std(np.apply_along_axis(np.median, axis=1, arr=x)) ** 2

# print(median_sd)
# print(abs((1 / (4 * (n) * norm.pdf(0) ** 2)) - median_sd))
# print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2)) - median_sd))

# import numpy as np
# from scipy.stats import norm
# from scipy.special import expit, logit

# # Example quantiles (you would replace this with your actual quantiles)
# quantiles = [0.25, 0.50, 0.75]

# # Observed values corresponding to the quantiles
# # (you would replace this with your actual data)
# # observed_values = [-1 + 5, 1 + 5]
# observed_values = [logit(79.90 / 100)]


# # Define the log-likelihood function
# def log_likelihood(params, observed_values):
#     mu, sigma = params
#     likelihoods = [norm.pdf(value, loc=mu, scale=sigma) for value in observed_values]
#     log_likelihood = np.log(np.prod(likelihoods))
#     return log_likelihood


# # Initial parameter values for the optimization
# initial_params = [0, 1]  # You can start with any values

# # Optimization to find the parameters that maximize the log-likelihood
# from scipy.optimize import minimize

# result = minimize(lambda params: -log_likelihood(params, observed_values), initial_params)

# # Extract the estimated parameters
# mu_est, sigma_est = result.x

# print("Estimated mean (mu):", mu_est)
# print("Estimated standard deviation (sigma):", sigma_est)

# # import numpy as np
# # from scipy.optimize import minimize
# # from scipy.stats import norm
# # from scipy.special import expit, logit
# # from scipy.special import erf
# # from math import sqrt

# # print(norm.cdf(logit(0.87), 1.92, 0.21))
# # print(1 / 2 * (1 + erf((logit(0.87) - 1.92) / sqrt(2 * 0.21**2))))
# # print("Something")
# # # Define the logit-normal loss function
# # def logit_norm_loss(parameters, quantiles, observed_values, scale):
# #     mean = parameters[0]
# #     standard_deviation = parameters[1]

# #     expected_values = logitnorm.ppf(quantiles, s=standard_deviation, loc=0, scale=np.exp(mean))
# #     squared_differences = (np.log(observed_values/scale) - np.log(expected_values/scale))**2

# #     return np.sum(squared_differences)

# # lower_bound = 0
# # upper_bound = 84
# # scale = upper_bound - lower_bound

# # quantiles = np.array([0.25, 0.50, 0.75])
# # observed_values = np.array([56.87, 64.25, 70.59])

# # initial_parameters = [
# #     np.sum(np.log(observed_values/scale)) / len(observed_values),
# #     (np.log(observed_values[-1]/scale) - np.log(observed_values[0]/scale)) / (norm.ppf(quantiles[-1]) - norm.ppf(quantiles[0]))
# # ]

# # # Perform optimization
# # optimization_result = minimize(
# #     logit_norm_loss,
# #     initial_parameters,
# #     args=(quantiles, observed_values, scale),
# #     method='Nelder-Mead'
# # )

# # minimum_loss = optimization_result.fun
# # mean = optimization_result.x[0]
# # sd = optimization_result.x[1]

# # # Calculate expected values
# # expected_values = scale * np.exp(logitnorm.ppf(quantiles, s=sd, loc=0, scale=np.exp(mean)))

# # # Calculate transformed observed and expected values
# # transformed_observed = np.log(observed_values/scale)
# # transformed_expected = np.log(expected_values/scale)

# # print("Minimum Loss:", minimum_loss)
# # print("Optimal Mean:", mean)
# # print("Optimal Standard Deviation:", sd)
# # print("Predicted Quantiles:", list(zip(quantiles, expected_values)))
# # print("Squared Sum Error:", np.sum((observed_values - expected_values)**2))
# # print("Squared Sum Error Normal:", np.sum((transformed_observed - transformed_expected)**2))
# # print("Cumulative Probability at x = 78:", logitnorm.cdf(78/84, s=sd, loc=0, scale=np.exp(mean)))

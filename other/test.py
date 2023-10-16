import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit

# Example quantiles (you would replace this with your actual quantiles)
quantiles = [0.25, 0.50, 0.75]

# Observed values corresponding to the quantiles
# (you would replace this with your actual data)
# observed_values = [-1 + 5, 1 + 5]
observed_values = [logit(79.90 / 100)]


# Define the log-likelihood function
def log_likelihood(params, observed_values):
    mu, sigma = params
    likelihoods = [norm.pdf(value, loc=mu, scale=sigma) for value in observed_values]
    log_likelihood = np.log(np.prod(likelihoods))
    return log_likelihood


# Initial parameter values for the optimization
initial_params = [0, 1]  # You can start with any values

# Optimization to find the parameters that maximize the log-likelihood
from scipy.optimize import minimize

result = minimize(lambda params: -log_likelihood(params, observed_values), initial_params)

# Extract the estimated parameters
mu_est, sigma_est = result.x

print("Estimated mean (mu):", mu_est)
print("Estimated standard deviation (sigma):", sigma_est)

# import numpy as np
# from scipy.optimize import minimize
# from scipy.stats import norm
# from scipy.special import expit, logit
# from scipy.special import erf
# from math import sqrt

# print(norm.cdf(logit(0.87), 1.92, 0.21))
# print(1 / 2 * (1 + erf((logit(0.87) - 1.92) / sqrt(2 * 0.21**2))))
# print("Something")
# # Define the logit-normal loss function
# def logit_norm_loss(parameters, quantiles, observed_values, scale):
#     mean = parameters[0]
#     standard_deviation = parameters[1]

#     expected_values = logitnorm.ppf(quantiles, s=standard_deviation, loc=0, scale=np.exp(mean))
#     squared_differences = (np.log(observed_values/scale) - np.log(expected_values/scale))**2

#     return np.sum(squared_differences)

# lower_bound = 0
# upper_bound = 84
# scale = upper_bound - lower_bound

# quantiles = np.array([0.25, 0.50, 0.75])
# observed_values = np.array([56.87, 64.25, 70.59])

# initial_parameters = [
#     np.sum(np.log(observed_values/scale)) / len(observed_values),
#     (np.log(observed_values[-1]/scale) - np.log(observed_values[0]/scale)) / (norm.ppf(quantiles[-1]) - norm.ppf(quantiles[0]))
# ]

# # Perform optimization
# optimization_result = minimize(
#     logit_norm_loss,
#     initial_parameters,
#     args=(quantiles, observed_values, scale),
#     method='Nelder-Mead'
# )

# minimum_loss = optimization_result.fun
# mean = optimization_result.x[0]
# sd = optimization_result.x[1]

# # Calculate expected values
# expected_values = scale * np.exp(logitnorm.ppf(quantiles, s=sd, loc=0, scale=np.exp(mean)))

# # Calculate transformed observed and expected values
# transformed_observed = np.log(observed_values/scale)
# transformed_expected = np.log(expected_values/scale)

# print("Minimum Loss:", minimum_loss)
# print("Optimal Mean:", mean)
# print("Optimal Standard Deviation:", sd)
# print("Predicted Quantiles:", list(zip(quantiles, expected_values)))
# print("Squared Sum Error:", np.sum((observed_values - expected_values)**2))
# print("Squared Sum Error Normal:", np.sum((transformed_observed - transformed_expected)**2))
# print("Cumulative Probability at x = 78:", logitnorm.cdf(78/84, s=sd, loc=0, scale=np.exp(mean)))

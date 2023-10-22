import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit, erfinv
from scipy.optimize import minimize

import plotly.graph_objs as go

# loss function for linear regression is
# sum (yi - (b0 + b1 * xi))^2

# loss function for norm dist q matching is
# sum (observations - (expected quantiles))^2
# sum (observations - (mu + std * sqrt(2)*erf^-1(2p - 1)))^2

# so norm dist observations is analogous to yi
# mu is analogous to b0
# b1 is analogous to std
# sqrt(2)*erf^-1(2p - 1) is analogous to xi

lower_bound = 0
upper_bound = 84
scale = upper_bound - lower_bound

quantiles = np.array([0.25, 0.50, 0.75])
observed_values = np.array([56.87, 64.25, 70.59]) - lower_bound

logit_observations = logit(observed_values / scale)

x_arr = np.sqrt(2) * erfinv(2 * quantiles - 1)

coefficients = np.polyfit(x_arr, logit_observations, 1)
slope, intercept = coefficients

print(slope, intercept)

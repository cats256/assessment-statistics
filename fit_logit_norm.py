import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit
from scipy.optimize import minimize
import plotly.graph_objs as go


def norm_loss(params, quantiles, scaled_observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, loc=mean, scale=std)

    squared_differences = (logit(scaled_observations) - expected_values) ** 2
    # squared_differences = (scaled_observations - expit(expected_values)) ** 2

    # not sure which loss function to use but both produces very similar results.
    # i personally prefer calculating the SSE by transforming the data back into the
    # logit-normal. main question is what's the type of error? multiplicative or
    # additive? i don't have enough data to answer and check for heteroskedasticity
    # but i believe it's the latter or it could be a mix of both. i don't know.

    # edit: i went with the SSE using data in its normal (logistic transformed) form.
    # thought the logistic transformed SSE is convex since i tested it and it seemed
    # convex but i plotted the loss function again with a wider range for mean and
    # standard deviation and lo and behold, it is not convex. not that there's anything
    # inherently wrong with non-convex function. i just don't like them. lesson learned:
    # don't forget to double check your assumptions XD

    return np.sum(squared_differences)


lower_bound = 0
upper_bound = 84
scale = upper_bound - lower_bound

quantiles = np.array([0.25, 0.50, 0.75])
observed_values = np.array([56.87, 64.25, 70.59])

logit_observations = logit(observed_values / scale)
scaled_observations = observed_values / scale

mean_estimate = np.mean(logit_observations)
std_estimate = (logit_observations[-1] - logit_observations[0]) / (norm.ppf(quantiles[-1]) - norm.ppf(quantiles[0]))
initial_parameters = np.array([mean_estimate, std_estimate])

optimization_result = minimize(
    norm_loss,
    initial_parameters,
    args=(quantiles, scaled_observations),
    method="L-BFGS-B",
    bounds=[(None, None), (0, None)],
)

mean, std = optimization_result.x
expected_norm = norm.ppf(quantiles, loc=mean, scale=std)
expected_values = scale * expit(expected_norm)

print("Mean:", mean)
print("Standard Deviation:", std)
print("Expected Values:", expected_values)
print("Sum Squared Error (Logit-Normal):", np.sum((observed_values - expected_values) ** 2))
print("Sum Squared Error (Normal):", np.sum((logit_observations - expected_norm) ** 2))

# mean_range = np.linspace(1.19354772770165 - 0.4, 1.19354772770165 + 0.4, 100)
# std_range = np.linspace(0.01, 1.4, 100)

mean_range = np.linspace(-10, 10, 100)
std_range = np.linspace(0.01, 10, 100)

mean_grid, std_grid = np.meshgrid(mean_range, std_range)

loss_values = np.zeros_like(mean_grid)
for i in range(len(mean_range)):
    for j in range(len(std_range)):
        params = (mean_grid[i, j], std_grid[i, j])
        loss_values[i, j] = norm_loss(params, quantiles, scaled_observations)

fig = go.Figure(data=[go.Surface(z=loss_values, x=mean_grid, y=std_grid)])
fig.update_layout(
    scene=dict(
        xaxis_title="Mean",
        yaxis_title="Standard Deviation",
        zaxis_title="Loss",
        xaxis=dict(range=[-10, 10]),
        yaxis=dict(range=[0.01, 10]),
    )
)

fig.write_html("first_figure.html", auto_open=True)

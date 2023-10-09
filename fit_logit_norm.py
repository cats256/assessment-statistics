import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit
from scipy.optimize import minimize
import plotly.graph_objs as go


# for a general informative view only, very high error at the tails


def norm_loss(params, quantiles, logit_observations):
    mean, std = params
    expected_values = norm.ppf(quantiles, mean, std)

    squared_differences = (logit_observations - expected_values) ** 2
    # squared_differences = (expit(logit_observations) - expit(expected_values)) ** 2

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
observed_values = np.array([56.87, 64.25, 70.59]) - lower_bound

logit_observations = logit(observed_values / scale)

mean_estimate = np.mean(logit_observations)
std_estimate = (logit_observations[-1] - logit_observations[0]) / (norm.ppf(quantiles[-1]) - norm.ppf(quantiles[0]))
initial_parameters = np.array([mean_estimate, std_estimate])

# L-BFGS-B method because loss function is convex
optimization_result = minimize(
    norm_loss,
    initial_parameters,
    args=(quantiles, logit_observations),
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
print("Cumulative Probabillity for x = 78: ", norm.cdf(logit(81 / 84), mean, std))

# n_points = 200
# # very restricted range but this shows how the function is convex more neatly
# mean_range = np.linspace(mean - 0.4, mean + 0.4, n_points)
# std_range = np.linspace(std - 0.6, std + 0.6, n_points)

# mean_grid, std_grid = np.meshgrid(mean_range, std_range)

# params = np.stack((mean_grid, std_grid), axis=-1)
# loss_values = np.apply_along_axis(lambda p: norm_loss(tuple(p), quantiles, logit_observations), -1, params)

# min_indices = np.unravel_index(loss_values.argmin(), loss_values.shape)
# min_mean, min_std = mean_grid[min_indices], std_grid[min_indices]

# fig = go.Figure(data=[go.Surface(z=loss_values, x=mean_grid, y=std_grid, colorscale="Viridis")])

# fig.add_trace(
#     go.Scatter3d(
#         x=[min_mean],
#         y=[min_std],
#         z=[loss_values[min_indices]],
#         mode="markers",
#         marker=dict(size=5, color="red"),
#         name="Minimum Point",
#     )
# )

# fig.update_layout(
#     scene=dict(
#         xaxis_title="Mean",
#         yaxis_title="Standard Deviation",
#         zaxis_title="Loss",
#         xaxis=dict(range=[mean - 0.4, mean + 0.4]),
#         yaxis=dict(range=[std - 0.6, std + 0.6]),
#     )
# )

# fig.write_html("logit_norm.html", auto_open=True)

# contour = go.Contour(
#     x=mean_range,
#     y=std_range,
#     z=loss_values,
#     colorscale="Viridis",
#     contours=dict(
#         showlabels=True,
#         labelfont=dict(size=12, color="white"),
#     ),
# )

# min_point = go.Scatter(
#     x=[min_mean],
#     y=[min_std],
#     mode="markers",
#     marker=dict(size=10, color="red"),
#     name="Minimum Point",
# )

# fig = go.Figure(data=[contour, min_point])

# fig.update_layout(
#     xaxis_title="Mean",
#     yaxis_title="Standard Deviation",
#     title="Loss Surface Contour Plot",
# )

# fig.write_html("contour_plot.html", auto_open=True)

x_values = np.linspace(0, 1, 1000)
y_values = norm.pdf(logit(x_values), mean, std)

fig = go.Figure(data=go.Scatter(x=scale * x_values, y=y_values, mode="lines", name="Normal Distribution"))
fig.update_layout(title="Estimated Grade Distribution (Scaled Logit Normal)", xaxis_title="X", yaxis_title="PDF")
fig.write_html("logit_norm_pdf.html", auto_open=True)

from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit
from scipy.optimize import minimize
import plotly.graph_objs as go

app = Flask(__name__)
CORS(app)

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


def logit_norm_pdf(x, mean, std):
    return 1 / (std * np.sqrt(2 * np.pi)) * 1 / (x * (1 - x)) * np.e ** (-((logit(x) - mean) ** 2) / (2 * std**2))


@app.route("/parameters", methods=["POST"])
def parameters():
    lower_bound = 0
    upper_bound = 84
    scale = upper_bound - lower_bound

    quantiles = np.array([0.25, 0.50, 0.75])
    observed_values = np.array([float(value) for value in request.json.values()]) - lower_bound
    print(observed_values)

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

    step_size = 1000
    x_values = np.linspace(0, 1, step_size)[1:-1]
    # y_values = norm.pdf(logit(x_values), mean, std)
    # y_values = 1 / (std * np.sqrt(2 * np.pi) * x_values * (1 - x_values)) * np.e ** (-((logit(x_values) - mean) ** 2) / (2 * std**2))
    y_values = logit_norm_pdf(x_values, mean, std)
    # fig = go.Figure(data=go.Scatter(x=scale * x_values, y=y_values, mode="lines", name="Normal Distribution"))

    # observed_y_values = (
    #     1 / (std * np.sqrt(2 * np.pi) * (observed_values / 84) * (1 - (observed_values / 84))) * np.e ** (-((logit((observed_values / 84)) - mean) ** 2) / (2 * std**2))
    # )
    observed_y_values = norm.pdf(logit(observed_values / scale), mean, std)
    # fig.add_trace(go.Scatter(x=observed_values, y=observed_y_values, mode="markers", name="Observed Quantiles"))

    expected_y_values = norm.pdf(logit(expected_values / scale), mean, std)
    # fig.add_trace(go.Scatter(x=expected_values, y=expected_y_values, mode="markers", name="Expected Quantiles"))

    # fig.update_layout(title="Estimated Grade Distribution (Scaled Logit Normal)", xaxis_title="X", yaxis_title="PDF")
    print(expected_values)
    print(mean)
    print(std)
    print(np.sum(x_values * y_values) / np.sum(y_values))
    print(np.sum(x_values * y_values) / (step_size - 1))
    print(observed_y_values)
    # print(expit(mean) * 84)
    # print(np.sum(y_values))
    # print(x_values)
    # print(y_values)
    # print(np.sum(y_values / 10000) * 84)
    print(np.sum(y_values))
    print(len(x_values))
    return jsonify(
        {
            "mean": mean,
            "std": std,
            "expected_values": expected_values.tolist(),
            "mse_logit_norm": np.mean((observed_values - expected_values) ** 2),
            "mse_norm": np.mean((logit_observations - expected_norm) ** 2),
            "mae_logit_norm": np.mean(abs((observed_values - expected_values))),
            "x_values": x_values.tolist(),
            "y_values": y_values.tolist(),
            "observed_y_values": observed_y_values.tolist(),
            "expected_y_values": expected_y_values.tolist(),
        }
    )


# implement views counter

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CORS(app)

# look at README.md then server.py then original files for more explanation. also, feel free to hit me up at nhatbui@tamu.edu for any question or suggestion. heavily refactored and concise method (hence small file size but this took a lot more work than you would expect), which involves transforming the data twice, through the response variable and the explanatory variable, then fit a weighted lin reg. i have tested various distributions and optimization methods and this method is as good as it gets.


def check_invalid_values(observed_values, scale):
    is_sorted = all(observed_values[i] <= observed_values[i + 1] for i in range(len(observed_values) - 1))
    if not is_sorted:
        abort(400)

    is_range = all(0 < observed_value < scale for observed_value in observed_values)
    if not is_range:
        abort(400)


def logitnorm_pdf(x, mean, std):
    return 1 / (std * np.sqrt(2 * np.pi)) * 1 / (x * (1 - x)) * np.e ** (-((logit(x) - mean) ** 2) / (2 * std**2))


@app.route("/parameters", methods=["POST"])
def parameters():
    request_json = request.json

    lower_bound = float(request_json["minGrade"])
    upper_bound = float(request_json["maxGrade"])
    scale = upper_bound - lower_bound

    sorted_dict = sorted(request_json["quantiles"].items(), key=lambda x: x[0])
    cumulative_probs = np.array([float(item[0]) for item in sorted_dict])
    observed_values = np.array([float(item[1]) for item in sorted_dict]) - lower_bound

    check_invalid_values(observed_values, scale)

    standard_norm_quantiles = norm.ppf(cumulative_probs)
    logit_transformed_observations = logit(observed_values / scale)

    standard_norm_quantiles = standard_norm_quantiles.reshape(-1, 1)
    logit_transformed_observations = logit_transformed_observations.reshape(-1, 1)

    raw_variance = cumulative_probs * (1 - cumulative_probs) / norm.pdf(norm.ppf(cumulative_probs)) ** 2
    sample_weight = 1 / raw_variance

    model = LinearRegression().fit(standard_norm_quantiles, logit_transformed_observations, sample_weight)
    mean, std = float(model.intercept_[0]), float(model.coef_[0][0])

    expected_norm_quantiles = norm.ppf(cumulative_probs, loc=mean, scale=std)
    expected_values = scale * expit(expected_norm_quantiles) + lower_bound
    observed_values = observed_values + lower_bound

    step_size = 1000
    x_values_unscaled = np.linspace(0, 1, step_size)[1:-1]
    y_values_unscaled = logitnorm_pdf(x_values_unscaled, mean, std)

    x_values = x_values_unscaled * scale + lower_bound
    y_values = y_values_unscaled / scale

    sse = np.sum((observed_values - expected_values) ** 2)
    sst = np.sum((observed_values - np.mean(observed_values)) ** 2)

    cumulative = None
    if "cumulative" in request_json and request_json["cumulative"] != "":
        cumulative = norm.cdf(logit(float(request_json["cumulative"]) / scale), mean, std)

    probability = None
    if "probability" in request_json and request_json["probability"] != "":
        probability = expit(norm.ppf(float(request_json["probability"]), mean, std)) * scale

    return jsonify(
        {
            "mean": np.sum(x_values * y_values) / (step_size - 1) * scale,
            "mean_logit_norm": mean,
            "std_logit_norm": std,
            "observed_values": observed_values.tolist(),
            "expected_values": expected_values.tolist(),
            "x_values": x_values.tolist(),
            "y_values": y_values.tolist(),
            "observed_y_values": (logitnorm_pdf((observed_values - lower_bound) / scale, mean, std) / scale).tolist(),
            "expected_y_values": (logitnorm_pdf((expected_values - lower_bound) / scale, mean, std) / scale).tolist(),
            "rmse": np.sqrt(sse / len(observed_values)),
            "mae": np.mean(np.abs(observed_values - expected_values)),
            "r_square": 1 - sse / sst,
            "cumulative": cumulative,
            "probability": probability,
        }
    )


if __name__ == "__main__":
    app.run(debug=False)

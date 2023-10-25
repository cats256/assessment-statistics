from flask import Flask, request, abort, jsonify
from flask_cors import CORS

import numpy as np
from scipy.stats import norm
from scipy.special import expit, logit, erfinv
from scipy.optimize import minimize

app = Flask(__name__)
CORS(app)

# for a general informative view only, very high error at the tails


def check_invalid_values(observed_values, scale):
    is_sorted = all(observed_values[i] <= observed_values[i + 1] for i in range(len(observed_values) - 1))
    if not is_sorted:
        print("Invalid request: The observed values are not sorted.")
        abort(400)

    is_range = all(0 < observed_value < scale for observed_value in observed_values)
    if not is_range:
        print("Invalid request: observed values are out of range: ")
        print(observed_values)
        abort(400)


def norm_loss(params, quantiles, logit_observations):
    try:
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

        # tried to use this but this is out of my expertise and package won't work and i'm too lazy
        # https://github.com/rsnirwan/bqme
        # https://arxiv.org/abs/2008.06423

        # don't really know what to name this but it's variance calculated without sample
        # size purely to figure out the weight to give to each quantile
        # https://blogs.sas.com/content/iml/2018/03/07/fit-distribution-matching-quantile.html
        # raw_variance = (quantiles * (1 - quantiles)) / (norm.pdf(expected_values, mean, std) ** 2)
        # below is pretty much same thing as the line above just more explicit and optimized
        # theoretically could take out std term and 2 * pi since they are constants and would not affect
        # estimated parameters but since we're estimating numerically, taking them out
        # increases error in estimated variance and decreases error in estimated mean
        # this is probably due to taking out std term leads to a decrease in how much change in std affects
        # change in sum squared error
        raw_variance = quantiles * (1 - quantiles) * np.exp(2 * erfinv(2 * quantiles - 1) ** 2) * (std**2) * 2 * np.pi

        return np.sum(squared_differences / raw_variance)
    except:
        print("Exception occured: ", mean, std)
        return np.inf


def optimize_logit_norm(observed_values, quantiles, scale):
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
        bounds=[(None, None), (0.01, None)],
    )

    return optimization_result.x


def logit_norm_pdf(x, mean, std):
    return 1 / (std * np.sqrt(2 * np.pi)) * 1 / (x * (1 - x)) * np.e ** (-((logit(x) - mean) ** 2) / (2 * std**2))


@app.route("/parameters", methods=["POST"])
def parameters():
    request_json = request.json

    lower_bound = float(request_json["minGrade"])
    upper_bound = float(request_json["maxGrade"])
    scale = upper_bound - lower_bound

    sorted_dict = sorted(request_json["quantiles"].items(), key=lambda x: x[0])
    quantiles = np.array([float(item[0]) for item in sorted_dict])
    observed_values = np.array([float(item[1]) for item in sorted_dict]) - lower_bound

    check_invalid_values(observed_values, scale)

    # took me way too long to realize i could have done this analytically
    # using linear regression lol
    mean, std = optimize_logit_norm(observed_values, quantiles, scale)

    expected_norm = norm.ppf(quantiles, loc=mean, scale=std)
    expected_values = scale * expit(expected_norm) + lower_bound
    observed_values = observed_values + lower_bound

    step_size = 1000
    x_values_unscaled = np.linspace(0, 1, step_size)[1:-1]
    y_values_unscaled = logit_norm_pdf(x_values_unscaled, mean, std)

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
            # can also do np.sum(x_values * y_values) / np.sum(y_values) * scale
            "mean": np.sum(x_values * y_values) / (step_size - 1) * scale,
            "mean_logit_norm": mean,
            "std_logit_norm": std,
            "observed_values": observed_values.tolist(),
            "expected_values": expected_values.tolist(),
            "x_values": x_values.tolist(),
            "y_values": y_values.tolist(),
            "observed_y_values": (logit_norm_pdf((observed_values - lower_bound) / scale, mean, std) / scale).tolist(),
            "expected_y_values": (logit_norm_pdf((expected_values - lower_bound) / scale, mean, std) / scale).tolist(),
            "rmse": np.sqrt(sse / len(observed_values)),
            "mae": np.mean(np.abs(observed_values - expected_values)),
            "r_square": 1 - sse / sst,
            "cumulative": cumulative,
            "probability": probability,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

# unoptimized code, for research purpose, not for production

library(logitnorm)
logit_norm_loss <- function(parameters, quantiles, observed_values, scale) {
  mean <- parameters[1]
  standard_deviation <- parameters[2]
  
  expected_values <- qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
  squared_differences <- (logit(observed_values/scale) - logit(expected_values))^2

  # expected_values <- 84 * qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
  # squared_differences <- (observed_values - expected_values)^2

  # not sure which loss function to use but both produces very similar results.
  # i personally prefer the calculating the SSE by transforming the data into the
  # normal. main question is what's the type of error? multiplicative error or
  # additive? i don't have enough data to answer and check for heteroskedasticity
  # but i believe it's the former or it could be a mix of both. i don't know.
  return(sum(squared_differences))
}

lower_bound <- 0
upper_bound <- 84
scale <- upper_bound - lower_bound

quantiles <- c(0.25, 0.50, 0.75)
observed_values <- c(56.87, 64.25, 70.59)

initial_parameters <- c(1.19257434039492, 0.677460313863577)
optimization_result <- optim(
  par = initial_parameters, fn = logit_norm_loss,
  quantiles = quantiles, observed_values = observed_values, scale = scale
)

minimum_loss <- optimization_result$value
mean <- optimization_result$par[1]
sd <- optimization_result$par[2]

expected_values <- scale * qlogitnorm(quantiles, mu = mean, sigma = sd)

# transformed using the logit function
transformed_observed <- logit(observed_values/scale)
transformed_expected <- logit(expected_values/scale)

print(paste("Minimum Loss:", minimum_loss))
print(paste("Optimal Mean:", mean))
print(paste("Optimal Standard Deviation:", sd))
print(paste("Predicted Quantiles:", paste(quantiles, expected_values, sep = ": ", collapse = ", ")))
print(paste("Squared Sum Error:", sum((observed_values - expected_values)^2)))
print(paste("Squared Sum Error Normal:", sum((transformed_observed - transformed_expected)^2)))
print(paste("Cumulative Probability at x = 78:", plogitnorm(c(78/84), mu = mean, sigma = sd)))

quantiles <- seq(0, 1, by = 0.01)
quantile_values <- dlogitnorm(quantiles, mu = mean, sigma = sd)
plot(quantiles, quantile_values, type = "l", 
     xlab = "Logit-Normal Values", ylab = "Probability Density",
     main = "Probability Density Function of Logit-Normal Distribution")
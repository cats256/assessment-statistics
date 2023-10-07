library(logitnorm)
logit_norm_loss <- function(parameters, quantiles, scaled_observations) {
  mean <- parameters[1]
  standard_deviation <- parameters[2]
  
  expected_values <- qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
  squared_differences <- (scaled_observations - expected_values)^2
  return(sum(squared_differences))
}

lower_bound <- 0
upper_bound <- 84
scale <- upper_bound - lower_bound

quantiles <- c(0.25, 0.50, 0.75)
observed_values <- c(56.87, 64.25, 70.59)
scaled_observations <- observed_values/scale

initial_parameters <- c(1.19257434039492, 0.677460313863577)
optimization_result <- optim(
  par = initial_parameters, 
  fn = logit_norm_loss, 
  quantiles = quantiles, scaled_observations = scaled_observations
)

minimum_loss <- optimization_result$value
mean <- optimization_result$par[1]
sd <- optimization_result$par[2]

print(paste("Minimum Loss:", minimum_loss))
print(paste("Optimal Mean:", mean))
print(paste("Optimal Standard Deviation:", sd))
print(paste("Squared Sum Error:", sum((observed_values - scale * qlogitnorm(quantiles, mu = mean, sigma = sd))^2)))
print(paste("Predicted Quantiles:", paste(quantiles, scale * qlogitnorm(quantiles, mu = mean, sigma = sd), sep = ": ", collapse = ", ")))
print(paste("Cumulative Distribution", plogitnorm(c(78/84), mu = mean, sigma = sd)))

quantiles <- seq(0, 1, by = 0.01)
quantile_values <- dlogitnorm(quantiles, mu = mean, sigma = sd)
plot(quantiles, quantile_values, type = "l", 
     xlab = "Logit-Normal Values", ylab = "Probability Density",
     main = "Probability Density Function of Logit-Normal Distribution")
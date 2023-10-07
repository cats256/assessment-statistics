observed_quantiles <- c(56.87, 64.25 , 70.59)
quantiles <- c(0.25, 0.50, 0.75)

mean <- 63.27
max_possible_val <- 84

prob <- mean / max_possible_val

binomial_cdf <- function(prob, k, n) {
  cdf <- 1 - pbeta(prob, k + 1, n - k)
  return(cdf)
}

cdf_loss_function <- function (k, quantile, prob, n) {
  return ((quantile - binomial_cdf(prob, k, n))^2)
}

binomial_quantile <- function (quantile, prob, n) {
  value <- optimize(
    f = function(k) cdf_loss_function(k, quantile, prob, n),
    interval = c(0, n)
  )$minimum
  return(value)
}

binomial_loss_function <- function(scale) {
  scaled_size = max_possible_val / scale
  
  expected_quantiles <- sapply(quantiles, function(q) scale * binomial_quantile(q, prob, scaled_size))
  squared_diff <- (observed_quantiles - expected_quantiles)^2
    print(sum(squared_diff))
  return(sum(squared_diff))
}

optimal_scale <- optimize(f = binomial_loss_function, interval = c(0.001, 10))

# quantiles <- c(0.25, 0.50, 0.75)
# print(c(sapply(quantiles, function(q) binomial_quantile(q, 0.5, 2))))

print(paste("Estimated scale:", optimal_scale$minimum))
print(paste("Estimated size:", max_possible_val / optimal_scale$minimum))
print(paste("Estimated probability:", prob))
print(c(sapply(quantiles, function(q) 3.41826318648445 * binomial_quantile(q, prob, max_possible_val/3.41826318648445))))

library(logitnorm)
trunc_norm_loss <- function(parameters, quantiles, observed_values) {
  mean <- parameters[1]
  standard_deviation <- parameters[2]
  
  expected_values <- qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
  squared_differences <- (observed_values/100 - expected_values)^2
  return(sum(squared_differences))
}

lower_bound <- 0
upper_bound <- 100

quantiles <- c(0.25, 0.50, 0.75)
observed_values <- c(77.09, 85.62, 92.87)

initial_parameters <- c(63.27/upper_bound, (70.59 - 56.87) / 1.35 / upper_bound)

optimization_result <- optim(
  par = initial_parameters, 
  fn = trunc_norm_loss, 
  quantiles = quantiles, observed_values = observed_values
)

minimum_loss <- optimization_result$value
optimal_parameters <- optimization_result$par

print(paste("Minimum Loss:", minimum_loss))
print(paste("Optimal Mean:", optimal_parameters[1]))
print(paste("Optimal Standard Deviation:", optimal_parameters[2]))

print(qlogitnorm(quantiles, mu = optimal_parameters[1], sigma = optimal_parameters[2]))
quantiles <- seq(0, 1, by = 0.01)

quantile_values <- dlogitnorm(quantiles, mu = optimal_parameters[1], sigma = optimal_parameters[2])

plot(quantiles, quantile_values, type = "l", 
     xlab = "Logit-Normal Values", ylab = "Probability Density",
     main = "Probability Density Function of Logit-Normal Distribution")

# print(plogitnorm(c(78/84), mu = optimal_parameters[1], sigma = optimal_parameters[2]))
print((56.87 - 84 * qlogitnorm(c(0.25), mu = optimal_parameters[1], sigma = optimal_parameters[2]))^2)
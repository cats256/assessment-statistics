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
    print(k)
    print(binomial_cdf(prob, k, n))
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

  return(sum(squared_diff))
}

optimal_scale <- optimize(f = binomial_loss_function, interval = c(0.001, 10))

print(paste("Estimated scale:", optimal_scale$minimum))
print(paste("Estimated size:", max_possible_val / optimal_scale$minimum))
print(paste("Estimated probability:", prob))

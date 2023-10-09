# this may seems simple but it takes a lot more work than you may expect so
# please don't forget to attribute/credit me at https://github.com/cats256/ XD

# continuous analog of a binomial distribution
# utilizes the beta distribution
# similar but two different things!!!
library(cbinom)

observed_quantiles <- c(1, 2, 3)
quantiles <- c(0.25, 0.50, 0.75)

mean <- 2
max_possible_val <- 4

# estimated p for binomial is mean over size
# this wouldn't have worked at first glance
# since mean and size refers to the mean and size
# of a binomial distribution, that is they are not
# scaled by a constant factor. however since 
# both the numerator and denominator are scaled,
# this is also the estimated p for the scaled 
#  binomial we're trying to find
prob <- mean / max_possible_val

# otherwise known as sum of squared errors
loss_function <- function(scale) {
  scaled_size = max_possible_val / scale
  
  expected_quantiles <- scale * qcbinom(quantiles, size = scaled_size, prob = prob)
  squared_diff <- (observed_quantiles - expected_quantiles)^2
  print(scale)
  print(expected_quantiles)
  print(sum(squared_diff))
  cat("\n")
  return(sum(squared_diff))
}

# utilizes least square principles
# was about to manually implement gradient descent
# but i realized there exists a built in function
optimal_scale <- optimize(
  f = loss_function,
  interval = c(0.001, 1000)
)

print(paste("Estimated scale:", optimal_scale$minimum))
print(paste("Estimated size:", max_possible_val / optimal_scale$minimum))
print(paste("Estimated probability:", prob))

# size <- 20
# prob <- 0.5
# x <- 0:20
# xx <- seq(0, 20, length = 200)
# xxx <- seq(0, 21, length = 200)
# 
# binomial_pmf <- function(k, n, p) {
#   factorial(n) / (factorial(k) * factorial(n - k)) * p^k * (1 - p)^(n - k)
# }
# 
# print(dbinom(0, 2, 0.5))
# print(dcbinom(0, 2, 0.5))
# 
# plot(x, dbinom(x, size, prob), xlab = "x", ylab = "P(x)", ylim = c(0, 1))
# lines(xx, binomial_pmf(xx, size, prob))
# lines(xxx, dcbinom(xx, size, prob))
# 
# legend('topleft', legend = c("standard binomial", "continuous binomial"), pch = c(1, NA), lty = c(NA, 1))
# mtext(side = 3, line = 1.5, text = "pcbinom resembles pbinom but continuous and shifted")

# # Define a range of scale values to explore
# scale_values <- seq(0.001, 100, by = 0.01)
# 
# # Calculate the loss for each scale value
# loss_values <- sapply(scale_values, loss_function)
# 
# # Create a plot
# plot(scale_values, loss_values, type = "l", 
#      xlab = "Scale", ylab = "Loss",
#      main = "Loss vs. Scale")
# 
# # Find the scale value that minimizes the loss
# min_loss_scale <- scale_values[which.min(loss_values)]
# print(min_loss_scale)
# # Add a vertical line at the minimum loss point
# abline(v = min_loss_scale, col = "red", lty = 2)
# 
# # Add text to label the minimum loss point
# text(min_loss_scale, max(loss_values), 
#      sprintf("Min Loss: %.2f", min_loss_scale), 
#      pos = 4, col = "red")
# 
# # Show the plot


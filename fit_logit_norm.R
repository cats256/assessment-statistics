# more updated code in the python file
# unoptimized code, for research purpose, not for production

if (!requireNamespace("logitnorm", quietly = TRUE)) {
  install.packages("logitnorm")
}

if (!requireNamespace("plotly", quietly = TRUE)) {
  install.packages("plotly")
}

library(logitnorm)
library(plotly)

logit_norm_loss <- function(parameters, quantiles, observed_values, scale) {
  mean <- parameters[1]
  standard_deviation <- parameters[2]

  # not sure which loss function to use but both produces very similar results.
  # i personally prefer the calculating the SSE by transforming the data into the
  # normal. main question is what's the type of error? multiplicative error or
  # additive? i don't have enough data to answer and check for heteroskedasticity
  # but i believe it's the latter or it could be a mix of both. i don't know.

  expected_values <- qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
  squared_differences <- (logit(observed_values/scale) - logit(expected_values))^2

  # expected_values <- 84 * qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
  # squared_differences <- (observed_values - expected_values)^2

  return(sum(squared_differences))
}

# logit_norm_loss <- function(parameters, quantiles, observed_values, scale) {
#   mean <- parameters[1]
#   standard_deviation <- parameters[2]

#   observed_values <- observed_values/84
#   expected_values <- qlogitnorm(quantiles, mu = mean, sigma = standard_deviation)
#   pinball_losses <- 0

#   for (i in seq_len(3)) {
#     if (observed_values[i] >= expected_values[i]) {
#       pinball_losses <- pinball_losses + (observed_values[i] - expected_values[i]) * quantiles[i]
#     } else {
#       pinball_losses <- pinball_losses + (expected_values[i] - observed_values[i]) * (1 - quantiles[i])
#     }
#   }
#   # Return the sum of pinball losses for all quantiles
#   return(pinball_losses)
# }


lower_bound <- 0
upper_bound <- 84
scale <- upper_bound - lower_bound

quantiles <- c(0.25, 0.50, 0.75)
observed_values <- c(56.87, 64.25, 70.59)

initial_parameters <- c(
  sum(logit(observed_values/scale))/length(observed_values), 
  (logit(observed_values[length(observed_values)]/scale) - logit(observed_values[1]/scale)) / (qnorm(quantiles[length(quantiles)]) - qnorm(quantiles[1]))
)

optimization_result <- optim(
  par = initial_parameters, fn = logit_norm_loss,
  quantiles = quantiles, observed_values = observed_values, scale = scale
)

minimum_loss <- optimization_result$value
mean <- optimization_result$par[1]
sd <- optimization_result$par[2]

expected_values <- scale * qlogitnorm(quantiles, mu = mean, sigma = sd)

transformed_observed <- logit(observed_values/scale)
transformed_expected <- logit(expected_values/scale)

print(paste("Minimum Loss:", minimum_loss))
print(paste("Optimal Mean:", mean))
print(paste("Optimal Standard Deviation:", sd))
print(paste("Predicted Quantiles:", paste(quantiles, expected_values, sep = ": ", collapse = ", ")))
print(paste("Squared Sum Error:", sum((observed_values - expected_values)^2)))
print(paste("Squared Sum Error Normal:", sum((transformed_observed - transformed_expected)^2)))
print(paste("Cumulative Probability at x = 78:", plogitnorm(c(78/84), mu = mean, sigma = sd)))

# very restricted range but this effectively show how the function is convex
mean_values <- seq(1.19354772770165-0.4, 1.19354772770165+0.4, length.out = 100)  
std_deviation_values <- seq(0.01, 1.4, length.out = 100)  

# for the logit transformation thing
# mean_values <- seq(1.19354772770165-20, 1.19354772770165+20, length.out = 200)  
# std_deviation_values <- seq(0.01, 20, length.out = 300)  

loss_matrix <- matrix(NA, nrow = length(mean_values), ncol = length(std_deviation_values))

for (i in 1:length(mean_values)) {
  for (j in 1:length(std_deviation_values)) {
    parameters <- c(mean_values[i], std_deviation_values[j])
    loss_matrix[i, j] <- logit_norm_loss(parameters, quantiles, observed_values, scale)
  }
}

loss_values = as.vector(loss_matrix)
mean_vector = rep(mean_values, times = length(std_deviation_values))
std_deviation_vector = rep(std_deviation_values, each = length(mean_values))

loss_data <- data.frame(
  mean = rep(mean_values, times = length(std_deviation_values)),
  std_deviation = rep(std_deviation_values, each = length(mean_values)),
  loss = as.vector(loss_matrix)
)

my_plot <- plotly::plot_ly(
  data = loss_data, 
  x = ~mean, 
  y = ~std_deviation, 
  z = ~loss, 
  type = "scatter3d", 
  mode = "markers", 
  marker = list(size = 5, color = ~loss, colorscale = "Viridis")
) %>%
  plotly::layout(
    scene = list(xaxis = list(title = "Mean"), yaxis = list(title = "Standard Deviation"), zaxis = list(title = "Loss"))
  )

# Add marker to the lowest point
# min_loss_row <- loss_data[which.min(loss_data$loss), ]
# my_plot <- my_plot %>% 
#   plotly::add_markers(
#     data = min_loss_row,
#     color = I("red"), 
#     size = 10,
#     marker = list(
#       size = 10,
#       line = list(
#         width = 200
#       )
#     )
#   )

print(my_plot)

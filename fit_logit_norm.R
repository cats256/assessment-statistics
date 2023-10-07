# unoptimized code, for research purpose, not for production

if (!requireNamespace("logitnorm", quietly = TRUE)) {
  install.packages("logitnorm")
}

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

# initial_parameters <- c(1.19257434039492, 0.677460313863577)
# optimization_result <- optim(
#   par = initial_parameters, fn = logit_norm_loss,
#   quantiles = quantiles, observed_values = observed_values, scale = scale
# )

# minimum_loss <- optimization_result$value
# mean <- optimization_result$par[1]
# sd <- optimization_result$par[2]

# expected_values <- scale * qlogitnorm(quantiles, mu = mean, sigma = sd)

# # transformed using the logit function
# transformed_observed <- logit(observed_values/scale)
# transformed_expected <- logit(expected_values/scale)

# print(paste("Minimum Loss:", minimum_loss))
# print(paste("Optimal Mean:", mean))
# print(paste("Optimal Standard Deviation:", sd))
# print(paste("Predicted Quantiles:", paste(quantiles, expected_values, sep = ": ", collapse = ", ")))
# print(paste("Squared Sum Error:", sum((observed_values - expected_values)^2)))
# print(paste("Squared Sum Error Normal:", sum((transformed_observed - transformed_expected)^2)))
# print(paste("Cumulative Probability at x = 78:", plogitnorm(c(78/84), mu = mean, sigma = sd)))

# quantiles <- seq(0, 1, by = 0.01)
# quantile_values <- dlogitnorm(quantiles, mu = mean, sigma = sd)
# plot(quantiles, quantile_values, type = "l", 
#      xlab = "Logit-Normal Values", ylab = "Probability Density",
#      main = "Probability Density Function of Logit-Normal Distribution")

# Load necessary libraries if not already loaded
# library(stats)

# # Define a grid of values for mean and standard_deviation
# mean_values <- seq(-10, 10, length.out = 100)  # Adjust the range and resolution as needed
# std_deviation_values <- seq(0.01, 5, length.out = 100)  # Adjust the range and resolution as needed

# # Create an empty matrix to store the loss values
# loss_matrix <- matrix(NA, nrow = length(mean_values), ncol = length(std_deviation_values))

# # Compute the loss values for each combination of mean and standard_deviation
# for (i in 1:length(mean_values)) {
#   for (j in 1:length(std_deviation_values)) {
#     parameters <- c(mean_values[i], std_deviation_values[j])
#     loss_matrix[i, j] <- logit_norm_loss(parameters, quantiles, observed_values, scale)
#   }
# }

# # Create the 3D plot
# persp(x = mean_values, y = std_deviation_values, z = loss_matrix,
#       xlab = "Mean", ylab = "Standard Deviation", zlab = "Loss",
#       theta = 40, phi = 40, expand = 0.5, col = "lightblue")

# Load the required libraries
library(plotly)

# Define a grid of values for mean and standard_deviation
mean_values <- seq(-5, 5, length.out = 100)  
std_deviation_values <- seq(0.01, 10, length.out = 100)  

# Create an empty matrix to store the loss values
loss_matrix <- matrix(NA, nrow = length(mean_values), ncol = length(std_deviation_values))

# Compute the loss values for each combination of mean and standard_deviation
for (i in 1:length(mean_values)) {
  for (j in 1:length(std_deviation_values)) {
    parameters <- c(mean_values[i], std_deviation_values[j])
    loss_matrix[i, j] <- logit_norm_loss(parameters, quantiles, observed_values, scale)
  }
}

# Create a data frame for the loss values
loss_data <- data.frame(
  mean = rep(mean_values, each = length(std_deviation_values)),
  std_deviation = rep(std_deviation_values, length(mean_values)),
  loss = as.vector(loss_matrix)
)

# # Create a 3D scatter plot using Plotly
# my_plot <- plotly::plot_ly(data = loss_data, x = ~mean, y = ~std_deviation, z = ~loss, type = "scatter3d", mode = "markers") %>%
#   plotly::layout(scene = list(xaxis = list(title = "Mean"), yaxis = list(title = "Standard Deviation"), zaxis = list(title = "Loss")))
# print(my_plot)

# Create a 3D scatter plot using Plotly with a color scale
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

min_loss_row <- loss_data[which.min(loss_data$loss), ]
my_plot <- my_plot %>% 
  plotly::add_markers(data = min_loss_row, x = ~mean, y = ~std_deviation, z = ~loss, color = I("red"), size = 5)

print(my_plot)

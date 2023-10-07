# Define the quantile level(s) you want to find
quantiles <- c(0.25, 0.5, 0.75)  # Change these values as needed

# Parameters of the normal distribution (mean and standard deviation)
mean <- 63.95880
sd <- 10.18865

# Calculate the quantiles for the normal distribution
quantile_values <- qnorm(quantiles, mean = mean, sd = sd)

# Print the results
cat("Quantile Values:")
print(quantile_values)

observed_values <- c(56.87, 64.25, 70.59)
squared_errors <- (observed_values - quantile_values)^2
sse <- sum(squared_errors)
cat("Sum of Squared Errors (SSE):", sse, "\n")

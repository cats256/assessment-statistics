# library("bln")
# library("GA")

# log_likelihood_bln <- function(samples, size, mean, std) {
#     log_likelihood <- 0
#     for (sample in samples) {
#         log_likelihood <- log_likelihood + log(dbln(sample, size, mean, std))
#     }
#     print(log_likelihood)
#     return(log_likelihood)
# }

# neg_log_likelihood_bln <- function(params, samples, size) {
#     mean <- params[1]
#     std <- params[2]

#     if (std <= 0 || size <= 0) {
#         return(1e6)  # Return a large number instead of Inf
#     }

#     return(-log_likelihood_bln(samples, size, mean, std))
# }

# data <- read.csv("C:/Users/nhatt/Downloads/All/2023 - Fall/Code/R/Assessment-Statistics/assessment-statistics/flask-server/diemthi2019.csv")
# math_data <- na.omit(data$GDCD)
# random_samples <- sample(math_data, size = 100)

# size_values <- 1:150
# best_result <- NULL

# for (size in size_values) {
#     initial_params <- c(mean = 0, std = 1.2)
#     #   result <- optim(par = initial_params, fn = neg_log_likelihood_bln, samples = random_samples, size = size, method = "Nelder-Mead")
#     result <- ga(type = "real-valued", fitness = function(x) -neg_log_likelihood_bln(x, samples = random_samples, size = size), lower = c(-1000, 0.2), upper = c(1000, 100))

#     if (is.null(best_result) || result$value < best_result$value) {
#         best_result <- result
#         best_size <- size
#     }
# }

# print(best_result)
# print(best_size)


# library("bln")

# log_likelihood_bln <- function(samples, size, mean, std) {
#     log_likelihood <- 0
#     for (sample in samples) {
#         log_likelihood <- log_likelihood + log(dbln(sample, size, mean, std))
#     }
#     return(log_likelihood)
# }

# neg_log_likelihood_bln <- function(params, samples, size) {
#     mean <- params[1]
#     std <- params[2]
#     size <- round(abs(params[3]))
    
#     return(-log_likelihood_bln(samples, size, mean, std))
# }

data <- read.csv("assessment-statistics/flask-server/diemthi2019.csv")

data <- na.omit(data$GDCD) * 4

bin_width <-1
num_bins <- (max(data, na.rm = TRUE) - min(data, na.rm = TRUE)) / bin_width

hist(data, breaks = 40, main = "Histogram of GDCD Scores", xlab = "Scores", ylab = "Frequency", border = "white", col = "skyblue", xlim = c(min(data), max(data)))

set.seed(1)
random_samples <- sample(data, size = 100)

initial_params <- c(mean = 2, std = 1.20, size = 100)

result <- optim(par = initial_params, fn = neg_log_likelihood_bln, samples = random_samples * 10)

print(result)


# library(ggplot2)

# # Define the normal distribution parameters
# mean <- 0
# std_dev <- 1

# # Create a sequence of x-values
# x_values <- seq(0, 107, by = 1)

# # Evaluate the PDF at each x-value
# pdf_values <- dbln(x_values, 105, 0.7880395, 0.6120927)
# # pdf_values <- normal_pdf(x_values, mean, std_dev)

# # Create a data frame for plotting
# pdf_data <- data.frame(x = x_values, y = pdf_values)

# # Create the plot
# plot <- ggplot(pdf_data, aes(x = x, y = y)) +
#   geom_col(width = 1, fill = 'skyblue', color = 'white') +
#   labs(title = 'Bar Plot from Normal Distribution PDF',
#        x = 'Value',
#        y = 'Probability Density') +
#   theme_minimal()

# # Print the plot
# print(plot)

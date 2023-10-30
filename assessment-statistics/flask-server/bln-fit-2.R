library("bln")
library(ggplot2)

setwd("C:/Users/nhatt/Downloads/All/2023 - Fall/Code/R/Assessment-Statistics/assessment-statistics/flask-server")

# https://github.com/PejLab/bln

log_likelihood_bln <- function(samples, size, mean, std) {
    log_likelihood <- 0
    for (sample in samples) {
        log_likelihood <- log_likelihood + log(dbln(sample, size, mean, std))
    }
    return(log_likelihood)
}

neg_log_likelihood_bln <- function(params, samples, size) {
    mean <- params[1]
    std <- params[2]
    
    return(-log_likelihood_bln(samples, size, mean, std))
}

data <- read.csv("diemthi2019.csv")
data <- na.omit(data$GDCD) * 4 + 0.5

bin_width <-1
num_bins <- (max(data, na.rm = TRUE) - min(data, na.rm = TRUE)) / bin_width

data_df <- data.frame(value = data)

hist_plot <- ggplot(data_df, aes(x = value)) +
  geom_histogram(aes(y = ..density..), binwidth = 1, fill = 'skyblue', color = 'white', boundary = 0.5) +
  labs(title = 'Normalized Histogram of College Entrance Exam Scores in Vietnam 2019 Civics Subject',
       x = 'Score (Scaled by 4 due to ggplot issue)',
       y = 'Probabillity Mass (Normalized from Frequency)') +
  xlim(-0.5, 40.5) +
  ylim(0, 0.09) +
  theme_minimal()

print(hist_plot)

# set.seed(1)
# data <- sample(data, size = 100)

# initial_params <- c(mean = 2, std = 1.20)

# result <- optim(par = initial_params, fn = neg_log_likelihood_bln, samples = data, size = 40)

# print(result)

# plot

x_values <- seq(0, 40, by = 1)

pdf_values <- dbln(x_values, 40, 1.0955405, 0.5767234)
pdf_data <- data.frame(x = x_values, y = pdf_values)

print(pdf_data)

plot <- ggplot(pdf_data, aes(x = x, y = y)) +
    geom_col(width = 1, fill = 'skyblue', color = 'white') +
    labs(title = 'PMF of Binomial-Logit-Normal Compound Distribution with mu = 1.0955405 and sigma = 0.5767234',
       x = 'Score (Scaled by 4 due to ggplot issue)',
        y = 'Probability Mass') +
    xlim(-0.5, 40.5) +
    ylim(0, 0.09) +
    theme_minimal()

print(plot)


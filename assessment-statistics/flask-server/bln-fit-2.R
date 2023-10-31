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

neg_log_likelihood_bln_vectorized <- function(params, frequencies, size) {
    mean <- params[1]
    std <- params[2]

    log_likelihood <- 0
    for (i in 1:size) {
        log_likelihood <- log_likelihood + (log(dbln(i, size, mean, std)) * frequencies[i + 1])
        # print(log(dbln(i, size, mean, std)))
        # print("Frequencies: ")
        # print(i + 1)
        # print(frequencies[i + 1])
        # print(log_likelihood)
    }
    
    return(-log_likelihood)
}

data <- read.csv("diemthi2019.csv")
data <- na.omit(data$GDCD) * 4
data <- data[data == floor(data)]

# set.seed(1)
# data <- sample(data, size = 100)

frequency_table <- table(data)
frequencies <- as.vector(frequency_table)

print(frequency_table)

initial_params <- c(mean = 0.4171083, std = 0.4208499)

result <- optim(par = initial_params, fn = neg_log_likelihood_bln_vectorized, frequencies = frequencies, size = 40)

print(result)
# print(neg_log_likelihood_bln_vectorized(c(1.0955405, 0.5767234), frequencies, 40))
# print(neg_log_likelihood_bln(c(1.0955405, 0.5767234), data, 40))


data_df <- data.frame(value = data + 0.5)

hist_plot <- ggplot(data_df, aes(x = value)) +
  geom_histogram(aes(y = ..density..), binwidth = 1, fill = 'skyblue', color = 'white', boundary = 0.5) +
  labs(title = 'Normalized Histogram of College Entrance Exam Scores in Vietnam 2019 Civics Subject',
       x = 'Score (Scaled by 4 due to ggplot issue)',
       y = 'Probabillity Mass (Normalized from Frequency)') +
  xlim(-0.5, 40.5) +
  ylim(0, 0.09) +
  theme_minimal()

print(hist_plot)

# plot

# biology parameters
# pdf_values <- dbln(x_values, 40, -0.1379180, 0.4104577)

# physics parameters
# pdf_values <- dbln(x_values, 40, 0.3013156, 0.6304329)

# civics parameters
# pdf_values <- dbln(x_values, 40, 1.0955405, 0.5767234)

x_values <- seq(0, 40, by = 1)

pdf_values <- dbln(x_values, 40, result$par[1], result$par[2])
pdf_data <- data.frame(x = x_values, y = pdf_values)

plot <- ggplot(pdf_data, aes(x = x, y = y)) +
    geom_col(width = 1, fill = 'skyblue', color = 'white') +
    labs(title = 'PMF of Binomial-Logit-Normal Compound Distribution with mu = 1.0955405 and sigma = 0.5767234',
       x = 'Score (Scaled by 4 due to ggplot issue)',
        y = 'Probability Mass') +
    xlim(-0.5, 40.5) +
    ylim(0, 0.09) +
    theme_minimal()

print(plot)


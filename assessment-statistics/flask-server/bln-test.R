library("optimx")
library("bln")

log_likelihood_bln <- function(samples, size, mean, std) {
    log_likelihood <- 0
    for (sample in samples) {
        dbln_value <- dbln(sample, size, mean, std)
        if (is.nan(dbln_value) || dbln_value <= 0) {
            return(-Inf)
        }
        log_likelihood <- log_likelihood + log(dbln_value)
    }
    return(log_likelihood)
}

neg_log_likelihood_bln <- function(params, samples, size) {
    mean <- params[1]
    std <- abs(params[2])
    
    if (std <= 0 || size <= 0) {
        return(Inf)
    }
    
    result <- -log_likelihood_bln(samples, size, mean, std)
    
    if (is.nan(result) || is.infinite(result)) {
        return(Inf)
    }
    
    return(result)
}

data <- read.csv("C:/Users/nhatt/Downloads/All/2023 - Fall/Code/R/Assessment-Statistics/assessment-statistics/flask-server/diemthi2019.csv")
math_data <- na.omit(data$GDCD)
random_samples <- sample(math_data, size = 100)

# Define a range of possible sizes
size_values <- 1:150

# Initialize a variable to store the best result
best_result <- NULL
best_size <- NULL

# Loop over the size values
for (size in size_values) {
    initial_params <- c(mean = 2, std = 1.20)
    result <- optimx(par = initial_params, fn = neg_log_likelihood_bln, samples = random_samples, size = size)
    if (is.null(best_result) || result$value < best_result$value) {
        best_result <- result
        best_size <- size
    }
}

print(best_result)
print(best_size)

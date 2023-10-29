library("bln")

log_likelihood_bln <- function(samples, size, mean, std) {
    log_likelihood <- 0
    for (sample in samples) {
        log_likelihood <- log_likelihood + log(dbln(sample, size, mean, std))
    }
    return(log_likelihood)
}

neg_log_likelihood_bln <- function(params, samples, size) {
    mean <- params[1]
    std <- abs(params[2])
    
    return(-log_likelihood_bln(samples, size, mean, std))
}

grades <- c(8, 10, 11, 12, 13, 13, 14, 15, 15, 16, 17, 17, 18, 19, 19, 20, 20, 20, 22, 23, 23, 24, 24, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 31, 32, 32, 33, 33, 34, 34, 34, 35, 35, 35, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39, 39, 40, 40, 40, 41, 41, 41, 42, 42, 42, 43, 43, 43, 44, 44, 44, 45, 45, 45, 46, 46, 46, 47, 47, 47, 47, 48, 48, 48, 49, 49, 50, 50, 50, 51, 51, 51, 52, 52, 53, 53, 54, 54)

initial_params <- c(mean = 0.80, std = 1.20)
result <- optim(par = initial_params, fn = neg_log_likelihood_bln, samples = grades, size = 54)

hist(grades, breaks = 47, main = "Histogram of Grades", xlab = "Grade", ylab = "Frequency", border = "white", col = "skyblue")

print(result)

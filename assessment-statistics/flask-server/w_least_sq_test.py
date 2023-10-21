# r code
# p <- 0.25
# 1 / (p*(1-p)/(101 * (dnorm(qnorm(p)))^2))
# p <- 0.50
# 1 / (p*(1-p)/(101 * (dnorm(qnorm(p)))^2))
# p <- 0.75
# 1 / (p*(1-p)/(101 * (dnorm(qnorm(p)))^2))

import numpy as np
from scipy.stats import norm
import multiprocessing

quantile = 0.75


def generate_data_chunk(chunk_size, n):
    data_chunk = np.random.normal(size=(chunk_size, n))
    return np.percentile(data_chunk, 75, axis=1)


if __name__ == "__main__":
    n = 101
    chunk_size = 250
    num_processes = 6
    # 10000000
    n_rep = chunk_size * num_processes * 10000
    medians = []

    with multiprocessing.Pool(processes=num_processes) as pool:
        data_chunk_list = pool.starmap(generate_data_chunk, [(chunk_size, n)] * (n_rep // chunk_size))

    medians = np.concatenate(data_chunk_list)
    median_sd = np.var(medians)

    print(median_sd)
    print(abs((1 / (4 * (n) * norm.pdf(norm.ppf(quantile)) ** 2))))
    print(abs((1 / (4 * (n + 2) * norm.pdf(norm.ppf(quantile)) ** 2))))
    print(abs((1 / (4 * (n) * norm.pdf(norm.ppf(quantile)) ** 2)) - median_sd))
    print(abs((1 / (4 * (n + 2) * norm.pdf(norm.ppf(quantile)) ** 2)) - median_sd))

# # result is
# # 0.015486708764160906
# # 0.015552438879157393
# # 0.015250449774707735
# # 6.573011499648625e-05
# # 0.00023625898945317178

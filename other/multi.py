# import time
# import numpy as np
# import multiprocessing


# def generate_data_chunk(chunk_size, n):
#     data_chunk = np.random.normal(size=(chunk_size, n))
#     return np.median(data_chunk, axis=1)


# def generate_and_process_data_chunk(chunk_size, n, num_chunks):
#     data_chunk_list = []
#     with multiprocessing.Pool() as pool:
#         data_chunk_list = pool.starmap(generate_data_chunk, [(chunk_size, n)] * num_chunks)
#     return data_chunk_list


# if __name__ == "__main__":
#     n = 75
#     n_rep = 50000 * 6 * 10
#     num_processes = 6

#     chunk_sizes_to_test = [200, 250, 300, 350, 400]  # Test different chunk sizes

#     for chunk_size in chunk_sizes_to_test:
#         num_chunks = n_rep // chunk_size
#         start_time = time.time()
#         data_chunk_list = generate_and_process_data_chunk(chunk_size, n, num_chunks)
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         print(f"Chunk Size: {chunk_size}, Time Taken: {elapsed_time:.2f} seconds")

import numpy as np
from scipy.stats import norm
import multiprocessing


def generate_data_chunk(chunk_size, n):
    data_chunk = np.random.normal(size=(chunk_size, n))
    return np.median(data_chunk, axis=1)


if __name__ == "__main__":
    n = 75
    n_rep = 250 * 6 * 10000000
    chunk_size = 250
    num_processes = 6
    medians = []

    with multiprocessing.Pool(processes=num_processes) as pool:
        data_chunk_list = pool.starmap(generate_data_chunk, [(chunk_size, n)] * (n_rep // chunk_size))

    data_chunk_array = np.concatenate(data_chunk_list)
    median_sd = np.var(data_chunk_array)

    print(median_sd)
    print(abs((1 / (4 * (n) * norm.pdf(0) ** 2))))
    print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2))))
    print(abs((1 / (4 * (n) * norm.pdf(0) ** 2)) - median_sd))
    print(abs((1 / (4 * (n + 2) * norm.pdf(0) ** 2)) - median_sd))

# # result is
# # 0.015486708764160906
# # 0.015552438879157393
# # 0.015250449774707735
# # 6.573011499648625e-05
# # 0.00023625898945317178

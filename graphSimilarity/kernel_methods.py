from math import exp


def rbf_kernel(item1, item2, dist_func, sigma = 0.1):
    'Radial basis function - Gaussian Kernel'

    distance = dist_func(item1, item2)
    kernel = rbf(distance, sigma)

    return kernel

def rbf(distance, sigma = 0.1):
    'Radial basis function with pre-computed distance'

    square_dist = distance ** 2
    gaussian_sim = exp(-(square_dist / 2 * sigma ** 2))

    return gaussian_sim


def dc_kernel(item1, item2, dist_func):
    'Distance to similarity conversion proposed by DeltaCon'

    distance = dist_func(item1, item2)
    kernel = 1 / (1 + distance)

    return kernel

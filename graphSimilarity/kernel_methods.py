from math import exp


def rbf_kernel(item1, item2, dist_func, sigma = 0.1):

    distance = dist_func(item1, item2)
    square_dist = distance ** 2
    kernel = exp(-(square_dist / 2 * sigma ** 2))

    return kernel

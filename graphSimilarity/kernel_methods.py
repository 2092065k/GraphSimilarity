from math import exp
from graph import Graph

def rbf_kernel(g1, g2, dist_func, sigma = 0.1):

    distance = dist_func(g1, g2)
    square_dist = distance ** 2
    kernel = exp(-(square_dist / 2 * sigma ** 2))

    return kernel

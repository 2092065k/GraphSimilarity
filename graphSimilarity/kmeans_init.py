import random
import numpy as np


def __dist_from_centroid(graphs, centroid_indices, dist_func):

    distances = []

    for graph in graphs:

        distances.append(min([dist_func(graph, graphs[centroid_index]) for centroid_index in centroid_indices]))

    return np.array(distances)


def __choose_next_centroid(distances):

    probs = distances / distances.sum()
    cumprobs = probs.cumsum()
    rand = np.random.random()
    ind = np.where(cumprobs >= rand)[0][0]
    return ind


def kmeans_pp(k, seed, graphs, dist_func):

    random.seed(seed)
    np.random.seed(seed)

    centroid_indices = random.sample(range(len(graphs)), 1)

    while len(centroid_indices) < k:

        distances = __dist_from_centroid(graphs, centroid_indices, dist_func)
        next_centroid_index = __choose_next_centroid(distances)
        centroid_indices.append(next_centroid_index)

    return centroid_indices


def get_random_centroids(k, seed, graphs):

    random.seed(seed)
    return random.sample(range(len(graphs)), k)

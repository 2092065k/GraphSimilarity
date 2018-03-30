import random

import numpy as np


def __dist_from_centroid(items, centroid_indices, dist_func):
    'Return the distance from each item to its closest centroid'

    distances = []

    for item in items:

        distances.append(min([dist_func(item, items[centroid_index]) for centroid_index in centroid_indices]))

    return np.array(distances)


def __choose_next_centroid(distances):
    'Retrun the index of the next item to become a centroid'

    probs = distances / distances.sum()
    cumprobs = probs.cumsum()
    rand = np.random.random()
    ind = np.where(cumprobs >= rand)[0][0]
    return ind


def kmeans_pp(k, seed, items, dist_func):
    'Run K-Means++ to obtain the indices of k initial centroids'

    random.seed(seed)
    np.random.seed(seed)

    centroid_indices = random.sample(range(len(items)), 1)

    while len(centroid_indices) < k:

        distances = __dist_from_centroid(items, centroid_indices, dist_func)
        next_centroid_index = __choose_next_centroid(distances)
        centroid_indices.append(next_centroid_index)

    return centroid_indices


def get_random_centroids(k, seed, items):
    'Return the indices of k random items to be used as initial centroids'

    random.seed(seed)
    return random.sample(range(len(items)), k)

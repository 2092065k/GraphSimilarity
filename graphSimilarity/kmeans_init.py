import random
import numpy as np


def __dist_from_centroid(items, centroid_indices, dist_func):

    distances = []

    for item in items:

        distances.append(min([dist_func(item, items[centroid_index]) for centroid_index in centroid_indices]))

    return np.array(distances)


def __choose_next_centroid(distances):

    probs = distances / distances.sum()
    cumprobs = probs.cumsum()
    rand = np.random.random()
    ind = np.where(cumprobs >= rand)[0][0]
    return ind


# def __choose_next_centroid(distances):

#     probs = distances / distances.sum()
#     cumprobs = probs.cumsum()

#     max_prob = max(probs)
#     average_prob = 1.0 / len(distances)
#     likely_prob = (max_prob + average_prob) / 2.0
#     likely_choice = False

#     while not likely_choice:
#         rand = np.random.random()
#         ind = np.where(cumprobs >= rand)[0][0]

#         if probs[ind] >= likely_prob:
#             likely_choice = True

#     return ind


def kmeans_pp(k, seed, items, dist_func):

    random.seed(seed)
    np.random.seed(seed)

    centroid_indices = random.sample(range(len(items)), 1)

    while len(centroid_indices) < k:

        distances = __dist_from_centroid(items, centroid_indices, dist_func)
        next_centroid_index = __choose_next_centroid(distances)
        centroid_indices.append(next_centroid_index)

    return centroid_indices


def get_random_centroids(k, seed, items):

    random.seed(seed)
    return random.sample(range(len(items)), k)

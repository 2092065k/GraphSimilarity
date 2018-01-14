import numpy as np
from kmeans_init import get_random_centroids, kmeans_pp


def __get_distance_matrix(items, dist_func):

    distance_matrix = np.zeros((len(items), len(items)))

    j = 0
    for i in range(len(items)):

        while j < len(items):

            distance = dist_func(items[i], items[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

            j += 1

        j = i + 1

    return distance_matrix


def __compute_cluster_assignment(centroid_indices, items, distance_matrix):

    labels = {}

    for centroid_index in centroid_indices:
        labels[centroid_index] = []

    for item_index in range(len(items)):
        
        min_distance = float("inf")
        closest_centroid = -1

        for centroid_index in centroid_indices:

            dist = distance_matrix[centroid_index, item_index]

            if dist < min_distance:
                min_distance = dist
                closest_centroid = centroid_index

        labels[closest_centroid].append(item_index)

    return labels


def __compute_new_cluster_centroids(labels, items, distance_matrix):

    new_centroid_indices = []

    for old_centroid_index in labels:

        cluster = labels[old_centroid_index]

        min_average_dist = float("inf")
        new_centroid = -1

        for item_index in cluster:

            distance = 0
            for i_i in cluster:
                distance += distance_matrix[item_index, i_i]
            
            average_dist = distance / len(cluster)

            if average_dist < min_average_dist:
                min_average_dist = average_dist
                new_centroid = item_index

        new_centroid_indices.append(new_centroid)

    return new_centroid_indices


def sd_kmeans(k, max_iters, seed, items, dist_func, init = "random"):

    num_iters = 0
    converged = False

    distance_matrix = __get_distance_matrix(items, dist_func)

    # select k distinct items as the cluster centers
    if init == "random":
        centroid_indices = get_random_centroids(k, seed, items)
    else:
        centroid_indices = kmeans_pp(k, seed, items, dist_func)

    while not converged:

        labels = __compute_cluster_assignment(centroid_indices, items, distance_matrix)

        new_centroid_indices = __compute_new_cluster_centroids(labels, items, distance_matrix)

        num_iters += 1

        if new_centroid_indices == centroid_indices or num_iters >= max_iters:
            converged = True
        else:
            centroid_indices = new_centroid_indices

    return centroid_indices


def get_sd_labels(centroid_indices, items, dist_func):

    labels = []

    for item in items:
        
        min_distance = float("inf")
        label = -1

        for index in range(len(centroid_indices)):

            dist = dist_func(items[centroid_indices[index]], item)

            if dist < min_distance:
                min_distance = dist
                label = index

        labels.append(label)

    return labels


def get_sd_wcss(centroid_indices, items, dist_func):

    wcss = 0
    labels = get_sd_labels(centroid_indices, items, dist_func)

    for item_index in range(len(labels)):
        centroid_index = centroid_indices[labels[item_index]]
        squared_dist = dist_func(items[item_index], items[centroid_index])  ** 2
        wcss += squared_dist

    return wcss

import numpy as np
from graph import Graph


def __get_distance_matrix(graphs, dist_func):

    distance_matrix = np.zeros((len(graphs), len(graphs)))

    j = 0
    for i in range(len(graphs)):

        while j < len(graphs):

            distance = dist_func(graphs[i], graphs[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

            j += 1

        j = i + 1

    return distance_matrix


def __compute_cluster_assignment(centroid_indices, graphs, distance_matrix):

    labels = {}

    for centroid_index in centroid_indices:
        labels[centroid_index] = []

    for graph_index in range(len(graphs)):
        
        min_distance = float("inf")
        closest_centroid = -1

        for centroid_index in centroid_indices:

            dist = distance_matrix[centroid_index, graph_index]

            if dist < min_distance:
                min_distance = dist
                closest_centroid = centroid_index

        labels[closest_centroid].append(graph_index)

    return labels


def __compute_new_cluster_centroids(labels, graphs, distance_matrix):

    new_centroid_indices = []

    for old_centroid_index in labels:

        cluster = labels[old_centroid_index]

        min_average_dist = float("inf")
        new_centroid = -1

        for graph_index in cluster:

            distance = 0
            for gi in cluster:
                distance += distance_matrix[graph_index, gi]
            average_dist = distance / len(cluster)

            if average_dist < min_average_dist:
                min_average_dist = average_dist
                new_centroid = graph_index

        new_centroid_indices.append(new_centroid)

    return new_centroid_indices


def __get_random_centroids(k, seed, graphs):

    np.random.seed(seed)
    unique_random_indices = set()
    while len(unique_random_indices) < k:
        unique_random_indices.add(np.random.randint(0, len(graphs)))

    return list(unique_random_indices)


def sd_kmeans(k, max_iters, seed, graphs, dist_func):

    num_iters = 0
    converged = False

    distance_matrix = __get_distance_matrix(graphs, dist_func)

    # select k distinct graphs as the cluster centers
    centroid_indices = __get_random_centroids(k, seed, graphs)

    while not converged:

        labels = __compute_cluster_assignment(centroid_indices, graphs, distance_matrix)

        new_centroid_indices = __compute_new_cluster_centroids(labels, graphs, distance_matrix)

        num_iters += 1

        if new_centroid_indices == centroid_indices or num_iters >= max_iters:
            converged = True
        else:
            centroid_indices = new_centroid_indices

    return centroid_indices


def get_sd_wcss(centroid_indices, graphs, dist_func):

    wcss = 0
    labels = __compute_cluster_assignment(centroid_indices, graphs, dist_func)

    for centoid_index in labels:
        for graph_index in labels[centoid_index]:
            
            squared_dist = dist_func(graphs[graph_index], graphs[centoid_index]) ** 2
            wcss += squared_dist

    return wcss

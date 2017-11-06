import numpy as np
from graph import Graph
from graph_edit_distance import graph_edit_distance

def __compute_cluster_assignment(centroid_indices, graphs, dist_func):

    labels = {}

    for centroid_index in centroid_indices:
        labels[centroid_index] = []

    for graph_index in range(len(graphs)):
        
        min_distance = float("inf")
        closest_centroid = -1

        for centroid_index in centroid_indices:

            dist = dist_func(graphs[centroid_index], graphs[graph_index])

            if dist < min_distance:
                min_distance = dist
                closest_centroid = centroid_index

        labels[closest_centroid].append(graph_index)

    return labels

def __compute_new_cluster_centroids(labels, graphs, dist_func):

    new_centroid_indices = []

    for old_centroid_index in labels:

        cluster = labels[old_centroid_index]

        min_average_dist = float("inf")
        new_centroid = -1

        for graph_index in cluster:

            distance = 0
            for gi in cluster:
                distance += dist_func(graphs[graph_index], graphs[gi])
            average_dist = distance / len(cluster)

            if average_dist < min_average_dist:
                min_average_dist = average_dist
                new_centroid = graph_index

        new_centroid_indices.append(new_centroid)

    return new_centroid_indices




def sd_kmeans(k, max_iters, seed, graphs, dist_func):

    np.random.seed(seed)
    num_iters = 0

    # select k distinct graphs as the cluster centers
    unique_random_indices = set()
    while len(unique_random_indices) < k:
        unique_random_indices.add(np.random.randint(0, len(graphs)))

    centroid_indices = list(unique_random_indices)

    converged = False

    while not converged:

        labels = __compute_cluster_assignment(centroid_indices, graphs, dist_func)

        new_centroid_indices = __compute_new_cluster_centroids(labels, graphs, dist_func)

        num_iters += 1

        if new_centroid_indices == centroid_indices or num_iters >= max_iters:
            converged = True
        else:
            centroid_indices = new_centroid_indices

    return centroid_indices

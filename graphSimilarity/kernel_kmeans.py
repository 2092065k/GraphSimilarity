import numpy as np
from copy import deepcopy
from kmeans_init import get_random_centroids, kmeans_pp


def __get_kernel_matrix(graphs, dist_func, kernel):

    kernel_matrix = np.zeros((len(graphs), len(graphs)))

    j = 0
    for i in range(len(graphs)):

        while j < len(graphs):

            kernel_res = kernel(graphs[i], graphs[j], dist_func)
            kernel_matrix[i, j] = kernel_res
            kernel_matrix[j, i] = kernel_res

            j += 1

        j = i + 1

    return kernel_matrix


def __get_graph_indices_per_cluster(k, labels):

    indices_per_cluster = [[] for x in range(k)]
    for i in range(len(labels)):
        indices_per_cluster[labels[i]].append(i)

    return indices_per_cluster


def __distance_to_centroid(graph_index, centroid_index, graph_indices_per_cluster, kernel_matrix):

    graph_indices_in_cluster = graph_indices_per_cluster[centroid_index]
    num_graphs_in_cluster = len(graph_indices_in_cluster)

    param1 = kernel_matrix[graph_index, graph_index]
    param2 = 0
    param3 = 0

    # check in case there are no graphs assigned to the cluster
    if num_graphs_in_cluster != 0:

        kernel_sum = 0
        for i in graph_indices_in_cluster:
            kernel_sum += kernel_matrix[graph_index, i]

        param2 = (-2 * kernel_sum) / num_graphs_in_cluster

        kernel_sum = 0
        for i in graph_indices_in_cluster:
            for j in graph_indices_in_cluster:
                kernel_sum += kernel_matrix[i, j]

        param3 = kernel_sum / (num_graphs_in_cluster ** 2)

    distance = param1 + param2 + param3

    return distance


def __random_cluster_assignment(k, seed, graphs):

    np.random.seed(seed)
    labels = [np.random.randint(0, k) for x in range(len(graphs))]
    return labels


def __proximity_cluster_assignment(k, seed, graphs, dist_func, init):

    if init == "proxy":
        centroid_indices = get_random_centroids(k, seed, graphs)
    else:
        centroid_indices = kmeans_pp(k, seed, graphs, dist_func)

    labels = []

    for graph in graphs:

        min_distance = float("inf")
        closest_centroid = -1

        for label in range(len(centroid_indices)):

            dist = dist_func(graph, graphs[centroid_indices[label]])

            if dist < min_distance:
                min_distance = dist
                closest_centroid = label

        labels.append(closest_centroid)

    return labels


def kernel_kmeans(k, max_iters, seed, graphs, dist_func, kernel, init = "random"):

    num_iters = 0
    converged = False

    # compute kernel matrix
    kernel_matrix = __get_kernel_matrix(graphs, dist_func, kernel)

    # initial assignment of cluster membership
    if init == "random":
        labels = __random_cluster_assignment(k, seed, graphs)
    else:
        labels = __proximity_cluster_assignment(k, seed, graphs, dist_func, init)

    while not converged:

        graph_indices_per_cluster = __get_graph_indices_per_cluster(k, labels)
        old_labels = deepcopy(labels)

        for graph_index in range(len(graphs)):

            min_distance = float("inf")
            closest_centroid = -1

            # find the nearest cluster centoid
            for centroid_index in range(k):

                dist = __distance_to_centroid(graph_index, centroid_index, graph_indices_per_cluster, kernel_matrix)
                if dist < min_distance:
                    min_distance = dist
                    closest_centroid = centroid_index

            # update the label of the graph
            labels[graph_index] = closest_centroid

            # TODO: compute update more efficiently
            graph_indices_per_cluster = __get_graph_indices_per_cluster(k, labels)

        num_iters += 1

        if labels == old_labels or num_iters >= max_iters:
            converged = True

    return labels


def get_kernel_wcss(k, graphs, labels, dist_func, kernel):

    wcss = 0
    kernel_matrix = __get_kernel_matrix(graphs, dist_func, kernel)
    graph_indices_per_cluster = __get_graph_indices_per_cluster(k, labels)

    for i in range(len(graphs)):
        squared_dist = __distance_to_centroid(i, labels[i], graph_indices_per_cluster, kernel_matrix)
        wcss += squared_dist

    return wcss

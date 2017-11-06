import numpy as np
from copy import deepcopy
from graph import Graph
from kernel_methods import rbf_kernel
from graph_edit_distance import graph_edit_distance


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


def __distance_to_centroid(graph_index, centroid_index, graph_indices_per_cluster, graphs, kernel_matrix):

    # this will include the current graph if we are inspecting its curren centroid
    graph_indices_in_cluster = graph_indices_per_cluster[centroid_index]
    num_graphs_in_cluster = len(graph_indices_in_cluster)

    param1 = kernel_matrix[graph_index, graph_index]

    # check in case there are no graphs assigned to the cluster
    if num_graphs_in_cluster != 0:

        kernel_sum = 0
        for i in graph_indices_in_cluster:
            kernel_sum += kernel_matrix[graph_index, i]


        param2 = kernel_sum / (-2 * num_graphs_in_cluster)

        kernel_sum = 0
        for i in graph_indices_in_cluster:
            for j in graph_indices_in_cluster:
                kernel_sum += kernel_matrix[i, j]

        param3 = kernel_sum / (num_graphs_in_cluster ** 2)

    else:
        param2 = 0
        param3 = 0

    distance = param1 + param2 + param3

    return distance


def kernel_kmeans(k, max_iters, seed, graphs, dist_func, kernel):

    np.random.seed(seed)
    num_iters = 0

    # compute kernel matrix
    kernel_matrix = __get_kernel_matrix(graphs, dist_func, kernel)

    # initial random assignment of cluster membership
    labels = [np.random.randint(0, k) for x in range(len(graphs))]

    converged = False

    while not converged:

        graph_indices_per_cluster = __get_graph_indices_per_cluster(k, labels)
        old_labels = deepcopy(labels)

        for graph_index in range(len(graphs)):

            min_distance = float("inf")
            closest_centroid = -1

            # find the nearest cluster centoid
            for centroid_index in range(k):

                dist = __distance_to_centroid(graph_index, centroid_index, graph_indices_per_cluster, graphs, kernel_matrix)
                if dist < min_distance:
                    min_distance = dist
                    closest_centroid = centroid_index

            # update the label of the graph
            labels[graph_index] = closest_centroid

        num_iters += 1

        if labels == old_labels or num_iters >= max_iters:
            converged = True

    return labels

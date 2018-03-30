import numpy as np

from copy import deepcopy
from kmeans_init import get_random_centroids, kmeans_pp


def __get_item_indices_per_cluster(k, labels):
    'Get a 2-D array where the array at position i holds the indices of all items in cluster i'

    indices_per_cluster = [[] for x in range(k)]
    for i in range(len(labels)):
        indices_per_cluster[labels[i]].append(i)

    return indices_per_cluster


def __distance_to_centroid(item_index, centroid_index, item_indices_per_cluster, kernel_matrix):
    'Compute the distance between a given item and centroid in the projected space'

    item_indices_in_cluster = item_indices_per_cluster[centroid_index]
    num_items_in_cluster = len(item_indices_in_cluster)

    param1 = kernel_matrix[item_index, item_index]
    param2 = 0
    param3 = 0

    # check in case there are no items assigned to the cluster
    if num_items_in_cluster != 0:

        kernel_sum = 0
        for i in item_indices_in_cluster:
            kernel_sum += kernel_matrix[item_index, i]

        param2 = (-2 * kernel_sum) / num_items_in_cluster

        kernel_sum = 0
        for i in item_indices_in_cluster:
            for j in item_indices_in_cluster:
                kernel_sum += kernel_matrix[i, j]

        param3 = kernel_sum / (num_items_in_cluster ** 2)

    distance = param1 + param2 + param3

    return distance


def __random_cluster_assignment(k, seed, items):
    'Assign random cluster labels to each element'

    np.random.seed(seed)
    labels = [np.random.randint(0, k) for x in range(len(items))]
    return labels


def __proximity_cluster_assignment(k, seed, items, dist_func, init):
    'Choose K centroid items and assign labels to all items based on their proximity to the centroids'

    if init == "proxy":
        centroid_indices = get_random_centroids(k, seed, items)
    else:
        centroid_indices = kmeans_pp(k, seed, items, dist_func)

    labels = []

    for item in items:

        min_distance = float("inf")
        closest_centroid = -1

        for label in range(len(centroid_indices)):

            dist = dist_func(item, items[centroid_indices[label]])

            if dist < min_distance:
                min_distance = dist
                closest_centroid = label

        labels.append(closest_centroid)

    return labels


def get_kernel_matrix(items, dist_func, kernel, **kernel_args):
    'Compute the NxN matrix of kernel values for all pairs of items'

    kernel_matrix = np.zeros((len(items), len(items)))

    j = 0
    for i in range(len(items)):

        while j < len(items):

            kernel_res = kernel(items[i], items[j], dist_func, **kernel_args)
            kernel_matrix[i, j] = kernel_res
            kernel_matrix[j, i] = kernel_res

            j += 1

        j = i + 1

    return kernel_matrix


def kernel_kmeans(k, max_iters, seed, items, dist_func, kernel, init = "random", kernel_matrix = None, **kernel_args):
    '''Run Kernel K-Means - returns

    Parameters
    ----------
    k: int
        the number of clusters

    max_iters: int
        the number of maximum allowed itterations before the method terminates
        (termination will occure earlier if the cluster labels converge)

    seed: int
        a seed paramether for controlling randomness

    items: 1-D list
        the list of structured data items thet will be clustered

    dist_func: function pointer
        a function for computing the distance between any two items in the items list

    kernel: function pointer
        a kernel function

    init: string
        a string indicating the cluster label initialization method

    kernel_matrix: 2-D numpy array
        an optional pre-computed NxN kernal matrix

    The possible initialization methods are: 'random', 'proxy' and 'kpp':
        random - provide a random cluster label to each item
        proxy  - randomly choose representative items and assign labels based on proximity to representatives
        kpp    - similar to 'proxy' except the representatives are chosen using k-means++

    **kernel_args: optional kernel arguments
        any further parameters are passed directly to the kernel function

    Return
    ------
    labels: 1-D list of ints
        a list of cluster assignment labels
    '''

    num_iters = 0
    converged = False

    # compute the kernel matrix if one is not provided
    if kernel_matrix is None:
        kernel_matrix = get_kernel_matrix(items, dist_func, kernel, **kernel_args)

    # initial assignment of cluster membership
    if init == "random":
        labels = __random_cluster_assignment(k, seed, items)
    else:
        labels = __proximity_cluster_assignment(k, seed, items, dist_func, init)

    item_indices_per_cluster = __get_item_indices_per_cluster(k, labels)

    while not converged:

        old_labels = deepcopy(labels)

        for item_index in range(len(items)):

            old_label = labels[item_index]
            min_distance = float("inf")
            closest_centroid = -1

            # find the nearest cluster centoid
            for centroid_index in range(k):

                dist = __distance_to_centroid(item_index, centroid_index, item_indices_per_cluster, kernel_matrix)
                if dist < min_distance:
                    min_distance = dist
                    closest_centroid = centroid_index

            # update the label of the item
            labels[item_index] = closest_centroid

            # update the item's cluster assignment
            if old_label != closest_centroid:
                item_indices_per_cluster[old_label].remove(item_index)
                item_indices_per_cluster[closest_centroid].append(item_index)


        num_iters += 1

        if labels == old_labels or num_iters >= max_iters:
            converged = True

    return labels


def get_kernel_wcss(k, items, labels, dist_func, kernel, kernel_matrix = None, **kernel_args):
    'Compute the within-cluster sum of squares value for a given label assignment'

    wcss = 0

    if kernel_matrix is None:
        kernel_matrix = get_kernel_matrix(items, dist_func, kernel, **kernel_args)

    item_indices_per_cluster = __get_item_indices_per_cluster(k, labels)

    for i in range(len(items)):
        squared_dist = __distance_to_centroid(i, labels[i], item_indices_per_cluster, kernel_matrix)
        wcss += squared_dist

    return wcss

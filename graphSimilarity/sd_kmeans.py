import numpy as np

from kmeans_init import get_random_centroids, kmeans_pp


def __compute_cluster_assignment(centroid_indices, items, distance_matrix):
    'Get a dictionary with cluster ids as keys and arrays of assinged item indices as values'

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
    'The new centroids are the items with minimum average distance to all other items in their cluster'

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


def get_distance_matrix(items, dist_func):
    'Compute the NxN matrix of distances between all pairs of items'

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


def sd_kmeans(k, max_iters, seed, items, dist_func, init = "random", distance_matrix = None):
    """Run Structured Data K-Means

    Parameters
    ----------
    k: int
        the number of clusters

    max_iters: int
        the number of maximum allowed itterations before the method terminates
        (termination will occure earlier if the chosen centroids converge)

    seed: int
        a seed paramether for controlling randomness

    items: 1-D list
        the list of structured data items thet will be clustered

    dist_func: function pointer
        a function for computing the distance between any two items in the items list

    init: string
        a string indicating the centroid initialization method

    distance_matrix: 2-D numpy array
        an optional pre-computed NxN matrix of distance values between all pairs of items

    The possible initialization methods are: 'random' and 'kpp':
        random - randomly choose centroids amongst the input items
        kpp    - use k-means++ to choose centroids amongst the input items

    Return
    ------
    labels: 1-D list of ints
        the indices of the input items which best approximate the centroids
    """

    num_iters = 0
    converged = False

    # compute the distance matrix if one is not provided
    if distance_matrix is None:
        distance_matrix = get_distance_matrix(items, dist_func)

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


def get_sd_labels(centroid_indices, items, dist_func, distance_matrix = None):
    'Compute the assigned cluster label for each item given the indices of the approximate centroids'

    labels = []

    for item_index in range(len(items)):
        
        min_distance = float("inf")
        label = -1

        # the distance matrix is not computed here as n*n >> n*k
        for index in range(len(centroid_indices)):

            # compute or look up the distance
            if distance_matrix is None:
                dist = dist_func(items[centroid_indices[index]], items[item_index])
            else:
                dist = distance_matrix[centroid_indices[index], item_index]

            if dist < min_distance:
                min_distance = dist
                label = index

        labels.append(label)

    return labels


def get_sd_wcss(centroid_indices, items, dist_func, distance_matrix = None):
    'Compute the within-cluster sum of squares value for a set of approximate centroids'

    wcss = 0
    labels = get_sd_labels(centroid_indices, items, dist_func, distance_matrix)

    for item_index in range(len(labels)):
        centroid_index = centroid_indices[labels[item_index]]

        # compute or look up the distance
        if distance_matrix is None:
            dist = dist_func(items[item_index], items[centroid_index])
        else:
            dist = distance_matrix[item_index, centroid_index]

        wcss += (dist ** 2)

    return wcss

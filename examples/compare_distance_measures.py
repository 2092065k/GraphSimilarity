import sys
import operator

from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_wcss, get_kernel_matrix
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_wcss, get_sd_labels, get_distance_matrix

from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score


def compare_distance_measures(file, cluster_method, cluster_params, cluster_restarts, rolx_params = {}, deep_walk_params = {}, node_weight_algs = False):
    """This method compares all available graph distance measures according
       to silhouette score, using a provided clustring algorithm
    """

    # load graphs from the input data file
    graphs = load_data(file)

    # compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
    for graph in graphs:
        graph.compute_adjacency_matrix()
        graph.compute_diagonal_matrix()

    silhouette_values = {}

    # only eavluate algorithms that do not consider node weights
    if not node_weight_algs: 

        print "Calculating Graph Edit Distance Sillhouette"
        ged_distance_matrix = get_distance_matrix(graphs, graph_edit_distance)
        ged_kernel_matrix = get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)
        silhouette_values["Graph Edit Distance"] = compute_silhouette(graphs, graph_edit_distance,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = ged_distance_matrix, kernel_matrix = ged_kernel_matrix)

        print "Calculating DeltaCon Sillhouette"
        fabp_matrices = [fabp(graph) for graph in graphs]
        dc_distance_matrix = get_distance_matrix(fabp_matrices, root_ed)
        dc_kernel_matrix = get_kernel_matrix(fabp_matrices, root_ed, rbf_kernel)
        silhouette_values["DeltaCon"] = compute_silhouette(fabp_matrices, root_ed,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = dc_distance_matrix, kernel_matrix = dc_kernel_matrix)

        print "Calculating SimRank Sillhouette"
        sim_rank_matrices = [sim_rank(graph) for graph in graphs]
        sr_distance_matrix = get_distance_matrix(sim_rank_matrices, matrix_ed)
        sr_kernel_matrix = get_kernel_matrix(sim_rank_matrices, matrix_ed, rbf_kernel)
        silhouette_values["SimRank"] = compute_silhouette(sim_rank_matrices, matrix_ed,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = sr_distance_matrix, kernel_matrix = sr_kernel_matrix)

        print "Calculating In/Out Node Degree Sillhouette"
        degree_matrices = [node_degree_matrix(graph) for graph in graphs]
        deg_distance_matrix = get_distance_matrix(degree_matrices, matrix_ed)
        deg_kernel_matrix = get_kernel_matrix(degree_matrices, matrix_ed, rbf_kernel)
        silhouette_values["Degree In/Out"] = compute_silhouette(degree_matrices, matrix_ed,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = deg_distance_matrix, kernel_matrix = deg_kernel_matrix)

        if len(rolx_params) > 0:

            print "Calculating RolX Sillhouette"
            rolx_matrices = get_rolx_matrices(graphs, **rolx_params)
            rolx_distance_matrix = get_distance_matrix(rolx_matrices, matrix_cd)
            rolx_kernel_matrix = get_kernel_matrix(rolx_matrices, matrix_cd, rbf_kernel)
            silhouette_values["RolX"] = compute_silhouette(rolx_matrices, matrix_cd,
                cluster_method, cluster_params, cluster_restarts, distance_matrix = rolx_distance_matrix, kernel_matrix = rolx_kernel_matrix)

        if len(deep_walk_params) > 0:

            print "Calculating DeepWalk Sillhouette"
            dw_matrices = get_deep_walk_matrices(graphs, **deep_walk_params)
            dw_distance_matrix = get_distance_matrix(dw_matrices, matrix_cd)
            dw_kernel_matrix = get_kernel_matrix(dw_matrices, matrix_cd, rbf_kernel)
            silhouette_values["DeepWalk"] = compute_silhouette(dw_matrices, matrix_cd,
                cluster_method, cluster_params, cluster_restarts, distance_matrix = dw_distance_matrix, kernel_matrix = dw_kernel_matrix)

    # only eavluate algorithms that do consider node weights
    else:

        print "Calculating Graph Edit Distance with Node Weights Sillhouette"
        ged_nw_distance_matrix = get_distance_matrix(graphs, graph_edit_distance_nw)
        ged_nw_kernel_matrix = get_kernel_matrix(graphs, graph_edit_distance_nw, rbf_kernel)
        silhouette_values["Graph Edit Distance With Node Weights"] = compute_silhouette(graphs, graph_edit_distance_nw,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = ged_nw_distance_matrix, kernel_matrix = ged_nw_kernel_matrix)

        print "Calculating DeltaCon with Node Weights Sillhouette"
        norm = get_largest_node_weight(graphs)
        fabp_nw_matrices = [fabp_nw(graph, norm) for graph in graphs]
        dc_nw_distance_matrix = get_distance_matrix(fabp_nw_matrices, root_ed)
        dc_nw_kernel_matrix = get_kernel_matrix(fabp_nw_matrices, root_ed, rbf_kernel)
        silhouette_values["DeltaCon With Node Weights"] = compute_silhouette(fabp_nw_matrices, root_ed,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = dc_nw_distance_matrix, kernel_matrix = dc_nw_kernel_matrix)

        print "Calculating In/Out Node Degree with Node Weights Sillhouette"
        degree_matrices_nw = [node_degree_weight_matrix(graph) for graph in graphs]
        deg_nw_distance_matrix = get_distance_matrix(degree_matrices_nw, matrix_ed)
        deg_nw_kernel_matrix = get_kernel_matrix(degree_matrices_nw, matrix_ed, rbf_kernel)
        silhouette_values["Degree In/Out With Node Weights"] = compute_silhouette(degree_matrices_nw, matrix_ed,
            cluster_method, cluster_params, cluster_restarts, distance_matrix = deg_nw_distance_matrix, kernel_matrix = deg_nw_kernel_matrix)

    # sort the sillhouette values in descending order
    sorted_silhouette_values = sorted(silhouette_values.items(), key=operator.itemgetter(1), reverse = True)

    return sorted_silhouette_values


def compute_silhouette(items, dist_func, cluster_method, cluster_params, cluster_restarts, distance_matrix = None, kernel_matrix = None):
    'Compute the silhouette score for the labels returned from the chosen clustering method + graph distance metric'

    # the cluster assignment labels for each item
    labels = []

    # use structured data k-means to obtain cluster labels for sillhouette
    if cluster_method == "sd_kmeans":

        best_wcss = float("inf")
        best_centroids = []

        for run in range(cluster_restarts):

            centroids = sd_kmeans(seed = run, items = items, dist_func = dist_func, distance_matrix = distance_matrix, **cluster_params)
            wcss = get_sd_wcss(centroids, items, dist_func, distance_matrix = distance_matrix)

            if wcss < best_wcss:

                best_wcss = wcss
                best_centroids = centroids

        labels = get_sd_labels(best_centroids, items, dist_func, distance_matrix = distance_matrix)

    # use kernel k-means to obtain cluster labels for sillhouette
    elif cluster_method == "kernel_kmeans":

        best_wcss = float("inf")
        
        for run in range(cluster_restarts):

            current_labels = kernel_kmeans(seed = run, items = items, dist_func = dist_func, kernel_matrix = kernel_matrix, **cluster_params)
            wcss = get_kernel_wcss(k = cluster_params["k"], items = items, labels = current_labels,
                dist_func = dist_func, kernel = cluster_params["kernel"], kernel_matrix = kernel_matrix)

            if wcss < best_wcss:

                best_wcss = wcss
                labels = current_labels

    # use spectral clustering to obtain cluster labels for sillhouette
    else:

        labels = SpectralClustering(n_init=cluster_restarts, affinity='precomputed', **cluster_params).fit(kernel_matrix).labels_


    return silhouette_score(distance_matrix, labels, metric="precomputed")



# example invokation using structured data k-means
silhouette_values = compare_distance_measures(sys.argv[1], "sd_kmeans", {"k": 2, "max_iters": 50, "init": "random"}, 5,
                    rolx_params = {"rolx_path": "/home/aquila/CS/L5P/snap/examples/rolx/testrolx", "num_roles": 3}, 
                    deep_walk_params = {"representation_size" : 64, "number_walks": 10, "walk_length": 40, "undirected": True})

# example invokation using kernel k-means
# silhouette_values = compare_distance_measures(sys.argv[1], "kernel_kmeans", {"k": 2, "max_iters": 50, "init": "random", "kernel": rbf_kernel}, 5,
#                     rolx_params = {"rolx_path": "/home/aquila/CS/L5P/snap/examples/rolx/testrolx", "num_roles": 3}, 
#                     deep_walk_params = {"representation_size" : 64, "number_walks": 10, "walk_length": 40, "undirected": True})

# example invokation using spectral clustering
# silhouette_values = compare_distance_measures(sys.argv[1], "spectral", {"n_clusters": 2}, 5,
#                     rolx_params = {"rolx_path": "/home/aquila/CS/L5P/snap/examples/rolx/testrolx", "num_roles": 3}, 
#                     deep_walk_params = {"representation_size" : 64, "number_walks": 10, "walk_length": 40, "undirected": True})


# print the silhouette score obtained from each distance meausre
for silhouette_value in silhouette_values:
    print silhouette_value

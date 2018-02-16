import sys
import time
import numpy as np

from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.graph_generator import generate_graphs_file
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_wcss, get_kernel_matrix
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_wcss, get_sd_labels, get_distance_matrix
from graphSimilarity.kmeans_init import get_random_centroids, kmeans_pp

from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_samples, silhouette_score



graphs = load_data(sys.argv[1])

for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()

# graphs = load_matrix_data("/home/aquila/CS/L5P/FC/formatConversion3/outDir/data.txt", 21)
# graphs = load_deep_walk_files("/home/aquila/CS/L5P/FC/formatConversion4/outDir", 20)

print "Input data loaded"



distance_matrix = get_distance_matrix(graphs, graph_edit_distance)
print "Distance matrix computed"

kernel_matrix = get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)
print "Kernel matrix computed"



# for k in range(1, 10):
# 	labels = SpectralClustering(n_clusters=k, random_state=1, n_init=1, affinity='precomputed').fit(kernel_matrix).labels_
# 	kernel_wcss = get_kernel_wcss(k, graphs, labels, graph_edit_distance, rbf_kernel, kernel_matrix = kernel_matrix)
# 	print str(k) + " " + str(kernel_wcss)

# 	if k > 1:
# 		print str(k) + " " + str(silhouette_score(distance_matrix, labels, metric="precomputed"))


#---------------------------------------------------------------------------------------------


# for k in range(1, 10):
# 	labels = kernel_kmeans(k, 50, 0, graphs, graph_edit_distance, rbf_kernel, kernel_matrix = kernel_matrix)
# 	kernel_wcss = get_kernel_wcss(k, graphs, labels, graph_edit_distance, rbf_kernel, kernel_matrix = kernel_matrix)
# 	print str(k) + " " + str(kernel_wcss)

# 	if k > 1:
# 		print str(k) + " " + str(silhouette_score(distance_matrix, labels, metric="precomputed"))


#---------------------------------------------------------------------------------------------


# for k in range(1, 10):
# 	centroids = sd_kmeans(k, 50, 0, graphs, graph_edit_distance, distance_matrix = distance_matrix)
# 	sd_wcss = get_sd_wcss(centroids, graphs, graph_edit_distance)
# 	print str(k) + " " + str(sd_wcss)

# 	if k > 1:
# 		labels = get_sd_labels(centroids, graphs, graph_edit_distance)
# 		print str(k) + " " + str(silhouette_score(distance_matrix, labels, metric="precomputed"))


#---------------------------------------------------------------------------------------------

# labels = [x/100 for x in range(400)]
# print silhouette_score(distance_matrix, labels, metric="precomputed")

#---------------------------------------------------------------------------------------------

# draw_matrix_heat_map(distance_matrix)

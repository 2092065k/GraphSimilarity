import sys
import time
import numpy as np

from graphSimilarity.utils import *
from graphSimilarity.graph import Graph
from graphSimilarity.kernel_methods import rbf_kernel
from graphSimilarity.graph_edit_distance import graph_edit_distance
from graphSimilarity.delta_con import delta_con, fabp, root_ed
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_wcss
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_wcss, get_sd_labels
from graphSimilarity.kmeans_init import get_random_centroids, kmeans_pp

from graphSimilarity.kernel_kmeans import __get_kernel_matrix
from sklearn.cluster import SpectralClustering

from graphSimilarity.graph_generator import generate_graphs_file

#graph = Graph(2, [(0, 1)])
#print(graph.get_num_vertices())
#graph.compute_adjacency_matrix()
#print(graph.get_adjacency_matrix())

#graphs = load_data(sys.argv[1])
#for graph in graphs:
#    graph.compute_adjacency_matrix()
#    print graph.get_adjacency_matrix()
#    print 

#---------------------------------------------------------------------------------------------

graphs = load_data(sys.argv[1])

for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()

#---------------------------------------------------------------------------------------------


#print graph_edit_distance(graphs[0], graphs[1])

#print rbf_kernel(graphs[0], graphs[1], graph_edit_distance, 0.1)

#---------------------------------------------------------------------------------------------

# res = []
# for seed in range(1000):
#     res.append(kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel, "random"))

# correct = 0
# wrong = 0

# for items in res:
#     if all(x == items[0] for x in items[:10]) and all(x == items[10] for x in items[10:]) and  not all(x == items[0] for x in items):
#         #print "Correct: " + str(items)
#         correct +=1
#     else:
#         #print "Wrong: " + str(items)
#         wrong +=1

# print "Correct: " + str(correct)
# print "Wrong: " + str(wrong)

#---------------------------------------------------------------------------------------------

# for seed in range(200):
#    print kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel, "random")

#---------------------------------------------------------------------------------------------

# for seed in range(200):
#    print sd_kmeans(2, 50, seed, graphs, delta_con, "random")

#---------------------------------------------------------------------------------------------

# labels = kernel_kmeans(2, 50, 0, graphs, graph_edit_distance, rbf_kernel)
# print labels

# kernel_wcss = get_kernel_wcss(2, graphs, labels, graph_edit_distance, rbf_kernel)
# print kernel_wcss


# centroids = sd_kmeans(2, 50, 0, graphs, graph_edit_distance)
# print centroids

# labels = get_sd_labels(centroids, graphs, graph_edit_distance)
# print labels

# sd_wcss = get_sd_wcss(centroids, graphs, graph_edit_distance)
# print sd_wcss

#---------------------------------------------------------------------------------------------


# labels = kernel_kmeans(2, 50, 0, graphs, graph_edit_distance, rbf_kernel, "proxy")
# print labels

#---------------------------------------------------------------------------------------------

# res = []
# for seed in range(1000):
#     res.append(kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel, "proxy"))

# correct = 0
# wrong = 0

# for items in res:
#     if all(x == items[0] for x in items[:10]) and all(x == items[10] for x in items[10:]) and  not all(x == items[0] for x in items):
#         correct +=1
#     else:
#         wrong +=1

# print "Correct: " + str(correct)
# print "Wrong: " + str(wrong)


#---------------------------------------------------------------------------------------------

# dist = delta_con(graphs[16], graphs[18])
# print dist

#---------------------------------------------------------------------------------------------


# start = time.time()

# for seed in range(200):
#     sd_kmeans(2, 50, seed, graphs, graph_edit_distance)

# end = time.time()
# print end - start


# start = time.time()

# for seed in range(200):
#     sd_kmeans(2, 50, seed, graphs, delta_con)

# end = time.time()
# print end - start


# fabp_graphs = [fabp(g) for g in graphs]

# start = time.time()

# for seed in range(200):
#     sd_kmeans(2, 50, seed, fabp_graphs, root_ed)

# end = time.time()
# print end - start


#---------------------------------------------------------------------------------------------

# start = time.time()

# for seed in range(200):
#     kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel)

# end = time.time()
# print end - start


# start = time.time()

# for seed in range(200):
#     kernel_kmeans(2, 50, seed, graphs, delta_con, rbf_kernel)

# end = time.time()
# print end - start


# fabp_graphs = [fabp(g) for g in graphs]

# start = time.time()

# for seed in range(200):
#     kernel_kmeans(2, 50, seed, fabp_graphs, root_ed, rbf_kernel)

# end = time.time()
# print end - start

#---------------------------------------------------------------------------------------------

# kernel_matrix = __get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)

# spectral_kmeans = SpectralClustering(n_clusters=2, random_state=0, n_init=1, affinity='precomputed').fit(kernel_matrix)

# print spectral_kmeans.labels_

#---------------------------------------------------------------------------------------------

# kernel_matrix = __get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)

# res = []
# for seed in range(1000):
#     spectral_kmeans = SpectralClustering(n_clusters=2, random_state=seed, n_init=1, affinity='precomputed').fit(kernel_matrix)
#     res.append(spectral_kmeans.labels_)

# correct = 0
# wrong = 0

# for items in res:
#     if all(x == items[0] for x in items[:10]) and all(x == items[10] for x in items[10:]) and  not all(x == items[0] for x in items):
#         correct +=1
#     else:
#         wrong +=1

# print "Correct: " + str(correct)
# print "Wrong: " + str(wrong)

#---------------------------------------------------------------------------------------------

# start = time.time()

# kernel_matrix = __get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)

# for seed in range(200):
#     SpectralClustering(n_clusters=2, random_state=seed, n_init=1, affinity='precomputed').fit(kernel_matrix)

# end = time.time()
# print end - start

#---------------------------------------------------------------------------------------------

# generate_graphs_file("test.txt", 4, 10, 0)
# draw_all_graphs("test.txt")

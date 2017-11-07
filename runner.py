import sys
import numpy as np

from graphSimilarity.graph import Graph
from graphSimilarity.data_loader import load_data
from graphSimilarity.kernel_methods import rbf_kernel
from graphSimilarity.graph_edit_distance import graph_edit_distance
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_wcss
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_wcss


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


#---------------------------------------------------------------------------------------------


#print graph_edit_distance(graphs[0], graphs[1])

#print rbf_kernel(graphs[0], graphs[1], graph_edit_distance, 0.1)

#---------------------------------------------------------------------------------------------

# res = []
# for seed in range(1000):
#     res.append(kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel))

# correct = 0
# wrong = 0

# for items in res:
#     if all(x == items[0] for x in items[:10]) and all(x == items[10] for x in items[10:]) and  not all(x == items[0] for x in items):
#         print "Correct: " + str(items)
#         correct +=1
#     else:
#         print "Wrong: " + str(items)
#         wrong +=1

# print "Correct: " + str(correct)
# print "Wrong: " + str(wrong)

#---------------------------------------------------------------------------------------------

#for seed in range(200):
#    print kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel)

#---------------------------------------------------------------------------------------------

labels = kernel_kmeans(2, 50, 0, graphs, graph_edit_distance, rbf_kernel)
print labels

kernel_wcss = get_kernel_wcss(2, graphs, labels, graph_edit_distance, rbf_kernel)
print kernel_wcss


centroids = sd_kmeans(2, 50, 0, graphs, graph_edit_distance)
print centroids

sd_wcss = get_sd_wcss(centroids, graphs, graph_edit_distance)
print sd_wcss

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

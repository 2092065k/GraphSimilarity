import sys
import numpy as np

from graphSimilarity.graph import Graph
from graphSimilarity.data_loader import load_data
from graphSimilarity.kernel_methods import rbf_kernel
from graphSimilarity.graph_edit_distance import graph_edit_distance
from graphSimilarity.kernel_kmeans import kernel_kmeans
from graphSimilarity.sd_kmeans import sd_kmeans


#graph = Graph(2, [(0, 1)])
#print(graph.get_num_vertices())
#graph.compute_adjacency_matrix()
#print(graph.get_adjacency_matrix())

#graphs = load_data(sys.argv[1])
#for graph in graphs:
#    graph.compute_adjacency_matrix()
#    print graph.get_adjacency_matrix()
#    print 


graphs = load_data(sys.argv[1])

for graph in graphs:
    graph.compute_adjacency_matrix()


#print graph_edit_distance(graphs[0], graphs[1])

#print rbf_kernel(graphs[0], graphs[1], graph_edit_distance, 0.1)

#res = []
#for seed in range(200):
#    res.append(kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel))
#
#correct = 0
#wrong = 0
#
#for items in res:
#    if all(x == items[0] for x in items):
#        wrong +=1
#    else:
#        correct +=1
#
#print "Correct: " + str(correct)
#print "Wrong: " + str(wrong)

#for seed in range(200):
#    print kernel_kmeans(2, 50, seed, graphs, graph_edit_distance, rbf_kernel)


#seed 2 fails
#seed 5 works
print kernel_kmeans(2, 50, 5, graphs, graph_edit_distance, rbf_kernel)


print sd_kmeans(2, 50, 5, graphs, graph_edit_distance)

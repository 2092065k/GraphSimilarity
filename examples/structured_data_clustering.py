import numpy as np

from graphSimilarity.utils import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_wcss, get_sd_labels

# The used distance measure (Graph Edit Distance in this case) can be
# swaped out for any other function which takes two items form the
# 'graphs' list and reurns the distance between them


# load graphs from an input data file
graphs = load_data(sys.argv[1])

# compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()

# compute the distance between two graphs using GED
print graph_edit_distance(graphs[0], graphs[1])

# cluster the graphs using structured data k-means and GED
centroids = sd_kmeans(2, 50, 0, graphs, graph_edit_distance, "random")
print centroids

# get the cluster label for each graph
labels = get_sd_labels(centroids, graphs, graph_edit_distance)
print labels

# compute the within-cluster sum of squares for the obtained centroids 
wcss = get_sd_wcss(centroids, graphs, graph_edit_distance)
print wcss

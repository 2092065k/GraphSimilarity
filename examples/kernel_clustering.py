from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_wcss

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

# compute the radial basis function (Gaussian kernel) for two graphs
print rbf_kernel(graphs[0], graphs[1], graph_edit_distance, sigma = 0.1)

# cluster the graphs and get the cluster label for each graph using kernel k-means
labels = kernel_kmeans(2, 50, 0, graphs, graph_edit_distance, rbf_kernel, "random")
print labels

# compute the within-cluster sum of squares for the obtained labels 
wcss = get_kernel_wcss(2, graphs, labels, graph_edit_distance, rbf_kernel)
print wcss

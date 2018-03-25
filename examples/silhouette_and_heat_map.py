from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_labels, get_distance_matrix

from sklearn.metrics import silhouette_score


# load graphs from an input data file
graphs = load_data(sys.argv[1])

# compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()

# compute the NxN distance matrix
distance_matrix = get_distance_matrix(graphs, graph_edit_distance)

# perform clustering and obtain k centroids
centroids = sd_kmeans(2, 50, 0, graphs, graph_edit_distance, init = "random", distance_matrix = distance_matrix)

# get the cluster lable for each input graph
labels = get_sd_labels(centroids, graphs, graph_edit_distance, distance_matrix = distance_matrix)

# compute the silhouette score for the obtained lables
score = silhouette_score(distance_matrix, labels, metric="precomputed")
print score

# plot the heat map of the distance_matrix
draw_matrix_heat_map(distance_matrix)

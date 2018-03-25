from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_matrix
from graphSimilarity.sd_kmeans import sd_kmeans, get_distance_matrix


# It is possible to precompute the NxN matrix of distance (kernel) values between any two
# graphs and directly supply it to a clustering method, so as to speed up computation if the
# clustering method is invoked multiple times


# load graphs from an input data file
graphs = load_data(sys.argv[1])

# compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()


# Graph Edit Distance can be directly applied to compute the NxN matrix as it does not involve
# any pre-processing stage

ged_distance_matrix = get_distance_matrix(graphs, graph_edit_distance)
ged_kernel_matrix = get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)

# All other algorithms include a pre-processing stage where the input graphs are converted
# to another format (matrices) and the distances are then comuted over the new objects.
# It is therefore more efficient to explicitly perform format conversion first and
# compute the NxN distance (kernel) matrix afterwords

# Slow variant uning DeltaCon - involvels a lot of redundant computation

slow_dc_distance_matrix = get_distance_matrix(graphs, delta_con)
slow_dc_kernel_matrix = get_kernel_matrix(graphs, delta_con, rbf_kernel)

# Fast variant uning DeltaCon - include an explicit pre-processing stage

affinity_matrices = [fabp(graph) for graph in graphs]
fast_dc_distance_matrix = get_distance_matrix(affinity_matrices, root_ed)
fast_dc_kernel_matrix = get_kernel_matrix(affinity_matrices, root_ed, rbf_kernel)

# The fast and slow variants now hold identical data

# Witout passing the pre-computing matrix to the clustering algorithm, it will
# re-compute it for each invocation.


# Examples for passing a pre-computed distance/kernel matrix for clustering:

for k in range(1, 5):
	centroids = sd_kmeans(k, 50, 0, graphs, graph_edit_distance, distance_matrix = ged_distance_matrix)
	print centroids

for k in range(1, 5):
	labels = kernel_kmeans(k, 50, 0, graphs, delta_con, rbf_kernel, kernel_matrix = slow_dc_kernel_matrix)
	print labels

for k in range(1, 5):
	labels = kernel_kmeans(k, 50, 0, affinity_matrices, root_ed, rbf_kernel, kernel_matrix = fast_dc_kernel_matrix)
	print labels

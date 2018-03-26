from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph
from graphSimilarity.kernel_kmeans import kernel_kmeans, get_kernel_wcss, get_kernel_matrix
from graphSimilarity.sd_kmeans import sd_kmeans, get_sd_wcss, get_sd_labels, get_distance_matrix

from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score

# This method allows you to use all available distance measures along with a chosen clustering
# algorithm to determine the best distance metric according to silhouette

def compare_distance_measures(file, cluster_method, cluster_params, cluster_restarts, rolx_params = {}, deep_walk_params = {}, node_weight_algs = False):
	
	# load graphs from the input data file
	graphs = load_data(file)

	# compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
	for graph in graphs:
	    graph.compute_adjacency_matrix()
	    graph.compute_diagonal_matrix()

	distance_matrices = {}
	kernel_matrices = {}

	# only eavluate algorithms that do not consider node weights
	if not node_weight_algs: 

		# distance/kernel matrix for Graph Edit Distance
		ged_distance_matrix = get_distance_matrix(graphs, graph_edit_distance)
		ged_kernel_matrix = get_kernel_matrix(graphs, graph_edit_distance, rbf_kernel)

		# distance/kernel matrix for DeltaCon
		fabp_matrices = [fabp(graph) for graph in graphs]
		dc_distance_matrix = get_distance_matrix(fabp_matrices, root_ed)
		dc_kernel_matrix = get_kernel_matrix(fabp_matrices, root_ed, rbf_kernel)

		# distance/kernel matrix for SimRank
		sim_rank_matrices = [sim_rank(graph) for graph in graphs]
		sr_distance_matrix = get_distance_matrix(sim_rank_matrices, matrix_ed)
		sr_kernel_matrix = get_kernel_matrix(sim_rank_matrices, matrix_ed, rbf_kernel)

		# distance/kernel matrix for In/Out Node Degree
		degree_matrices = [node_degree_matrix(graph) for graph in graphs]
		deg_distance_matrix = get_distance_matrix(degree_matrices, matrix_ed)
		deg_kernel_matrix = get_kernel_matrix(degree_matrices, matrix_ed, rbf_kernel)

		if len(rolx_params) > 0:

			# distance/kernel matrix for RolX
			rolx_matrices = get_rolx_matrices(graphs, **rolx_params)
			rolx_distance_matrix = get_distance_matrix(rolx_matrices, matrix_cd)
			rolx_kernel_matrix = get_kernel_matrix(rolx_matrices, matrix_cd, rbf_kernel)

		if len(deep_walk_params) > 0:

			# distance/kernel matrix for DeepWalk
			dw_matrices = get_deep_walk_matrices(graphs, **deep_walk_params)
			dw_distance_matrix = get_distance_matrix(dw_matrices, matrix_cd)
			dw_kernel_matrix = get_kernel_matrix(dw_matrices, matrix_cd, rbf_kernel)

	# only eavluate algorithms that do consider node weights
	else:

		# distance/kernel matrix for Graph Edit Distance with Node Weights
		ged_nw_distance_matrix = get_distance_matrix(graphs, graph_edit_distance_nw)
		ged_nw_kernel_matrix = get_kernel_matrix(graphs, graph_edit_distance_nw, rbf_kernel)

		# distance/kernel matrix for DeltaCon with Node Weights
		norm = get_largest_node_weight(graphs)
		fabp_nw_matrices = [fabp_nw(graph, norm) for graph in graphs]
		dc_nw_distance_matrix = get_distance_matrix(fabp_nw_matrices, root_ed)
		dc_nw_kernel_matrix = get_kernel_matrix(fabp_nw_matrices, root_ed, rbf_kernel)

		# distance/kernel matrix for In/Out Node Degree with Node Weights
		degree_matrices_nw = [node_degree_weight_matrix(graph) for graph in graphs]
		deg_nw_distance_matrix = get_distance_matrix(degree_matrices_nw, matrix_ed)
		deg_nw_kernel_matrix = get_kernel_matrix(degree_matrices_nw, matrix_ed, rbf_kernel)


	if cluster_method == "sd_kmeans":


		centroids = sd_kmeans()


	elif cluster_method == "kernel_kmeans":



	else:






	for run in range(cluster_restarts):


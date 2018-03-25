from graphSimilarity.utils import *
from graphSimilarity.kernel_methods import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph

# load graphs from an input data file
graphs = load_data(sys.argv[1])

# compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()


# --- Methods that do not account for node weights ---

# compute the distance between two graphs using Graph Edit Distance
print graph_edit_distance(graphs[0], graphs[1])

# compute the distance between two graphs using DeltaCon
print delta_con(graphs[0], graphs[1])

# compute the distance between two graphs using SimRank
print sim_rank_distance(graphs[0], graphs[1])

# compute the distance between two graphs using In/Out Degree features
print degree_dist(graphs[0], graphs[1])


# --- Methods that account for node weights ---

# compute the distance between two graphs using Graph Edit Distance with Node Weights
print graph_edit_distance_nw(graphs[0], graphs[1])

# compute the distance between two graphs using DeltaCon with Node Weights
norm = get_largest_node_weight(graphs)
print root_ed(fabp_nw(graphs[0], norm), fabp_nw(graphs[1], norm))

# compute the distance between two graphs using In/Out Degree and Node Weight features
print degree_dist_nw(graphs[0], graphs[1])

from graphSimilarity.utils import *
from graphSimilarity.distance_functions import *
from graphSimilarity.graph import Graph

# load graphs from an input data file
graphs = load_data(sys.argv[1])

# compute the graphs' adjacency and diagonal matrices - required for all distance algorithms
for graph in graphs:
    graph.compute_adjacency_matrix()
    graph.compute_diagonal_matrix()

# There are two methods for obtaining RolX and DeepWalk representations of the
# graphs: using external scripts or wrapper functions:

# Method 1: external scripts - this method involves creating external scripts
# and additional manual steps but it can allow for additional customization
# of the external tools

# For RolX it is necessary to supply a directory where a file with an edge list
# representation for every graph will be created.

# The common node parameter is necessary for the correct execution of the RolX
# implementation: it creates a common node which is connected to every other node.
# If it is necessary to obtain edge list files as normal - set the parameter to false
create_basic_edgelist_files(graphs, dir_name = sys.argv[2], common_node = True)

# Then another script which will execute RolX for each file needs to be launced
# (the provided RolX implementation needs to be modified to retrieve the RxN role matrix)

# The outputs of Rolex then need to concatenated into a single file which can be read back in
# Node that the lines_per_matrix parameter needs to be equal to the number of nodes in
# the processed graphs (+1 if 'common_node' was set to true when generating edge lists)
rx_matrices = load_matrix_data(file = sys.argv[3], lines_per_matrix = sys.argv[4])

# For DeepWalk is is necessary to supply a directory where a file with an
# adjacency list representation for each grah will be created.
# The optional ammend paramether is included to overcome a bug in the implementation
# of DeepWalk where node zero is discarded if it is disconnected - an additional
# edge is created between node zero and node one.
create_basic_adjacency_files(graphs, dir_name = sys.argv[5], ammend = True)

# Onec the files are created, another script needs to be launched to run the
# DeepWalk implementation on every output file, which will create DeepWalk format
# files for each grahp. This data is then read back in.
# Note that the lines_per_matrix parameter needs to be equal to the number of nodes in the graph
dw_matrices = load_deep_walk_files(dir_name = sys.argv[6], lines_per_matrix = sys.argv[7])


# Method 2: using the wrapper functions: these functions are simpler to use but
# provide less flexibility

# Calculate the RolX NxR matrix of each graph - assumes the RolX executable provides the
# full NxR matrix. A temporary directory called format_conversion is also created and
# deleted when the method terminates.
rx_matrices = get_rolx_matrices(graphs, rolx_path = "/path/to/rolx", num_roles = 3)

# Calculate the DeepWalk matrix of each graph - assumes that DeepWalk is already installed.
# A temporary directory called format_conversion is also created and deleted when the method terminates.
dw_matrices = get_deep_walk_matrices(graphs, representation_size = 64, number_walks = 10, walk_length = 40, undirected = True)


# The distance between the obtained matrices can then be calculated using either
# euclidean or cosine diatance - from this point clustering is performed as normal
# over the obtained matrices with the chosen distance measure

print matrix_ed(rx_matrices[0], rx_matrices[1])
print matrix_cd(rx_matrices[0], rx_matrices[1])

print matrix_ed(dw_matrices[0], dw_matrices[1])
print matrix_cd(dw_matrices[0], dw_matrices[1])

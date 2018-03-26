import subprocess

from graphSimilarity.utils import *
from graphSimilarity.graph_generator_2 import generate_graphs_file_2


# The graph generator can easily be invoked once to generate graphs from a single set of
# parameters. Here we show how to generate multiple sets of graphs, where each set has
# common connectivity values for the respective graph regions.

# the number of times tha graph generator will be invoked with different parameters
num_runs = 4

# the number of graphs generated in each run
num_graphs = 10

# the number of nodes in each graph
num_nodes = 15

# the boundries of each region in each graph
region_bounds = [[0, 5], [5, 10], [10, 15]]

# obtain permutations for the connectivity of the different regions
# different runs will use a differen permutation of connectivity values
permutations =  get_random_permutations([0.8, 0.4, 0.1], num_runs, seed = 0)

# controls the connectivity between the regions
region_connectivity = 0.5

# the range of node weights per region
region_node_weights = [[20, 30], [10, 20], [1, 10]]

# names of the files generated in each run
file_names = []


for run_id in range(num_runs):

	file_names.append("graphs" + str(run_id) + ".txt")
	
	# merge the region bounds and connectivity list
	perm = permutations[run_id]
	regions_with_connectivity = []
	for region_id in range(len(region_bounds)):
		regions_with_connectivity.append(region_bounds[region_id] + [perm[region_id]])
		
	# run the graph generator
	generate_graphs_file_2(file_names[run_id], num_graphs, num_nodes, seed = run_id,
						regions = regions_with_connectivity, region_con = region_connectivity, uniform_region_con = False,
						weighted_nodes = True, node_weight_ranges = region_node_weights)

# concatenate the files generated in each run
cat_cmd = ["cat"] + file_names

with open('graphs.txt', "w") as outfile:
	subprocess.call(cat_cmd, stdout=outfile)

# remove the graph files from each individual run
rm_cmd = ["rm"] + file_names
subprocess.call(rm_cmd)

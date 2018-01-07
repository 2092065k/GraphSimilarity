import numpy as np
from math import floor


def __get_num_of_edges(num_of_nodes):
    'The number of edges will be equal to 30% - 60% of the edges in a clique'

    edges_in_clique = (num_of_nodes * (num_of_nodes - 1)) / 2
    percentage = (np.random.randint(30, high = 60) + np.random.random()) / 100.0
    num_of_edges = int(floor(edges_in_clique * percentage))

    return num_of_edges


def generate_graphs_file(file_name, num_of_graphs, num_of_nodes, seed,
                         weighted = False, weight_range = [1, 10],
                         dense_regions = [], sparse_regions = []):
    
    np.random.seed(seed)
    file = open(file_name, 'w')

    for graph in range(num_of_graphs):

        file.write(str(num_of_nodes) + '\n')

        num_of_edges =  __get_num_of_edges(num_of_nodes)

        for edge in range(num_of_edges):

            # somehow retry if edge already exists
            node1 = np.random.randint(0, high = num_of_nodes)
            node2 = np.random.randint(0, high = num_of_nodes)
            weight = 1

            file.write(str(node1) + ' ' + str(node2) + ' ' + str(weight) + '\n')

    file.close()
    return 0

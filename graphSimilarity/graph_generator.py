import numpy as np


def __get_num_of_edges(num_of_nodes, clique_range):
    'The number of edges will be equal to a percentage of the edges in a clique'

    edges_in_clique = (num_of_nodes * (num_of_nodes - 1)) / 2
    percentage = (np.random.randint(clique_range[0], clique_range[1]) + np.random.random()) / 100.0
    num_of_edges = int(round(edges_in_clique * percentage))

    return num_of_edges


def __get_edge_weight(weighted, weight_range):

    if not weighted:
        weight = 1
    else:
        weight = np.random.randint(weight_range[0], weight_range[1] + 1)

    return weight


def __generate_edges(num_of_nodes, clique_range, weighted, weight_range, directed, dense_regions, sparse_regions):

    #add the weights at the end
    num_of_edges =  __get_num_of_edges(num_of_nodes, clique_range)
    edges = []

    for e in range(num_of_edges):

        approved = False

        while not approved:

            # generate an edge in one of the dense regions
            if len(dense_regions) > 0 and np.random.random() < 0.50:
                region = dense_regions[np.random.randint(0, len(dense_regions))]
                node1 = np.random.randint(region[0], region[1])
                node2 = np.random.randint(region[0], region[1])
                edge = [node1, node2]

            # generate an edge in the rest of the graphs
            else:
                node1 = np.random.randint(0, num_of_nodes)
                node2 = np.random.randint(0, num_of_nodes)
                edge = [node1, node2]

                # if the edge is from one of the sparse regions possibly reject it
                for region in sparse_regions:
                    if edge[0] in range(region[0], region[1]) and edge[1] in range(region[0], region[1]):
                        if np.random.random() < 0.80:
                            edge = [0, 0]
                            break

            if not directed:
                edge.sort()

            # currently excluding self edges
            if edge[0] != edge[1] and edge not in edges:
                edges.append(edge)
                approved = True

    # include a weight for each edge
    for edge in edges:
        weight = __get_edge_weight(weighted, weight_range)
        edge.append(weight)

    return edges


def generate_graphs_file(file_name, num_of_graphs, num_of_nodes, seed = 0,
                         clique_range = [30, 60], weighted = False, weight_range = [1, 10],
                         directed = False, dense_regions = [], sparse_regions = []):
    
    np.random.seed(seed)
    file = open(file_name, 'w')

    for graph in range(num_of_graphs):

        file.write(str(num_of_nodes) + '\n')

        edges = __generate_edges(num_of_nodes, clique_range, weighted, weight_range,
                                directed, dense_regions, sparse_regions)

        for edge in edges:
            file.write(str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(edge[2]) + '\n')

    file.close()

import itertools
import numpy as np


def __assert_all_nodes_in_regions(num_of_nodes, regions):
    'Assert that every oned is included in exactly one region'

    all_nodes = range(num_of_nodes)
    nodes_in_region = []
    for region in regions:
        nodes_in_region += range(region[0], region[1])
    nodes_in_region.sort()

    return nodes_in_region == all_nodes


def __get_num_of_edge_in_region(num_of_nodes, percentage):
    'The number of edges will be equal to a percentage of the edges in a clique'

    edges_in_clique = (num_of_nodes * (num_of_nodes - 1)) / 2
    num_of_edges = int(round(edges_in_clique * percentage))

    return num_of_edges


def __get_edge_weight(weighted, weight_range):

    if not weighted:
        weight = 1
    else:
        weight = np.random.randint(weight_range[0], weight_range[1] + 1)

    return weight


def generate_edge_between_regions(edges, directed, region_0, region_1):
    'Create a single edge between the two regions'

    approved = False

    while not approved:

        node1 = np.random.randint(region_0[0], region_0[1])
        node2 = np.random.randint(region_1[0], region_1[1])
        
        if not directed:
            edge = [node1, node2]
            edge.sort()
        else:
            # randomly choose the source/destination region
            if np.random.random() > 0.5:
                edge = [node1, node2]
            else:
                edge = [node2, node1]

        if edge not in edges:
            edges.append(edge)
            approved = True


def __generate_uniform_cross_region_edges(edges, directed, region_con, regions):
    'Create an equal number of edges joining all region pairs'

    region_pairs = list(itertools.combinations(regions, 2))

    for region_pair in region_pairs:

        region_0 = region_pair[0]
        region_1 = region_pair[1]

        smaller_group_size = min(len(range(region_0[0], region_0[1])), len(range(region_1[0], region_1[1])))
        num_edges_between_regions = int(round(smaller_group_size * region_con))

        for e in range(num_edges_between_regions):
            generate_edge_between_regions(edges, directed, region_0, region_1)




def __generate_cross_region_edges(edges, directed, num_of_nodes, region_con, regions):
    'Randomly create edges joining region pairs'

    region_pairs = list(itertools.combinations(regions, 2))
    avg_region_size = num_of_nodes / float(len(regions))
    num_edges_between_regions = int(round(region_con * avg_region_size * len(region_pairs)))

    for e in range(num_edges_between_regions):

        region_pair = region_pairs[np.random.randint(0, len(region_pairs))]
        generate_edge_between_regions(edges, directed, region_pair[0], region_pair[1])




def __generate_edges(num_of_nodes, weighted, weight_range, directed, regions, region_con, uniform_region_con):

    edges = []

    # generate edges within each region
    for region in regions:

        num_nodes_in_region = len(range(region[0], region[1]))
        num_edges_in_region = __get_num_of_edge_in_region(num_nodes_in_region, region[2])

        for e in range(num_edges_in_region):

            approved = False

            while not approved:

                node1 = np.random.randint(region[0], region[1])
                node2 = np.random.randint(region[0], region[1])
                edge = [node1, node2]

                if not directed:
                    edge.sort()

                # currently excluding self edges
	            if edge[0] != edge[1] and edge not in edges:
	                edges.append(edge)
	                approved = True

    # generate edges between different regions
    if uniform_region_con:
        __generate_uniform_cross_region_edges(edges, directed, region_con, regions)
    else:
        __generate_cross_region_edges(edges, directed, num_of_nodes, region_con, regions)

    # include a weight for each edge
    for edge in edges:
        weight = __get_edge_weight(weighted, weight_range)
        edge.append(weight)

    return edges


def generate_graphs_file_2(file_name, num_of_graphs, num_of_nodes, seed = 0,
                         weighted = False, weight_range = [1, 10], directed = False,
                         regions = [], region_con = 0.1, uniform_region_con = True):
    
    if not __assert_all_nodes_in_regions(num_of_nodes, regions):
        print("Some nodes are not part of a region or are included in multiple regions")

    np.random.seed(seed)
    file = open(file_name, 'w')

    for graph in range(num_of_graphs):

        file.write(str(num_of_nodes) + '\n')

        edges = __generate_edges(num_of_nodes, weighted, weight_range,
                                directed, regions, region_con, uniform_region_con)

        for edge in edges:
            file.write(str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(edge[2]) + '\n')

    file.close()

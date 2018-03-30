import random
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


def __get_num_of_edge_in_region(num_of_nodes, directed, percentage):
    'The number of edges will be equal to a percentage of the edges in a clique'

    edges_in_clique = (num_of_nodes * (num_of_nodes - 1)) / 2
    num_of_edges = int(round(edges_in_clique * percentage))

    # if the edges are directed we can have twice as many
    if directed:
        num_of_edges = num_of_edges * 2

    return num_of_edges


def __generate_edge_weight(weighted_edges, edge_weight_range):
    'Generate an edge weight'

    # if the edge is unweighted assign a weight of one, otherwise assign a random weight in the given range
    if not weighted_edges:
        weight = 1
    else:
        weight = np.random.randint(edge_weight_range[0], edge_weight_range[1] + 1)

    return weight


def __generate_edge_between_regions(cross_region_edges, directed, region_0, region_1):
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

        if edge not in cross_region_edges:
            cross_region_edges.append(edge)
            approved = True


def __generate_uniform_cross_region_edges(edges, directed, region_con, regions):
    'Create an equal number of edges joining all region pairs'

    region_pairs = list(itertools.combinations(regions, 2))

    for region_pair in region_pairs:

        cross_region_edges = []

        region_0 = region_pair[0]
        region_1 = region_pair[1]

        smaller_group_size = min(len(range(region_0[0], region_0[1])), len(range(region_1[0], region_1[1])))
        num_edges_between_regions = int(round(smaller_group_size * region_con))

        for e in range(num_edges_between_regions):
            __generate_edge_between_regions(cross_region_edges, directed, region_0, region_1)

        edges += cross_region_edges




def __generate_cross_region_edges(edges, directed, num_of_nodes, region_con, regions):
    'Randomly create edges joining region pairs'

    region_pairs = list(itertools.combinations(regions, 2))
    avg_region_size = num_of_nodes / float(len(regions))
    num_edges_between_regions = int(round(region_con * avg_region_size * len(region_pairs)))
    all_cross_region_edges = [[] for pair_id in range(len(region_pairs))]

    for e in range(num_edges_between_regions):

        pair_id = np.random.randint(0, len(region_pairs))
        region_pair = region_pairs[pair_id]
        cross_region_edges = all_cross_region_edges[pair_id]
        __generate_edge_between_regions(cross_region_edges, directed, region_pair[0], region_pair[1])

    for cross_region_edges in all_cross_region_edges:
        edges += cross_region_edges




def __generate_edges(num_of_nodes, weighted_edges, edge_weight_range, directed, regions, region_con, uniform_region_con):
    'Generate all edges for a given graph'

    edges = []

    # generate edges within each region
    for region in regions:

        num_nodes_in_region = region[1] - region[0]
        num_edges_in_region = __get_num_of_edge_in_region(num_nodes_in_region, directed, region[2])

        possible_edges = []

        if not directed:
            possible_edges = list((list(tup) for tup in itertools.combinations(range(region[0], region[1]), 2)))

        else:
            possible_edges = list((list(tup) for tup in itertools.permutations(range(region[0], region[1]), 2)))

        region_edges = random.sample(possible_edges, num_edges_in_region)
        edges += region_edges

    # generate edges between different regions
    if uniform_region_con:
        __generate_uniform_cross_region_edges(edges, directed, region_con, regions)
    else:
        __generate_cross_region_edges(edges, directed, num_of_nodes, region_con, regions)

    # include a weight for each edge
    for edge in edges:
        weight = __generate_edge_weight(weighted_edges, edge_weight_range)
        edge.append(weight)

    return edges


def __generate_node_weights(regions, node_weight_ranges):
    'For each node, produce a weight in the specified weight range for its region'

    node_weights = []
    node_ids_in_regions = [range(region[0], region[1]) for region in regions]

    for region_id in range(len(regions)):

        node_ids_in_region = node_ids_in_regions[region_id]
        node_weight_range = node_weight_ranges[region_id]

        for node_id in node_ids_in_region:

            node_weight = (node_weight_range[1] - node_weight_range[0]) * np.random.random() + node_weight_range[0]
            node_weights.append([node_id, node_weight])

    return node_weights


def generate_graphs_file_2(file_name, num_of_graphs, num_of_nodes, seed = 0,
                         weighted_edges = False, edge_weight_range = [1, 10], directed = False,
                         regions = [], region_con = 0.1, uniform_region_con = True,
                         weighted_nodes = False, node_weight_ranges = []):

    """Generate a collection of graphs with a set of regions with variable connectivity

    Parameters
    ----------
    file_name: string
        name of the generated graphs file

    num_of_graphs: int
        the nuber of graphs that will be generated and written into the file

    num_of_nodes: int
        the number of nodes that every graph will have

    seed: int
        a seed paramether for controlling randomness

    weighted_edges: boolean
        determines if the edges will be weighted or not

    edge_weight_range: [lwb: int, upb: int]
        the weight of each edge will be a random integer form lwb to upb

    directed: boolean
        determines if the edges will be directed or not

    regions: list of (region_start_node: int, region_end_node: int, region_connectivity: float) tuples
        outlines the partitioning of the graph into regions along with their connectivity level
        (percentage of the edges in a clique made up of the nodes in the region)

    region_con: float
        determines tha cross region connectivity

    uniform_region_con: boolean
        determines if the number of edges between each pair of regions are equal

    weighted_nodes: boolean
        determines if the nodes will be weighted or not

    node_weight_ranges: list of (lwb: float, upb: float) tuples
        the lwb and upb of node weights for each region
    """
    
    # assert that the input parameters provide consistent information
    if not __assert_all_nodes_in_regions(num_of_nodes, regions):
        print("Some nodes are not part of a region or are included in multiple regions")
        return

    if weighted_nodes and len(regions) != len(node_weight_ranges):
        print("The number of node regions and node weight ranges do not match")
        return

    np.random.seed(seed)
    random.seed(seed)
    file = open(file_name, 'w')

    # for each graph write out - number of nodes, node weights, edges
    for graph in range(num_of_graphs):

        # write out the number of nodes in the graph - also indicates the start of a new graph
        file.write(str(num_of_nodes) + '\n')

        # write out all node weights
        if weighted_nodes:
            for node_weight in __generate_node_weights(regions, node_weight_ranges):
                file.write(str(node_weight[0]) + ' ' + str(node_weight[1]) + '\n')

        # write out all edges in the graph
        edges = __generate_edges(num_of_nodes, weighted_edges, edge_weight_range,
                                directed, regions, region_con, uniform_region_con)

        for edge in edges:
            file.write(str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(edge[2]) + '\n')

    file.close()

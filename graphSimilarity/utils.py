import os
import sys
import itertools
import subprocess

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from graph import Graph


def draw_graph(num_nodes, edges):
    'Draw a single graph'

    # create networkx graph
    G = nx.Graph()

    # add nodes
    G.add_nodes_from(range(num_nodes))

    # add edges
    G.add_edges_from(edges)

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)
    nx.draw_networkx_labels(G, pos)

    # show graph
    plt.show()


def draw_all_graphs(file):
    'Draw all graphs in a file'

    file = open(file, 'r')

    edges = []
    num_nodes = int(file.readline())
    for line in file:

        line_elements = line.split()

        # parse more data on the current graph
        if len(line_elements) == 3:
            edge = map(lambda x: int(x), line_elements)
            edges.append(edge[:2])

        # animate the graph and clear
        elif len(line_elements) == 1:
            draw_graph(num_nodes, edges)
            edges = []
            num_nodes = int(line)

    file.close()
    draw_graph(num_nodes, edges)


def map_over_matrix_elements(matrix, function, **kwds):
    'Apply a function to every element of a matrix'

    function_vec = np.vectorize(function)
    mapped_matrix = function_vec(matrix, **kwds)

    return mapped_matrix


def draw_matrix_heat_map(matrix, color="hot"):
    'Draw a heat map of a matrix'

    plt.imshow(matrix, cmap=color, interpolation='nearest')
    plt.show()


def add_matrix_noise(matrix, percentage):
    'Append noise to the end of an n*n matrix representing n*percentage elements'

    dim_1 = int(round(percentage * matrix.shape[0]))
    dim_2 = matrix.shape[0] + dim_1

    noise = np.random.random((dim_1, dim_2)) * matrix.max()

    phase1 = np.vstack((matrix, noise[:, 0:matrix.shape[0]]))
    phase2 = np.hstack((phase1, noise.T))

    return phase2


def get_random_permutations(vals, num_permutations, seed = 0):
    'Get n permutations of the elements in vals'

    np.random.seed(seed)
    permutations = []
    all_permutations = list(itertools.permutations(vals, len(vals)))

    for index in range(num_permutations):

        permutation =  all_permutations[np.random.randint(0, len(all_permutations))]
        permutations.append(permutation)
        all_permutations.remove(permutation)

    return permutations


def load_data(file):
    'Parse a graph data file'

    graphs = []
    file = open(file, 'r')

    edges = []
    vertex_weights = {}
    num_nodes = int(file.readline())

    for line in file:

        line_elements = line.split()

        # parse vertex weight line
        if len(line_elements) == 2:
            vertex_weights[int(line_elements[0])] = float(line_elements[1])

        # parse edge line
        if len(line_elements) == 3:
            edge = map(lambda x: int(x), line_elements)
            edges.append(edge)

        # parse number of vertices line
        elif len(line_elements) == 1:
            graphs.append(Graph(num_nodes, edges, vertex_weights))
            edges = []
            vertex_weights = {}
            num_nodes = int(line)

    graphs.append(Graph(num_nodes, edges, vertex_weights))
    file.close()

    return graphs


def create_basic_edgelist_files(graphs, dir_name, common_node = False):
    'Creates files with basic edge list representations of the graphs'

    for index in range(len(graphs)):

        file = open(dir_name + '/' + "graph" + str(index) + ".txt", "w")
        graph = graphs[index]

        if common_node:

            num_vertices = graph.get_num_vertices()

            for i in range(num_vertices):
                file.write("0 " + str(i + 1) + '\n')

            for edge in graph.get_edges():
                file.write(str(edge[0]+1) + ' ' + str(edge[1] + 1) + '\n')

        else:

            for edge in graph.get_edges():
                file.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')

        file.close()


def create_basic_adjacency_files(graphs, dir_name, ammend = False):
    'Creates files with basic adjacency list representations of the graphs'

    for index in range(len(graphs)):

        file = open(dir_name + '/' + "graph" + str(index) + ".txt", "w")
        graph = graphs[index]
        num_vertices = graph.get_num_vertices()

        # assumes adjacency matrix is computed
        adj_matrix = graph.get_adjacency_matrix()

        for vertex in range(num_vertices):

            file.write(str(vertex) + " ")
            row = adj_matrix[vertex]

            # there is an issue in the provided DeepWalk implementation
            # where node zero is sometimes discarded if it is disconnected
            if ammend and vertex == 0 and sum(row) == 0:
                file.write(str(1) + " ")

            for v in range(len(row)):

                if row[v] != 0:
                    file.write(str(v) + " ")

            # do not print a new line after the final row
            if vertex != num_vertices - 1:
                file.write("\n")

        file.close()


def load_matrix_data(file, lines_per_matrix):
    'Load a file with concatenated matrix data'

    matrices = []
    file = open(file, 'r')

    matrix = []
    num_lines = 0

    for line in file:

        row = [float(num) for num in line.split()]
        matrix.append(row)
        num_lines += 1

        if num_lines == lines_per_matrix:

            matrices.append(np.array(matrix))
            num_lines = 0
            matrix = []

    file.close()

    return matrices


def load_deep_walk_files(dir_name, lines_per_matrix):
    'Load all DeepWalk formated files from a directory'

    matrices = []
    num_files = len(os.listdir(dir_name))

    for index in range(num_files):

        file = open(dir_name + '/' + "graph" + str(index) + ".txt", "r")
        adj_dict = {}
        matrix = []

        # discard the first line of each file - unneeded metadata
        line = file.readline()

        for line in file:
            row = [float(num) for num in line.split()]
            adj_dict[row[0]] = row[1:]

        for i in range(lines_per_matrix):
            matrix.append(adj_dict[i])

        matrices.append(np.array(matrix))
        adj_dict = {}
        matrix = []

        file.close()

    return matrices


def get_rolx_matrices(graphs, rolx_path = "/path/to/rolx", num_roles = 3):
    'Convert a collection of graphs into RolX matrices'

    # the matrix has num_node lines + the extra node connected to everything
    lines_per_matrix = graphs[0].get_num_vertices() + 1
    
    # create directoriries where the intermediate files will be stored
    subprocess.call(["mkdir", "format_conversion"])
    subprocess.call(["mkdir", "format_conversion/in"])
    subprocess.call(["mkdir", "format_conversion/out"])

    # create the edge lists which will be provided to RolX
    create_basic_edgelist_files(graphs, "format_conversion/in", common_node = True)

    input_file_names = ["format_conversion/in/graph" + str(i) + ".txt" for i in range(len(graphs))]
    output_file_names = ["format_conversion/out/graph" + str(i) + ".txt" for i in range(len(graphs))]

    # conver each graph into a RolX matrix
    for i in range(len(graphs)):

        # this method assumes that RolX has been modified to putput the NxR matrix
        rolx_cmd = [rolx_path, "-i:" + input_file_names[i], "-o:" + output_file_names[i], "-l:" + str(num_roles), "-u:" + str(num_roles)]
        subprocess.call(rolx_cmd)

    # concatenate all output matrix files into a single file
    cat_cmd = ["cat"] + output_file_names
    with open("format_conversion/out/graphs.txt", "w") as outfile:
        subprocess.call(cat_cmd, stdout=outfile)

    # read in the RolX matrices
    matrices = load_matrix_data("format_conversion/out/graphs.txt", lines_per_matrix)

    # discard the common node from each output matrix
    matrices = [m[1:] for m in matrices]

    # delete the intermediate files
    subprocess.call(["rm", "-rf", "format_conversion"])

    return matrices


def get_deep_walk_matrices(graphs, representation_size = 64, number_walks = 10, walk_length = 40, undirected = True,
                            window_size = 5, seed = 0, workers = 1):
    'Convert a collection of graphs into DeepWalk matrices'

    # the matrix has num_node lines
    lines_per_matrix = graphs[0].get_num_vertices()

    # create directoriries where the intermediate files will be stored
    subprocess.call(["mkdir", "format_conversion"])
    subprocess.call(["mkdir", "format_conversion/in"])
    subprocess.call(["mkdir", "format_conversion/out"])

    # create the adjacency lists which will be provided to DeepWalk
    create_basic_adjacency_files(graphs, "format_conversion/in", ammend = True)

    input_file_names = ["format_conversion/in/graph" + str(i) + ".txt" for i in range(len(graphs))]
    output_file_names = ["format_conversion/out/graph" + str(i) + ".txt" for i in range(len(graphs))]

    # conver each graph into a DeepWalk matrix
    for i in range(len(graphs)):

        # this method assumes that DeepWalk has been insatlled
        dw_cmd = ["deepwalk", "--input", input_file_names[i], "--output", output_file_names[i], 
                "--representation-size", str(representation_size), "--number-walks", str(number_walks),
                "--walk-length", str(walk_length), "--undirected", str(undirected), "--seed", str(seed),
                "--window-size", str(window_size), "--workers", str(workers)]
        subprocess.call(dw_cmd)

    # read in the DeepWalk matrices
    matrices = load_deep_walk_files("format_conversion/out", lines_per_matrix)

    # delete the intermediate files
    subprocess.call(["rm", "-rf", "format_conversion"])

    return matrices

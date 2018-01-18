import os
import sys
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


def load_data(file):
    'Parse a graph data file'

    graphs = []
    file = open(file, 'r')

    edges = []
    num_nodes = int(file.readline())

    for line in file:

        line_elements = line.split()

        if len(line_elements) == 3:
            edge = map(lambda x: int(x), line_elements)
            edges.append(edge)

        elif len(line_elements) == 1:
            graphs.append(Graph(num_nodes, edges))
            edges = []
            num_nodes = int(line)

    graphs.append(Graph(num_nodes, edges))
    file.close()

    return graphs


def create_basic_edgelist_files(graphs, dir_name, common_node = False):
    'Creates files with basic edge list representations of the graphs'

    for index in range(len(graphs)):

        file = open(dir_name + '/' + "graph" + str(index) + ".txt", "w")
        graph = graphs[index]
        num_vertices = graph.get_num_vertices()

        if common_node:

            for i in range(num_vertices):
                file.write("0 " + str(i + 1) + '\n')

            for edge in graph.get_edges():
                file.write(str(edge[0]+1) + ' ' + str(edge[1] + 1) + '\n')

        else:

            for edge in graph.get_edges():
                file.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')

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

            matrices.append(np.matrix(matrix))
            num_lines = 0
            matrix = []

    file.close()

    return matrices

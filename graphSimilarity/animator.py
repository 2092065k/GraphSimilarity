import sys
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(num_nodes, edges):

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

    file = open(file, 'r')

    edges = []
    num_nodes = int(file.readline())
    for line in file:

        line_elements = line.split()

        # parse more data on the current graph
        if len(line_elements) == 2:
            edge = map(lambda x: int(x), line_elements)
            edges.append(edge)

        # animate the graph and clear
        elif len(line_elements) == 1:
            draw_graph(num_nodes, edges)
            edges = []
            num_nodes = int(line)

    draw_graph(num_nodes, edges)

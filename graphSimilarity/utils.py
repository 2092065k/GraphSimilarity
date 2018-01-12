from graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


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

    return graphs


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

    draw_graph(num_nodes, edges)

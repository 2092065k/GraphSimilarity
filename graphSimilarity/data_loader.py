from graph import Graph

def load_data(file):

    graphs = []
    file = open(file, 'r')

    edges = []
    num_nodes = int(file.readline())

    for line in file:

        line_elements = line.split()

        if len(line_elements) == 2:
            edge = map(lambda x: int(x), line_elements)
            edges.append(edge)

        elif len(line_elements) == 1:
            graphs.append(Graph(num_nodes, edges))
            edges = []
            num_nodes = int(line)

    graphs.append(Graph(num_nodes, edges))

    return graphs

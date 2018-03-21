import numpy as np

class Graph:
    'Class representing a graph with weighted edges and vertices'

    def __init__(self, num_vertices, edges, vertex_weights):
        self.num_vertices = num_vertices
        self.edges = edges

        # all vertices have a weight of one unless explicitly specified
        self.vertex_weights = np.ones(num_vertices)
        for node_id in vertex_weights:
            self.vertex_weights[node_id] = vertex_weights[node_id]

    def get_num_vertices(self):
        return self.num_vertices

    def get_edges(self):
        return self.edges

    def get_vertex_weights(self):
        return self.vertex_weights

    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    def get_diagonal_matrix(self):
        return self.diagonal_matrix

    def compute_adjacency_matrix(self, directed = False):
        'Compute the adjacency matrix for the graph using the list of edges'

        # if the edges are undirected, two locations in the
        # adjacency matrix are modified for each edge in the list
        adjacency_matrix = np.zeros((self.num_vertices, self.num_vertices))
        for edge in self.edges:
            i, j, weight = edge
            adjacency_matrix[i, j] = weight
            if not directed:
                adjacency_matrix[j, i] = weight

        self.adjacency_matrix = adjacency_matrix

    def compute_diagonal_matrix(self):
        'Compute the diaginal matrix for the graph using its adjacency matrix'

        diagonal_matrix = np.zeros(self.adjacency_matrix.shape)
        np.fill_diagonal(diagonal_matrix, self.adjacency_matrix.sum(axis=1))
        self.diagonal_matrix = diagonal_matrix

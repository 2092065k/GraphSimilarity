import numpy as np
from graph import Graph

# assumes all matrices are already computed
def graph_edit_distance(g1, g2):
    'The sum of the number of edges that are present only in g1 or g2'

    m1 = g1.get_adjacency_matrix()
    m2 = g2.get_adjacency_matrix()

    diff = m1 - m2

    return sum(sum(abs(diff)))

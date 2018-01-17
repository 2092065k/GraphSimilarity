import numpy as np
from graph import Graph

# All algorithms assume that the relevant graph matrices are already computed 

# --- Graph Edit Distance ---

def graph_edit_distance(g1, g2):
    'The sum of the number of edges that are present only in g1 or g2'

    m1 = g1.get_adjacency_matrix()
    m2 = g2.get_adjacency_matrix()

    diff = m1 - m2

    return sum(sum(abs(diff)))

# --- DeltaCon ---

def root_ed(s1, s2):

    ed = 0
    dimension = s1.shape[0]

    for i in range(dimension):
        for j in range(dimension):
            ed += (np.sqrt(s1[i,j]) - np.sqrt(s2[i,j])) ** 2

    root_ed = np.sqrt(ed)

    return root_ed


def fabp(g, e = 0.2):

    adj = g.get_adjacency_matrix()
    diag = g.get_diagonal_matrix()
    identity = np.identity(adj.shape[0])
    s = np.linalg.inv(identity + (e ** 2) * diag - e * adj)
    
    return s


def delta_con(g1, g2, e = 0.2):

    s1 = fabp(g1, e)
    s2 = fabp(g2, e)

    dist = root_ed(s1, s2)

    return dist

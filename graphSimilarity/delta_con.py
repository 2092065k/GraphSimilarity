import numpy as np
from graph import Graph


def __root_ed(s1, s2):

    ed = 0
    dimension = s1.shape[0]

    for i in range(dimension):
        for j in range(dimension):
            ed += (np.sqrt(s1[i,j]) - np.sqrt(s2[i,j])) ** 2

    root_ed = np.sqrt(ed)

    return root_ed

def __fabp(g, e):

    adj = g.get_adjacency_matrix()
    diag = g.get_diagonal_matrix()
    identity = np.identity(adj.shape[0])
    s = np.linalg.inv(identity + (e ** 2) * diag - e * adj)
    
    return s

# assumes all matrices are already computed
def delta_con(g1, g2, e = 0.2):

    s1 = __fabp(g1, e)
    s2 = __fabp(g2, e)

    dist = __root_ed(s1, s2)

    return dist

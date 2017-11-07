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


# assumes all matrices are already computed
def delta_con(g1, g2, e = 0.2):

    a1 = g1.get_adjacency_matrix()
    a2 = g2.get_adjacency_matrix()

    d1 = g1.get_diagonal_matrix()
    d2 = g2.get_diagonal_matrix()

    i = np.identity(a1.shape[0])

    s1 = np.linalg.inv(i + (e ** 2) * d1 - e * a1)
    s2 = np.linalg.inv(i + (e ** 2) * d2 - e * a2)

    dist = __root_ed(s1, s2)

    return dist

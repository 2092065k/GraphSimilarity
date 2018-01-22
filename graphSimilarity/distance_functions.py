import numpy as np
import scipy as sp
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

    for i in range(s1.shape[0]):
        for j in range(s1.shape[1]):
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

# --- Matrix Euclidean Distance ---

def matrix_ed(m1, m2):

	dist = 0

	for i in range(m1.shape[0]):

		dist += np.linalg.norm(m1[i] - m2[i])

	return dist

# --- Matrix Cosine Distance ---

def matrix_cd(m1, m2):

    dist = 0

    for i in range(m1.shape[0]):

        dist += sp.spatial.distance.cosine(m1[i], m2[i])

    return dist

# -- Matrix Manhattan Distance --

def matrix_md(m1, m2):

    dist = 0

    for i in range(m1.shape[0]):

        dist += sp.spatial.distance.cityblock(m1[i], m2[i])

    return dist

# --- Matrix Frobenius Distance ---

def frob_dist(m1, m2):

    dist = np.linalg.norm(m1 - m2, ord='fro')

    return dist

# --- Matrix Eigenvector Euclidean Distance ---

def matrix_eig_ed(m1, m2):

    w1, v1 = np.linalg.eig(m1)
    w2, v2 = np.linalg.eig(m2)

    dist = matrix_ed(v1, v2)

    return dist

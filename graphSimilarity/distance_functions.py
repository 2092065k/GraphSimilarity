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

    root_ed = np.sqrt(sum(sum((np.sqrt(s1) - np.sqrt(s2)) ** 2)))

    return root_ed


def fabp(g):

    adj = g.get_adjacency_matrix()
    diag = g.get_diagonal_matrix()
    identity = np.identity(adj.shape[0])
    
    e = 1/(1 + diag.max())
    s = np.linalg.inv(identity + (e ** 2) * diag - e * adj)
    
    return s


def delta_con(g1, g2):

    s1 = fabp(g1)
    s2 = fabp(g2)

    dist = root_ed(s1, s2)

    return dist

# --- SimRank Distance ---

def sim_rank(g, c = 0.8, max_iters = 10):

    adj = g.get_adjacency_matrix()
    col_degree = adj.sum(axis = 0)
    col_degree = [x if x != 0 else 1 for x in col_degree]
    col_norm_adj = adj / col_degree

    s = np.identity(adj.shape[0])
    
    for i in range(max_iters):

        s = c * np.dot(np.dot(col_norm_adj.T, s), col_norm_adj)
        np.fill_diagonal(s, np.ones(adj.shape[0]))

    return s

def sim_rank_distance(g1, g2, c = 0.8, max_iters = 10):

    s1 = sim_rank(g1, c, max_iters)
    s2 = sim_rank(g2, c, max_iters)

    dist = matrix_ed(s1, s2)

    return dist

# --- Node In/Out Degree Distance ---

def node_degree_matrix(g):

    adj = g1.get_adjacency_matrix()
    in_deg = adj.sum(axis=1)
    out_deg = adj.sum(axis=0)
    s = np.vstack((in_deg, out_deg))

    return s

def degree_dist(g1, g2):

    s1 = node_degree_matrix(g1)
    s2 = node_degree_matrix(g2)

    dist = matrix_ed(s1, s2)

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

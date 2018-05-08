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

    return np.sum(np.sum(np.abs(diff)))

# --- DeltaCon ---

def root_ed(s1, s2):

    root_ed = np.sqrt(np.sum(np.sum((np.sqrt(s1) - np.sqrt(s2)) ** 2)))

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

    adj = g.get_adjacency_matrix()
    in_deg = adj.sum(axis=1)
    out_deg = adj.sum(axis=0)
    s = np.vstack((in_deg, out_deg))

    return s.T

def degree_dist(g1, g2):

    s1 = node_degree_matrix(g1)
    s2 = node_degree_matrix(g2)

    dist = matrix_ed(s1, s2)

    return dist

# --- Matrix Euclidean Distance ---

def matrix_ed(m1, m2):

    dist = np.sum(np.sqrt(np.sum((m1 - m2) ** 2, axis = 1)))

    return dist

def flat_matrix_ed(m1, m2):

    dist = np.linalg.norm(m1 - m2)

    return dist


# --- Matrix Cosine Distance ---

def matrix_cd(m1, m2):

    norm1 = np.sqrt(np.sum(m1 ** 2, axis = 1))
    norm2 = np.sqrt(np.sum(m2 ** 2, axis = 1))
    norm = norm1 * norm2

    dot = np.sum(m1 * m2, axis = 1)

    dist = np.sum(np.ones(dot.shape) - dot / norm)

    return dist

def flat_matrix_cd(m1, m2):

    dist = sp.spatial.distance.cosine(m1.flatten(), m2.flatten())

    return dist

# -- Matrix Manhattan Distance --

def matrix_md(m1, m2):

    dist = sp.spatial.distance.cityblock(m1.flatten(), m2.flatten())

    return dist

# Graph Distance Algorithms Considering Node Weights

# --- Graph Edit Distance With Node Weights ---

def graph_edit_distance_nw(g1, g2):

    m1 = g1.get_adjacency_matrix()
    m2 = g2.get_adjacency_matrix()

    nw1 = g1.get_vertex_weights()
    nw2 = g2.get_vertex_weights()

    ged_diff = np.sum(np.sum(np.abs(m1 - m2)))
    nw_diff = np.sum(np.abs(nw1 - nw2))

    return ged_diff + nw_diff

# --- DeltaCon With Node Weights ---

def fabp_nw(g, norm):

    adj = g.get_adjacency_matrix()
    diag = g.get_diagonal_matrix()
    node_weights = g.get_vertex_weights()
    identity = np.identity(adj.shape[0])
    
    e = 1/(1 + diag.max())
    s = np.linalg.inv(identity + (e ** 2) * diag - e * adj)

    nw_matrix = np.zeros(s.shape)
    np.fill_diagonal(nw_matrix, node_weights)
    s = np.dot(nw_matrix, s) / norm
    
    return s

def get_largest_node_weight(graphs):

    return max([graph.get_vertex_weights().max() for graph in graphs])

# --- Node In/Out Degree and Node Weigh Distance ---

def node_degree_weight_matrix(g):

    adj = g.get_adjacency_matrix()
    nw = g.get_vertex_weights()
    in_deg = adj.sum(axis=1)
    out_deg = adj.sum(axis=0)
    s = np.vstack((in_deg, out_deg, nw))

    return s.T

def degree_dist_nw(g1, g2):

    s1 = node_degree_weight_matrix(g1)
    s2 = node_degree_weight_matrix(g2)

    dist = matrix_ed(s1, s2)

    return dist

# --- SimRank Distance With Node Weights ---


def sim_rank_nw(g, c = 0.8, max_iters = 10):

    adj = g.get_adjacency_matrix()
    nw = g.get_vertex_weights()

    col_degree = adj.sum(axis = 0)
    col_degree = [x if x != 0 else 1 for x in col_degree]
    col_norm_adj = adj / col_degree

    s = np.zeros(adj.shape)
    np.fill_diagonal(s, nw)
    
    for i in range(max_iters):

        s = c * np.dot(np.dot(col_norm_adj.T, s), col_norm_adj)
        np.fill_diagonal(s, nw)

    return s

def sim_rank_distance_nw(g1, g2, c = 0.8, max_iters = 10):

    s1 = sim_rank_nw(g1, c, max_iters)
    s2 = sim_rank_nw(g2, c, max_iters)

    dist = matrix_ed(s1, s2)

    return dist

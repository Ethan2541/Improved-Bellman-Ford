from src.Graph import Graph
import numpy as np

def generate_random_test_set(n_instances, n_nodes, weight_min, weight_max, p_edge=0.1, mode=None):
    G = create_random_graph(n_nodes, p_edge, mode)
    weighted_graphs = [create_weighted_graph_from_template(G, weight_min, weight_max) for _ in range(n_instances)]
    return G, weighted_graphs

def generate_levelled_test_set(n_instances, n_levels, n_nodes_per_level, weight_min, weight_max):
    G = create_levelled_graph(n_levels, n_nodes_per_level)
    weighted_graphs = [create_weighted_graph_from_template(G, weight_min, weight_max) for _ in range(n_instances)]
    return G, weighted_graphs


def create_random_graph(n_nodes, p_edge, mode):
    if mode is None:
        return create_random_standard_graph(n_nodes, p_edge)
    elif mode == 'acyclic':
        return create_random_acyclic_graph(n_nodes, p_edge)
    
def create_levelled_graph(n_levels, n_nodes_per_level):
    n_levels = 2500
    n_nodes_per_level = 4
    n_nodes = n_nodes_per_level * n_levels
    nodes = range(n_nodes)
    levels = []
    for j in range(n_levels):
        levels.append(nodes[4*j:4*(j+1)])
    edges = []
    for i in range(len(levels)-1):
        for u in levels[i]:
            for v in levels[i+1]:
                edges.append((u,v))
    created_graph = Graph(nodes, edges)
    return created_graph
    
def create_weighted_graph_from_template(template_graph, weight_min, weight_max):
    new_edges = []
    for (u,v), w in zip(template_graph.edges, np.random.randint(weight_min, weight_max+1, len(template_graph.edges))):
        new_edges.append((u, v, {'weight': w}))
    weighted_graph = Graph(template_graph.nodes, new_edges)
    return weighted_graph

def create_random_standard_graph(n_nodes, p_edge):
    nodes = range(0, n_nodes)
    edges = []
    for u in nodes:
        possible_neighbours = [v for v in nodes if (v != u) and ((v,u) not in edges)]
        neighbours = choose_neighbours(possible_neighbours, p_edge)
        edges += [(u,v) for v in neighbours]
    created_graph = Graph(nodes, edges)
    return created_graph

def create_random_acyclic_graph(n_nodes, p_edge):
    nodes = range(0, n_nodes)
    edges = []
    ranks = rank_nodes(nodes)
    for i in range(len(ranks)):
        for u in ranks[i]:
            possible_neighbours = [v for j in range(i+1, len(ranks)) for v in ranks[j]]
            neighbours = choose_neighbours(possible_neighbours, p_edge)
            edges += [(u,v) for v in neighbours]
    created_graph = Graph(nodes, edges)
    return created_graph


def rank_nodes(nodes):
    ranks = []
    choosable_nodes = set(nodes)
    while len(choosable_nodes) > 0:
        n_nodes_for_rank = np.random.randint(1, len(choosable_nodes)+1)
        rank_nodes = np.random.choice(list(choosable_nodes), n_nodes_for_rank, replace=False)
        ranks.append(rank_nodes)
        choosable_nodes -= set(rank_nodes)
    return ranks


def choose_neighbours(possible_neighbours, p_edge):
    neighbours = []
    for v in possible_neighbours:
        p = np.random.rand()
        if p < p_edge:
            neighbours.append(v)
    return neighbours
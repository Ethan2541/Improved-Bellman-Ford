from Graph import Graph
import numpy as np

def generate_random_test_set(n_instances, n_nodes, weight_min, weight_max):
    G = create_random_graph(n_nodes)
    weighted_graphs = [create_weighted_graph_from_template(G, weight_min, weight_max) for _ in range(n_instances)]
    return G, weighted_graphs

def create_random_graph(n_nodes):
    nodes = range(0, n_nodes)
    edges = []
    for u in nodes:
        possible_neighbours = [v for v in nodes if (v != u) and ((v,u) not in edges)]
        neighbours = choose_neighbours(possible_neighbours)
        edges += [(u,v) for v in neighbours]
    created_graph = Graph(nodes, edges)
    return created_graph

def choose_neighbours(possible_neighbours, p_edge=0.1):
    neighbours = []
    for v in possible_neighbours:
        p = np.random.rand()
        if p < p_edge:
            neighbours.append(v)
    return neighbours

def create_weighted_graph_from_template(template_graph, weight_min, weight_max):
    new_edges = []
    for (u,v), w in zip(template_graph.edges, np.random.randint(weight_min, weight_max+1, len(template_graph.edges))):
        new_edges.append((u, v, {'weight': w}))
    weighted_graph = Graph(template_graph.nodes, new_edges)
    return weighted_graph
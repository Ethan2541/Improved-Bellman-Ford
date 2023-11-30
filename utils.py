from ShortestPaths import ShortestPaths
import networkx as nx
import numpy as np


def compute_shortest_paths(graph: nx.DiGraph, source:int):
    shortest_paths = ShortestPaths(graph, source)
    shortest_paths.bellman_ford()
    shortest_paths_graph = shortest_paths.create_graph_of_shortest_paths()
    n_iterations = shortest_paths.n_iterations
    return shortest_paths_graph, n_iterations



"""
The GloutonFas algorithm aims to determine an order of the nodes for the Bellman-Ford algorithm
First, we choose all the sources (nodes with no predecessors=)
Then, we determine the targets (nodes with no successor)
If there is neither any source nor target, the next greatest node is the one whose the difference between the number of successors and predecessors is maximal
"""

def glouton_fas(graph: nx.DiGraph):
    s1 = []
    s2 = []
    graph_copy = graph.copy()

    while len(graph_copy.nodes) > 0:
        graph_copy, removed_sources = remove_sources(graph_copy)
        s1 += removed_sources

        graph_copy, removed_targets = remove_targets(graph_copy)
        s2 += removed_targets
        
        if len(graph_copy.nodes) > 0:
            v = find_node_with_maximal_gap_out_in_degrees(graph_copy)
            s1.append(v)
            graph_copy.remove_node(v)

    return s1+s2


def remove_sources(graph: nx.DiGraph):
    sources = [x for x in graph.nodes() if graph.in_degree(x) == 0]
    removed_sources = []
    while len(sources) > 0:
        removed_node = sources.pop(0)
        removed_sources.append(removed_node)
        graph.remove_node(removed_node)
        sources += [s for s in graph.nodes() if (graph.in_degree(s) == 0) and (s not in sources)]
    return graph, removed_sources


def remove_targets(graph: nx.DiGraph):
    targets = [x for x in graph.nodes() if graph.out_degree(x) == 0]
    removed_targets = []
    while len(targets) > 0:
        removed_node = targets.pop(0)
        removed_targets.append(removed_node)
        graph.remove_node(removed_node)
        targets += [t for t in graph.nodes() if (graph.out_degree(t) == 0) and (t not in targets)]
    return graph, removed_targets


def find_node_with_maximal_gap_out_in_degrees(graph: nx.DiGraph):
    max_gap = -np.inf
    node_max = None
    for v in graph.nodes:
        if max_gap < graph.out_degree(v) - graph.in_degree(v):
            max_gap = graph.out_degree(v) - graph.in_degree(v)
            node_max = v
    return node_max



def generate_random_test_set(n_instances, n_nodes, weight_min, weight_max):
    G = create_random_graph(n_nodes)
    weighted_graphs = [create_weighted_graph_from_template(G, weight_min, weight_max) for _ in range(n_instances)]
    return G, weighted_graphs


def create_random_graph(n_nodes):
    nodes = range(0, n_nodes)
    edges = []
    for u in nodes:
        possible_neighbours = [v for v in nodes if v != u]
        n_neighbours = np.random.randint(0, n_nodes)
        neighbours = np.random.choice(possible_neighbours, n_neighbours, replace=False)
        edges += [(u,v) for v in neighbours]
    created_graph = nx.DiGraph(edges)
    return created_graph


def create_weighted_graph_from_template(template_graph, weight_min, weight_max):
    new_edges = []
    for (u,v), w in zip(template_graph.edges, np.random.randint(weight_min, weight_max+1, len(template_graph.edges))):
        new_edges.append((u, v, {'weight': w}))
    weighted_graph = nx.DiGraph(new_edges)
    return weighted_graph



def display_graph(graph):
    pos = nx.spring_layout(graph)
    try:
        labels = {x[:2]: np.round(graph.get_edge_data(*x)['weight'], 2) for x in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, labels)
    except KeyError:
        pass
    nx.draw_networkx(graph, pos, with_labels=True, arrows=True)
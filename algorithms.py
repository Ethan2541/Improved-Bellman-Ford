from ShortestPaths import ShortestPaths
import networkx as nx
import numpy as np


def compute_shortest_paths(graph: nx.DiGraph, source:int):
    shortest_paths = ShortestPaths(graph, source)
    shortest_paths.bellman_ford()
    shortest_paths_graph = shortest_paths.create_shortest_paths_graph()
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
        print(removed_sources)

        graph_copy, removed_targets = remove_targets(graph_copy)
        s2 += removed_targets
        print(removed_targets)
        if len(graph_copy.nodes) > 0:
            v = find_node_with_maximal_gap_out_in_degrees(graph_copy)
            s1.append(v)
            graph_copy.remove_node(v)

    return s1+s2


def remove_sources(graph: nx.DiGraph):
    sources = [x for x in graph.nodes() if graph.in_degree(x)==0]
    removed_sources = []
    while len(sources) > 0:
        removed_sources.append(sources[0])
        graph.remove_node(sources[0])
        sources = [x for x in graph.nodes() if graph.in_degree(x)==0]
    return graph, removed_sources


def remove_targets(graph: nx.DiGraph):
    targets = [x for x in graph.nodes() if graph.out_degree(x)==0]
    removed_targets = []
    while targets: 
        removed_targets.append(targets[0])
        graph.remove_node(targets[0])
        targets = [x for x in graph.nodes() if graph.out_degree(x)==0]
    return graph, removed_targets


def find_node_with_maximal_gap_out_in_degrees(graph: nx.DiGraph):
    max_gap = -np.inf
    node_max = None
    for v in graph.nodes:
        if max_gap < graph.out_degree(v) - graph.in_degree(v):
            max_gap = graph.out_degree(v) - graph.in_degree(v)
            node_max = v
    return node_max
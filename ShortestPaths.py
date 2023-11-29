import networkx as nx
import numpy as np

class ShortestPaths:
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.hasConverged = False
        self.n_iterations = 0
        self.init_distances_and_predecessors()

    def init_distances_and_predecessors(self):
        self.distances = {node: np.inf for node in self.graph.nodes}
        self.distances[self.source] = 0
        self.predecessors = {node: None for node in self.graph.nodes}

    def bellman_ford(self, ordered_nodes=None):
        n_nodes = len(self.graph.nodes)
        if ordered_nodes is None:
            ordered_nodes = self.graph.nodes
        while (self.n_iterations < n_nodes - 1) and (not self.hasConverged):
            self.n_iterations += 1
            self.hasConverged = True
            for v in ordered_nodes:
                for predecessor, _ in self.graph.in_edges(v):
                    if self.distances[predecessor] + self.graph[predecessor][v]['weight'] < self.distances[v]:   
                        self.distances[v] = self.distances[predecessor] + self.graph[predecessor][v]['weight']
                        self.predecessors[v] = predecessor
                        self.hasConverged = False

    def create_shortest_paths_graph(self):
        edges = [(self.predecessors[v], v) for v in range(len(self.predecessors)) if v != self.source]
        shortest_paths_graph = nx.DiGraph(edges)
        return shortest_paths_graph
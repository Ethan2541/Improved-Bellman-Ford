import networkx as nx
import numpy as np

class ShortestPaths:
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.n_iterations = 0
        self.init_distances_and_predecessors()

    def init_distances_and_predecessors(self):
        n_nodes = len(self.graph.nodes)
        self.distances = np.full(n_nodes, np.inf)
        self.distances[self.source] = 0
        self.predecessors = np.full(n_nodes, np.nan, dtype=int)

    def bellman_ford(self):
        nodes_to_update = [v for v in self.graph.nodes if v != self.source]        
        for v in nodes_to_update:
            incoming_edges_of_node = self.graph.in_edges(v)
            for predecessor, _ in incoming_edges_of_node:
                dpredecessor = self.distances[predecessor]
                dv = self.distances[v]
                weight = self.graph[predecessor][v]['weight']
                if dpredecessor + weight < dv:   
                    self.distances[v] = dpredecessor + weight
                    self.predecessors[v] = predecessor
            self.n_iterations += 1

    def create_shortest_paths_graph(self):
        edges = [(self.predecessors[v], v) for v in range(len(self.predecessors)) if v != self.source]
        shortest_paths_graph = nx.DiGraph(edges)
        return shortest_paths_graph
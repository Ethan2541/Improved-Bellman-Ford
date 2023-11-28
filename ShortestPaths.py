import numpy as np

class ShortestPaths:
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.n_iterations = 0
        self.distances = {}
        self.predecessors = {}
        self.init_distances_and_predecessors()

    def init_distances_and_predecessors(self):
        for v in self.graph.nodes:
            if v == self.source:
                self.distances[v] = 0
            else:
                self.distances[v] = np.inf
            self.predecessors[v] = None

    def update_all_nodes(self):
        nodes_to_update = [v for v in self.graph.nodes if v != self.source]        
        for v in nodes_to_update:
            self.update(v)
            self.n_iterations += 1

    def update(self, v):
        incoming_edges_of_node = self.graph.in_edges(v)
        for predecessor, _ in incoming_edges_of_node:
            dpredecessor = self.distances[predecessor]
            dv = self.distances[v]
            weight = self.graph[predecessor][v]['weight']
            if dpredecessor + weight < dv:   
                self.distances[v] = dpredecessor + weight
                self.predecessors[v] = predecessor
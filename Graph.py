from ShortestPaths import ShortestPaths
import networkx as nx
import numpy as np

class Graph(nx.DiGraph):
    def __init__(self, nodes, edges):
        nx.DiGraph.__init__(self)
        self.add_nodes_from(nodes)
        self.add_edges_from(edges)
        self.is_weighted = self.check_if_weighted()

    def check_if_weighted(self):
        try:
            for e in self.edges:
                self.get_edge_data(*e)['weight']
            return True
        except KeyError:
            return False
        
    def display(self):
        pos = nx.spring_layout(self)
        if self.is_weighted:
            labels = {x[:2]: np.round(self.get_edge_data(*x)['weight'], 2) for x in self.edges}
            nx.draw_networkx_edge_labels(self, pos, labels)
        nx.draw_networkx(self, pos, with_labels=True, arrows=True)


    def choose_source(self):
        n_neighbours_for_each_node = [degree for node, degree in self.out_degree]
        source = np.argmax(n_neighbours_for_each_node)
        return source
    
    def compute_shortest_paths(self, source:int):
        shortest_paths = ShortestPaths(self, source)
        shortest_paths.bellman_ford()
        shortest_paths_graph = self.create_graph_from_shortest_paths(shortest_paths)
        n_iterations = shortest_paths.n_iterations
        return shortest_paths_graph, n_iterations
    
    def create_graph_from_shortest_paths(self, shortest_paths):
        edges = [(shortest_paths.predecessors[v], v) for v in range(len(shortest_paths.predecessors)) if shortest_paths.predecessors[v] != None]
        shortest_paths_graph = Graph(self.nodes, edges)
        return shortest_paths_graph
    

    def glouton_fas(self):
        s1 = []
        s2 = []
        graph_copy = Graph(self.nodes, self.edges)

        while len(graph_copy.nodes) > 0:
            graph_copy, removed_sources = self.remove_sources(graph_copy)
            s1 += removed_sources

            graph_copy, removed_targets = self.remove_targets(graph_copy)
            s2 += removed_targets
            
            if len(graph_copy.nodes) > 0:
                v = self.find_node_with_maximal_gap_out_in_degrees(graph_copy)
                s1.append(v)
                graph_copy.remove_node(v)

        return s1+s2

    @staticmethod
    def remove_sources(graph):
        sources = [x for x in graph.nodes() if graph.in_degree(x) == 0]
        removed_sources = []
        while len(sources) > 0:
            removed_node = sources.pop(0)
            removed_sources.append(removed_node)
            graph.remove_node(removed_node)
            sources += [s for s in graph.nodes() if (graph.in_degree(s) == 0) and (s not in sources)]
        return graph, removed_sources

    @staticmethod
    def remove_targets(graph):
        targets = [x for x in graph.nodes() if graph.out_degree(x) == 0]
        removed_targets = []
        while len(targets) > 0:
            removed_node = targets.pop(0)
            removed_targets.append(removed_node)
            graph.remove_node(removed_node)
            targets += [t for t in graph.nodes() if (graph.out_degree(t) == 0) and (t not in targets)]
        return graph, removed_targets

    @staticmethod
    def find_node_with_maximal_gap_out_in_degrees(graph):
        max_gap = -np.inf
        node_max = None
        for v in graph.nodes:
            if max_gap < graph.out_degree(v) - graph.in_degree(v):
                max_gap = graph.out_degree(v) - graph.in_degree(v)
                node_max = v
        return node_max

    @staticmethod
    def union(graphs_list):
        edges_of_graphs_union = []
        for graph in graphs_list:
            nodes = graph.nodes
            edges_of_graphs_union = list(set(edges_of_graphs_union + list(graph.edges)))
        graph_of_union = Graph(nodes, edges_of_graphs_union)
        return graph_of_union
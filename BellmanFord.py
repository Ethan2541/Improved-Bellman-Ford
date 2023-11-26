import networkx as nx
import numpy as np
import functools as fun



def Bellman_Ford(input_graph : nx.DiGraph, s:int):
    n_iterations = 0
    vertices_of_input_graph = input_graph.nodes
    shortest_path_matrix = {}
    for vertex_of_input_graph in vertices_of_input_graph:
        if vertex_of_input_graph == s:
            shortest_path_matrix[vertex_of_input_graph] = {'distance': 0, 'previous_vertex': None}
        else:
            shortest_path_matrix[vertex_of_input_graph] = {'distance': np.inf, 'previous_vertex': None}


    for v in vertices_of_input_graph:
        if v == s:
            continue

        incoming_edges_of_vertex = input_graph.in_edges(v)
        for u, _ in incoming_edges_of_vertex:
            du = shortest_path_matrix[u]['distance']
            dv = shortest_path_matrix[v]['distance']
            weight = input_graph[u][v]['weight']

            if du + weight < dv:
                shortest_path_matrix[v]['distance'] = du + weight
                shortest_path_matrix[v]['previous_vertex'] = u

        print(shortest_path_matrix)

        n_iterations += 1
    return shortest_path_matrix, n_iterations



def GloutonFas(G: nx.DiGraph):
    s1 = []
    s2 = []
    G_copy = G.copy()
    while G_copy.nodes:
        max = -1
        sommetmax = None
        sources = [x for x in G_copy.nodes() if G_copy.in_degree(x)==0]

        print(sources)
        while sources: #enleve toutes les sources à chaque itération
            s1.append(sources[0])
            G_copy.remove_node(sources[0])
            sources = [x for x in G_copy.nodes() if G_copy.in_degree(x)==0]
            print(sources)
        targets = [x for x in G_copy.nodes() if G_copy.out_degree(x)==0]
        while targets : 
            #enleve tous les puits à chaque itération
            s2.append(targets[0])
            G_copy.remove_node(targets[0])
            targets = [x for x in G_copy.nodes() if G_copy.out_degree(x)==0]
            print(targets)
        if G_copy.nodes:
            for n in G_copy.nodes: #choix du sommet sur les noeud restant tel qu'il maximise 
                if max<G_copy.out_degree(n)-G_copy.in_degree(n):
                    max=G_copy.out_degree(n)-G_copy.in_degree(n)
                    sommetmax = n
            s1.append(sommetmax)
            G_copy.remove_node(sommetmax)
        
    return s1+s2

    
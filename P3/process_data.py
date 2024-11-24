from collections import defaultdict

def adjacencylist_from_edgelistFile(filename):

    adjacency_list = defaultdict(list)
    n_edges = 0

    with open(filename, 'r') as file:
        for line in file:
            n_edges+=1
            node1, node2 = map(int, line.strip().split())
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1) 
            
    return adjacency_list, n_edges

def cluster_coeficiency_distribution_from_adjacencylist(adjacency_list):
    cluster_coeficiency_distribution = {}

    # TODO: fill that shit up

    return cluster_coeficiency_distribution

def graph_degree_distribution_from_adjacencylist(adjacency_list):
    graph_degree_distribution = {}

    for n in adjacency_list.keys():
        degree = len(adjacency_list[n])
        if degree not in graph_degree_distribution:
            graph_degree_distribution[degree] = 1
        else:
            graph_degree_distribution[degree] += 1
    
    return graph_degree_distribution

def process_edgelist(filename):
    adjacency_list, n_edges = adjacencylist_from_edgelistFile(filename)
    graph_degree_distribution = graph_degree_distribution_from_adjacencylist(adjacency_list)
    cluster_coeficiency_distribution = cluster_coeficiency_distribution_from_adjacencylist(adjacency_list)

    return adjacency_list, n_edges, graph_degree_distribution, cluster_coeficiency_distribution
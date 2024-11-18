from collections import defaultdict

def adjacencylist_from_edgelistFile(filename):

    adjacency_list = defaultdict(list)
    n_edges = 0

    with open(filename, 'r') as file:
        for line in file:
            n_edges+=1
            node1, node2 = map(int, line.strip().split())
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)  # Assuming the graph is undirected

    return adjacency_list, n_edges

def process_edgelist(filename, n_hub):
    # Convert the edgelist to adjacency list
    adjacency_list, n_edges = adjacencylist_from_edgelistFile(filename)

    print('Hubs with more than ' + str(n_hub) + ' edges:')
    for n in adjacency_list.keys():
        if len(adjacency_list[n]) > n_hub:
            print('     ' + str(n) + ' :    '+  str(len(adjacency_list[n])))

    print('number of nodes:     ' + str(len(adjacency_list)))
    print('number of edges:     ' + str(n_edges))

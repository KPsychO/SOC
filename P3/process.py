from collections import defaultdict

file_path = './datasets/bitcoin.edgelist'

def adjacencylist_from_edgelistFile():

    adjacency_list = defaultdict(list)
    n_edges = 0

    with open(file_path, 'r') as file:
        for line in file:
            n_edges+=1
            node1, node2 = map(int, line.strip().split())
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)  # Assuming the graph is undirected

    return adjacency_list, n_edges



# Convert the edgelist to adjacency list

adjacency_list, n_edges = adjacencylist_from_edgelistFile()

edges_to_be_hub = 250
print('Hubs with more than ' + str(edges_to_be_hub) + ' edges:')
for n in adjacency_list.keys():
    if len(adjacency_list[n]) > edges_to_be_hub:
        print('     ' + str(n) + ' :    '+  str(len(adjacency_list[n])))

print('number of nodes:     ' + str(len(adjacency_list)))
print('number of edges:     ' + str(n_edges))
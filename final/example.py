import click
from process_data import process_edgelist


def print_info(
    n_hub,
    adjacency_list,
    n_edges,
    graph_degree_distribution,
    cluster_coeficiency_distribution,
):
    print(n_hub)
    print("Graph degree distribution:")
    for n in graph_degree_distribution.keys():
        print("     " + str(n) + " :    " + str(graph_degree_distribution[n]))

    print("Cluster coeficiency distribution:")
    for n in cluster_coeficiency_distribution.keys():
        print("     " + str(n) + " :    " + str(cluster_coeficiency_distribution[n]))

    print("Hubs with more than " + str(n_hub) + " edges:")
    for n in adjacency_list.keys():
        if len(adjacency_list[n]) > int(n_hub):
            print("     " + str(n) + " :    " + str(len(adjacency_list[n])))

    print("number of nodes:     " + str(len(adjacency_list)))
    print("number of edges:     " + str(n_edges))


def generate_graphs(
    n_hub,
    adjacency_list,
    n_edges,
    graph_degree_distribution,
    cluster_coeficiency_distribution,
):
    print("[TODO]: IDK man, use pandas and pyplot or some shit and do cute shit here")


@click.command()
@click.argument("filename")
@click.argument("n_hub")
def main(filename, n_hub):

    (
        adjacency_list,
        n_edges,
        graph_degree_distribution,
        cluster_coeficiency_distribution,
    ) = process_edgelist(filename)

    print_info(
        n_hub,
        adjacency_list,
        n_edges,
        graph_degree_distribution,
        cluster_coeficiency_distribution,
    )
    generate_graphs(
        n_hub,
        adjacency_list,
        n_edges,
        graph_degree_distribution,
        cluster_coeficiency_distribution,
    )


main()


# parametros(click): numero de nodos para ser hub, nombre del fichero a procesar
# invocar al py que toca por parametro
# prints bonitos
# calculo de carga y estatisticas de tiempo de ejecucion
#
#
#
#
#
#

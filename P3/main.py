import click
from process_data import process_edgelist

@click.command()
@click.argument('filename')
@click.option('-n', '--n_hub', type=int)

def main(filename, n_hub):
    process_edgelist(filename, n_hub)

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
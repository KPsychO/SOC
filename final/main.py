import click
from chesscom import process_chesscom
from goodreads import process_goodreads

@click.command('chesscom')
@click.option('--country', prompt='Country to analyze on chess.com', help='Country to analyze on chess.com.')
def chess_com(country):
    print('main::chess_com::' + country)
    process_chesscom(country)

# @click.command('goodreads')
# @click.option('--country', prompt='Country to analyze on chess.com', help='Country to analyze on chess.com.')
def goodreads():
    print('main::goodreads')
    process_goodreads()

@click.command()
@click.option(
    '--socialNetwork', 
    type=click.STRING,
    prompt='Social network to analyze', 
    help='Social network to analyze.'
)
def test(socialnetwork):  # Chooses that social network to analyse
    print('main::main')
    match socialnetwork:
        case 'chess.com':
            print('chesscom')
            chess_com()
        case 'goodreads':
            print('goodreads')
            goodreads()
        case _:
            print('Valid values for "socialNetwork" parameters are:')
            print('     chesscom')
            print('     goodreads')
            print('     strava')
            print('     letterboxd')

if __name__ == '__main__':
    
    test()
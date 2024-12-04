import os
import click
from chesscom import process_chesscom
from goodreads import process_goodreads

def delCache(delcache):
    print("main::delCache::delcache: " + delcache)
    match delcache.lower():
        case "y" | "yes":
            folder = './cache/'
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            print("Cache files were succesfully deleted...")
        case "n" | "no":
            print("Reading data from './cache/'...")
        case _:
            print('Valid values for "delcache" parameters are:')
            print("     y | yes")
            print("     n | no")


def chess_com():
    process_chesscom()


# @click.command('goodreads')
# @click.option('--country', prompt='Country to analyze on chess.com', help='Country to analyze on chess.com.')
def goodreads():
    print("main::goodreads")
    process_goodreads()


@click.command("main")
@click.option(
    "--socialNetwork",
    type=click.STRING,
    prompt="Social network to analyze",
    help="Social network to analyze.",
)
@click.option(
    "--delcache",
    prompt="Do you want to delete the cache files in case they exist? (Please, take into account they will take a long time to regenerate)"
)
def main(socialnetwork, delcache):  # Chooses that social network to analyse
    delCache(delcache)
    print("main::main")
    match socialnetwork.lower():
        case "cc" | "chess.com":
            print("chesscom")
            chess_com()
        case "gr" | "goodreads":
            print("goodreads")
            goodreads()
        case _:
            print('Valid values for "socialNetwork" parameters are:')
            print("     cc | chesscom")
            print("     gr | goodreads")
            print("     strava")
            print("     letterboxd")

main()

from os import getcwd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '-u',
    '--url',
    default=False,
    help='Youtube mix url to download the songs from',
)

parser.add_argument(
    '-l',
    '--location',
    default=getcwd(),
    help='Location to store the downloaded songs'
         '(default to current directory)',
)

parser.add_argument(
    '-a',
    '--artist',
    default=False,
    help='If the mix is an album provide the artist',
)

parser.add_argument(
    '-s',
    '--songs',
    default=False,
    help='.txt that contains the songs. These songs will be downloaded',
)

args = parser.parse_args()

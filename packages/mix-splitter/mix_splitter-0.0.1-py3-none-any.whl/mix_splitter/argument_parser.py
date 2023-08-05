from os import getcwd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '-u',
    '--url',
    help='Youtube mix url to download the songs from',
    required=True
)

parser.add_argument(
    '-l',
    '--location',
    default=getcwd(),
    help='Location to store the downloaded songs'
         '(default to current directory)',
)

args = parser.parse_args()

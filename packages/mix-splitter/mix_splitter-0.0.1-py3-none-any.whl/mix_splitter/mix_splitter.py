from .downloader import yt_downloader
from .argument_parser import args
from sys import exit
from .helpers import (get_video_description, get_songs,
                      make_ids_list, make_urls_list)


def main():
    mix_url = args.url
    location = args.location
    mix_id = mix_url.split('=')[1]

    print('\n*******************')
    print('Collecting songs...')
    print('*******************')
    description = get_video_description(mix_id)
    songs_list = get_songs(description)
    ids_list, not_found = make_ids_list(songs_list)
    urls = make_urls_list(ids_list)

    print('\n*******************')
    print('Downloading songs...')
    print('*******************')
    yt_downloader(urls, location)

    print('\n*******************')
    print('Task finished. Songs downloaded in: ' + location)
    print('*******************')

    exit()


if __name__ == '__main__':
    main()

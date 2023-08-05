from downloader import yt_downloader
from argument_parser import args
from sys import exit
from helpers import (get_video_description, get_songs,
                     make_ids_list, make_urls_list,
                     append_artist, makes_songs_to_download_list,
                     get_songs_txt)


def main():
    mix_url = args.url
    location = args.location
    artist = args.artist
    txt_source = args.songs

    if mix_url and txt_source:
        print('\n*** You must provide only one source to download '
              'the songs ***')
        exit()

    if not mix_url and not txt_source:
        print('\n*** You must provide one source to download the songs ***')
        exit()

    print('\n*******************')
    print('Collecting songs...')
    print('*******************')

    if mix_url:
        mix_id = mix_url.split('=')[1]
        description = get_video_description(mix_id)
        songs_list = get_songs(description)
    else:
        # .txt source
        songs_list = get_songs_txt(txt_source)

    if artist:
        songs_list = append_artist(songs_list, artist)

    ids_list = make_ids_list(songs_list)
    titles_list = makes_songs_to_download_list(songs_list)

    if not titles_list:
        print("\n")
        print("**** This mix is not compatible (I couldn't find any song "
              "in the video description or txt_source) ****")
        print("\n")
        exit()

    print('-- List of songs to download --')
    for title in titles_list:
        print(title)

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
    try:
        main()
    except KeyboardInterrupt:
        pass

    exit()

import requests
import re
import urllib

from difflib import SequenceMatcher
from .random_proxy import main as random_proxy
from bs4 import BeautifulSoup

songs_not_found = []


def get_video_id(search_query):
    """
    Gets the first video that is found with the search query,
    then it extracts its id.
    :param str search_query: query to search in youtube
    :return str: first video found's id, if the first video title found
    doesn't have anything to do with the search query, then returns None
    """
    search_query = search_query.lower().strip()
    base_url = 'https://www.youtube.com/results?search_query='
    search_query_parsed = urllib.parse.quote_plus(search_query)
    search_url = base_url + search_query_parsed

    proxies = {
        'http': random_proxy()
    }

    request = requests.get(search_url, proxies=proxies)
    page = request.text
    page_parsed = BeautifulSoup(page, features='lxml')

    videos_found = page_parsed.findAll(attrs={'class': 'yt-lockup-title'})

    # number of attempts before giving up on getting the song's id
    max_attempts = 5

    for video in videos_found:
        href = video.a['href']
        video_title = video.a['title'].lower()

        similarity_ratio = SequenceMatcher(
            None,
            video_title,
            search_query
        ).ratio()

        if max_attempts == 0:
            songs_not_found.append(search_query)
            return None

        # If found the incorrect video
        if similarity_ratio < .65:
            max_attempts -= 1
            continue

        id_video = href.split('=')[1]

        return id_video


def get_video_description(id_video):
    """
    Gets the video description scraped from youtube.
    :param str id_video: youtube video id
    :return str: a text with the video's description
    """
    base_url = 'https://www.youtube.com/watch?v='
    url = base_url + id_video
    request = requests.get(url)
    page = request.text

    page_parsed = BeautifulSoup(page, features='lxml')

    description = page_parsed.find(id='eow-description').contents

    return description


def get_songs(description):
    """
    Extracts the songs located in the description
    :param str description: video description
    :return list: song names
    """
    # pattern for a youtube video time (e.g. 34:87, 2:38:56)
    yt_time_regex = re.compile(r'(\d{1,2}:)?([0-5]?[0-9]):([0-5][0-9])')
    # "artist - song name" regex
    song_pattern = re.compile(
        r'[\w\s.()&\'!\-"\[\]]+\s?-\s?[\w\s.()&\'!\-"\[\]]+'
    )

    songs = []

    for idx, child in enumerate(description):
        if (child.string is not None
           and re.match(yt_time_regex, child.string)):

            # When the song name is located before the time
            if description[idx + 1].name == 'br':
                songs.append(description[idx - 1])
                continue

            # When the song name is located after the time
            songs.append(description[idx + 1])

    # If no songs were found, it might mean that the mix doesn't have
    # The times to go to certain songs in its description.
    # If that happens, the next block will perform
    # a similar search (with a song pattern)
    # but it's a bit less accurate.
    if not songs:
        songs = [child for child in description
                 if child.string is not None and
                 re.search(song_pattern, child.string)]

    return songs


def make_ids_list(song_list):
    """
    Extracts the youtube video id of each song in the list
    :param list song_list: list of song names
    :return list: video ids related to each song
    """
    ids_list = [get_video_id(song_name)
                for song_name in song_list
                if get_video_id(song_name) is not None]

    return ids_list, songs_not_found


def make_urls_list(ids_list):
    """
    Appends each video id to the base url and insert them into a list
    :param list ids_list: youtube video id list
    :return list: list of urls
    """
    base_url = 'https://www.youtube.com/watch?v='
    urls_list = [base_url + _id
                 for _id in ids_list
                 if _id is not None]

    return urls_list

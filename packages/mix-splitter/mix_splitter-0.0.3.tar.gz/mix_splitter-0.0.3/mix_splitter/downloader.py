from youtube_dl import YoutubeDL

ydl_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '251'
    }],
}


def yt_downloader(urls, location):
    ydl_options['outtmpl'] = f'{location}/%(title)s.%(ext)s'
    ydl = YoutubeDL(ydl_options)

    ydl.download(urls)

